#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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
from __future__ import annotations

from typing import List

from range_typed_integers import u32_checked

from skytemple_files.common.string_codec import PMD2_STR_ENCODER
from skytemple_files.common.util import (
    write_u32,
    read_var_length_string,
    read_u32,
)

# XXX: Removing this re-export his is a breaking change in skytemple < 1.5 due to a typo.
# noinspection PyUnresolvedReferences
from skytemple_files.common.util import open_utf8  # nopycln: import


class Str:
    def __init__(self, data: bytes, string_encoding: str = PMD2_STR_ENCODER):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        after_end = len(data)
        # File starts with pointers. Last pointer points to after end of file
        pointers = []
        current_pointer = 0
        cursor = 0
        self.string_encoding = string_encoding
        while current_pointer < after_end:
            current_pointer = read_u32(data, cursor)
            if current_pointer < after_end:
                pointers.append(current_pointer)
                cursor += 4
        # Then follow the strings
        self.strings = []
        for pnt in pointers:
            self.strings.append(self._read_string(data, pnt))

    def _read_string(self, data, pnt):
        return read_var_length_string(data, pnt, self.string_encoding)[1]

    def to_bytes(self):
        """Convert the string list back to bytes"""
        length_of_index = 4 * (len(self.strings) + 1)
        length_of_str_bytes = 0
        offset_list = []
        strings_bytes = []
        for s in self.strings:
            b = bytes(s, self.string_encoding) + bytes([0])
            offset_list.append(u32_checked(length_of_index + length_of_str_bytes))
            length_of_str_bytes += len(b)
            strings_bytes.append(b)

        result = bytearray(length_of_index + length_of_str_bytes)
        cursor = 0
        for pnt in offset_list:
            write_u32(result, pnt, cursor)
            cursor += 4
        # End of pointers markers
        write_u32(result, u32_checked(length_of_index + length_of_str_bytes), cursor)
        cursor += 4

        # Write string bytes
        offset_list.append(u32_checked(length_of_index + length_of_str_bytes))
        for i, s in enumerate(strings_bytes):
            length = offset_list[i + 1] - offset_list[i]
            result[cursor : cursor + length] = s
            cursor += length

        return result

    @classmethod
    def internal__get_all_raw_strings_from(cls, data: bytes) -> List[bytes]:
        """Returns all strings in this file, undecoded."""
        if not isinstance(data, memoryview):
            data = memoryview(data)
        after_end = len(data)

        # File starts with pointers. Last pointer points to after end of file
        pointers = []
        current_pointer = 0
        cursor = 0
        while current_pointer < after_end:
            current_pointer = read_u32(data, cursor)
            if current_pointer < after_end:
                pointers.append(current_pointer)
                cursor += 4

        # Then follow the strings
        strings = []
        for pnt in pointers:
            bytes_of_string = bytearray()
            current_byte = -1
            cursor = pnt
            while current_byte != 0:
                current_byte = data[cursor]
                cursor += 1
                if current_byte != 0:
                    bytes_of_string.append(current_byte)

            strings.append(bytes(bytes_of_string))

        return strings
