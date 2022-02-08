#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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

class DseFilenameString(str):
    def __init__(self, string: str):
        super().__init__()
        self.string = string

    @classmethod
    def from_bytes(cls, data: bytes):
        pos = 0
        while data[pos] != 0 and pos < len(data):
            pos += 1
        if pos >= len(data):
            raise ValueError("DseFilenameString: EOF")
        string = str(data[:pos], 'ascii')
        rest = data[pos:]
        assert rest == bytes([0x00] + [0xAA] * (len(rest) - 1)) or rest == bytes([0x00] + [0xFF] * (len(rest) - 1)), "Invalid DseFilenameString padding"
        return cls(string)

    def to_bytes(self, end_byte_0xaa=False):
        if len(self.string) > 0xF:
            raise ValueError("DSE filename too long to convert.")
        data = bytearray(16)
        encoded = bytes(self.string, 'ascii')
        data[:len(encoded)] = encoded
        data[len(encoded) + 1:16] = [0xFF if not end_byte_0xaa else 0xAA] * (15 - len(encoded))
        return data

    def __eq__(self, other):
        if not isinstance(other, DseFilenameString):
            return False
        return vars(self) == vars(other)

    def __str__(self):
        return self.string
