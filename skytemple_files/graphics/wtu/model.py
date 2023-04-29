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

from range_typed_integers import u16, u32

from skytemple_files.common.util import AutoString, read_u16, read_u32

MAGIC_NUMBER = b"WTU\0"
WTU_ENTRY_LEN = 8


class WtuEntry(AutoString):
    x: u16
    y: u16
    width: u16
    height: u16

    def __init__(self, x: u16, y: u16, width: u16, height: u16):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WtuEntry):
            return False
        return (
            self.x == other.x
            and self.y == other.y
            and self.width == other.width
            and self.height == other.height
        )


class Wtu(AutoString):
    image_mode: u32
    header_size: u32

    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        assert self.matches(
            data, 0
        ), "The Wtu file must begin with the WTU magic number"
        number_entries = read_u32(data, 0x4)
        self.image_mode = read_u32(data, 0x8)
        # The size of this header; Wtu entries start from this address
        self.header_size = read_u32(data, 0xC)

        self.entries = []
        for i in range(
            self.header_size,
            self.header_size + number_entries * WTU_ENTRY_LEN,
            WTU_ENTRY_LEN,
        ):
            self.entries.append(
                WtuEntry(
                    read_u16(data, i + 0x00),
                    read_u16(data, i + 0x02),
                    read_u16(data, i + 0x04),
                    read_u16(data, i + 0x06),
                )
            )

    @staticmethod
    def matches(data, header_pnt):
        return data[header_pnt : header_pnt + len(MAGIC_NUMBER)] == MAGIC_NUMBER

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Wtu):
            return False
        return (
            self.image_mode == other.image_mode
            and self.header_size == other.header_size
            and self.entries == other.entries
        )
