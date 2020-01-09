from bitstring import BitStream

from skytemple_files.compression.bpc_tilemap.compressor import BpcTilemapCompressor
from skytemple_files.compression.bpc_tilemap.decompressor import BpcTilemapDecompressor


class BpcTilemapHandler:
    """
    todo
    """
    @classmethod
    def decompress(cls, compressed_data: BitStream, stop_when_size: int) -> BitStream:
        """todo. Stops when stop_when_size bytes have been decompressed."""
        return BpcTilemapDecompressor(compressed_data, stop_when_size).decompress()

    @classmethod
    def compress(cls, uncompressed_data: BitStream) -> BitStream:
        """todo"""
        return BpcTilemapCompressor(uncompressed_data).compress()
