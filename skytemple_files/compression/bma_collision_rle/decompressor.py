from typing import Tuple

from skytemple_files.common.util import *


DEBUG = False


# noinspection PyAttributeOutsideInit
class BmaCollisionRleDecompressor:
    def __init__(self, compressed_data: bytes, stop_when_size):
        self.compressed_data = compressed_data
        self.stop_when_size = stop_when_size
        self.max_size = len(compressed_data)
        self.reset()

    def reset(self):
        self.decompressed_data = bytearray(self.stop_when_size)
        self.cursor = 0
        self.bytes_written = 0
        pass

    def decompress(self) -> Tuple[bytes, int]:
        self.reset()
        if DEBUG:
            print(f"BMA Collision RLE decompression start....")

        # Handle data
        while self.cursor < self.max_size and self.bytes_written < self.stop_when_size:
            self._process()

        if self.bytes_written != self.stop_when_size:
            raise ValueError(f"BMA Collision RLE Decompressor: End result length unexpected. "
                             f"Should be {self.stop_when_size}, is {self.bytes_written} "
                             f"Diff: {self.bytes_written - self.stop_when_size}")

        return self.decompressed_data[:self.bytes_written], self.cursor

    def _process(self):
        cmd = self._read()
        byte_to_write = cmd >> 7
        times_to_write = cmd & 0x7F
        if DEBUG:
            print(f"byte_to_write: {byte_to_write}")
            print(f"times_to_write: {times_to_write+1}")

        for i in range(-1, times_to_write):
            self._write(byte_to_write)

    def _read(self):
        """Read a single byte and increase cursor"""
        if self.cursor >= self.max_size:
            raise ValueError("BMA Collision RLE Decompressor: Reached EOF while reading compressed data.")
        oc = self.cursor
        self.cursor += 1
        return read_uintle(self.compressed_data, oc)

    def _write(self, pattern_to_write):
        """Writes a byte"""
        self.decompressed_data[self.bytes_written:self.bytes_written+1] = pattern_to_write.to_bytes(1, 'big')
        self.bytes_written += 1
