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
from skytemple_files.compression.px import PX_MIN_MATCH_SEQLEN


DEBUG = False


def compute_four_nibbles_pattern(idx_ctrl_flags, low_nibble) -> bytes:
    # The index of the control flag defines modifies one or more nibbles to modify.
    if idx_ctrl_flags == 0:
        # In this case, all our 4 nibbles have the value of the "low_nibble" as their value
        # Since we're dealing with half bytes, shift one left by 4 and bitwise OR it with the other!
        byte1 = byte2 = low_nibble << 4 | low_nibble
    else:
        # Here we handle 2 special cases together
        nibble_base = low_nibble
        # At these indices exactly, the base value for all nibbles has to be changed:
        if idx_ctrl_flags == 1:
            nibble_base += 1
        elif idx_ctrl_flags == 5:
            nibble_base -= 1

        ns = [nibble_base, nibble_base, nibble_base, nibble_base]
        # In these cases, only specific nibbles have to be changed:
        if 1 <= idx_ctrl_flags <= 4:
            ns[idx_ctrl_flags - 1] -= 1
        else:
            ns[idx_ctrl_flags - 5] += 1

        byte1 = ns[0] << 4 | ns[1]
        byte2 = ns[2] << 4 | ns[3]

    return bytes([byte1, byte2])


class PxDecompressor:
    def __init__(self, compressed_data: bytes, flags: bytes):
        self.compressed_data = compressed_data
        self.flags = flags
        self.reset()

    # noinspection PyAttributeOutsideInit
    def reset(self):
        self.cursor = 0
        self.uncompressed_data = bytearray()

    def decompress(self) -> bytes:
        self.reset()
        # Let's get started!
        if DEBUG:
            print("Starting PX decomp.")
        c_data_len = len(self.compressed_data)
        if DEBUG:
            print(f"Bytes in input: {c_data_len}")
        while self.cursor < c_data_len:
            self._handle_control_byte(c_data_len)
        return self.uncompressed_data

    def _handle_control_byte(self, c_data_len):
        ctrl_byte = self._read_next_byte()
        if DEBUG:
            print(f"HANDLE CONTROL BYTE: {ctrl_byte:>08b}")

        for ctrl_bit in iter_bits(ctrl_byte):
            if self.cursor >= c_data_len:
                break
            if ctrl_bit == 1:
                if DEBUG:
                    print(f"> Handling uncompressed.")
                self.uncompressed_data.append(self._read_next_byte())
            else:
                if DEBUG:
                    print(f"> Handling special case.")
                self._handle_special_case()

    def _handle_special_case(self):
        next_byte = self._read_next_byte()
        high_nibble = (next_byte >> 4) & 0xF
        low_nibble = next_byte & 0xF

        idx_ctrl_flags = self._matches_flags(high_nibble)
        if DEBUG:
            print(f"> High nibble matches flag: {idx_ctrl_flags}")

        if idx_ctrl_flags is not False:
            self._insert_byte_pattern(idx_ctrl_flags, low_nibble)
        else:
            self._copy_sequence(low_nibble, high_nibble)

        pass

    def _read_next_byte(self):
        b = read_uintle(self.compressed_data, self.cursor)
        if DEBUG:
            print(f"IDX {int(self.cursor)} - READING BYTE: {b:>08b}")
        self.cursor += 1
        return b

    def _matches_flags(self, high_nibble):
        """
        Check if the passed nibble matches any of the control flags.
        The flags are assumed to be in the lower half of each self.flags byte.
        Returns index or False
        """
        for idx, byte in enumerate(self.flags):
            # The game compares with the entire byte, not just the lower nibble of the flag
            nbl = byte
            if nbl == high_nibble:
                return idx
        return False

    def _insert_byte_pattern(self, idx_ctrl_flags, low_nibble):
        # Based on the control flag, build two new bytes from the low_nibble data
        two_bytes = compute_four_nibbles_pattern(idx_ctrl_flags, low_nibble)
        if DEBUG:
            print(f"> Inserting by byte pattern: {two_bytes}")
        self.uncompressed_data += two_bytes
        pass

    def _copy_sequence(self, low_nibble, high_nibble):
        # In this case, we append a a sequence from a previous position in the decompressed data.
        # High half-byte is length of sequence copied over
        # Low half-byte is part of the position of the sequence
        offset = (-0x1000 + (low_nibble << 8)) | self._read_next_byte()
        outcurbyte = len(self.uncompressed_data)
        if offset < -outcurbyte:
            raise ValueError(f"Sequence to copy out of bound! Expected max. {-self.cursor} but got {offset}. "
                             f"Either the data to decompress is not valid PX compressed data, or "
                             f"something happened with our cursor that made us read the wrong bytes..")

        # Copy data sequence
        copy_pos = outcurbyte + offset
        bytes_to_copy = high_nibble + PX_MIN_MATCH_SEQLEN
        if DEBUG:
            print(f"> Copying {bytes_to_copy} from offset: {offset}")
        self.uncompressed_data += read_bytes(self.uncompressed_data, copy_pos, bytes_to_copy)
        pass
