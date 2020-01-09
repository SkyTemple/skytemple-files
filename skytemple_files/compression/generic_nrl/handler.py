from typing import Tuple

from bitstring import BitStream

from skytemple_files.compression.generic_nrl.compressor import GenericNrlCompressor
from skytemple_files.compression.generic_nrl.decompressor import GenericNrlDecompressor


class GenericNrlHandler:
    """
    Generic version of the NRL compression algorithm. Uses 1 byte as input and output sizes.
    todo
    """
    @classmethod
    def decompress(cls, compressed_data: BitStream, stop_when_size: int) -> Tuple[BitStream, int]:
        """todo. Stops when stop_when_size bytes have been decompressed.
        Second return is compressed original size.
        """
        return GenericNrlDecompressor(compressed_data, stop_when_size).decompress()

    @classmethod
    def compress(cls, uncompressed_data: BitStream) -> BitStream:
        """todo"""
        return GenericNrlCompressor(uncompressed_data).compress()
