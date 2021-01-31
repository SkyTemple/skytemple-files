"""Converts FontSir0 models back into the binary format used by the game"""
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
from skytemple_files.graphics.fonts.font_sir0 import *
from skytemple_files.graphics.fonts.font_sir0.model import FontSir0
from skytemple_files.common.i18n_util import f, _


class FontSir0Writer:
    def __init__(self, model: FontSir0):
        self.model = model

    def write(self) -> Tuple[bytes, List[int], Optional[int]]:
        pointer_offsets = []

        sorted_entries = sorted(self.model.entries, key=lambda x:(x.table, x.char))
        buffer = bytearray()
        # Image data
        for i, e in enumerate(sorted_entries):
            buffer += e.data

        if len(buffer)%16!=0:
            buffer += bytearray([0xAA] * (16 - len(buffer)%16))
        # Character pointers
        char_pointer = bytearray(len(self.model.entries) * FONT_SIR0_ENTRY_LEN)
        char_pointer_offset = len(buffer)
        last = (None, None)
        for i, e in enumerate(sorted_entries):
            if last==(e.char, e.table):
                raise ValueError(_("Character {e.char} in table {e.table} is be defined multiple times in a font file!"))
            last = (e.char, e.table)
            pointer_offsets.append(len(buffer)+i * FONT_SIR0_ENTRY_LEN)
            write_uintle(char_pointer, i * FONT_SIR0_DATA_LEN, i * FONT_SIR0_ENTRY_LEN, 4)
            write_uintle(char_pointer, e.char, i * FONT_SIR0_ENTRY_LEN + 0x4)
            write_uintle(char_pointer, e.table, i * FONT_SIR0_ENTRY_LEN + 0x5)
            write_uintle(char_pointer, e.width, i * FONT_SIR0_ENTRY_LEN + 0x6, 4)
            write_uintle(char_pointer, e.cat, i * FONT_SIR0_ENTRY_LEN + 0xA)
            write_uintle(char_pointer, e.padding, i * FONT_SIR0_ENTRY_LEN + 0xB)
        buffer += char_pointer
        
        # Header
        header = bytearray(0x8)
        write_uintle(header, len(self.model.entries), 0, 4)
        pointer_offsets.append(len(buffer)+4)
        write_uintle(header, char_pointer_offset, 0x4, 4)

        header_pointer = len(buffer)
        buffer += header

        return buffer, pointer_offsets, header_pointer
