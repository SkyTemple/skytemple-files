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

from enum import Enum

from skytemple_files.common.util import *
from skytemple_files.compression.bpc_image import *

DEBUG = False

# How much space is in the CMD byte to store the number of repetitions
BPC_IMGC_REPEAT_MAX_CMD = 31 - 1  # -1 because of the __NEXT reserved special case
# Same for the CMD_LOAD_BYTE_AS_PATTERN_AND_CP case (C0-80)=64(dec.)
BPC_IMGC_REPEAT_MAX_CMD_LOAD_AS_PATTERN = 63 - 1
# How much space for the __NEXT case there is (storing it in one separate byte)
BPC_IMGC_REPEAT_MAX_NEXT = 255

# Copy pattern limits
BPC_IMGC_COPY_MAX_CMD = 127 - 2  # -2 because of the __NEXT reserved special cases
# How much space for the __NEXT case there is (storing it in one separate byte)
BPC_IMGC_COPY_MAX_NEXT = 255
# How much space for the CMD_COPY__NEXT__LE_16 case there is (storing as 16 bit after cmd byte)
BPC_IMGC_COPY_MAX_NEXT_16B = 0xffff

# Minimum repeat count for using the pattern ops.
BPC_MIN_REPEAT_COUNT = 3


class WherePattern(Enum):
    WRITE_AS_BYTE = 0
    IS_CURRENT_PATTERN = 1
    IS_PREVIOUS_PATTERN_CYCLE = 2


class BpcImageCompressorOperation:
    def __init__(self, byte=None, pattern_op=False, where_pattern=None, repeats=0):
        # Byte for repeat case with WherePattern.WRITE_AS_BYTE and sequence for COPY. None otherwise
        self.byte_or_sequence = byte
        self.pattern_op = pattern_op
        self.where_pattern = where_pattern  # only relevant for pattern_op = True
        self.repeats = repeats

    def __str__(self):
        if self.pattern_op:
            return f"PATTERN: Repeat {self.repeats} - Where?: {self.where_pattern} - {self.byte_or_sequence}"
        return f"COPY:    Length {self.repeats+1} - {self.byte_or_sequence}"


# noinspection PyAttributeOutsideInit
class BpcImageCompressor:
    def __init__(self, uncompressed_data: bytes):
        if not isinstance(uncompressed_data, memoryview):
            uncompressed_data = memoryview(uncompressed_data)
        self.uncompressed_data = uncompressed_data
        self.length_input = len(uncompressed_data)
        self.reset()

    def reset(self):
        # At worst we just use CMD_COPY__NEXT__LE_16 operations with one byte + two size cmd byte
        self.compressed_data = bytearray(self.length_input * 3)
        self.cursor = 0
        self.bytes_written = 0
        # The currently stored pattern. This has to be in-sync with the decompression!
        self.pattern = 0
        # The previously stored pattern. Also has to be in-sync!
        self.pattern_buffer = 0

    def compress(self) -> bytes:
        self.reset()
        if DEBUG:
            print("BPC Image Compressor start...")

        while self.cursor < self.length_input:
            self._process()

        return self.compressed_data[:self.bytes_written]

    def _process(self):
        """
        Process a single byte. This reads first and builds an operation,
        and then calls _run_operation to run the actual operation.
        """
        if DEBUG:
            print("----------------------")
            print(f"@0x{self.bytes_written:08x} [in input @0x{self.cursor:08x}]")
            print(f"Pattern buffer before: {self.pattern:02x} and {self.pattern_buffer:02x}")
        op = BpcImageCompressorOperation()

        # Check if byte repeats
        repeat_pattern, repeat_count = self._look_ahead_repeats()
        if repeat_count >= BPC_MIN_REPEAT_COUNT:
            op.repeats = repeat_count
            # Don't forget to also advance the read cursor! The lookahead functions don't do that
            self.cursor += repeat_count + 1
            op.pattern_op = True
            if repeat_pattern == self.pattern:
                # Check if byte is current pattern
                op.where_pattern = WherePattern.IS_CURRENT_PATTERN
            elif repeat_pattern == self.pattern_buffer:
                # ...or the previous stored pattern...
                op.where_pattern = WherePattern.IS_PREVIOUS_PATTERN_CYCLE
            else:
                # ...or something new.
                op.where_pattern = WherePattern.WRITE_AS_BYTE
                op.byte_or_sequence = repeat_pattern
        else:
            # If not: COPY_BYTES
            len_seq, sequence = self._look_ahead_byte_sequence()
            op.repeats = len_seq - 1
            # Don't forget to also advance the read cursor! The lookahead functions don't do that
            self.cursor += len_seq
            op.byte_or_sequence = sequence

        if DEBUG:
            print(f"Operation: {op}")

        # Run the actual operation
        self._run_operation(op)

        if DEBUG:
            print(f"Pattern buffer after: {self.pattern:02x} and {self.pattern_buffer:02x}")

    def _run_operation(self, op: BpcImageCompressorOperation):
        """Actually write the operation"""
        if op.pattern_op:
            return self._run_pattern_operation(op)
        # else:
        self._run_copy_operation(op)

    def _run_pattern_operation(self, op: BpcImageCompressorOperation):
        """Write a pattern operation"""
        if op.where_pattern == WherePattern.IS_CURRENT_PATTERN:
            cmd = CMD_USE_LAST_PATTERN_AND_CP
            # Nothing to change for pattern buffers
        elif op.where_pattern == WherePattern.IS_PREVIOUS_PATTERN_CYCLE:
            cmd = CMD_CYCLE_PATTERN_AND_CP
            # The decompressor will now swap the pattern buffers
            old_buf = self.pattern_buffer
            self.pattern_buffer = self.pattern
            self.pattern = old_buf
        else:
            cmd = CMD_LOAD_BYTE_AS_PATTERN_AND_CP
            # This now means, that we will write the pattern into the next byte.
            # The decompressor will load this and change it's pattern buffers like so:
            self.pattern_buffer = self.pattern
            self.pattern = op.byte_or_sequence

        # Determine the length
        if op.repeats <= BPC_IMGC_REPEAT_MAX_CMD or (op.repeats <= BPC_IMGC_REPEAT_MAX_CMD_LOAD_AS_PATTERN
                                                     and op.where_pattern == WherePattern.WRITE_AS_BYTE):
            # Fits in CMD
            cmd += op.repeats
            self._write(cmd)
        else:
            # Store in next byte
            cmd = CMD_LOAD_BYTE_AS_PATTERN_AND_CP__NEXT
            if op.where_pattern == WherePattern.IS_CURRENT_PATTERN:
                cmd = CMD_USE_LAST_PATTERN_AND_CP__NEXT
            elif op.where_pattern == WherePattern.IS_PREVIOUS_PATTERN_CYCLE:
                cmd = CMD_CYCLE_PATTERN_AND_CP__NEXT
            self._write(cmd)
            self._write(op.repeats)

        if op.where_pattern == WherePattern.WRITE_AS_BYTE:
            # Don't forget to write the pattern as a byte
            self._write(op.byte_or_sequence)

    def _run_copy_operation(self, op: BpcImageCompressorOperation):
        """Write an instruction to copy the following bytes and paste that sequence"""
        # Determine the length
        if op.repeats <= BPC_IMGC_COPY_MAX_CMD:
            # Fits in CMD
            self._write(op.repeats)
        elif op.repeats <= BPC_IMGC_COPY_MAX_NEXT:
            # Fits in one byte
            self._write(CMD_CP_FROM_POS__NEXT)
            self._write(op.repeats)
        else:
            # Fits in two bytes (LE!)
            self._write(CMD_COPY__NEXT__LE_16)
            self._write_16le(op.repeats)
        # Write the sequence
        # + 1 since we are counting repeats and always have 1
        len_of_seq = op.repeats + 1
        #assert len_of_seq == len(op.byte_or_sequence)
        self.compressed_data[self.bytes_written:self.bytes_written+len_of_seq] = op.byte_or_sequence
        # Don't forget to advance the cursors.
        self.bytes_written += len_of_seq

    def _write(self, data):
        """Writes to the output as byte"""
        if DEBUG:
            print(f"W {data:02x}")
        self.compressed_data[self.bytes_written] = data
        self.bytes_written += 1

    def _write_16le(self, data):
        """Writes to the output as 16 byte LE"""
        if DEBUG:
            print(f"W {data:04x}")
        self.compressed_data[self.bytes_written:self.bytes_written+1] = data.to_bytes(2, 'little')
        self.bytes_written += 2

    def _look_ahead_repeats(self):
        """Look how often the byte in the input data repeats, up to NRL_LOOKAHEAD_MAX_BYTES"""
        byte_at_pos = read_uintle(self.uncompressed_data, self.cursor)
        nc = self.cursor + 1
        repeats = 0
        while read_uintle(self.uncompressed_data, nc) == byte_at_pos and \
                repeats < BPC_IMGC_REPEAT_MAX_NEXT and \
                nc < self.length_input:
            repeats += 1
            nc += 1
        return byte_at_pos, repeats

    def _look_ahead_byte_sequence(self):
        seq = bytearray(BPC_IMGC_COPY_MAX_NEXT_16B)
        seq_len = 0
        # If the repeat counter reaches BPC_MIN_REPEAT_COUNT,
        # the sequence ends BPC_MIN_REPEAT_COUNT entries before that
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

            if repeat_counter > BPC_MIN_REPEAT_COUNT:
                seq_len -= BPC_MIN_REPEAT_COUNT
                break

            if seq_len+1 >= BPC_IMGC_COPY_MAX_NEXT_16B or nc >= self.length_input:
                break

            seq_len += 1
            nc += 1

        return seq_len, seq[:seq_len]
