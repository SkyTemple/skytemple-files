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

from typing import Tuple

from skytemple_files.compression.rle_nibble.compressor import RleNibbleCompressor
from skytemple_files.compression.rle_nibble.decompressor import RleNibbleDecompressor


class RleNibbleHandler:
    """
    Deals with the RLE compression algorithm.
    This RLE implementation works with 4-bit nibbles.
    Does not follow default DataHandler pattern,
    is more complex as it also needs the decompressed size.
    """
    @classmethod
    def decompress(cls, compressed_data: bytes, decompressed_size: int) -> bytes:
        """Decompresses data stored as RLE."""
        return RleNibbleDecompressor(compressed_data, decompressed_size).decompress()

    @classmethod
    def compress(cls, uncompressed_data: bytes) -> bytes:
        """Compresses data as RLE and returns the compressed data."""
        return RleNibbleCompressor(uncompressed_data).compress()
