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
        with open('/tmp/before.bin', 'wb') as f:
            f.write(compressed_data)
        data = BpcImageDecompressor(compressed_data, stop_when_size).decompress()
        with open('/tmp/before_un.bin', 'wb') as f:
            f.write(data[0])
        new_compressed = cls.compress(data[0])
        with open('/tmp/after.bin', 'wb') as f:
            f.write(new_compressed)
        de = BpcImageDecompressor(new_compressed, stop_when_size)
        try:
            after_data = de.decompress()
            with open('/tmp/after_un.bin', 'wb') as f:
                f.write(after_data[0])
        except ValueError as e:
            with open('/tmp/after_un.bin', 'wb') as f:
                f.write(de.decompressed_data)
            raise e
        assert data[0] == after_data[0]
        return data

    @classmethod
    def compress(cls, uncompressed_data: bytes) -> bytes:
        """todo"""
        return BpcImageCompressor(uncompressed_data).compress()
