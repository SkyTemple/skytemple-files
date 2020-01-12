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
