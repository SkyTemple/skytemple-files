from typing import Tuple

from bitstring import BitStream

from skytemple_files.compression.bma_layer_nrl.compressor import BmaLayerNrlCompressor
from skytemple_files.compression.bma_layer_nrl.decompressor import BmaLayerNrlDecompressor


class BmaLayerNrlHandler:
    """
    todo
    """
    @classmethod
    def decompress(cls, compressed_data: BitStream, stop_when_size: int) -> Tuple[BitStream, int]:
        """todo. Stops when stop_when_size bytes have been decompressed.
        Second return is compressed original size.
        """
        return BmaLayerNrlDecompressor(compressed_data, stop_when_size).decompress()

    @classmethod
    def compress(cls, uncompressed_data: BitStream) -> BitStream:
        """todo"""
        return BmaLayerNrlCompressor(uncompressed_data).compress()
