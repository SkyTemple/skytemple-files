"""Converts GraphicFont models back into the binary format used by the game"""
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

from skytemple_files.common.util import *
from skytemple_files.graphics.fonts import *
from skytemple_files.graphics.fonts.graphic_font import *
from skytemple_files.graphics.fonts.graphic_font.model import GraphicFont


class GraphicFontWriter:
    def __init__(self, model: GraphicFont):
        self.model = model

    def write(self) -> bytes:
        buffer = bytearray(GRAPHIC_FONT_ENTRY_LEN * len(self.model.entries))
        
        # Font Data
        for i, e in enumerate(self.model.entries):
            if e:
                write_uintle(buffer, e.width, i*GRAPHIC_FONT_ENTRY_LEN+0x00)
                write_uintle(buffer, e.height, i*GRAPHIC_FONT_ENTRY_LEN+0x01)
                write_uintle(buffer, len(buffer), i*GRAPHIC_FONT_ENTRY_LEN+0x02, 2)
                data_raw = e.tobytes("raw", "P")
                buffer += bytearray(data_raw)
            else:
                write_uintle(buffer, 0xffff0000, i*GRAPHIC_FONT_ENTRY_LEN+0x00, 4)

        return buffer
