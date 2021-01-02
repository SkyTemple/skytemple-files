#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.

from skytemple_files.common.util import *
from skytemple_files.compression.bpc_tilemap import *

DEBUG = False


# noinspection PyAttributeOutsideInit
class BpcTilemapDecompressor:
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

    def decompress(self) -> bytes:
        self.reset()
        if DEBUG:
            print(f"BPC tilemap decompression start....")

        # Handle high bytes
        while self.cursor < self.max_size and self.bytes_written < self.stop_when_size:
            self._process_phase1()

        if DEBUG:
            print(f"End Phase 1. Begin Phase 2")
            print(f"Cursor begin phase 2: {self.cursor}")

        if self.bytes_written != self.stop_when_size:
            raise ValueError(f"BPC Tilemap Decompressor: Phase1: End result length unexpected. "
                             f"Should be {self.stop_when_size}, is {self.bytes_written} "
                             f"Diff: {self.bytes_written - self.stop_when_size}")

        self.bytes_written = 0

        # Handle low bytes
        while self.cursor < self.max_size and self.bytes_written < self.stop_when_size:
            self._process_phase2()

        if self.bytes_written != self.stop_when_size:
            raise ValueError(f"BPC Tilemap Decompressor: Phase2: End result length unexpected. "
                             f"Should be {self.stop_when_size}, is {self.bytes_written} "
                             f"Diff: {self.bytes_written - self.stop_when_size}")

        return self.decompressed_data

    def _process_phase1(self):
        if DEBUG:
            cursor_before = self.cursor
            wr_before = self.bytes_written
        cmd = self._read()
        if DEBUG:
            print(f"cmd: {cmd:02x}")

        if cmd < CMD_1_ZERO_OUT:
            # cmd encodes how many 0 words to write
            if DEBUG:
                print(f"READ 0 - WRITE {cmd+1}")
            for i in range(-1, cmd):
                self._write(0)
        elif CMD_1_FILL_OUT <= cmd < CMD_1_COPY_BYTES:
            # cmd - CMD_1_FILL_OUT is the nb of words to write with the next byte as high byte
            param = self._read() << 8
            if DEBUG:
                print(f"READ 1 - WRITE {cmd - (CMD_1_FILL_OUT-1)}")
            for i in range(CMD_1_FILL_OUT-1, cmd):
                self._write(param)
        else:  # elif cmd > CMD_1_COPY_BYTES:
            # cmd - CMD_1_COPY_BYTES is the nb of words to write with the sequence of bytes as high byte
            if DEBUG:
                print(f"READ {cmd - (CMD_1_COPY_BYTES-1)} - WRITE {cmd - (CMD_1_COPY_BYTES-1)}")
            for i in range(CMD_1_COPY_BYTES-1, cmd):
                param = self._read() << 8
                self._write(param)

        if DEBUG:
            print(f"-- cursor advancement: {self.cursor - cursor_before} -- write advancement: {self.bytes_written - wr_before}")

    def _process_phase2(self):
        cmd = self._read()
        if DEBUG:
            print(f"cmd: {cmd:02x}")

        if cmd < CMD_2_SEEK_OFFSET:
            # We skip over the nb of words indicated by the cmd
            if DEBUG:
                print(f"READ 0 - WRITE {cmd+1}")
            self.bytes_written += (cmd + 1) * 2
            if self.bytes_written > self.stop_when_size:
                raise ValueError("BPC Tilemap Decompressor: Reached EOF while writing decompressed data.")
        elif CMD_2_SEEK_OFFSET <= cmd < CMD_2_COPY_LOW:
            # cmd - CMD_2_SEEK_OFFSET is the nb of words to write with the next byte as low byte
            cmd_value = self._read()
            if DEBUG:
                print(f"READ 1 - WRITE {cmd - (CMD_2_SEEK_OFFSET-1)}")
            for i in range(CMD_2_SEEK_OFFSET-1, cmd):
                self._write(read_uintle(self.decompressed_data, self.bytes_written, 2) | cmd_value)
        else:  # elif cmd > CMD_2_COPY_LOW:
            # cmd - CMD_2_COPY_LOW is the nb of words to write with the sequence of bytes as low byte
            if DEBUG:
                print(f"READ {cmd - (CMD_2_COPY_LOW-1)} - WRITE {cmd - (CMD_2_COPY_LOW-1)}")
            for i in range(CMD_2_COPY_LOW-1, cmd):
                value_at_pos = read_uintle(self.decompressed_data, self.bytes_written, 2)
                value_at_pos |= self._read()
                self._write(value_at_pos)

    def _read(self, bytes=1):
        """Read a single byte and increase cursor"""
        if self.cursor >= self.max_size:
            raise ValueError("BPC Tilemap Decompressor: Reached EOF while reading compressed data.")
        oc = self.cursor
        self.cursor += bytes
        return read_uintle(self.compressed_data, oc, bytes)

    def _write(self, pattern_to_write):
        """Writes the pattern to the output as LE"""
        self.decompressed_data[self.bytes_written:self.bytes_written+2] = pattern_to_write.to_bytes(2, 'little')
        self.bytes_written += 2
        pass
