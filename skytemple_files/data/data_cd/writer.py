"""Converts WazaP models back into the binary format used by the game"""
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

from range_typed_integers import u16_checked, u32_checked

from skytemple_files.common.util import write_u16, write_u32
from skytemple_files.data.data_cd.model import DataCD


class DataCDWriter:
    def __init__(self, model: DataCD):
        self.model = model

    def write(self) -> bytes:
        nb_items = len(self.model.items_effects)

        header = bytearray(4 + 2 * nb_items + len(self.model.effects_code) * 8)
        write_u32(header, u32_checked(4 + 2 * nb_items), 0)
        code_data = bytearray(0)
        current_ptr = len(header)
        for i, c in enumerate(self.model.effects_code):
            write_u32(header, u32_checked(current_ptr), 4 + 2 * nb_items + i * 8)
            write_u32(header, u32_checked(len(c)), 4 + 2 * nb_items + i * 8 + 4)
            code_data += bytearray(c)
            current_ptr += len(c)

        for i, x in enumerate(self.model.items_effects):
            write_u16(header, u16_checked(x), 4 + 2 * i)
        file_data = header + code_data
        return bytes(file_data)
