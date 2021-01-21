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
from skytemple_files.compression_container.common_at.model import CommonAt

class At4pn(CommonAt):
    def __init__(self, data: bytes, new=False):
        """
        Create a AT4PN container from data.
        If new is true, a new container is created, with data being the content.
        """
        if new:
            self.data = data
        else:
            self.data = data[0x07:]
            assert self.cont_size(data) == len(data) - 0x7

    def get(self) -> bytes:
        """Returns the data stored in the container"""
        return self.data

    def to_bytes(self) -> bytes:
        """Converts the container back into bytes representation"""
        return b'AT4PN'\
               + len(self.data).to_bytes(2, 'little') \
               + self.data

    @classmethod
    def cont_size(cls, data: bytes, byte_offset=0):
        return read_uintle(data, byte_offset + 5, 2)


    # For compatibility with other AT formats
    def decompress(self) -> bytes:
        return self.get()

    @classmethod
    def compress(cls, data: bytes) -> CommonAt:
        return At4pn(data, new=True)
