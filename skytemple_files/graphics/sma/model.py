#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable

TEX_SIZE = 8

DEBUG_PRINT = False


class SmaFile(Sir0Serializable):
    def __init__(self, data: bytes | None = None, header_pnt: int = 0):
        if data is None:
            self.imgData = None
            self.animData = None
            self.customPalette = None
        else:
            self.ImportSma(data, header_pnt)

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: int,
    ) -> Sir0Serializable:
        return cls(content_data, data_pointer)

    def ImportSma(self, data, ptrSMA=0):
        in_file = BytesIO()
        in_file.write(data)
        in_file.seek(0)

        ##Read SMA header: ptr to AnimData, ptr to ImgData, PaletteData
        in_file.seek(ptrSMA)
        updateUnusedStats([], "Unk#1", int.from_bytes(in_file.read(4), "little"))
        ptrAnimData = int.from_bytes(in_file.read(4),'little')
        nbFrames = int.from_bytes(in_file.read(4),'little')
        print('  nbFrames:' + str(nbFrames))
        ptrImgData = int.from_bytes(in_file.read(4),'little')
        updateUnusedStats([], "Unk#2", int.from_bytes(in_file.read(4), "little"))
        ptrPaletteDataBlock = int.from_bytes(in_file.read(4),'little')
        updateUnusedStats([], "Unk#3", int.from_bytes(in_file.read(4), "little"))
        updateUnusedStats([], "Unk#4", int.from_bytes(in_file.read(4), "little"))

        ##Read palette info
        nbColorsPerRow = 16
        in_file.seek(ptrPaletteDataBlock)
        totalColors = (ptrSMA-ptrPaletteDataBlock) // 4
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

        ##read image data
        self.imgData = []
        in_file.seek(ptrImgData)
        while (in_file.tell() < ptrPaletteDataBlock):
            px = int.from_bytes(in_file.read(1),'little')
            self.imgData.append(px % 16)
            self.imgData.append(px // 16)

        self.animData = []
        in_file.seek(ptrAnimData)
        for ii in range(nbFrames):
            blockX = int.from_bytes(in_file.read(1),'little')
            blockY = int.from_bytes(in_file.read(1),'little')
            updateUnusedStats([], "Unk#5", int.from_bytes(in_file.read(2), "little"))
            byteOffset = int.from_bytes(in_file.read(2),'little')
            in_file.read(2)
            blockLength = int.from_bytes(in_file.read(2),'little')
            updateUnusedStats([], "Unk#6", int.from_bytes(in_file.read(2), "little"))
            anim = SmaAnim(blockX, blockY, byteOffset, blockLength)
            self.animData.append(anim)


class SmaAnim(object):

    def __init__(self, blockWidth, blockHeight, byteOffset, frameCount):

        self.blockWidth = blockWidth
        self.blockHeight = blockHeight
        self.byteOffset = byteOffset
        self.frameCount = frameCount



def updateUnusedStats(log_params, name, val):
    # stats.append([log_params[0], log_params[1], name, log_params[2:], val])
    if DEBUG_PRINT and val != 0:
        print("  " + name + ":" + str(val))