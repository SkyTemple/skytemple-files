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

from skytemple_files.common.util import read_uintle
from skytemple_files.compression.generic_nrl import CMD_ZERO_OUT, CMD_COPY_BYTES, CMD_FILL_OUT


# How much bytes we look ahead for at most
NRL_LOOKAHEAD_ZERO_MAX_BYTES = 127
NRL_LOOKAHEAD_FILL_MAX_BYTES = 63
NRL_LOOKAHEAD_COPY_BYTES_MAX_BYTES = 63
# How often a byte needs to repeat for ZERO_OUT and FILL_OUT
NRL_MIN_SEQ_LEN = 3
DEBUG = False


# noinspection PyAttributeOutsideInit
class GenericNrlCompressor:
    def __init__(self, uncompressed_data: bytes):
        if not isinstance(uncompressed_data, memoryview):
            uncompressed_data = memoryview(uncompressed_data)
        self.uncompressed_data = uncompressed_data
        self.length_input = len(uncompressed_data)
        self.reset()

    def reset(self):
        # At worst we just use COPY_BYTES operations with one byte + one cmd byte
        self.compressed_data = bytearray(self.length_input * 2)
        self.cursor = 0
        self.bytes_written = 0

    def compress(self) -> bytes:
        self.reset()
        if DEBUG:
            print("Generic NRL compressor start...")

        while self.cursor < self.length_input:
            self._process()

        return self.compressed_data[:self.bytes_written]

    def _process(self, cursor_process_multiplier=1):
        """
        Process a single byte. The cursor_process_multiplier is used, when
        bytes in between should be skipped, like for the BPC Tilemap Compressor
        (because it processes high bytes first, then low bytes)
        """
        len_seq, sequence = self._look_ahead_byte_sequence(cursor_process_multiplier)
        if DEBUG:
            cursor_before = self.cursor
            wr_before = self.bytes_written
            print(f"Read a sequence of length {len_seq}")
        if len_seq > NRL_MIN_SEQ_LEN:
            # CMD_COPY_BYTES
            if DEBUG:
                print(f"CMD_COPY_BYTES")
            self.cursor += len_seq * cursor_process_multiplier
            cmd_byte = CMD_COPY_BYTES + (len_seq - 1)
            self._write(cmd_byte)
            for b in sequence:
                self._write(b)
        else:
            current_byte = self._read(cursor_process_multiplier)
            repeats = self._look_ahead_repeats(current_byte, cursor_process_multiplier)
            if DEBUG:
                print(f"Read {repeats} repeats of {current_byte}")
            self.cursor += repeats * cursor_process_multiplier
            if current_byte == 0:
                if DEBUG:
                    print(f"CMD_ZERO_OUT")
                # CMD_ZERO_OUT
                assert repeats < CMD_ZERO_OUT
                cmd_byte = repeats
                self._write(cmd_byte)
            else:
                # CMD_FILL_OUT
                if DEBUG:
                    print(f"CMD_FILL_OUT")
                # To big for one cmd, just make it into two.
                if repeats > NRL_LOOKAHEAD_FILL_MAX_BYTES:
                    repeats_byte1 = repeats - NRL_LOOKAHEAD_FILL_MAX_BYTES
                    # -1 because each cmd byte in itself codes 1 output
                    # 2 + 63 + 63 = 127 + 1 = 128
                    cmd_byte1 = CMD_FILL_OUT + (repeats_byte1 - 1)
                    cmd_byte2 = CMD_FILL_OUT + (repeats - repeats_byte1)
                    self._write(cmd_byte1)
                    self._write(current_byte)
                    self._write(cmd_byte2)
                    self._write(current_byte)
                else:
                    cmd_byte = CMD_FILL_OUT + repeats
                    self._write(cmd_byte)
                    self._write(current_byte)

        if DEBUG:
            print(f"-- cursor advancement: {self.cursor - cursor_before} -- write advancement: {self.bytes_written - wr_before}")

    def _read(self, cursor_process_multiplier):
        """Read a single byte and increase cursor"""
        if self.cursor >= self.length_input:
            raise ValueError("Generic NRL Compressor: Reached EOF while reading data.")
        oc = self.cursor
        self.cursor += cursor_process_multiplier
        return read_uintle(self.uncompressed_data, oc)

    def _write(self, data):
        """Writes to the output as byte"""
        if DEBUG:
            print(f"W {data:02x}")
        self.compressed_data[self.bytes_written] = data
        self.bytes_written += 1

    def _look_ahead_repeats(self, data, cursor_process_multiplier):
        """Look how often the byte in the input data repeats, up to NRL_LOOKAHEAD_MAX_BYTES"""
        nc = self.cursor
        repeats = 0
        while read_uintle(self.uncompressed_data, nc) == data and \
                repeats < NRL_LOOKAHEAD_ZERO_MAX_BYTES and \
                nc < self.length_input:
            repeats += 1
            nc += cursor_process_multiplier
        return repeats

    def _look_ahead_byte_sequence(self, cursor_process_multiplier):
        """Look ahead for the next byte sequence until the first repeating pattern starts"""
        seq = bytearray(NRL_LOOKAHEAD_COPY_BYTES_MAX_BYTES)
        seq_len = 0
        # If the repeat counter reaches NRL_MIN_SEQ_LEN, the sequence ends NRL_MIN_SEQ_LEN entries before that
        repeat_counter = 0
        previous_byt_at_pos = 0x100  # Impossible "null" value for now
        nc = self.cursor
        while True:
            byt_at_pos = read_uintle(self.uncompressed_data, nc)
            if byt_at_pos == previous_byt_at_pos:
                repeat_counter += 1
            else:
                repeat_counter = 0
            previous_byt_at_pos = byt_at_pos

            seq[seq_len] = byt_at_pos

            if repeat_counter > NRL_MIN_SEQ_LEN:
                seq_len -= NRL_MIN_SEQ_LEN
                break

            if seq_len+1 >= NRL_LOOKAHEAD_COPY_BYTES_MAX_BYTES or nc >= self.length_input:
                break

            seq_len += 1
            nc += cursor_process_multiplier

        return seq_len, seq[:seq_len]
