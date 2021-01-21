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
from skytemple_files.compression_container.at4pn.model import At4pn


class At4pnHandler(DataHandler[At4pn]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> At4pn:
        """Load a AT4PX container into a high-level representation"""
        if not cls.matches(data):
            raise ValueError("The provided data is not an AT4PN container.")
        return At4pn(data)

    @classmethod
    def serialize(cls, data: At4pn, **kwargs) -> bytes:
        """Convert the high-level AT4PN representation back into bytes."""
        return data.to_bytes()

    @classmethod
    def new(cls, data: bytes) -> At4pn:
        """Turn uncompressed data into a new AT4PN container"""
        return At4pn(data, new=True)

    @classmethod
    def cont_size(cls, data: bytes, byte_offset=0):
        """Get the size of an AT4PN container starting at the given offset in data."""
        if not cls.matches(data, byte_offset):
            raise ValueError("The provided data is not an AT4PN container.")
        return At4pn.cont_size(data, byte_offset)

    @classmethod
    def matches(cls, data: bytes, byte_offset=0):
        """Check if the given data is a At4pn container"""
        return read_bytes(data, byte_offset, 5) == b'AT4PN'

    # For compatibility with other AT formats
    @classmethod
    def compress(cls, data: bytes) -> At4pn:
        return At4pn.compress(data)
