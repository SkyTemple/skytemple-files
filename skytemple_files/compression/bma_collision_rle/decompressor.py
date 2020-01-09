from typing import Tuple

import bitstring
from bitstring import BitStream

from skytemple_files.common.util import read_bytes


DEBUG = False


# noinspection PyAttributeOutsideInit
class BmaCollisionRleDecompressor:
    def __init__(self, compressed_data: BitStream, stop_when_size):
        self.compressed_data = compressed_data
        self.stop_when_size = stop_when_size
        self.max_size = int(len(compressed_data) / 8)
        self.reset()

    def reset(self):
        # For currently unknown reason, some BMAs have extra trailing tiles...
        # so we buffer x2
        self.decompressed_data = BitStream(self.stop_when_size*8*2)
        #self.decompressed_data = BitStream()
        self.cursor = 0
        self.bytes_written = 0
        pass

    def decompress(self) -> Tuple[BitStream, int]:
        self.reset()
        if DEBUG:
            print(f"BMA Collision RLE decompression start....")

        # Handle data
        while self.cursor < self.max_size and self.bytes_written < self.stop_when_size:
            self._process()

        # TODO: For currently unknown reasons, some maps have more
        #       chunks/meta tiles then they should have. That's why we only check <
        if self.bytes_written < self.stop_when_size:
            raise ValueError(f"BMA Collision RLE Decompressor: End result length unexpected. "
                             f"Should be {self.stop_when_size}, is {self.bytes_written} "
                             f"Diff: {self.bytes_written - self.stop_when_size}")

        return self.decompressed_data[:self.bytes_written*8], self.cursor

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
        return read_bytes(self.compressed_data, oc).uint

    def _write(self, pattern_to_write):
        """Writes a byte"""
        # Pair-24 packing:
        #self.decompressed_data.append(bitstring.pack('uint:8', pattern_to_write))
        self.decompressed_data.overwrite(bitstring.pack('uint:8', pattern_to_write), self.bytes_written*8)
        self.bytes_written += 1
