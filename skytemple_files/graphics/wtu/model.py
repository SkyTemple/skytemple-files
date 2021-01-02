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
MAGIC_NUMBER = b'WTU\0'
WTU_ENTRY_LEN = 8


class WtuEntry(AutoString):
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __eq__(self, other):
        if not isinstance(other, WtuEntry):
            return False
        return self.x == other.x and \
               self.y == other.y and \
               self.width == other.width and \
               self.height == other.height


class Wtu(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        assert self.matches(data, 0), "The Wtu file must begin with the WTU magic number"
        number_entries = read_uintle(data, 0x4, 4)
        self.image_mode = read_uintle(data, 0x8, 4)
        # The size of this header; Wtu entries start from this address
        self.header_size = read_uintle(data, 0xC, 4)

        self.entries = []
        for i in range(self.header_size, self.header_size + number_entries * WTU_ENTRY_LEN, WTU_ENTRY_LEN):
            self.entries.append(WtuEntry(
                read_uintle(data, i + 0x00, 2),
                read_uintle(data, i + 0x02, 2),
                read_uintle(data, i + 0x04, 2),
                read_uintle(data, i + 0x06, 2),
            ))

    @staticmethod
    def matches(data, header_pnt):
        return data[header_pnt:header_pnt+len(MAGIC_NUMBER)] == MAGIC_NUMBER

    def __eq__(self, other):
        if not isinstance(other, Wtu):
            return False
        return self.image_mode == other.image_mode and \
               self.header_size == other.header_size and \
               self.entries == other.entries
