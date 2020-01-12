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
