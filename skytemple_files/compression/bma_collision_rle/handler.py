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


from skytemple_files.compression.bma_collision_rle.compressor import (
    BmaCollisionRleCompressor,
)
from skytemple_files.compression.bma_collision_rle.decompressor import (
    BmaCollisionRleDecompressor,
)


class BmaCollisionRleHandler:
    """
    todo
    """

    @classmethod
    def decompress(
        cls, compressed_data: bytes, stop_when_size: int
    ) -> tuple[bytes, int]:
        """todo. Stops when stop_when_size bytes have been decompressed.
        Second return is compressed original size.
        """
        return BmaCollisionRleDecompressor(compressed_data, stop_when_size).decompress()

    @classmethod
    def compress(cls, uncompressed_data: bytes) -> bytes:
        """todo"""
        return BmaCollisionRleCompressor(uncompressed_data).compress()
