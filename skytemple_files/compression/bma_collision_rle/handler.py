from typing import Tuple

from bitstring import BitStream

from skytemple_files.compression.bma_collision_rle.compressor import BmaCollisionRleCompressor
from skytemple_files.compression.bma_collision_rle.decompressor import BmaCollisionRleDecompressor


class BmaCollisionRleHandler:
    """
    todo
    """
    @classmethod
    def decompress(cls, compressed_data: BitStream, stop_when_size: int) -> Tuple[BitStream, int]:
        """todo. Stops when stop_when_size bytes have been decompressed.
        Second return is compressed original size.
        """
        return BmaCollisionRleDecompressor(compressed_data, stop_when_size).decompress()

    @classmethod
    def compress(cls, uncompressed_data: BitStream) -> BitStream:
        """todo"""
        return BmaCollisionRleCompressor(uncompressed_data).compress()
