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

from skytemple_files.common.util import write_u32, write_u16
from skytemple_files.data.inter_d.model import InterD


class InterDWriter:
    def __init__(self, model: InterD):
        self.model = model

    def write(self) -> bytes:
        header = bytearray(6 + 2 * len(self.model.list_dungeons))
        write_u32(header, u32_checked(len(header)), 0)
        code_data = bytearray(0)
        current = 0
        for i, x in enumerate(self.model.list_dungeons):
            for y in sorted(x, key=lambda v: v.floor):
                code_data += bytearray(y.to_bytes())
                current += 1
            write_u16(header, u16_checked(current), 6 + 2 * i)
        file_data = header + code_data
        return bytes(file_data)
