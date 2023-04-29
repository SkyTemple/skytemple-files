"""Converts GraphicFont models back into the binary format used by the game"""
#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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
from __future__ import annotations

from range_typed_integers import u8_checked, u16_checked, u32

from skytemple_files.common.util import write_u8, write_u16, write_u32
from skytemple_files.graphics.fonts.graphic_font import GRAPHIC_FONT_ENTRY_LEN
from skytemple_files.graphics.fonts.graphic_font.model import GraphicFont


class GraphicFontWriter:
    def __init__(self, model: GraphicFont):
        self.model = model

    def write(self) -> bytes:
        buffer = bytearray(GRAPHIC_FONT_ENTRY_LEN * len(self.model.entries))

        # Font Data
        for i, e in enumerate(self.model.entries):
            if e:
                write_u8(buffer, u8_checked(e.width), i * GRAPHIC_FONT_ENTRY_LEN + 0x00)
                write_u8(
                    buffer, u8_checked(e.height), i * GRAPHIC_FONT_ENTRY_LEN + 0x01
                )
                write_u16(
                    buffer, u16_checked(len(buffer)), i * GRAPHIC_FONT_ENTRY_LEN + 0x02
                )
                data_raw = e.tobytes("raw", "P")
                buffer += bytearray(data_raw)
            else:
                write_u32(buffer, u32(0xFFFF0000), i * GRAPHIC_FONT_ENTRY_LEN + 0x00)

        return buffer
