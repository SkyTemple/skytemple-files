"""TODO: MERGE WITH GENERIC NRL"""
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

from skytemple_files.compression.bma_layer_nrl.compressor import BmaLayerNrlCompressor
from skytemple_files.compression.bma_layer_nrl.decompressor import BmaLayerNrlDecompressor


class BmaLayerNrlHandler:
    """
    todo
    """
    @classmethod
    def decompress(cls, compressed_data: bytes, stop_when_size: int) -> Tuple[bytes, int]:
        """todo. Stops when stop_when_size bytes have been decompressed.
        Second return is compressed original size.
        Returns 16 bit LE integer list. Input is compressed as pair24 (pairs of two 12 bit ints).
        """
        return BmaLayerNrlDecompressor(compressed_data, stop_when_size).decompress()

    @classmethod
    def compress(cls, uncompressed_data: bytes) -> bytes:
        """todo"""
        return BmaLayerNrlCompressor(uncompressed_data).compress()
