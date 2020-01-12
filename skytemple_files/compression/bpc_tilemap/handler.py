from skytemple_files.compression.bpc_tilemap.compressor import BpcTilemapCompressor
from skytemple_files.compression.bpc_tilemap.decompressor import BpcTilemapDecompressor


class BpcTilemapHandler:
    """
    todo
    """
    @classmethod
    def decompress(cls, compressed_data: bytes, stop_when_size: int) -> bytes:
        """todo. Stops when stop_when_size bytes have been decompressed."""
        with open('/tmp/before.bin', 'wb') as f:
            f.write(compressed_data)
        data = BpcTilemapDecompressor(compressed_data, stop_when_size).decompress()
        with open('/tmp/before_un.bin', 'wb') as f:
            f.write(data)
        new_compressed = cls.compress(data)
        with open('/tmp/after.bin', 'wb') as f:
            f.write(new_compressed)
        de = BpcTilemapDecompressor(new_compressed, stop_when_size)
        try:
            after_data = de.decompress()
            with open('/tmp/after_un.bin', 'wb') as f:
                f.write(after_data)
        except ValueError as e:
            with open('/tmp/after_un.bin', 'wb') as f:
                f.write(de.decompressed_data)
            raise e
        assert data[0] == after_data[0]
        return data

    @classmethod
    def compress(cls, uncompressed_data: bytes) -> bytes:
        """todo"""
        return BpcTilemapCompressor(uncompressed_data).compress()
