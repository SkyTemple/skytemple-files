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

from range_typed_integers import u32

from io import BytesIO

from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable

TEX_SIZE = 8
SCREEN_ATTR_DrawMask = 0x8000  # 1000 0000 0000 0000
SCREEN_ATTR_FlipYMask = 0x0800  # 0000 1000 0000 0000
SCREEN_ATTR_FlipXMask = 0x0400  # 0000 0100 0000 0000
SCREEN_ATTR_ValueMask = 0x03FF  # 0000 0011 1111 1111

DEBUG_PRINT = False


class ScreenEffectFile(Sir0Serializable):
    def __init__(self, data: bytes | None = None, header_pnt: int = 0):
        if data is None:
            self.imgData = None
            self.animData = None
            self.customPalette = None
        else:
            self.ImportScreenEffect(data, header_pnt)

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: int,
    ) -> Sir0Serializable:
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> tuple[bytes, list[u32], u32 | None]:
        raise NotImplementedError("Serialization not currently supported.")

    def ImportScreenEffect(self, data, ptrEffect=0):
        in_file = BytesIO()
        in_file.write(data)
        in_file.seek(0)

        ##Read Effect header: ptr to AnimData, ptr to ImgData, PaletteData
        in_file.seek(ptrEffect)
        nbFrames = int.from_bytes(in_file.read(4), "little")
        ptrAnimData = int.from_bytes(in_file.read(4), "little")
        updateUnusedStats([], "Unk#3", int.from_bytes(in_file.read(4), "little"))
        ptrImgData = int.from_bytes(in_file.read(4), "little")
        ptrPaletteDataBlock = int.from_bytes(in_file.read(4), "little")
        updateUnusedStats([], "Unk#1", int.from_bytes(in_file.read(2), "little"))
        updateUnusedStats([], "Unk#2", int.from_bytes(in_file.read(2), "little"))

        ##Read palette info
        nbColorsPerRow = 16
        in_file.seek(ptrPaletteDataBlock)
        totalColors = (ptrImgData - ptrPaletteDataBlock) // 4
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
        while in_file.tell() < ptrEffect:
            px = int.from_bytes(in_file.read(1), "little")
            self.imgData.append(px % 16)
            self.imgData.append(px // 16)

        ptrFrames = []
        in_file.seek(ptrAnimData)
        for idx in range(nbFrames):
            ##read the location
            ptrFrame = int.from_bytes(in_file.read(4), "little")
            ptrFrames.append(ptrFrame)

        self.animData = []
        for frame_idx, ptrFrame in enumerate(ptrFrames):
            in_file.seek(ptrFrame)

            updateUnusedStats([], "Unk#5", int.from_bytes(in_file.read(2), "little"))
            updateUnusedStats([], "Unk#7", int.from_bytes(in_file.read(2), "little"))

            # Must be 0x21 or else the animation doesn't play
            updateUnusedStats([], "Unk#6", int.from_bytes(in_file.read(2), "little"))
            row_height = int.from_bytes(in_file.read(2), "little")
            frame_dur = int.from_bytes(in_file.read(2), "little")
            in_file.read(18)
            alpha = int.from_bytes(in_file.read(2), "little")
            in_file.read(3)
            updateUnusedStats([], "Unk#4", int.from_bytes(in_file.read(1), "little"))
            in_file.read(2)

            pieces = []
            totalSlots = 0
            while True:
                drawValue = int.from_bytes(in_file.read(2), "little")
                skip = (SCREEN_ATTR_DrawMask & drawValue) == 0
                flipX = (SCREEN_ATTR_FlipXMask & drawValue) != 0
                flipY = (SCREEN_ATTR_FlipYMask & drawValue) != 0
                drawArg = SCREEN_ATTR_ValueMask & drawValue

                pieces.append(ScreenPiece(drawArg, flipX, flipY, skip))
                if skip:
                    totalSlots += drawArg
                else:
                    totalSlots += 1

                if totalSlots >= row_height * 33:
                    break

            end_ptr = ptrAnimData
            if frame_idx < len(ptrFrames) - 1:
                end_ptr = ptrFrames[frame_idx + 1]

            cur_pos = in_file.tell()
            if cur_pos != end_ptr and cur_pos != end_ptr - 2:
                raise Exception()

            self.animData.append(ScreenFrame(frame_dur, alpha, row_height, pieces))


class ScreenFrame(object):
    def __init__(self, duration, alpha, rowHeight, pieces):
        self.duration = duration
        self.alpha = alpha
        self.rowHeight = rowHeight
        self.pieces = pieces


class ScreenPiece(object):
    def __init__(self, index, flipX, flipY, skip):
        self.index = index
        self.flipX = flipX
        self.flipY = flipY
        self.skip = skip


def updateUnusedStats(log_params, name, val):
    # stats.append([log_params[0], log_params[1], name, log_params[2:], val])
    if DEBUG_PRINT and val != 0:
        print("  " + name + ":" + str(val))
