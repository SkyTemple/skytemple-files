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

from skytemple_files.compression.px.compressor import PxCompressor
from skytemple_files.compression.px.decompressor import PxDecompressor


class PxHandler:
    """
    Deals with the PX compression algorithm.
    Does not follow default DataHandler pattern,
    is more complex as it also needs control flags.
    """
    @classmethod
    def decompress(cls, compressed_data: bytes, flags: bytes) -> bytes:
        """Decompresses data stored as PX."""
        return PxDecompressor(compressed_data, flags).decompress()

    @classmethod
    def compress(cls, uncompressed_data: bytes) -> Tuple[bytes, bytes]:
        """Compresses data as PX and returns the control flags (0) and data (1)."""
        return PxCompressor(uncompressed_data).compress()
