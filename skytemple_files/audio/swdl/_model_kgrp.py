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
from typing import Union

from skytemple_files.audio.common import HasId
from skytemple_files.audio.swdl.protocol import SwdlKeygroupProtocol, SwdlKgrpProtocol
from skytemple_files.common.util import *

KEYGROUP_LEN = 8


class SwdlKeygroup(SwdlKeygroupProtocol, AutoString, HasId):
    def __init__(self, data: Union[bytes, memoryview], _assertId: int):
        self.id = read_uintle(data, 0x00, 2)
        HasId.__init__(self, self.id)
        assert self.id == _assertId, "Data is not valid WDL KGRP Keygroup"
        self.poly = read_sintle(data, 0x02)
        self.priority = read_uintle(data, 0x03)
        self.vclow = read_uintle(data, 0x04)
        self.vchigh = read_uintle(data, 0x05)
        self.unk50 = read_uintle(data, 0x06)
        self.unk51 = read_uintle(data, 0x07)

    def equals_without_id(self, other):
        if not isinstance(other, SwdlKeygroup):
            return False
        return self.poly == other.poly and self.priority == other.priority and self.vclow == other.vclow \
               and self.vchigh == other.vchigh and self.unk50 == other.unk50

    def to_bytes(self):
        data = bytearray(8)
        write_uintle(data, self.id, 0, 2)
        write_sintle(data, self.poly, 2)
        write_uintle(data, self.priority, 3)
        write_uintle(data, self.vclow, 4)
        write_uintle(data, self.vchigh, 5)
        write_uintle(data, self.unk50, 6)
        write_uintle(data, self.unk51, 7)
        return data


class SwdlKgrp(SwdlKgrpProtocol[SwdlKeygroup]):
    def __init__(self, data: Union[bytes, memoryview]):
        assert data[0x00:0x04] == b'kgrp', "Data is not valid SWDL KGRP"
        assert data[0x004:0x06] == bytes(2), "Data is not valid SWDL KGRP"
        assert data[0x006:0x08] == bytes([0x15, 0x04]), "Data is not valid SWDL KGRP"
        assert data[0x008:0x0C] == bytes([0x10, 0x00, 0x00, 0x00]), "Data is not valid SWDL KGRP"
        len_chunk_data = read_uintle(data, 0x0C, 4)

        self._length = 0x10 + len_chunk_data + (len_chunk_data % 16)
        number_slots = len_chunk_data // KEYGROUP_LEN  # TODO: Is this the way to do it?

        self.keygroups: List[SwdlKeygroup] = []
        for idx, pnt in enumerate(range(0, number_slots * KEYGROUP_LEN, KEYGROUP_LEN)):
            self.keygroups.append(SwdlKeygroup(data[0x10 + pnt:], _assertId=idx))

    def get_initial_length(self):
        return self._length

    def to_bytes(self) -> bytes:
        chunk = bytearray()
        for i, kgrp in enumerate(self.keygroups):
            assert kgrp.id == i
            chunk += kgrp.to_bytes()

        len_chunk = len(chunk)
        if len(chunk) % 16 != 0:
            # It's unknown what this seemingly magic value means.
            chunk += bytes([0xc7, 0xc8, 0x40, 0x00, 0xd0, 0x11, 0xa0, 0x04])
        assert len(chunk) % 16 == 0

        buffer = bytearray(b'kgrp\0\0\x15\x04\x10\0\0\0\0\0\0\0')
        write_uintle(buffer, len_chunk, 0x0C, 4)
        return buffer + chunk

    def __str__(self):
        chunks = ""
        for kgrp in self.keygroups:
            chunks += f">> {kgrp}\n"
        return """KGRP
""" + chunks

    def __eq__(self, other):
        if not isinstance(other, SwdlKgrp):
            return False
        return self.keygroups == other.keygroups
