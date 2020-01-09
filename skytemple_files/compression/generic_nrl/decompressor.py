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
class GenericNrlDecompressor:
    def __init__(self, compressed_data: BitStream, stop_when_size):
        self.compressed_data = compressed_data
        self.stop_when_size = stop_when_size
        self.max_size = int(len(compressed_data) / 8)
        self.reset()

    def reset(self):
        self.decompressed_data = BitStream(self.stop_when_size*8)
        #self.decompressed_data = BitStream()
        self.cursor = 0
        self.bytes_written = 0
        pass

    def decompress(self) -> Tuple[BitStream, int]:
        self.reset()
        if DEBUG:
            print(f"Generic NRL decompression start....")

        # Handle data
        while self.cursor < self.max_size and self.bytes_written < self.stop_when_size:
            self._process()

        if self.bytes_written != self.stop_when_size:
            raise ValueError(f"Generic NRL Decompressor: End result length unexpected. "
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
            # cmd encodes how many bytes to write
            if DEBUG:
                print(f"READ 0 - WRITE {(cmd+1)}")
            for i in range(-1, cmd):
                self._write(0)
        elif CMD_FILL_OUT <= cmd < CMD_COPY_BYTES:
            # cmd - CMD_FILL_OUT. Copy the next three bytes
            param = self._read()
            if DEBUG:
                print(f"READ 1 - WRITE {cmd - (CMD_FILL_OUT-1)}")
            for i in range(CMD_FILL_OUT-1, cmd):
                self._write(param)
        else:  # elif cmd > CMD_1_COPY_BYTES:
            # cmd - CMD_COPY_BYTES. Copy the next byte and repeat.
            if DEBUG:
                print(f"READ {(cmd - (CMD_COPY_BYTES-1))} - WRITE {(cmd - (CMD_COPY_BYTES-1))}")
            for i in range(CMD_COPY_BYTES-1, cmd):
                param = self._read()
                self._write(param)

        if DEBUG:
            print(f"-- cursor advancement: {self.cursor - cursor_before} -- write advancement: {self.bytes_written - wr_before}")

    def _read(self):
        """Read a single byte and increase cursor"""
        if self.cursor >= self.max_size:
            raise ValueError("Generic NRL Decompressor: Reached EOF while reading compressed data.")
        oc = self.cursor
        self.cursor += 1
        return read_bytes(self.compressed_data, oc).uint

    def _write(self, pattern_to_write):
        """Writes the pattern to the output as byte"""
        #self.decompressed_data.append(bitstring.pack('uint:8', pattern_to_write))
        self.decompressed_data.overwrite(bitstring.pack('uint:8', pattern_to_write), self.bytes_written*8)
        self.bytes_written += 1
