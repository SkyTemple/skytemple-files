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

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.util import read_bytes
from skytemple_files.compression_container.at3px.model import At3px


class At3pxHandler(DataHandler[At3px]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> At3px:
        """Load a AT3PX container into a high-level representation"""
        if not cls.matches(data):
            raise ValueError("The provided data is not an AT3PX container.")
        return At3px(data)

    @classmethod
    def serialize(cls, data: At3px, **kwargs) -> bytes:
        """Convert the high-level AT3PX representation back into a BitStream."""
        return data.to_bytes()

    @classmethod
    def compress(cls, data: bytes) -> At3px:
        """Turn uncompressed data into a new AT3PX container"""
        return At3px.compress(data)

    @classmethod
    def cont_size(cls, data: bytes, byte_offset=0):
        """Get the size of an AT3PX container starting at the given offset in data."""
        if not cls.matches(data, byte_offset):
            raise ValueError("The provided data is not an AT3PX container.")
        return At3px.cont_size(data, byte_offset)

    @classmethod
    def matches(cls, data: bytes, byte_offset=0):
        """Check if the given data stream is a At3px container"""
        return read_bytes(data, byte_offset, 5) == b'AT3PX'
