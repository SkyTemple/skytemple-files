"""Converts BgList models back into the binary format used by the game"""
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

import string
from typing import Optional

from skytemple_files.graphics.bg_list_dat._model import BgList

ALLOWED_CHARS = set(string.digits + string.ascii_uppercase)
MAX_LEN = 8


class BgListWriter:
    def __init__(self) -> None:
        self.data: Optional[bytearray] = None
        self.bytes_written = 0

    def write(self, model: BgList) -> bytes:
        # At max we will need 11 8 character cstrings for each entry:
        self.data = bytearray(len(model.level) * 11 * 9)
        self.bytes_written = 0
        for l in model.level:
            # BPL
            self._write_string(l.bpl_name)
            self._write_string(l.bpc_name)
            self._write_string(l.bma_name)
            for i in range(0, 8):
                if l.bpa_names[i] is not None:
                    self._write_string(l.bpa_names[i])  # type: ignore
                else:
                    self._write_string("")

        return self.data[: self.bytes_written]

    def _write_string(self, string: str) -> None:
        byts = self._read_string(string)
        self.data[self.bytes_written : self.bytes_written + MAX_LEN] = byts  # type: ignore
        self.bytes_written += MAX_LEN

    def _read_string(self, string: str) -> bytes:
        if set(string) > ALLOWED_CHARS:
            raise ValueError(
                f"The string '{string}' can not be used for bg_list.dat. Only "
                f"digits and uppercase characters are allowed."
            )
        length = len(string)
        if length > MAX_LEN:
            raise ValueError(
                f"The string '{string}' is too long for bg_list.dat. Max size "
                f"is {MAX_LEN}"
            )
        out = bytearray(MAX_LEN)
        out[0:length] = bytearray(string, "ascii")
        return out
