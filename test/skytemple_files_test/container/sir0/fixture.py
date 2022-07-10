#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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

from dataclasses import dataclass
from typing import Optional, Tuple, List

from range_typed_integers import u32, u8, u16, u8_checked

from skytemple_files.common.util import read_u32, read_u16
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable


@dataclass
class DummySir0Serializable(Sir0Serializable):
    """
    A dummy test class for testing Sir0Serialization.

    Layout as bytes
    ---------------

    [0]: a
    [1]: b
    [2-19]: <Header>
    [20]: c
    [21]: d
    [22]: 0x3
    [23]: 0x4
    [24]: 0x5
    [25]: 0x6

    Header:
    [0-1]: header_val
    [2-5]: <PTR to a => 0>
    [6-9]: <PTR to b => 1>
    [10-13]: <PTR to c => 20>
    [14-17]: <PTR to d => 21>

    """

    a: u8
    b: u8
    c: u8
    d: u8
    header_val: u16

    def sir0_serialize_parts(self) -> Tuple[bytes, List[u32], Optional[u32]]:
        data = bytearray(26)
        data[0] = self.a
        data[1] = self.b
        data[2 : 2 + 2] = self.header_val.to_bytes(2, "little", signed=False)
        data[4 : 4 + 4] = (0).to_bytes(4, "little", signed=False)
        data[8 : 8 + 4] = (1).to_bytes(4, "little", signed=False)
        data[12 : 12 + 4] = (20).to_bytes(4, "little", signed=False)
        data[16 : 16 + 4] = (21).to_bytes(4, "little", signed=False)
        data[20] = self.c
        data[21] = self.d
        data[22] = 3
        data[23] = 4
        data[24] = 5
        data[25] = 6

        return data, [u32(4), u32(8), u32(12), u32(16)], u32(2)

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: u32,
    ) -> Sir0Serializable:
        # We are using the pointers to get the values of a, b, c, d to test that they are valid.
        assert data_pointer == 2
        return DummySir0Serializable(
            a=u8_checked(
                content_data[
                    read_u32(content_data[data_pointer + 2 : data_pointer + 6])
                ]
            ),
            b=u8_checked(
                content_data[
                    read_u32(content_data[data_pointer + 6 : data_pointer + 10])
                ]
            ),
            c=u8_checked(
                content_data[
                    read_u32(content_data[data_pointer + 10 : data_pointer + 14])
                ]
            ),
            d=u8_checked(
                content_data[
                    read_u32(content_data[data_pointer + 14 : data_pointer + 18])
                ]
            ),
            header_val=read_u16(content_data[data_pointer : data_pointer + 2]),
        )


DUMMY_FIXTURES = [
    (0, DummySir0Serializable(u8(1), u8(2), u8(3), u8(4), u16(0))),
    (1, DummySir0Serializable(u8(12), u8(34), u8(56), u8(78), u16(1234))),
    (2, DummySir0Serializable(u8(99), u8(32), u8(14), u8(45), u16(12345))),
]
