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
from skytemple_files.common.string_codec import PMD2_STR_ENCODER
from skytemple_files.common.util import *


class Str:
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        after_end = len(data)
        # File starts with pointers. Last pointer points to after end of file
        pointers = []
        current_pointer = 0
        cursor = 0
        while current_pointer < after_end:
            current_pointer = read_uintle(data, cursor, 4)
            if current_pointer < after_end:
                pointers.append(current_pointer)
                cursor += 4
        # Then follow the strings
        self.strings = []
        for pnt in pointers:
            self.strings.append(self._read_string(data, pnt))

    @staticmethod
    def _read_string(data, pnt):
        return read_var_length_string(data, pnt)[1]

    def to_bytes(self):
        """Convert the string list back to bytes"""
        length_of_index = 4 * (len(self.strings) + 1)
        length_of_str_bytes = 0
        offset_list = []
        strings_bytes = []
        for s in self.strings:
            b = bytes(s, PMD2_STR_ENCODER) + bytes([0])
            offset_list.append(length_of_index + length_of_str_bytes)
            length_of_str_bytes += len(b)
            strings_bytes.append(b)

        result = bytearray(length_of_index + length_of_str_bytes)
        cursor = 0
        for pnt in offset_list:
            write_uintle(result, pnt, cursor, 4)
            cursor += 4
        # End of pointers markers
        write_uintle(result, length_of_index + length_of_str_bytes, cursor, 4)
        cursor += 4

        # Write string bytes
        offset_list.append(length_of_index + length_of_str_bytes)
        for i, s in enumerate(strings_bytes):
            length = offset_list[i+1] - offset_list[i]
            result[cursor:cursor+length] = s
            cursor += length

        return result
