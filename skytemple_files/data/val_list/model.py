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

class ValList(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.data = bytearray(data)

    def get_list(self, value_size = 2):
        lst = []
        for x in range(0, len(self.data), value_size):
            lst.append(read_uintle(self.data, x, value_size))
        return lst
    
    def set_list(self, lst, value_size = 2):
        self.data = bytearray(len(lst)*value_size)
        for i, x in enumerate(lst):
            write_uintle(self.data, x, i*value_size, value_size)
    
    def __eq__(self, other):
        if not isinstance(other, ValList):
            return False
        return self.data == other.data
