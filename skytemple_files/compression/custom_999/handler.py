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
#
#  This compression format is a modified version of
#  the AT6P container compression format used in 999
#  Changes made to the original algorithm are documented in the code
#  As this is based on AT6P,
#  the algorithm itself is based on this code (an AT6P decompressor): 
#  https://github.com/pleonex/tinke/blob/master/Plugins/999HRPERDOOR/999HRPERDOOR/AT6P.cs


from typing import Tuple

from skytemple_files.compression.custom_999.compressor import Custom999Compressor
from skytemple_files.compression.custom_999.decompressor import Custom999Decompressor


class Custom999Handler:
    """
    Deals with the compression algorithm, originally from 999.
    Does not follow default DataHandler pattern,
    is more complex as it also needs the decompressed size.
    """
    @classmethod
    def decompress(cls, compressed_data: bytes, decompressed_size: int) -> bytes:
        """Decompresses data stored."""
        return Custom999Decompressor(compressed_data, decompressed_size).decompress()

    @classmethod
    def compress(cls, uncompressed_data: bytes) -> bytes:
        """Compresses data and returns the compressed data."""
        return Custom999Compressor(uncompressed_data).compress()
