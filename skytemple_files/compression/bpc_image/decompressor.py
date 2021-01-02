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

from typing import Tuple

from skytemple_files.compression.bpc_image import *
from skytemple_files.common.util import *


DEBUG = False


class BpcImageDecompressor:
    def __init__(self, compressed_data: bytes, stop_when_size: int):
        self.compressed_data = compressed_data
        self.stop_when_size = stop_when_size
        # Input size
        self.max_size = len(self.compressed_data)
        self.reset()

    # noinspection PyAttributeOutsideInit
    def reset(self):
        self.decompressed_data = bytearray(self.stop_when_size)

        # todo
        self.has_leftover = False

        # todo
        # aka. leftover_val1, wordbuf, r2 in game
        self.leftover = 0

        # todo
        # aka. leftover_val2, hbyte, r7 in game
        self.pattern = 0

        # todo
        # aka. leftover_buf, cachedhbyte, r13_14h in game
        self.pattern_buffer = 0

        # todo
        self.cursor = 0

        # Used to keep track of when to end
        self.bytes_written = 0

    def decompress(self) -> Tuple[bytes, int]:
        """Returns the decompressed data and the size of the read, compressed data"""
        self.reset()
        if DEBUG:
            print("Start BPC image decompression...")
        initial_cursor = self.cursor
        while self.cursor < self.max_size and self.bytes_written < self.stop_when_size:
            self._process()

        if self.bytes_written != self.stop_when_size:
            raise ValueError(f"BPC Image Decompressor: End result length unexpected. "
                             f"Should be {self.stop_when_size}, is {self.bytes_written}. "
                             f"Diff: {self.bytes_written - self.stop_when_size}")

        return self.decompressed_data, self.cursor - initial_cursor

    def _process(self):
        """Process a single run"""
        if DEBUG:
            cursor_was_at = self.cursor
        cmd = self._read()
        if DEBUG:
            print(f"-----------------------")
            print(f"Reading CMD {cmd:02x}")
        number_of_bytes_to_output = self._read_nb_bytes_to_output(cmd)
        if DEBUG:
            print(f"Number of bytes to output: {number_of_bytes_to_output})")

        # Perform the special pattern operations based on the current CMD's value:
        if self._should_cycle_pattern(cmd):
            if DEBUG:
                print(f"Cycling.")
            self._cycle_pattern()
        if self._is_loading_pattern_from_next_byte(cmd):
            if DEBUG:
                print(f"Reading pattern.")
            self.pattern = self._read()

        # Check if we have leftover byte patterns to add:
        # This leftover exists because we are always working with words (= 2 bytes).
        # Keep in mind, that the number of bytes to write, is actually one lower than it should actually be. On odd
        # numbers there are supposed to be one word written more. Because we are always writing two words,
        # this is the case. However if there is an even amount of number_of_bytes_to_output, we are actually missing
        # one written byte because the ACTUAL amount of bytes to write is actually one higher.
        # So we need to "fill" the boundaries like this.
        # This is also why we decrease the number_of_bytes_to_output in the _read_nb_words_to_output
        # method: We are writing this byte right here!
        # Example:
        # number_of_bytes_to_output = 2
        #   -> bb [leftover = true]
        #   On next run:
        #   -> bb bx xx ...
        #
        # number_of_bytes_to_output = 3
        #   -> bb bb [leftover = false]
        #   On next run:
        #   -> bb bb xx ...
        if self.has_leftover:
            if DEBUG:
                print(f"Have leftover.")
            if self._is_pattern_op(cmd):
                final_pattern = self.leftover | (self.pattern << 8)
            else:
                final_pattern = self.leftover | (self._read() << 8)
            self._write(final_pattern)
            self.has_leftover = False

        if number_of_bytes_to_output >= 0:
            self._handle_main_operation(cmd, number_of_bytes_to_output)

        if DEBUG:
            print(f"== Cursor advanced: {self.cursor - cursor_was_at}")

    def _handle_main_operation(self, cmd, number_of_bytes_to_output):
        count_of_copy = 0
        if self._is_pattern_op(cmd):
            # We are writing the stored pattern!
            if DEBUG:
                print(f"Writing pattern.")
            # Convert current stored pattern in a 2 byte repeating pattern
            pattern = self.pattern | (self.pattern << 8)
            for count_of_copy in range(0, number_of_bytes_to_output, 2):  # step is 2 because we are wrt. words
                self._write(pattern)
        else:
            # We are copying whatever comes next!
            if DEBUG:
                print(f"Copying next.")
            for count_of_copy in range(0, number_of_bytes_to_output, 2):
                pattern = self._read(2)
                self._write(pattern)

        if number_of_bytes_to_output > 0:
            count_of_copy += 2  # python for+range does NOT increment at the end of loop!

        # If the amount copied was even, we setup the copy a leftover word on the next command byte
        if DEBUG:
            print(f"# {count_of_copy} copied. should: {number_of_bytes_to_output}")
        if count_of_copy == number_of_bytes_to_output:
            self.has_leftover = True
            if self._is_pattern_op(cmd):
                self.leftover = self.pattern
            else:
                self.leftover = self._read()
            if DEBUG:
                print(f"# Now have leftover: {self.leftover}")

    def _read_nb_bytes_to_output(self, cmd):
        """Determine the number of bytes to output. This is controlled by the CMD value."""
        if cmd in CMD__NEXT:
            # Number is encoded in next byte
            nb = self._read()
            if DEBUG:
                print(f"READ nb from next: {nb})")
        elif cmd == CMD_COPY__NEXT__LE_16:
            # Number is encoded in next two bytes
            nb = self._read(2)
            if DEBUG:
                print(f"READ nb from next 2: {nb})")
        else:
            # Number is in CMD. Depending on the case, we may need to subtract different things
            nb = cmd
            if cmd >= CMD_CYCLE_PATTERN_AND_CP:
                nb -= CMD_CYCLE_PATTERN_AND_CP
            elif cmd >= CMD_USE_LAST_PATTERN_AND_CP:
                nb -= CMD_USE_LAST_PATTERN_AND_CP
            elif cmd >= CMD_LOAD_BYTE_AS_PATTERN_AND_CP:
                nb -= CMD_LOAD_BYTE_AS_PATTERN_AND_CP

        # When we currently have a leftover word, we subtract one word to read
        if self.has_leftover:
            nb -= 1
        return nb

    def _should_cycle_pattern(self, cmd):
        return self._is_loading_pattern_from_next_byte(cmd) or (
            CMD_CYCLE_PATTERN_AND_CP <= cmd <= CMD_CYCLE_PATTERN_AND_CP__NEXT
        )

    def _is_loading_pattern_from_next_byte(self, cmd):
        return CMD_LOAD_BYTE_AS_PATTERN_AND_CP <= cmd < CMD_USE_LAST_PATTERN_AND_CP

    def _is_pattern_op(self, cmd):
        return cmd >= CMD_LOAD_BYTE_AS_PATTERN_AND_CP

    def _cycle_pattern(self):
        tmp = self.pattern_buffer
        self.pattern_buffer = self.pattern
        self.pattern = tmp

    def _write(self, pattern_to_write):
        """Writes the pattern to the output as LE"""
        self.decompressed_data[self.bytes_written:self.bytes_written+2] = pattern_to_write.to_bytes(2, 'little')
        self.bytes_written += 2
        pass

    def _read(self, bytes=1):
        """Read a single byte and increase cursor"""
        if self.cursor >= self.max_size:
            raise ValueError("BPC Image Decompressor: Reached EOF while reading compressed data.")
        if DEBUG:
            print("r", end="")
        oc = self.cursor
        self.cursor += bytes
        return read_uintle(self.compressed_data, oc, bytes)

