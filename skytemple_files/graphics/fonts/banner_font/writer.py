"""Converts BannerFont models back into the binary format used by the game"""
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
from typing import Optional

from skytemple_files.common.util import *
from skytemple_files.graphics.fonts import *
from skytemple_files.graphics.fonts.banner_font import *
from skytemple_files.graphics.fonts.banner_font.model import BannerFont

class BannerFontWriter:
    def __init__(self, model: BannerFont):
        self.model = model

    def write(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.common.types.file_types import FileType
        
        pointer_offsets = []

        char_offsets = []
        sorted_entries = sorted(self.model.entries, key=lambda x:(x.table, x.char))
        buffer = bytearray()
        # Image data
        for i, e in enumerate(sorted_entries):
            char_offsets.append(len(buffer))
            buffer += FileType.RLE_NIBBLE.compress(e.data)

        if len(buffer)%16!=0:
            buffer += bytearray([0xAA] * (16 - len(buffer)%16))
        # Character pointers
        char_pointer = bytearray(len(self.model.entries) * BANNER_FONT_ENTRY_LEN)
        char_pointer_offset = len(buffer)
        last = (None, None)
        for i, e in enumerate(sorted_entries):
            if last==(e.char, e.table):
                raise ValueError("Character {e.char} in table {e.table} is be defined multiple times in a font file!")
            last = (e.char, e.table)
            pointer_offsets.append(len(buffer)+i * BANNER_FONT_ENTRY_LEN)
            write_uintle(char_pointer, char_offsets[i], i * BANNER_FONT_ENTRY_LEN, 4)
            write_uintle(char_pointer, e.char, i * BANNER_FONT_ENTRY_LEN + 0x4)
            write_uintle(char_pointer, e.table, i * BANNER_FONT_ENTRY_LEN + 0x5)
            write_sintle(char_pointer, e.width, i * BANNER_FONT_ENTRY_LEN + 0x6, 2)
        buffer += char_pointer
        
        # Header
        header = bytearray(0xC)
        pointer_offsets.append(len(buffer))
        write_uintle(header, char_pointer_offset, 0, 4)
        write_uintle(header, len(self.model.entries), 0x4, 4)
        write_uintle(header, self.model.unknown, 0x8, 4)

        header_pointer = len(buffer)
        buffer += header

        return buffer, pointer_offsets, header_pointer
        
