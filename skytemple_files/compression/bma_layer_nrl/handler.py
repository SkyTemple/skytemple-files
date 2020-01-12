"""TODO: MERGE WITH GENERIC NRL"""
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
