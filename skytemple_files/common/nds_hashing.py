"""Utils for hashing on the NDS."""
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

# http://problemkaputt.de/gbatek.htm#biosmiscfunctions
from range_typed_integers import u16


def nds_crc16(data: bytes, offset: int, length: int) -> u16:
    val = [0xC0C1, 0xC181, 0xC301, 0xC601, 0xCC01, 0xD801, 0xF001, 0xA001]
    crc = 0xFFFF
    for i in range(offset, offset + length):
        crc = crc ^ data[i]
        for j in range(0, 8):
            carry = crc & 1
            crc = crc >> 1
            if carry:
                crc = crc ^ (val[j] << (7 - j))

    return u16(crc)
