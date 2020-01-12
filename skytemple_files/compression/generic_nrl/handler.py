from typing import Tuple

from skytemple_files.compression.generic_nrl.compressor import GenericNrlCompressor
from skytemple_files.compression.generic_nrl.decompressor import GenericNrlDecompressor


class GenericNrlHandler:
    """
    Generic version of the NRL compression algorithm. Uses 1 byte as input and output sizes.
    todo
    """
    @classmethod
    def decompress(cls, compressed_data: bytes, stop_when_size: int) -> Tuple[bytes, int]:
        """todo. Stops when stop_when_size bytes have been decompressed.
        Second return is compressed original size.
        """
        with open('/tmp/before.bin', 'wb') as f:
            f.write(compressed_data)
        data = GenericNrlDecompressor(compressed_data, stop_when_size).decompress()
        with open('/tmp/before_un.bin', 'wb') as f:
            f.write(data[0])
        new_compressed = cls.compress(data[0])
        with open('/tmp/after.bin', 'wb') as f:
            f.write(new_compressed)
        after_data = GenericNrlDecompressor(new_compressed, stop_when_size).decompress()
        with open('/tmp/after_un.bin', 'wb') as f:
            f.write(after_data[0])
        assert data[0] == after_data[0]
        return data

    @classmethod
    def compress(cls, uncompressed_data: bytes) -> bytes:
        """todo"""
        return GenericNrlCompressor(uncompressed_data).compress()
