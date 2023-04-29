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

from typing import Literal, Union

from skytemple_files.common.util import (
    AutoString,
    write_u32,
    read_dynamic,
    write_u16,
    write_u8,
)


class ValList(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.data = bytearray(data)

    def get_list(self, value_size=2):
        lst = []
        for x in range(0, len(self.data), value_size):
            lst.append(
                read_dynamic(
                    self.data, x, length=value_size, signed=False, big_endian=False
                )
            )
        return lst

    def set_list(self, lst, value_size: Union[Literal[1], Literal[2], Literal[4]] = 2):
        self.data = bytearray(len(lst) * value_size)
        if value_size == 1:
            for i, x in enumerate(lst):
                write_u8(self.data, x, i * value_size)
        elif value_size == 2:
            for i, x in enumerate(lst):
                write_u16(self.data, x, i * value_size)
        elif value_size == 4:
            for i, x in enumerate(lst):
                write_u32(self.data, x, i * value_size)
        else:
            raise TypeError("Invalid value size")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValList):
            return False
        return self.data == other.data
