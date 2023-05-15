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

from range_typed_integers import u16_checked, u32_checked, u16, u32

from skytemple_files.common.util import read_u16, read_u32
from skytemple_files.compression_container.common_at.model import CommonAt
from typing import Optional


class Atupx(CommonAt):
    length_compressed: u16
    length_decompressed: u32

    def __init__(self, data: Optional[bytes] = None):
        """
        Create a ATUPX container from already compressed data.
        Setting data None is private, use compress instead for compressing data.
        """
        if data:
            self.length_compressed = self.cont_size(data)
            self.length_decompressed = read_u32(data, 7)
            self.compressed_data = data[0xB:]

    def decompress(self) -> bytes:
        """Returns the uncompressed data stored in the container"""
        from skytemple_files.common.types.file_types import FileType

        data = FileType.CUSTOM_999.decompress(
            self.compressed_data[: self.length_compressed - 0xB],
            self.length_decompressed,
        )
        return data

    # pylint: disable=no-member
    def to_bytes(self) -> bytes:
        """Converts the container back into a bit (compressed) representation"""
        return (
            b"ATUPX"
            + self.length_compressed.to_bytes(2, "little")
            + self.length_decompressed.to_bytes(4, "little")
            + self.compressed_data
        )

    @classmethod
    def cont_size(cls, data: bytes, byte_offset=0):
        return read_u16(data, byte_offset + 5)

    @classmethod
    def compress(cls, data: bytes) -> "Atupx":
        """Create a new ATUPX container from originally uncompressed data."""
        from skytemple_files.common.types.file_types import FileType

        new_container = cls()
        compressed_data = FileType.CUSTOM_999.compress(data)

        new_container.compressed_data = compressed_data
        new_container.length_decompressed = u32_checked(len(data))
        new_container.length_compressed = u16_checked(len(compressed_data) + 0xB)
        return new_container
