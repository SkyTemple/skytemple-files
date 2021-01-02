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

from skytemple_files.common.util import read_uintle, read_bytes, iter_bytes
from skytemple_files.compression.generic_nrl import CMD_ZERO_OUT, CMD_COPY_BYTES, CMD_FILL_OUT


# How much pair24 we look ahead for at most
# 127 not possible because LA also use for fill and 2*63=126
NRL_LOOKAHEAD_ZERO_MAX_BYTES = 127
NRL_LOOKAHEAD_FILL_MAX_BYTES = 63
NRL_LOOKAHEAD_COPY_BYTES_MAX_BYTES = 63
# How often a pair24 needs to repeat for ZERO_OUT and FILL_OUT
NRL_MIN_SEQ_LEN = 3
DEBUG = False


# noinspection PyAttributeOutsideInit
class BmaLayerNrlCompressor:
    def __init__(self, uncompressed_data: bytes):
        if not isinstance(uncompressed_data, memoryview):
            uncompressed_data = memoryview(uncompressed_data)
        self.uncompressed_data = uncompressed_data
        self.length_input = len(uncompressed_data)
        self.reset()

    def reset(self):
        # At worst we just use COPY_BYTES operations with one pair24 + one cmd byte
        self.compressed_data = bytearray(self.length_input * 2 * 3)
        self.cursor = 0
        self.bytes_written = 0

    def compress(self) -> bytes:
        self.reset()
        if DEBUG:
            print("BMA Layer NRL compressor start...")

        while self.cursor < self.length_input:
            self._process()

        return self.compressed_data[:self.bytes_written]

    def _process(self):
        len_seq, sequence = self._look_ahead_two_int_sequence()
        if DEBUG:
            cursor_before = self.cursor
            wr_before = self.bytes_written
            print(f"Read a sequence of length {len_seq}")
        if len_seq > NRL_MIN_SEQ_LEN:
            # CMD_COPY_BYTES
            if DEBUG:
                print(f"CMD_COPY_BYTES")
            self.cursor += len_seq * 4
            cmd_byte = CMD_COPY_BYTES + (len_seq - 1)
            self._write_cmd(cmd_byte)
            for b in iter_bytes(sequence, 4):
                self._write_pair24(b)
        else:
            current_int_pair = self._read()
            repeats = self._look_ahead_repeats(current_int_pair)
            if DEBUG:
                print(f"Read {repeats} repeats of {current_int_pair:08x}")
            self.cursor += repeats * 4
            if read_uintle(current_int_pair, 0, 4) == 0:
                if DEBUG:
                    print(f"CMD_ZERO_OUT")
                # CMD_ZERO_OUT
                cmd_byte = repeats
                self._write_cmd(cmd_byte)
            else:
                # CMD_FILL_OUT
                if DEBUG:
                    print(f"CMD_FILL_OUT")
                # To big for one cmd, just make it into two.
                if repeats > NRL_LOOKAHEAD_FILL_MAX_BYTES:
                    repeats_byte1 = repeats - NRL_LOOKAHEAD_FILL_MAX_BYTES
                    cmd_byte1 = CMD_FILL_OUT + (repeats_byte1 - 1)
                    cmd_byte2 = CMD_FILL_OUT + (repeats - repeats_byte1)
                    self._write_cmd(cmd_byte1)
                    self._write_pair24(current_int_pair)
                    self._write_cmd(cmd_byte2)
                    self._write_pair24(current_int_pair)
                else:
                    cmd_byte = CMD_FILL_OUT + repeats
                    self._write_cmd(cmd_byte)
                    self._write_pair24(current_int_pair)

        if DEBUG:
            print(f"-- cursor advancement: {self.cursor - cursor_before} -- write advancement: {self.bytes_written - wr_before}")

    def _read(self) -> bytes:
        """Reads 4 bytes and increases cursor"""
        if self.cursor + 4 > self.length_input:
            raise ValueError("BMA Layer NRL Compressor: Reached EOF while reading data.")
        oc = self.cursor
        self.cursor += 4
        return read_bytes(self.uncompressed_data, oc, 4)

    def _write_cmd(self, data: int):
        """Writes CMD to the output as byte"""
        if DEBUG:
            print(f"W {data:02x}")
        self.compressed_data[self.bytes_written] = data
        self.bytes_written += 1

    def _write_pair24(self, data: bytes):
        """Writes 4 bytes of 2 16 bit LE integers in pair24 encoding."""
        assert len(data) == 4
        int1 = read_uintle(data, 0, 2)
        int2 = read_uintle(data, 2, 2)
        pair24 = ((int1 & 0xff) << 16) + ((int2 & 0xf) << 12) + (int1 & 0xf00) + ((int2 & 0xff0) >> 4)
        if DEBUG:
            print(f"W {int1:02x} and {int2:02x} as {pair24:06x}")
        self.compressed_data[self.bytes_written:self.bytes_written+3] = pair24.to_bytes(3, 'big')
        self.bytes_written += 3

    def _look_ahead_repeats(self, data: bytes):
        """Look how often the 4 byte pattern in the input data repeats, up to NRL_LOOKAHEAD_MAX_BYTES"""
        nc = self.cursor
        repeats = 0
        while read_bytes(self.uncompressed_data, nc, 4) == data and \
                repeats < NRL_LOOKAHEAD_ZERO_MAX_BYTES and \
                nc < self.length_input:
            repeats += 1
            nc += 4
        return repeats

    def _look_ahead_two_int_sequence(self):
        seq = bytearray(NRL_LOOKAHEAD_COPY_BYTES_MAX_BYTES * 4)
        seq_len = 0
        # If the repeat counter reaches NRL_MIN_SEQ_LEN, the sequence ends NRL_MIN_SEQ_LEN entries before that
        repeat_counter = 0
        previous_ints_at_pos = 0x1000000  # Impossible "null" value for now
        nc = self.cursor
        while True:
            ints_at_pos = read_bytes(self.uncompressed_data, nc, 4)
            if ints_at_pos == previous_ints_at_pos:
                repeat_counter += 1
            else:
                repeat_counter = 0
            previous_ints_at_pos = ints_at_pos

            seq[seq_len*4:(seq_len*4)+4] = ints_at_pos

            if repeat_counter > NRL_MIN_SEQ_LEN:
                seq_len -= NRL_MIN_SEQ_LEN
                break

            if seq_len + 1 >= NRL_LOOKAHEAD_COPY_BYTES_MAX_BYTES or nc >= self.length_input:
                break

            seq_len += 1
            nc += 4

        return seq_len, seq[:seq_len * 4]
