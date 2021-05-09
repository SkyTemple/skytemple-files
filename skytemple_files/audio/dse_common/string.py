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

class DseFilenameString(str):
    def __init__(self, string: str):
        super().__init__()
        self.string = str

    @classmethod
    def from_bytes(cls, data: bytes):
        pos = 0
        while data[pos] != 0 and pos < len(data):
            pos += 1
        if pos >= len(data):
            raise ValueError("DseFilenameString: EOF")
        string = str(data[:pos], 'ascii')
        rest = data[pos:]
        assert rest == bytes([0x00] + [0xAA] * (len(rest) - 1)), "Invalid DseFilenameString padding"
        return cls(string)

    def __str__(self):
        return self.string
