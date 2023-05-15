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

from range_typed_integers import u16_checked, u16

from skytemple_files.common.util import read_bytes, read_u16
from skytemple_files.compression_container.common_at.model import CommonAt
from typing import Optional


class At3px(CommonAt):
    length_decompressed: u16

    def __init__(self, data: Optional[bytes] = None):
        """
        Create a AT3PX container from already compressed data.
        Setting data None is private, use compress instead for compressing data.
        """
        if data:
            self.length_compressed = self.cont_size(data)
            self.compression_flags = read_bytes(data, 7, 9)
            self.compressed_data = data[0x10:]

    def decompress(self) -> bytes:
        """Returns the uncompressed data stored in the container"""
        from skytemple_files.common.types.file_types import FileType

        data = FileType.PX.decompress(
            self.compressed_data[: self.length_compressed - 0x10],
            self.compression_flags,
        )
        return data

    # pylint: disable=no-member
    def to_bytes(self) -> bytes:
        """Converts the container back into a bit (compressed) representation"""
        return (
            b"AT3PX"
            + self.length_compressed.to_bytes(2, "little")
            + self.compression_flags
            + self.compressed_data
        )

    @classmethod
    def cont_size(cls, data: bytes, byte_offset=0):
        return read_u16(data, byte_offset + 5)

    @classmethod
    def compress(cls, data: bytes) -> "At3px":
        """Create a new AT3PX container from originally uncompressed data."""
        from skytemple_files.common.types.file_types import FileType

        new_container = cls()
        flags, px_data = FileType.PX.compress(data)

        new_container.compression_flags = flags
        new_container.compressed_data = px_data
        new_container.length_compressed = u16_checked(len(px_data) + 0x10)
        return new_container
