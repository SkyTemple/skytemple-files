from typing import Tuple

import bitstring
from bitstring import BitStream

from skytemple_files.common.util import read_bytes

# Operations are encoded in command bytes (CMD):
CMD_ZERO_OUT      = 0x80  # All values below
CMD_FILL_OUT      = 0x80  # All values equal/above until next
CMD_COPY_BYTES    = 0xC0  # All values equal/above


DEBUG = False


# noinspection PyAttributeOutsideInit
class BmaLayerNrlDecompressor:
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
            print(f"BMA Layer NRL decompression start....")

        # Handle data
        while self.cursor < self.max_size and self.bytes_written < self.stop_when_size:
            self._process()

        # TODO: For currently unknown reasons, some maps have more
        #       chunks/meta tiles then they should have. That's why we only check <
        if self.bytes_written < self.stop_when_size:
            raise ValueError(f"BMA Layer NRL Decompressor: End result length unexpected. "
                             f"Should be {self.stop_when_size}, is {self.bytes_written} "
                             f"Diff: {self.bytes_written - self.stop_when_size}")

        return self.decompressed_data[:self.bytes_written*8], self.cursor

    def _process(self):
        if DEBUG:
            cursor_before = self.cursor
            wr_before = self.bytes_written
        cmd = self._read()
        if DEBUG:
            print(f"cmd: {cmd:02x}")

        if cmd < CMD_ZERO_OUT:
            # cmd encodes how many 2x12 pairs to write
            if DEBUG:
                print(f"READ 0 - WRITE {3*(cmd+1)}")
            for i in range(-1, cmd):
                self._write(0)
        elif CMD_FILL_OUT <= cmd < CMD_COPY_BYTES:
            # cmd - CMD_FILL_OUT. Copy the next three bytes
            param = self._read(3)
            if DEBUG:
                print(f"READ 3 - WRITE {cmd - (CMD_FILL_OUT-1)}")
            for i in range(CMD_FILL_OUT-1, cmd):
                self._write(param)
        else:  # elif cmd > CMD_1_COPY_BYTES:
            # cmd - CMD_COPY_BYTES. Copy the next three bytes and repeat.
            if DEBUG:
                print(f"READ {3*(cmd - (CMD_COPY_BYTES-1))} - WRITE {3*(cmd - (CMD_COPY_BYTES-1))}")
            for i in range(CMD_COPY_BYTES-1, cmd):
                param = self._read(3)
                self._write(param)

        if DEBUG:
            print(f"-- cursor advancement: {self.cursor - cursor_before} -- write advancement: {self.bytes_written - wr_before}")

    def _read(self, bytes=1):
        """Read a single byte and increase cursor"""
        if self.cursor >= self.max_size:
            raise ValueError("BMA Layer NRL Decompressor: Reached EOF while reading compressed data.")
        oc = self.cursor
        self.cursor += bytes
        return read_bytes(self.compressed_data, oc, bytes).uint

    def _write(self, pattern_to_write):
        """Writes the pattern to the output as 2 12 bit integers"""
        # Pair-24 packing:
        # 1111 1111 2222 3333 4444 4444
        # 1- The lowest 8 bits of the first value
        # 2- The lowest 4 bits of the second value
        # 3- The highest 4 bits of the first value
        # 4- The highest 8 bits of the second value
        # pattern_to_write = pattern_to_write >> 0xf
        # 01 20 00 -> 00 10 02 -> 001 002
        # 11 20 01 -> 01 10 12 -> 011 012
        pattern_to_write = (0xff000 & pattern_to_write >> 4) + ((0x000f & pattern_to_write >> 8) << 20) + (0x00f & pattern_to_write >> 12) + (0x0ff0 & pattern_to_write << 4)
        #self.decompressed_data.append(bitstring.pack('uint:24', pattern_to_write))
        self.decompressed_data.overwrite(bitstring.pack('uint:24', pattern_to_write), self.bytes_written*8)
        self.bytes_written += 3
