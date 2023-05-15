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

from range_typed_integers import u16, u16_checked

from skytemple_files.common.util import read_u16
from skytemple_files.compression_container.common_at.model import CommonAt
from typing import Optional


class BpcTilemapCompressionContainer(CommonAt):
    length_decompressed: u16

    def __init__(self, data: Optional[bytes] = None):
        if data:
            self.length_decompressed = read_u16(data, 6)
            self.compressed_data = data[8:]

    def decompress(self) -> bytes:
        from skytemple_files.common.types.file_types import FileType

        data = FileType.BPC_TILEMAP.decompress(
            self.compressed_data, self.length_decompressed
        )
        return data

    def to_bytes(self) -> bytes:
        return (
            b"BPCTLM"
            + self.length_decompressed.to_bytes(2, "little")
            + self.compressed_data
        )  # pylint: disable=no-member

    @classmethod
    def cont_size(cls, data: bytes, byte_offset=0):
        return len(data)

    @classmethod
    def compress(cls, data: bytes) -> "BpcTilemapCompressionContainer":
        from skytemple_files.common.types.file_types import FileType

        new_container = cls()
        compressed_data = FileType.BPC_TILEMAP.compress(data)

        new_container.length_decompressed = u16_checked(len(data))
        new_container.compressed_data = compressed_data
        return new_container
