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
import string

from skytemple_files.common.util import *

ALLOWED_CHARS = set(string.digits + string.ascii_uppercase)
MAX_LEN = 8


class Lsd:
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        number_entries = read_uintle(data, 0, 2)
        self.entries = []
        for entry in iter_bytes(data, 8, 2, (2 + number_entries * 8)):
            self.entries.append(read_bytes(bytes(entry), 0, 8).rstrip(b'\0').decode('ascii'))

    def to_bytes(self):
        """Convert the LSD back to bytes"""
        data = bytearray(2 + len(self.entries) * MAX_LEN)
        write_uintle(data, len(self.entries), 0, 2)
        bytes_written = 2
        for e in self.entries:
            data[bytes_written:bytes_written + MAX_LEN] = self._str_to_bytes(e)
            bytes_written += MAX_LEN

        return data[:bytes_written]

    def _str_to_bytes(self, string: str):
        if set(string) > ALLOWED_CHARS:
            raise ValueError(f"The string '{string}' can not be used for lsd. Only "
                             f"digits and uppercase characters are allowed.")
        length = len(string)
        if length > MAX_LEN:
            raise ValueError(f"The string '{string}' is too long for lsd. Max size "
                             f"is {MAX_LEN}")
        out = bytearray(MAX_LEN)
        out[0:length] = bytearray(string, 'ascii')
        return out
