"""TODO: MERGE WITH GENERIC NRL"""
from typing import Tuple

from skytemple_files.compression.bma_layer_nrl.compressor import BmaLayerNrlCompressor
from skytemple_files.compression.bma_layer_nrl.decompressor import BmaLayerNrlDecompressor


class BmaLayerNrlHandler:
    """
    todo
    """
    @classmethod
    def decompress(cls, compressed_data: bytes, stop_when_size: int) -> Tuple[bytes, int]:
        """todo. Stops when stop_when_size bytes have been decompressed.
        Second return is compressed original size.
        Returns 16 bit LE integer list. Input is compressed as pair24 (pairs of two 12 bit ints).
        """
        with open('/tmp/before.bin', 'wb') as f:
            f.write(compressed_data)
        data = BmaLayerNrlDecompressor(compressed_data, stop_when_size).decompress()
        with open('/tmp/before_un.bin', 'wb') as f:
            f.write(data[0])
        new_compressed = cls.compress(data[0])
        with open('/tmp/after.bin', 'wb') as f:
            f.write(new_compressed)
        after_data = BmaLayerNrlDecompressor(new_compressed, stop_when_size).decompress()
        with open('/tmp/after_un.bin', 'wb') as f:
            f.write(after_data[0])
        assert data[0] == after_data[0]
        return data

    @classmethod
    def compress(cls, uncompressed_data: bytes) -> bytes:
        """todo"""
        return BmaLayerNrlCompressor(uncompressed_data).compress()
