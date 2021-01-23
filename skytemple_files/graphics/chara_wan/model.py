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
from typing import Optional, Tuple, List

from PIL import Image
from io import BytesIO
import skytemple_files.graphics.chara_wan.utils as exUtils
from skytemple_files.common.ppmdu_config.data import Pmd2Data

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


class WanFile:

    def __init__(self, data: bytes = None, header_pnt: int = 0):
        if data is None:
            self.imgData = []
            self.frameData = []
            self.animGroupData = []
            self.offsetData = []
            self.customPalette = []
            self.sdwSize = 1
        else:
            self.ImportWan(data, header_pnt)
            self.sdwSize = 1

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int,
                    static_data: Optional[Pmd2Data] = None) -> 'Sir0Serializable':
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.graphics.chara_wan.writer import ExportWan
        return ExportWan(self)

    def get_filled_anims(self):
        anim_req = []
        for anim_group in self.animGroupData:
            anim_req.append(len(anim_group) > 0)
        return anim_req

    # This will accurately load all sir0 found in m_ground, m_attack, and monster.bin with a few exceptions:
    # m_ground_0546_0xb01840.wan - Armaldo.  Metaframe Unk#0 is a nonzero
    # m_ground_0587_0xbd0a10.wan - Latios.  Unknown difference
    # monster_0433_0x3dd1c0.sir0 - Giratina Origin.  Extra zeroes after file end.
    # monster_0438_0x3ec6d0.sir0 - Shaymin Sky.  Extra zeroes after file end.
    def ImportWan(self, data, ptrWAN=0):
        in_file = BytesIO()
        in_file.write(data)
        in_file.seek(0)

        self.customPalette = []
        # Read WAN header: ptr to AnimInfo, ptr to ImageDataInfo
        in_file.seek(ptrWAN)
        ptrAnimInfo = int.from_bytes(in_file.read(4), 'little')
        ptrImageDataInfo = int.from_bytes(in_file.read(4), 'little')
        if ptrAnimInfo == 0 or ptrImageDataInfo == 0:
            raise ValueError('Null pointer in Wan Header!')
        imgType = int.from_bytes(in_file.read(2), 'little')
        if imgType != 1:
            raise NotImplementedError('Non-character sprite import currently not supported.')

        updateUnusedStats([], 'Unk#12', int.from_bytes(in_file.read(2), 'little'))

        # Read ImageDataInfo: ptr to ImageDataTable block, ptr to PaletteInfo, NbImgs, print Unk#13 and Is256ColorSpr
        in_file.seek(ptrImageDataInfo)
        ptrImageDataTable = int.from_bytes(in_file.read(4), 'little')
        ptrPaletteInfo = int.from_bytes(in_file.read(4), 'little')
        if ptrImageDataTable == 0 or ptrPaletteInfo == 0:
            raise ValueError('Null pointer in Image Data Info!')
        # Unk#13 - ALWAYS 0
        int.from_bytes(in_file.read(2), 'little')
        # Is256ColorSpr - ALWAYS 0
        int.from_bytes(in_file.read(2), 'little')
        # Unk#11 - ALWAYS 1 unless completely empty?
        updateUnusedStats([], 'Unk#11', int.from_bytes(in_file.read(2), 'little'))
        nbImgs = int.from_bytes(in_file.read(2), 'little')
        # print('  NbImgs:' + str(nbImgs))

        # Read PaletteInfo: ptr to PaletteDataBlock, print NbColorsPerRow and All unknowns
        in_file.seek(ptrPaletteInfo)
        ptrPaletteDataBlock = int.from_bytes(in_file.read(4), 'little')
        # Unk#3 - ALWAYS 0
        int.from_bytes(in_file.read(2), 'little')
        nbColorsPerRow = max(1, int.from_bytes(in_file.read(2), 'little'))
        # Unk#4 - ALWAYS 0
        int.from_bytes(in_file.read(2), 'little')
        # Unk#5 - ALWAYS 255
        int.from_bytes(in_file.read(2), 'little')

        # Read PaletteDataBlock: Save contents
        in_file.seek(ptrPaletteDataBlock)
        self.customPalette = []
        totalColors = (ptrPaletteInfo - ptrPaletteDataBlock) // 4
        totalPalettes = totalColors // nbColorsPerRow
        for ii in range(totalPalettes):
            palette = []
            for jj in range(nbColorsPerRow):
                red = int.from_bytes(in_file.read(1), 'little')
                blue = int.from_bytes(in_file.read(1), 'little')
                green = int.from_bytes(in_file.read(1), 'little')
                in_file.read(1)
                palette.append((red, blue, green, 255))
            self.customPalette.append(palette)

        ##Read ImageDataTable: list of all ptr to CompressedImages (use the Nb of images variable to know when to stop)
        in_file.seek(ptrImageDataTable)
        ptrImgs = []
        for img in range(nbImgs):
            ptrImgs.append(int.from_bytes(in_file.read(4), 'little'))

        ##Read CompTable: Read all Image data and assemble; add byte arrays into a list.
        self.imgData = []  ##one continuous list of bytes
        for ptrImg in ptrImgs:
            in_file.seek(ptrImg)
            imgPiece = ImgPiece()
            imgPiece.imgPx = []
            ##Read pixels or zero padding.
            while True:
                ptrPixSrc = int.from_bytes(in_file.read(4), 'little')
                amt = int.from_bytes(in_file.read(2), 'little')
                # amt is ALWAYS a multiple of 32.  values 1-31 x 32 have been observed
                if ptrPixSrc == 0 and amt == 0:
                    break
                # Unk#14 - ALWAYS 0
                int.from_bytes(in_file.read(2), 'little')
                # z-sort is always consistent for a full image strip
                imgPiece.zSort = int.from_bytes(in_file.read(4), 'little')

                pxStrip = []
                if ptrPixSrc == 0:
                    for zero in range(amt):
                        pxStrip.append(0)
                else:
                    ptrCurrent = in_file.tell()
                    in_file.seek(ptrPixSrc)
                    for pix in range(amt):
                        pxStrip.append(int.from_bytes(in_file.read(1), 'little'))
                    in_file.seek(ptrCurrent)
                imgPiece.imgPx.append(pxStrip)
            self.imgData.append(imgPiece)

        ##Read AnimInfo: ptr to MetaFramesRefTable, ptr to AnimGroupTable
        in_file.seek(ptrAnimInfo)
        ptrMetaFramesRefTable = int.from_bytes(in_file.read(4), 'little')
        ptrOffsetsTable = int.from_bytes(in_file.read(4), 'little')
        ptrAnimGroupTable = int.from_bytes(in_file.read(4), 'little')
        nbAnimGroups = int.from_bytes(in_file.read(2), 'little')
        # Unk#6 - Max number of blocks that a frame takes
        int.from_bytes(in_file.read(2), 'little')
        # Unk#7 - ALWAYS 0
        int.from_bytes(in_file.read(2), 'little')
        # Unk#8 - ALWAYS 0
        int.from_bytes(in_file.read(2), 'little')
        # Unk#9 - ALWAYS 0
        int.from_bytes(in_file.read(2), 'little')
        # Unk#10 - ALWAYS 0
        int.from_bytes(in_file.read(2), 'little')
        # get ptr to AnimSequenceTable
        in_file.seek(ptrAnimGroupTable)
        ptrAnimGroups = []
        for ptrAnimSeq in range(nbAnimGroups):
            ##read the location
            animLoc = int.from_bytes(in_file.read(4), 'little')
            ##read the length
            animLength = int.from_bytes(in_file.read(2), 'little')
            # Unk#16 - ALWAYS 0
            int.from_bytes(in_file.read(2), 'little')
            ##save curlocation
            curLocation = in_file.tell()
            ##go to seq location
            in_file.seek(animLoc)
            ptrAnims = []
            for ii in range(animLength):
                ##read all anims
                animPtr = int.from_bytes(in_file.read(4), 'little')
                ptrAnims.append(animPtr)
            ptrAnimGroups.append(ptrAnims)
            in_file.seek(curLocation)

        if ptrOffsetsTable == 0:
            raise ValueError("Read a zero for offset table pointer.")

        ptrFramesRefTableEnd = ptrOffsetsTable

        # Read MetaFramesRefTable: list of all ptr to Meta Frames
        # stop when reached particleOffsetsTable
        # or on AnimSequenceTable, if the above is zero
        in_file.seek(ptrMetaFramesRefTable)
        ptrMetaFrames = []
        while in_file.tell() < ptrFramesRefTableEnd:
            ptrMetaFrames.append(int.from_bytes(in_file.read(4), 'little'))
        # print('  NbMetaframes:' + str(len(ptrMetaFrames)))

        ##Read MetaFrames: for each meta frame group, read until "end of meta frame group" bit is reached.
        self.frameData = []
        for idx, ptrMetaFrame in enumerate(ptrMetaFrames):
            in_file.seek(ptrMetaFrame)
            metaFrameData = []
            while True:
                imgIndex = int.from_bytes(in_file.read(2), 'little', signed=True)
                # Unk#0 - ALWAYS 0 EXCEPT for just ONE official sprite:
                # m_ground,0546,Unk#0,171,0,2560
                int.from_bytes(in_file.read(2), 'little')
                attr0 = int.from_bytes(in_file.read(2), 'little')
                attr1 = int.from_bytes(in_file.read(2), 'little')
                attr2 = int.from_bytes(in_file.read(2), 'little')
                newFramePiece = MetaFramePiece(imgIndex, attr0, attr1, attr2)

                # values of interest:
                # resolution y
                # color palette mode - ALWAYS 0
                # mosaic mode - ALWAYS 0
                # obj mode - ALWAYS Normal
                # obj disable -
                updateUnusedStats([str(len(self.frameData)), str(len(metaFrameData))],
                                  'MFDisabled', int(newFramePiece.isDisabled()))
                # rotation and scaling - ALWAYS 1 when DISABLE is 0
                # Y offset

                # resolution x
                # flip vertical
                # flip horizontal
                # last frame
                # unused - leave 0
                # X offset

                # palette - this will be autocalculated
                # priority - ALWAYS 3
                # tileindex - ALWAYS follows the rules of memory placement: 4 blocks = +1 index.  1 block min

                ##document the used config
                metaFrameData.append(newFramePiece)
                if newFramePiece.isLast():
                    break

            self.frameData.append(metaFrameData)

        in_file.seek(ptrOffsetsTable)
        self.offsetData = []
        for offset_idx in range(len(ptrMetaFrames)):
            headX = int.from_bytes(in_file.read(2), 'little', signed=True)
            headY = int.from_bytes(in_file.read(2), 'little', signed=True)
            lhandX = int.from_bytes(in_file.read(2), 'little', signed=True)
            lhandY = int.from_bytes(in_file.read(2), 'little', signed=True)
            rhandX = int.from_bytes(in_file.read(2), 'little', signed=True)
            rhandY = int.from_bytes(in_file.read(2), 'little', signed=True)
            centerX = int.from_bytes(in_file.read(2), 'little', signed=True)
            centerY = int.from_bytes(in_file.read(2), 'little', signed=True)
            self.offsetData.append(FrameOffset((headX, headY), (lhandX, lhandY), (rhandX, rhandY), (centerX, centerY)))

        ##read all anim pointers
        self.animGroupData = []
        for ptrAnimGroup in ptrAnimGroups:
            animGroup = []
            for a_idx, ptrAnim in enumerate(ptrAnimGroup):
                # if repeating the same pointer, it's the same animation. skip
                if a_idx > 0 and ptrAnim == ptrAnimGroup[a_idx - 1]:
                    continue
                in_file.seek(ptrAnim)
                animSequence = []
                while True:
                    frameDur = int.from_bytes(in_file.read(1), 'little')
                    flag = int.from_bytes(in_file.read(1), 'little')
                    frameIndex = int.from_bytes(in_file.read(2), 'little')
                    sprOffX = int.from_bytes(in_file.read(2), 'little', signed=True)
                    sprOffY = int.from_bytes(in_file.read(2), 'little', signed=True)
                    sdwOffX = int.from_bytes(in_file.read(2), 'little', signed=True)
                    sdwOffY = int.from_bytes(in_file.read(2), 'little', signed=True)
                    if frameDur == 0:
                        break
                    else:
                        animSequence.append(SequenceFrame(frameIndex, frameDur, flag,
                                                        (sprOffX, sprOffY), (sdwOffX, sdwOffY)))
                animGroup.append(animSequence)
            self.animGroupData.append(animGroup)




class SequenceFrame:

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


class MetaFramePiece:

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



class FrameOffset:

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


class ImgPiece:
    def __init__(self):
        self.imgPx = []
        self.zSort = 0


class AnimStat:

    def __init__(self, index, name, size, backref):
        self.index = index
        self.name = name
        self.size = size
        self.backref = backref
        self.durations = []
        self.rushFrame = -1
        self.hitFrame = -1
        self.returnFrame = -1


def updateUnusedStats(log_params, name, val):
    #stats.append([log_params[0], log_params[1], name, log_params[2:], val])
    if DEBUG_PRINT and val != 0:
        print('  ' + name + ':' + str(val))

