from typing import Tuple

from skytemple_files.compression.bma_collision_rle.compressor import BmaCollisionRleCompressor
from skytemple_files.compression.bma_collision_rle.decompressor import BmaCollisionRleDecompressor


class BmaCollisionRleHandler:
    """
    todo
    """
    @classmethod
    def decompress(cls, compressed_data: bytes, stop_when_size: int) -> Tuple[bytes, int]:
        """todo. Stops when stop_when_size bytes have been decompressed.
        Second return is compressed original size.
        """
        return BmaCollisionRleDecompressor(compressed_data, stop_when_size).decompress()

    @classmethod
    def compress(cls, uncompressed_data: bytes) -> bytes:
        """todo"""
        return BmaCollisionRleCompressor(uncompressed_data).compress()
