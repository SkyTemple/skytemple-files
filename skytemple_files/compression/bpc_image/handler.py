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

from skytemple_files.compression.bpc_image.compressor import BpcImageCompressor
from skytemple_files.compression.bpc_image.decompressor import BpcImageDecompressor


class BpcImageHandler:
    """
    todo
    """
    @classmethod
    def decompress(cls, compressed_data: bytes, stop_when_size: int) -> Tuple[bytes, int]:
        """todo. Stops when stop_when_size bytes have been decompressed."""
        return BpcImageDecompressor(compressed_data, stop_when_size).decompress()

    @classmethod
    def compress(cls, uncompressed_data: bytes) -> bytes:
        """todo"""
        return BpcImageCompressor(uncompressed_data).compress()
