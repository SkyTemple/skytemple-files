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

# directly based off https://github.com/PsyCommando/ppmdu/blob/master/src/ppmdu/fmts/px_compression.cpp
from collections import deque

from enum import Enum
from typing import Tuple

from skytemple_files.common.util import *
from skytemple_files.compression.px import PX_MIN_MATCH_SEQLEN, PX_LOOKBACK_BUFFER_SIZE, PX_MAX_MATCH_SEQLEN, \
    PX_NB_POSSIBLE_SEQUENCES_LEN, PX_NB_POSSIBLE_SEQ_LEN


DEBUG = False


class Operation(Enum):
    """
    All the possible operations that can be done to compress data!
    Entries 0 to 8 correspond to their respective ctrl flag indexes!
    """
    COPY_ASIS = -1
    COPY_NYBBLE_4TIMES = 0
    COPY_NYBBLE_4TIMES_EX_INCRALL_DECRNYBBLE0 = 1
    COPY_NYBBLE_4TIMES_EX_DECRNYBBLE1 = 2
    COPY_NYBBLE_4TIMES_EX_DECRNYBBLE2 = 3
    COPY_NYBBLE_4TIMES_EX_DECRNYBBLE3 = 4
    COPY_NYBBLE_4TIMES_EX_DECRALL_INCRNYBBLE0 = 5
    COPY_NYBBLE_4TIMES_EX_INCRNYBBLE1 = 6
    COPY_NYBBLE_4TIMES_EX_INCRNYBBLE2 = 7
    COPY_NYBBLE_4TIMES_EX_INCRNYBBLE3 = 8
    COPY_SEQUENCE = 9

    def __int__(self):
        return self.value


class PXCompLevel(Enum):
    # No compression     - All command bytes are 0xFF, and values are stored uncompressed. File size is increased!
    LEVEL_0 = 0
    # Low compression    - We handle 4 byte patterns, using only ctrl flag 0
    LEVEL_1 = 1
    # Medium compression - We handle 4 byte patterns, using all control flags
    LEVEL_2 = 2
    # Full compression   - We handle everything above, along with repeating sequences of bytes already decompressed.
    LEVEL_3 = 3


class CompOp:
    """Stores an operation to insert into the output buffer."""
    def __init__(self, type=Operation.COPY_ASIS, highnybble=0, lownybble=0, nextbytevalue=0):
        # The operation to do
        self.type = type
        # u8: The value of the compressed high nybble if applicable
        self.highnybble = highnybble
        # u8: The value of the compressed low nybble
        self.lownybble = lownybble
        # u8: Value of the compressed next byte if applicable
        self.nextbytevalue = nextbytevalue


class MatchingSeq:
    def __init__(self, pos, length):
        self.pos = pos
        self.length = length


# noinspection PyAttributeOutsideInit
class PxCompressor:
    def __init__(self, uncompressed_data: bytes, compression_level=PXCompLevel.LEVEL_3, should_search_first=True):
        if not isinstance(uncompressed_data, memoryview):
            uncompressed_data = memoryview(uncompressed_data)
        self.uncompressed_data = uncompressed_data
        self.compression_level = compression_level
        self.should_search_first = should_search_first
        self.reset()
        # Calculate the size of the input
        self.input_size = len(self.uncompressed_data)

    def reset(self):
        self.control_flags = None
        self.compressed_data = None
        self.pending_operations = deque()
        self.high_nibble_lenghts_possible = []
        self.nb_compressed_byte_written = 0

        self.cursor = 0
        self.output_cursor = 0

    def compress(self) -> Tuple[bytes, bytes]:
        """Compresses the input data"""
        self.reset()

        if DEBUG:
            print("Starting PX comp.")

        # Verify if we overflow
        if self.input_size > 2147483647:
            raise ValueError(f"PX Compression: The input data is too long {self.input_size}. "
                             f"Max size: 2147483647 [max 32bit int]")

        # Allocate at least as much memory as the input + some extra in case of dummy compression!
        # Worst case, we got 1 more bytes per 8 bytes.
        # And if we're not divisible by 8, add an extra
        # yte for the last command byte !
        self.compressed_data = bytearray(self.input_size + self.input_size + (1 if self.input_size % 8 != 0 else 0))

        # Set by default those two possible matching sequence length, given we want 99% of the time to
        # have those 2 to cover the gap between the 2 bytes to 1 algorithm and the string search, and also get
        # to use the string search's capability to its maximum!
        self.high_nibble_lenghts_possible.append(0)
        self.high_nibble_lenghts_possible.append(0xF)

        # Do compression
        while self._handle_a_block():
            pass

        if DEBUG:
            print(f"Len of operations: {len(self.pending_operations)}")

        # Build control flag table, now that we determined all our string search lengths!
        self._build_ctrl_flags_list()

        # Execute all operations from our queue
        self._output_all_operations()

        # Validate compressed size
        if self.nb_compressed_byte_written > 65536:
            raise ValueError(f"PX Compression: Compressed size {self.nb_compressed_byte_written} overflows "
                             f"16 bits unsigned integer!")

        if DEBUG:
            print(f"Written {self.nb_compressed_byte_written}")

        return self.control_flags, self.compressed_data

    def _handle_a_block(self):
        """
        Handle a block of 8 bytes and up to be compressed.
        Return false, when has reached the end.
        """
        if self.cursor < self.input_size:
            # Determine what to do for as much bytes as possible
            for i in range(0, 8):
                if not self.cursor < self.input_size:
                    break
                self.pending_operations.append(self._determine_best_operation())
            return True
        return False

    def _determine_best_operation(self) -> CompOp:
        """
        Determine and run the best possible operation to compress the data at cursor.
        """
        if DEBUG:
            print(f"Determining best operation for byte at {self.cursor}")

        myoperation = CompOp()
        if self.should_search_first and \
                self.compression_level.value >= PXCompLevel.LEVEL_3.value and \
                self._can_use_a_matching_sequence(self.cursor, myoperation):
            amount_to_advance = myoperation.highnybble + PX_MIN_MATCH_SEQLEN
            if DEBUG:
                print(f"> RESULT WAS Copy Sequence. Advancing {amount_to_advance}")

        elif self.compression_level.value >= PXCompLevel.LEVEL_1.value and \
                self._can_compress_to_2_in_1_byte(self.cursor, myoperation):
            amount_to_advance = 2
            if DEBUG:
                print(f"> RESULT WAS simple compression. {amount_to_advance}")

        elif self.compression_level.value >= PXCompLevel.LEVEL_2.value and \
                self._can_compress_to_2_in_1_byte_with_manipulation(self.cursor, myoperation):
            amount_to_advance = 2
            if DEBUG:
                print(f"> RESULT WAS complex compression. {amount_to_advance}")

        elif not self.should_search_first and \
                self.compression_level.value >= PXCompLevel.LEVEL_3.value and \
                self._can_use_a_matching_sequence(self.cursor, myoperation):
            amount_to_advance = myoperation.highnybble + PX_MIN_MATCH_SEQLEN
            if DEBUG:
                print(f"> RESULT WAS Copy Sequence. Advancing {amount_to_advance}")

        else:  # Level 0
            # If all else fails, add the byte as-is
            b = read_uintle(self.uncompressed_data, self.cursor)
            myoperation.type = Operation.COPY_ASIS
            myoperation.highnybble = (b >> 4) & 0x0F
            myoperation.lownybble = b & 0x0F
            amount_to_advance = 1
            if DEBUG:
                print(f"> RESULT WAS as is. Advancing {amount_to_advance}")

        # Advance the iterator
        self.cursor += amount_to_advance

        return myoperation

    def _can_compress_to_2_in_1_byte(self, l_cursor, out_result: CompOp) -> bool:
        """Check whether the 2 bytes at l_cusor can be stored as a single byte."""
        both_bytes = 0
        for i in [1, 0]:
            if l_cursor < self.input_size:
                both_bytes |= read_uintle(self.uncompressed_data, l_cursor) << 8 * i
                l_cursor += 1
            else:
                return False
        out_result.lownybble = both_bytes & 0x0F
        for i in [3, 2, 1, 0]:
            # Compare every nybbles with the low nybble we got above.
            # The 4 must match for this to work !
            if (both_bytes >> (4 * i)) & 0x0F != out_result.lownybble:
                return False
        out_result.type = Operation.COPY_NYBBLE_4TIMES

        return True

    def _can_compress_to_2_in_1_byte_with_manipulation(self, l_cursor, out_result):
        """
        Check whether the 2 bytes at l_cursor can be stored as a single byte,
        only if we use special operations based on the ctrl flag index contained
        in the high nibble!
        """
        nibbles = [0, 0, 0, 0]
        # Read 4 nibbles from the input
        for i in [0, 2]:
            if l_cursor < self.input_size:
                b = read_uintle(self.uncompressed_data, l_cursor)
                nibbles[i] = (b >> 4) & 0x0F
                nibbles[i+1] = b & 0x0F
                l_cursor += 1
            else:
                return False

        # Count the nb of occurrences for each nibble
        nibbles_matches = []
        for i in range(0, len(nibbles)):
            nibbles_matches.append(nibbles.count(nibbles[i]))

        # We got at least 3 values that come back 3 times
        if nibbles_matches.count(3) == 3:
            nmin, nmax = min(nibbles), max(nibbles)
            # If the difference between the biggest and smallest nybble is one, we're good
            if nmax - nmin == 1:
                # Get the index of the smallest value
                indexsmallest = nibbles.index(nmin)
                indexlargest = nibbles.index(nmax)

                if nibbles_matches[indexsmallest] == 1:
                    # This case is for ctrl flag indexes 1 to 4. There are 2 cases here:
                    # A) The decompressor decrements a nybble not at index 0 once.
                    # B) The decompressor increments all of them once, and then decrements the one at index 0 !
                    # indexsmallest : is the index of the nybble that gets decremented.
                    out_result.type = Operation(indexsmallest + int(Operation.COPY_NYBBLE_4TIMES_EX_INCRALL_DECRNYBBLE0))
                    if indexsmallest == 0:
                        # Copy as-is, given the decompressor increment it then decrement this value
                        out_result.lownybble = nibbles[indexsmallest]
                    else:
                        # Add one since we subtract 1 during decompression
                        out_result.lownybble = nibbles[indexsmallest] + 1
                else:
                    # This case is for ctrl flag indexes 5 to 8. There are 2 cases here:
                    # A) The decompressor increments a nybble not at index 0 once.
                    # B) The decompressor decrements all of them once, and then increments the one at index 0 again!
                    # indexlargest : is the index of the nybble that gets incremented.
                    out_result.type = Operation(indexlargest + int(Operation.COPY_NYBBLE_4TIMES_EX_DECRALL_INCRNYBBLE0))
                    if indexlargest == 0:
                        # Since we decrement and then increment this one during decomp, use it as-is
                        out_result.lownybble = nibbles[indexlargest]
                    else:
                        # Subtract 1 since we increment during decompression
                        out_result.lownybble = nibbles[indexlargest] - 1
                return True
        return False

    def _can_use_a_matching_sequence(self, l_cursor, out_result):
        """
        Search through the lookback buffer for a string of bytes that matches the
        string beginning at l_cursor. It searches for at least 3 matching bytes
        at first, then, finds the longest matching sequence it can!
        """
        # Get offset of LookBack Buffer beginning
        current_offset = l_cursor
        lb_buffer_begin = current_offset - PX_LOOKBACK_BUFFER_SIZE if current_offset > PX_LOOKBACK_BUFFER_SIZE else 0

        # Setup our iterators for clarity's sake
        it_look_back_begin = lb_buffer_begin
        it_look_back_end = l_cursor
        it_seq_begin = l_cursor
        it_seq_end = self._adv_as_much_as_possible(l_cursor, self.input_size, PX_MAX_MATCH_SEQLEN)

        cur_seq_len = it_seq_end - it_seq_begin

        # Make sure out sequence is at least three bytes long
        if cur_seq_len < PX_MIN_MATCH_SEQLEN:
            return False

        result = self._find_longest_matching_sequence(
            it_look_back_begin, it_look_back_end, it_seq_begin, it_seq_end, cur_seq_len
        )

        if result.length >= PX_MIN_MATCH_SEQLEN:
            # Subtract 3 given that's how they're stored!
            valid_high_nibble = result.length - PX_MIN_MATCH_SEQLEN
            # Check the length in the table!
            if not self._check_sequence_high_nibble_valid_or_add(result.length - PX_MIN_MATCH_SEQLEN):
                # If the size is not one of the allowed ones, and we can't add it to the list,
                # shorten our found sequence to the longest length in the list of allowed lengths!
                for i in range(0, len(self.high_nibble_lenghts_possible)):
                    # Since the list is sorted, just break once we can't find anything smaller than the value we found!
                    if self.high_nibble_lenghts_possible[i] + PX_MIN_MATCH_SEQLEN < result.length:
                        valid_high_nibble = self.high_nibble_lenghts_possible[i]
                assert valid_high_nibble <= (PX_MAX_MATCH_SEQLEN - PX_MIN_MATCH_SEQLEN)

            signed_offset = - (l_cursor - result.pos)
            out_result.lownybble = (signed_offset >> 8) & 0x0F
            out_result.nextbytevalue = signed_offset & 0xFF
            out_result.highnybble = valid_high_nibble
            out_result.type = Operation.COPY_SEQUENCE

            return True

        return False

    def _find_longest_matching_sequence(self, searchbeg, searchend, tofindbeg, tofindend, sequencelenght) -> MatchingSeq:
        """
         Find the longest matching sequence of at least PX_MIN_MATCH_SEQLEN bytes
         and at most PX_MAX_MATCH_SEQLEN bytes.
         - searchbeg      : Beginning of the zone to look for the sequence.
         - searchend      : End of the zone to look for the sequence.
         - tofindbeg      : Beginning of the sequence to find.
         - tofindend      : End of the sequence to find.
         - sequencelenght : Length of the sequence to look for in bytes.
        """
        longestmatch = MatchingSeq(searchend, 0)
        seq_to_find_short_end = self._adv_as_much_as_possible(tofindbeg, tofindend, PX_MIN_MATCH_SEQLEN)

        cur_search_pos = searchbeg
        while cur_search_pos < searchend:
            fnd_tpl = self.uncompressed_data.tobytes().find(
                read_bytes(self.uncompressed_data, tofindbeg, seq_to_find_short_end - tofindbeg),
                cur_search_pos, searchend
            )
            if fnd_tpl == -1:
                cur_search_pos = searchend
            else:
                cur_search_pos = fnd_tpl

            if cur_search_pos != searchend:
                nbmatches = self._count_equal_consecutive_elem(
                    cur_search_pos, self._adv_as_much_as_possible(cur_search_pos, searchend, PX_MAX_MATCH_SEQLEN),
                    tofindbeg, tofindend
                )
                if longestmatch.length < nbmatches:
                    longestmatch.length = nbmatches
                    longestmatch.pos = cur_search_pos

                if nbmatches == PX_MAX_MATCH_SEQLEN:
                    return longestmatch

                cur_search_pos += 1

        return longestmatch

    def _check_sequence_high_nibble_valid_or_add(self, hnybbleorlen):
        """
        Because the length is stored as the high nybble in the compressed output, and
        that the high nybble also contains the ctrl flags, we need to make sure the
        lengths of sequences to use do not overlap over values of the control flags !
        So we'll build a list of length to reserve as we go!
        -> If the value is in our reserved list, and we have PX_NB_POSSIBLE_SEQ_LEN
            of them already, return true.
        -> If the value isn't in our reserved list, and we still have space left,
            add it and return true!
        -> If the value isn't in our reserved list, and all PX_NB_POSSIBLE_SEQ_LEN
            slots are taken, return false!

        NOTE:
            DO NOT pass the exact sequence length. The value stored in the
            high nybble is essentially : SequenceLen - PX_MIN_MATCH_SEQLEN
        """
        if hnybbleorlen not in self.high_nibble_lenghts_possible:
            # We didn't find the length.. Check if we can add it.
            if len(self.high_nibble_lenghts_possible) < PX_NB_POSSIBLE_SEQUENCES_LEN:
                self.high_nibble_lenghts_possible.append(hnybbleorlen)
                self.high_nibble_lenghts_possible = sorted(self.high_nibble_lenghts_possible)
                return True
            return False

        # We found it in the list!
        return True

    def _output_an_operation(self, operation: CompOp):
        """
        Outputs into the output buffer at position self.output_cursor the compressed
        form of the operation passed in parameter!
        """
        insert_pos = self.output_cursor
        if operation.type == Operation.COPY_ASIS:
            self.compressed_data[insert_pos] = (operation.highnybble << 4 & 0xF0) | operation.lownybble
            self.output_cursor += 1
            self.nb_compressed_byte_written += 1
            if DEBUG:
                print(f"Writing as is {self.compressed_data[insert_pos]:>08b}")
        elif operation.type == Operation.COPY_SEQUENCE:
            self.compressed_data[insert_pos] = (operation.highnybble << 4 & 0xF0) | operation.lownybble
            self.output_cursor += 1
            self.nb_compressed_byte_written += 1
            self.compressed_data[insert_pos+1] = operation.nextbytevalue
            self.output_cursor += 1
            self.nb_compressed_byte_written += 1
            if DEBUG:
                print(f"Writing copy seq {self.compressed_data[insert_pos]:>08b} + {self.compressed_data[insert_pos+1]:>08b}")
        else:
            flag = self.control_flags[operation.type.value]
            self.compressed_data[insert_pos] = (flag << 4) | operation.lownybble
            self.output_cursor += 1
            self.nb_compressed_byte_written += 1
            if DEBUG:
                print(f"Writing compression {self.compressed_data[insert_pos]:>08b}")

    def _build_ctrl_flags_list(self):
        """
        This determines all the control flags values, based on what matching
        sequence lengths have been reserved so far !
        """
        # Make sure we got PX_NB_POSSIBLE_SEQ_LEN values taken up by the length nybbles
        if len(self.high_nibble_lenghts_possible) != PX_NB_POSSIBLE_SEQUENCES_LEN:
            # If we don't have PX_NB_POSSIBLE_SEQ_LEN nybbles reserved for the lengths,
            # just come up with some then.. Its a possible eventuality..
            for nybbleval in range(0, 0xF):
                if len(self.high_nibble_lenghts_possible) >= PX_NB_POSSIBLE_SEQ_LEN:
                    break
                if nybbleval not in self.high_nibble_lenghts_possible and len(self.high_nibble_lenghts_possible) < PX_NB_POSSIBLE_SEQUENCES_LEN:
                    self.high_nibble_lenghts_possible.append(nybbleval)

        # Build our flag list, based on the allowed length values!
        # We only have 16 possible values to contain lengths and control flags..

        self.control_flags = bytearray(9)
        # Pos to insert a ctrl flag at
        itctrlflaginsert = 0
        for flagval in range(0, 0xF):
            if flagval not in self.high_nibble_lenghts_possible:
                if itctrlflaginsert < len(self.control_flags):
                    # Flag value is not taken ! So go ahead and make it a control flag value !
                    self.control_flags[itctrlflaginsert] = flagval
                    itctrlflaginsert += 1

    def _output_all_operations(self):
        """
        This does the neccessary to execute all operations we put in our operation
        queue. It also calculate the proper high nybble value for operation
        using a control flag index !
        """
        # Output all our operations!
        while len(self.pending_operations) > 0:
            # Make a command byte using the 8 first operations in the operation queue !
            command_byte = 0
            for i in range(0, 8):
                if i >= len(self.pending_operations):
                    break
                if self.pending_operations[i].type == Operation.COPY_ASIS:
                    # Set the bit to 1 only when we copy the byte as-is !
                    command_byte |= 1 << (7 - i)

            if DEBUG:
                print(f"Writing command byte {command_byte:>08b}")

            # Output command byte
            self.compressed_data[self.output_cursor] = command_byte
            self.output_cursor += 1
            self.nb_compressed_byte_written += 1

            # Run 8 operations before another command byte !
            for i in range(0, 8):
                if len(self.pending_operations) <= 0:
                    break
                self._output_an_operation(self.pending_operations.popleft())

        # After we're done, shrink down the BitStream, and remove all the extra space
        self.compressed_data = self.compressed_data[:self.output_cursor]

    @staticmethod
    def _adv_as_much_as_possible(iter, itend, displacement):
        """
        Advance an counter until either the given number of increments are made,
        or the end is reached!
        """
        if iter + displacement > itend:
            return itend
        return iter + displacement

    def _count_equal_consecutive_elem(self, first_1, last_1, first_2, last_2):
        """
        Count the amount of similar consecutive values between two sequences.
        It stops counting once it stumbles on a differing value.
        :return:
        """
        count = 0
        while first_1 != last_1 and first_2 != last_2 and read_uintle(self.uncompressed_data, first_1) == read_uintle(self.uncompressed_data, first_2):
            count += 1
            first_1 += 1
            first_2 += 1
        return count
