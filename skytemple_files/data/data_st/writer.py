"""Converts DataST models back into the binary format used by the game"""
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

from range_typed_integers import i16_checked, u32_checked

from skytemple_files.common.util import write_i16, write_u32
from skytemple_files.data.data_st.model import DataST


class DataSTWriter:
    def __init__(self, model: DataST):
        self.model = model

    def write(self) -> bytes:
        nb_items = len(self.model.struct_ids)

        header = bytearray(4 + 2 * nb_items)
        write_u32(header, u32_checked(4 + 2 * nb_items), 0)

        for i, x in enumerate(self.model.struct_ids):
            write_i16(header, i16_checked(x), 4 + 2 * i)

        file_data = header + self.model.struct_data
        return bytes(file_data)
