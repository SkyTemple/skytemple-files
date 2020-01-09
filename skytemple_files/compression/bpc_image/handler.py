from typing import Tuple

from bitstring import BitStream

from skytemple_files.compression.bpc_image.compressor import BpcImageCompressor
from skytemple_files.compression.bpc_image.decompressor import BpcImageDecompressor


class BpcImageHandler:
    """
    todo
    """
    @classmethod
    def decompress(cls, compressed_data: BitStream, stop_when_size: int) -> Tuple[BitStream, int]:
        """todo. Stops when stop_when_size bytes have been decompressed."""
        return BpcImageDecompressor(compressed_data, stop_when_size).decompress()

    @classmethod
    def compress(cls, uncompressed_data: BitStream) -> BitStream:
        """todo"""
        return BpcImageCompressor(uncompressed_data).compress()
