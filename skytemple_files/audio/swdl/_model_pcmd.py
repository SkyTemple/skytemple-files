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

from skytemple_files.audio.swdl.protocol import SwdlPcmdProtocol
from skytemple_files.common.util import *


class SwdlPcmd(SwdlPcmdProtocol):
    def __init__(self, data: Union[bytes, memoryview]):
        assert data[0x00:0x04] == b'pcmd', "Data is not valid SWDL PCMD"
        assert data[0x004:0x06] == bytes(2), "Data is not valid SWDL PCMD"
        assert data[0x006:0x08] == bytes([0x15, 0x04]), "Data is not valid SWDL PCMD"
        assert data[0x008:0x0C] == bytes([0x10, 0x00, 0x00, 0x00]), "Data is not valid SWDL PCMD"
        len_chunk_data = read_uintle(data, 0x0C, 4)
        self._length = 0x10 + len_chunk_data
        assert len(data) >= self._length, "Data is not valid SWDL PCMD"
        self.chunk_data = bytes(data[0x10:self._length])

    def get_initial_length(self):
        return self._length

    def to_bytes(self) -> bytes:
        buffer = bytearray(b'pcmd\0\0\x15\x04\x10\0\0\0\0\0\0\0')
        write_uintle(buffer, len(self.chunk_data), 0x0C, 4)

        padding = bytes()
        if len(self.chunk_data) % 16 != 0:
            # TODO: Unknown what this magic value means
            padding += bytes([0xb4, 0x03, 0, 0, 0x68, 0x01, 0x51, 0x04])
        # TODO: is this ok???
        if (len(self.chunk_data) + len(padding)) % 16 != 0:
            padding += bytes([0x00] * (16 - ((len(self.chunk_data) + len(padding)) % 16)))

        return buffer + self.chunk_data + padding

    def __eq__(self, other):
        if not isinstance(other, SwdlPcmd):
            return False
        return self.chunk_data == other.chunk_data
