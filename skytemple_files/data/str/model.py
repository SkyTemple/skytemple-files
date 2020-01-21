from skytemple_files.common.util import *
from skytemple_files.data.str.codec import init, PMD2_STR_ENCODER


class Str:
    init()

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
        bytes_of_string = bytearray()
        current_byte = -1
        cursor = pnt
        while current_byte != 0:
            current_byte = data[cursor]
            cursor += 1
            if current_byte != 0:
                bytes_of_string.append(current_byte)

        return str(bytes_of_string, PMD2_STR_ENCODER)

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
