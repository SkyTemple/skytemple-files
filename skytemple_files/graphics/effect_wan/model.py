#  Copyright 2020-2025 SkyTemple Contributors
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
# mypy: ignore-errors
from __future__ import annotations

from io import BytesIO

from PIL import Image
from range_typed_integers import u32

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable

SPACE_WIDTH = 512
SPACE_HEIGHT = 1024
CENTER_X = 256
CENTER_Y = 508

TEX_SIZE = 8
DIM_TABLE = [
    (1, 1),
    (2, 2),
    (4, 4),
    (8, 8),
    (2, 1),
    (4, 1),
    (4, 2),
    (8, 4),
    (1, 2),
    (1, 4),
    (2, 4),
    (4, 8),
]

DEBUG_PRINT = False


class WanFile(Sir0Serializable):
    def __init__(self, data: bytes | None = None, header_pnt: int = 0):
        if data is None:
            self.imgType = -1
            self.is256Color = 0
            self.imgData = None
            self.frameData = []
            # List of list of SequenceFrame
            self.animData = []
            self.customPalette = []
            self.paletteOffset = 0
        else:
            self.ImportWan(data, header_pnt)

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: int,
        static_data: Pmd2Data | None = None,
    ) -> Sir0Serializable:
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> tuple[bytes, list[u32], u32 | None]:
        raise NotImplementedError()

    # This will accurately load all sir0 found in effect.bin with a few exceptions:
    # effect0268-00289: Not WAN.  Used for screen effects in moves and cutscenes.
    # effect0290-00291: Not Sir0
    def ImportWan(self, data, ptrOffsets, ptrWAN=0):
        in_file = BytesIO()
        in_file.write(data)
        in_file.seek(0)

        ##Read WAN header: ptr to AnimInfo, ptr to ImageDataInfo
        in_file.seek(ptrWAN)
        ptrAnimInfo = int.from_bytes(in_file.read(4), "little")
        ptrImageDataInfo = int.from_bytes(in_file.read(4), "little")
        if ptrAnimInfo == 0 and ptrImageDataInfo == 0:
            print("  Null Anim Info and Image Data Info pointer in Wan Header!")
            return None
        self.imgType = int.from_bytes(in_file.read(2), "little")
        if self.imgType < 1 or self.imgType > 3:
            print("  Not an effect! ImgType: {0}".format(self.imgType))
            return None

        updateUnusedStats([], "Unk#12", int.from_bytes(in_file.read(2), "little"))

        if ptrImageDataInfo > 0:
            ##Read ImageDataInfo: ptr to ImageDataTable block, ptr to PaletteInfo, NbImgs, print Unk#13 and Is256ColorSpr
            in_file.seek(ptrImageDataInfo)
            ptrImageDataTable = int.from_bytes(in_file.read(4), "little")
            ptrPaletteInfo = int.from_bytes(in_file.read(4), "little")
            if ptrImageDataTable == 0 or ptrPaletteInfo == 0:
                print("  Null pointer in Image Data Info!")
                return None

            # Unk#13 - ALWAYS 1
            updateUnusedStats([], "Unk#13", int.from_bytes(in_file.read(2), "little"))
            self.is256Color = int.from_bytes(in_file.read(2), "little")
            # Unk#11 - ALWAYS 1 except for:
            # effect_0292 - 12
            updateUnusedStats([], "Unk#11", int.from_bytes(in_file.read(2), "little"))
            nbImgs = int.from_bytes(in_file.read(2), "little")

            ##Read PaletteInfo: ptr to PaletteDataBlock, print NbColorsPerRow and All unknowns
            in_file.seek(ptrPaletteInfo)
            ptrPaletteDataBlock = int.from_bytes(in_file.read(4), "little")
            # Unk#3 - ALWAYS 1 except for:
            # effect_0001 - 0
            updateUnusedStats([], "Unk#11", int.from_bytes(in_file.read(2), "little"))
            # total number of colors... presumably.
            # But actually doesn't read all the way to the end of the palette block, and some colors would be missed!
            totalColors = int.from_bytes(in_file.read(2), "little")
            # Unk#4 - ALWAYS 1 except for:
            # effect_0001 - 0
            updateUnusedStats([], "Unk#4", int.from_bytes(in_file.read(2), "little"))
            # Unk#5 - ALWAYS 269 except for:
            # effect_0001 - 255
            # effect_0262 - 255
            unk5 = int.from_bytes(in_file.read(2), "little")

            # TODO: not sure if this accurately captures behavior of palette offset.
            # For now, assume the second nibble is the palette offset
            self.paletteOffset = unk5 % 16
            # and the last value is whether to offset or not
            makeOffset = unk5 // 256
            if makeOffset == 0:
                self.paletteOffset = 0

            ##Read PaletteDataBlock: Save contents
            if self.is256Color == 4:
                # TODO: this is a special case seen only in effect267
                # the current code results in texture but it appears incomplete
                # needs more research, but it is only one file.
                nbColorsPerRow = 256
                in_file.seek(ptrPaletteDataBlock)
                totalColors = (ptrPaletteInfo - ptrPaletteDataBlock) // 4
                self.customPalette = []
                palette = [(0, 0, 0, 0)] * nbColorsPerRow
                for jj in range(totalColors):
                    red = int.from_bytes(in_file.read(1), "little") // 8 * 8 * 32 // 31
                    blue = int.from_bytes(in_file.read(1), "little") // 8 * 8 * 32 // 31
                    green = int.from_bytes(in_file.read(1), "little") // 8 * 8 * 32 // 31
                    in_file.read(1)
                    palette[16 + jj] = (red, blue, green, 255)
                    self.customPalette.append(palette)
            elif self.is256Color == 1:
                # 8bpp = 2^8 colors
                nbColorsPerRow = 256
                nbReadsPerRow = 16
                in_file.seek(ptrPaletteDataBlock)
                totalColors = (ptrPaletteInfo - ptrPaletteDataBlock) // 4
                totalPalettes = totalColors // nbReadsPerRow
                self.customPalette = []
                for ii in range(totalPalettes):
                    palette = [(0, 0, 0, 0)] * nbColorsPerRow
                    for jj in range(nbReadsPerRow):
                        red = int.from_bytes(in_file.read(1), "little") // 8 * 8 * 32 // 31
                        blue = int.from_bytes(in_file.read(1), "little") // 8 * 8 * 32 // 31
                        green = int.from_bytes(in_file.read(1), "little") // 8 * 8 * 32 // 31
                        in_file.read(1)
                        palette[16 + jj] = (red, blue, green, 255)
                    self.customPalette.append(palette)
            else:
                # 4bpp = 2^4 colors
                nbColorsPerRow = 16
                in_file.seek(ptrPaletteDataBlock)
                totalColors = (ptrPaletteInfo - ptrPaletteDataBlock) // 4
                totalPalettes = totalColors // nbColorsPerRow
                self.customPalette = []
                for ii in range(totalPalettes):
                    palette = []
                    for jj in range(nbColorsPerRow):
                        red = int.from_bytes(in_file.read(1), "little")
                        blue = int.from_bytes(in_file.read(1), "little")
                        green = int.from_bytes(in_file.read(1), "little")
                        in_file.read(1)
                        palette.append((red, blue, green, 255))
                    self.customPalette.append(palette)

            ##Read ImageDataTable: list of all ptr to CompressedImages (use the Nb of images variable to know when to stop)
            in_file.seek(ptrImageDataTable)
            ptrImgs = []
            for img in range(nbImgs):
                ptrImgs.append(int.from_bytes(in_file.read(4), "little"))

            if self.imgType == 3:
                in_file.seek(ptrImgs[0])
                imgLists = []
                imgPx = []
                pxStrip = []
                ptrPixSrc = int.from_bytes(in_file.read(4), "little")
                atlasWidth = int.from_bytes(in_file.read(2), "little")
                atlasHeight = int.from_bytes(in_file.read(2), "little")
                updateUnusedStats([], "z-Sort", int.from_bytes(in_file.read(4), "little"))

                in_file.seek(ptrPixSrc)
                while in_file.tell() < ptrImgs[0]:
                    px = int.from_bytes(in_file.read(1), "little")
                    if self.is256Color:
                        pxStrip.append(px)
                    else:
                        pxStrip.append(px % 16)
                        pxStrip.append(px // 16)
                imgPx.append(pxStrip)
                imgLists.append(imgPx)
                self.imgData = ImageData(atlasWidth, atlasHeight, imgLists)
            else:
                ##Read CompTable: Read all Image data and assemble; add byte arrays into a list.
                imgLists = []  # list of imgPx, which is a list of pxStrip, which is a list of bytes
                # in 8bpp mode, each imgdata list entry must sum to 128 bytes
                for ptrImg in ptrImgs:
                    in_file.seek(ptrImg)
                    imgPx = []
                    ##Read pixels or zero padding.
                    while True:
                        ptrPixSrc = int.from_bytes(in_file.read(4), "little")
                        amt = int.from_bytes(in_file.read(2), "little")
                        if ptrPixSrc == 0 and amt == 0:
                            break
                        updateUnusedStats([], "Unk#14", int.from_bytes(in_file.read(2), "little"))
                        updateUnusedStats([], "z-Sort", int.from_bytes(in_file.read(4), "little"))

                        pxStrip = []
                        if ptrImg not in ptrOffsets:
                            for zero in range(amt):
                                pxStrip.append(0)
                        else:
                            ptrCurrent = in_file.tell()
                            in_file.seek(ptrPixSrc)
                            for pix in range(amt):
                                px = int.from_bytes(in_file.read(1), "little")
                                if self.is256Color:
                                    pxStrip.append(px)
                                else:
                                    pxStrip.append(px % 16)
                                    pxStrip.append(px // 16)

                            in_file.seek(ptrCurrent)
                        imgPx.append(pxStrip)
                    imgLists.append(imgPx)
                self.imgData = ImageData(0, 0, imgLists)
        else:
            self.is256Color = False
            self.imgData = None
            self.customPalette = None
            self.paletteOffset = 0

        if ptrAnimInfo > 0:
            ##Read AnimInfo: ptr to MetaFramesRefTable, ptr to AnimGroupTable
            in_file.seek(ptrAnimInfo)
            ptrMetaFramesRefTable = int.from_bytes(in_file.read(4), "little")
            in_file.read(4)
            ptrAnimGroupTable = int.from_bytes(in_file.read(4), "little")
            nbAnimGroups = int.from_bytes(in_file.read(2), "little")
            ##get ptr to AnimGroupTable
            in_file.seek(ptrAnimGroupTable)
            ptrAnims = []
            for ptrAnimSeq in range(nbAnimGroups):
                ##read the location
                animLoc = int.from_bytes(in_file.read(4), "little")
                ##read the length
                animLength = int.from_bytes(in_file.read(2), "little")
                ##read empty
                in_file.read(2)
                ##save curlocation
                curLocation = in_file.tell()
                ##go to seq location
                in_file.seek(animLoc)
                for ii in range(animLength):
                    ##read all anim frames
                    ptrAnims.append(int.from_bytes(in_file.read(4), "little"))
                in_file.seek(curLocation)

            in_file.seek(ptrAnimGroupTable)
            ptrAnimSequenceTable = int.from_bytes(in_file.read(4), "little")

            ##Read MetaFramesRefTable: list of all ptr to Meta Frames (stop when reached AnimGroupTable)
            in_file.seek(ptrMetaFramesRefTable)
            ptrMetaFrames = []
            while in_file.tell() < ptrAnimSequenceTable:
                ptrMetaFrames.append(int.from_bytes(in_file.read(4), "little"))

            ##Read MetaFrames: for each meta frame group, read until "end of meta frame group" bit is reached.
            self.frameData = []
            for frame_idx, ptrMetaFrame in enumerate(ptrMetaFrames):
                in_file.seek(ptrMetaFrame)
                if self.imgType == 3:
                    # TODO: research metaframe format for imgtype 3
                    pass
                else:
                    metaFrameData = []
                    while True:
                        in_file.read(3)
                        drawValue = int.from_bytes(in_file.read(1), "little")
                        ##Read Palette and Dimension values, and save with those values.
                        yData = int.from_bytes(in_file.read(2), "little")
                        xData = int.from_bytes(in_file.read(2), "little")
                        yOffset = yData % 1024
                        xOffset = xData % 512
                        dimType = yData // 16384
                        dimData = xData // 2048
                        endPiece = dimData % 2 == 1
                        flipHoriz = dimData // 2 % 2 == 1
                        flipVert = dimData // 4 % 2 == 1
                        dims = DIM_TABLE[dimType * 4 + dimData // 8]
                        blockOffset = int.from_bytes(in_file.read(1), "little")
                        paletteIndex = int.from_bytes(in_file.read(1), "little") // 16
                        ##document the used config
                        metaFrameData.append(
                            MetaFrame(
                                blockOffset,
                                paletteIndex,
                                dims,
                                (xOffset, yOffset),
                                flipHoriz,
                                flipVert,
                                (drawValue == 0),
                            )
                        )
                        ##break if last meta-frame
                        if endPiece:
                            break
                    self.frameData.append(metaFrameData)

            ##read all anim pointers
            self.animData = []
            for ptrAnim in ptrAnims:
                in_file.seek(ptrAnim)
                singleAnim = []
                while True:
                    frameDur = int.from_bytes(in_file.read(2), "little")
                    frameIndex = int.from_bytes(in_file.read(2), "little")
                    sprOffX = int.from_bytes(in_file.read(2), "little")
                    sprOffY = int.from_bytes(in_file.read(2), "little")
                    in_file.read(2)
                    in_file.read(2)
                    if frameDur == 0:
                        break
                    else:
                        singleAnim.append(SequenceFrame(frameIndex, frameDur, (sprOffX, sprOffY)))
                self.animData.append(singleAnim)
        else:
            self.frameData = None
            self.animData = None


class ImageData(object):
    def __init__(self, atlasX, atlasY, imageLists):
        self.atlasX = atlasX
        self.atlasY = atlasY
        self.imageLists = imageLists


class SequenceFrame(object):
    def __init__(self, frmIndex, duration, offset):
        self.frmIndex = frmIndex
        self.duration = duration
        self.offset = offset


class MetaFrame(object):
    def __init__(self, blockOffset, paletteIndex, res, offset, hFlip, vFlip, front):
        self.blockOffset = blockOffset
        self.paletteIndex = paletteIndex
        self.hFlip = hFlip
        self.vFlip = vFlip
        self.offset = offset
        self.res = res
        self.front = front

    def Clone(self):
        return MetaFrame(self.blockOffset, self.paletteIndex, self.res, self.offset, self.hFlip, self.vFlip, self.front)

    def DrawOn(self, inImg, imgPiece, exOffset):
        if self.hFlip:
            imgPiece = imgPiece.transpose(Image.FLIP_LEFT_RIGHT)
        if self.vFlip:
            imgPiece = imgPiece.transpose(Image.FLIP_TOP_BOTTOM)

        inImg.paste(imgPiece, (self.offset[0] - exOffset[0], self.offset[1] - exOffset[1]), imgPiece)


def mergeWithBasePalette(effectData, basePalette):
    if effectData.paletteOffset == 0:
        return

    # create a new palette data with the same values as the base
    newPalette = []
    for baseRow in basePalette:
        row = [col for col in baseRow]
        newPalette.append(row)

    # overwrite the region specified by the effectdata
    for idx, baseRow in enumerate(effectData.customPalette):
        row = [col for col in baseRow]
        while effectData.paletteOffset + idx >= len(newPalette):
            newPalette.append([(0, 0, 0, 0)] * len(baseRow))
        newPalette[effectData.paletteOffset + idx] = row

    # set effectData to the palette
    effectData.customPalette = newPalette
    # set offset to 0
    effectData.paletteOffset = 0


def updateUnusedStats(log_params, name, val):
    # stats.append([log_params[0], log_params[1], name, log_params[2:], val])
    if DEBUG_PRINT and val != 0:
        print("  " + name + ":" + str(val))
