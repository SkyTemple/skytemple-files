from skytemple_files.compression.bpc_tilemap.compressor import BpcTilemapCompressor
from skytemple_files.compression.bpc_tilemap.decompressor import BpcTilemapDecompressor


class BpcTilemapHandler:
    """
    todo
    """
    @classmethod
    def decompress(cls, compressed_data: bytes, stop_when_size: int) -> bytes:
        """todo. Stops when stop_when_size bytes have been decompressed."""
        return BpcTilemapDecompressor(compressed_data, stop_when_size).decompress()

    @classmethod
    def compress(cls, uncompressed_data: bytes) -> bytes:
        """todo"""
        return BpcTilemapCompressor(uncompressed_data).compress()
