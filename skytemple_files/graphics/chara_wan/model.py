#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
import sys
from PIL import Image
import chara_wan.utils as exUtils

CENTER_X = 256
CENTER_Y = 0

MINUS_FRAME = -1

OBJMODE_NORMAL = 0
OBJMODE_SEMITRANSP = 1
OBJMODE_WINDOW = 2
OBJMODE_BITMAP = 3

FRAME_HitMask = 0x0002  # 0000 0000 0000 0010
FRAME_ReturnMask = 0x0001  # 0000 0000 0000 0001

ATTR0_FlagBitsMask = 0xFF00  # 1111 1111 0000 0000
ATTR1_FlagBitsMask = 0xFE00  # 1111 1110 0000 0000
ATTR2_FlagBitsMask = 0xFC00  # 1111 1100 0000 0000

ATTR0_ColPalMask = 0x2000  # 0010 0000 0000 0000
ATTR0_MosaicMask = 0x1000  # 0001 0000 0000 0000
ATTR0_ObjModeMask = 0x0C00  # 0000 1100 0000 0000
ATTR0_DblSzDisabled = 0x0200  # 0000 0010 0000 0000 (Whether the obj is disabled if rot&scaling is off, or if double sized when rot&scaling is on!)
ATTR0_RotNScaleMask = 0x0100  # 0000 0001 0000 0000
ATTR0_YOffsetMask = ~ATTR0_FlagBitsMask  # 0000 0000 1111 1111

ATTR1_VFlipMask = 0x2000  # 0010 0000 0000 0000
ATTR1_HFlipMask = 0x1000  # 0001 0000 0000 0000
ATTR1_IsLastMask = 0x0800  # 0000 1000 0000 0000
ATTR1_RotNScalePrm = 0x3E00  # 0011 1110 0000 0000
ATTR1_XOffsetMask = ~ATTR1_FlagBitsMask  # 0000 0001 1111 1111

ATTR2_PalNumberMask = 0xF000  # 1111 0000 0000 0000
ATTR2_PriorityMask = 0x0C00  # 0000 1100 0000 0000
ATTR2_TileNumMask = 0x03FF  # 0000 0011 1111 1111

ATTR01_ResMask = 0xC000  # 1100 0000 0000 0000

TEX_SIZE = 8
DIM_TABLE = [(1, 1), (2, 2), (4, 4), (8, 8), \
             (2, 1), (4, 1), (4, 2), (8, 4), \
             (1, 2), (1, 4), (2, 4), (4, 8)]

DEBUG_PRINT = False


class WanFile():

    def __init__(self, imgData, frameData, animGroupData, offsetData, customPalette):
        self.imgData = imgData
        self.frameData = frameData
        self.animGroupData = animGroupData
        self.offsetData = offsetData
        self.customPalette = customPalette
        self.sdwSize = 1


class SequenceFrame():

    def __init__(self, frameIndex, duration, flag, offset, shadow):
        self.frameIndex = frameIndex
        self.duration = duration
        self.flag = flag
        self.isRushPoint = False
        self.offset = offset
        self.shadow = shadow

    def IsRushPoint(self):
        return self.isRushPoint

    def IsHitPoint(self):
        return self.flag % 4 // 2 == 1

    def IsReturnPoint(self):
        return self.flag % 2 == 1

    def SetRushPoint(self, rush):
        self.isRushPoint = rush

    def SetHitPoint(self, hit):
        if hit:
            self.flag = (FRAME_HitMask | self.flag)
        else:
            self.flag = (self.flag & ~FRAME_HitMask)

    def SetReturnPoint(self, ret):
        if ret:
            self.flag = (FRAME_ReturnMask | self.flag)
        else:
            self.flag = (self.flag & ~FRAME_ReturnMask)


class MetaFramePiece():

    def __init__(self, imgIndex, attr0, attr1, attr2):
        self.imgIndex = imgIndex
        self.attr0 = attr0
        self.attr1 = attr1
        self.attr2 = attr2

    def Clone(self):
        return MetaFramePiece(self.imgIndex, self.attr0, self.attr1, self.attr2)

    def isColorPal256(self):
        return (ATTR0_ColPalMask & self.attr0) != 0

    def isMosaicOn(self):
        return (ATTR0_MosaicMask & self.attr0) != 0

    def isDisabled(self):
        return not self.isRotAndScalingOn() and ((ATTR0_DblSzDisabled & self.attr0) != 0)

    def isDoubleSize(self):
        return self.isRotAndScalingOn() and ((ATTR0_DblSzDisabled & self.attr0) != 0)

    def isRotAndScalingOn(self):
        return (ATTR0_RotNScaleMask & self.attr0) != 0

    def setRotAndScalingOn(self, rns):
        if rns:
            self.attr0 = (ATTR0_RotNScaleMask | self.attr0)
        else:
            self.attr0 = (self.attr0 & ~ATTR0_RotNScaleMask)

    def getYOffset(self):
        rawY = ATTR0_YOffsetMask & self.attr0
        if rawY >= 128:
            rawY -= 256
        return rawY - CENTER_Y

    def setYOffset(self, yVal):
        rawY = yVal + CENTER_Y
        if rawY < 0:
            rawY += 256
        self.attr0 = (self.attr0 & ATTR0_FlagBitsMask) | (ATTR0_YOffsetMask & rawY)

    # Before checking VFlip and HFlip, make sure RnS isn't on!!!
    def isVFlip(self):
        return (ATTR1_VFlipMask & self.attr1) != 0

    def setVFlip(self, flip):
        if flip:
            self.attr1 = (ATTR1_VFlipMask | self.attr1)
        else:
            self.attr1 = (self.attr1 & ~ATTR1_VFlipMask)

    def isHFlip(self):
        return (ATTR1_HFlipMask & self.attr1) != 0

    def setHFlip(self, flip):
        if flip:
            self.attr1 = (ATTR1_HFlipMask | self.attr1)
        else:
            self.attr1 = (self.attr1 & ~ATTR1_HFlipMask)

    def isLast(self):
        return (ATTR1_IsLastMask & self.attr1) != 0

    def setIsLast(self, last):
        if last:
            self.attr1 = (ATTR1_IsLastMask | self.attr1)
        else:
            self.attr1 = (self.attr1 & ~ATTR1_IsLastMask)

    def getObjMode(self):
        return (self.attr0 & ATTR0_ObjModeMask) >> 10

    def getRnSParam(self):
        return (ATTR1_RotNScalePrm & self.attr1) >> 9

    def getXOffset(self):
        rawX = ATTR1_XOffsetMask & self.attr1
        return rawX - CENTER_X

    def setXOffset(self, xVal):
        rawX = xVal + CENTER_X
        self.attr1 = (self.attr1 & ATTR1_FlagBitsMask) | (ATTR1_XOffsetMask & rawX)

    def getPalNb(self):
        return (ATTR2_PalNumberMask & self.attr2) >> 12

    def getPriority(self):
        return (ATTR2_PriorityMask & self.attr2) >> 10

    def setPriority(self, priority):
        self.attr2 = (self.attr2 & ~ATTR2_PriorityMask) | (ATTR2_PriorityMask & priority)

    def getTileNum(self):
        return ATTR2_TileNumMask & self.attr2

    def setTileNum(self, tileNum):
        self.attr2 = (self.attr2 & ~ATTR2_TileNumMask) | (ATTR2_TileNumMask & tileNum)

    def getResolutionType(self):
        return ((self.attr1 & ATTR01_ResMask) >> 14) | ((self.attr0 & ATTR01_ResMask) >> 12)

    def setResolutionType(self, res):
        self.attr1 = (self.attr1 & ~ATTR01_ResMask) | ((res << 14) & ATTR01_ResMask)
        self.attr0 = (self.attr0 & ~ATTR01_ResMask) | ((res << 12) & ATTR01_ResMask)

    def GeneratePiece(self, imgData, paletteData, parentFrameIdx):
        ##creates a tex piece out of the imgdata, with the specified piece index and dimensions
        twidth, theight = DIM_TABLE[self.getResolutionType()]
        newImg = Image.new('RGBA', (twidth * TEX_SIZE, theight * TEX_SIZE), (0, 0, 0, 0))
        datas = [(0, 0, 0, 0)] * (twidth * TEX_SIZE * theight * TEX_SIZE)

        imgPx0 = imgData[parentFrameIdx].imgPx
        imgPx = []
        for pxLst in imgPx0:
            for px in pxLst:
                imgPx.append(px % 16)
                imgPx.append(px // 16)

        # print('imgPx:' + str(len(imgPx)) + ' dims:' + str(len(datas)))

        for yy in range(theight):
            for xx in range(twidth):
                blockIndex = (yy * twidth + xx)
                texPosition = blockIndex * TEX_SIZE * TEX_SIZE
                ##iterate the elements of the block and assign pixels
                for py in range(TEX_SIZE):
                    for px in range(TEX_SIZE):
                        paletteElement = imgPx[texPosition + py * TEX_SIZE + px]
                        paletteIndex = self.getPalNb()
                        if paletteElement == 0:
                            color = (0, 0, 0, 0)
                        else:
                            color = paletteData[paletteIndex][paletteElement]
                        imgPosition = (xx * TEX_SIZE + px, yy * TEX_SIZE + py)
                        datas[imgPosition[1] * twidth * TEX_SIZE + imgPosition[0]] = color

        newImg.putdata(datas)
        return newImg

    def GetBounds(self):
        start = self.getStart()
        width, height = DIM_TABLE[self.getResolutionType()]
        return (start[0], start[1], start[0] + width * TEX_SIZE, start[1] + height * TEX_SIZE)

    def getStart(self):
        return (self.getXOffset(), self.getYOffset())

    def DrawOn(self, inImg, imgPiece, exOffset):
        if self.isHFlip():
            imgPiece = imgPiece.transpose(Image.FLIP_LEFT_RIGHT)
        if self.isVFlip():
            imgPiece = imgPiece.transpose(Image.FLIP_TOP_BOTTOM)

        start = self.getStart()
        inImg.paste(imgPiece, (start[0] - exOffset[0], start[1] - exOffset[1]), imgPiece)



class FrameOffset():

    def __init__(self, head, lhand, rhand, center):
        self.head = head
        self.lhand = lhand
        self.rhand = rhand
        self.center = center

    def AddLoc(self, loc):
        self.head = exUtils.addLoc(self.head, loc)
        self.lhand = exUtils.addLoc(self.lhand, loc)
        self.rhand = exUtils.addLoc(self.rhand, loc)
        self.center = exUtils.addLoc(self.center, loc)

    def GetBounds(self):
        maxBounds = (10000, 10000, -10000, -10000)
        maxBounds = exUtils.combineExtents(maxBounds, self.getBounds(self.head))
        maxBounds = exUtils.combineExtents(maxBounds, self.getBounds(self.lhand))
        maxBounds = exUtils.combineExtents(maxBounds, self.getBounds(self.rhand))
        maxBounds = exUtils.combineExtents(maxBounds, self.getBounds(self.center))
        return maxBounds

    def getBounds(self, start):
        return (start[0], start[1], start[0] + 1, start[1] + 1)

    def DrawOn(self, inImg, exOffset):
        self.drawOn(inImg, exOffset, self.head, (0, 0, 0, 255))
        self.drawOn(inImg, exOffset, self.lhand, (255, 0, 0, 255))
        self.drawOn(inImg, exOffset, self.rhand, (0, 0, 255, 255))
        self.drawOn(inImg, exOffset, self.center, (0, 255, 0, 255))

    def drawOn(self, inImg, exOffset, start, color):
        srcColor = inImg.getpixel((start[0] - exOffset[0], start[1] - exOffset[1]))
        srcColor = (max(srcColor[0], color[0]), max(srcColor[1], color[1]),
                    max(srcColor[2], color[2]), max(srcColor[3], color[3]))
        inImg.putpixel((start[0] - exOffset[0], start[1] - exOffset[1]), srcColor)


class ImgPiece():
    def __init__(self):
        self.imgPx = []
        self.zSort = 0


class AnimStat():

    def __init__(self, index, name, size, backref):
        self.index = index
        self.name = name
        self.size = size
        self.backref = backref
        self.durations = []
        self.rushFrame = -1
        self.hitFrame = -1
        self.returnFrame = -1


