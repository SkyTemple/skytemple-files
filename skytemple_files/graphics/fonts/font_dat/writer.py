"""Converts FontDat models back into the binary format used by the game"""
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

from typing import Optional, Tuple

from range_typed_integers import u32_checked

from skytemple_files.common.i18n_util import _
from skytemple_files.common.util import (
    write_u32,
    write_u8,
)
from skytemple_files.graphics.fonts.font_dat import model, FONT_DAT_ENTRY_LEN
from skytemple_files.graphics.fonts.font_dat.model import FontDat


class FontDatWriter:
    def __init__(self, model: FontDat):
        self.model = model

    def write(self) -> bytes:
        buffer = bytearray(FONT_DAT_ENTRY_LEN * len(self.model.entries))
        write_u32(buffer, u32_checked(len(self.model.entries)), 0x00)

        # Font Data
        last: Tuple[Optional[int], Optional[int]] = (None, None)
        for i, e in enumerate(
            sorted(self.model.entries, key=lambda x: (x.table, x.char))
        ):
            if last == (e.char, e.table):
                raise ValueError(
                    _(
                        "Character {e.char} in table {e.table} is defined multiple times in a font file!"
                    )
                )
            last = (e.char, e.table)
            off_start = 0x4 + (i * FONT_DAT_ENTRY_LEN)
            write_u8(buffer, e.char, off_start + 0x00)
            write_u8(buffer, e.table, off_start + 0x01)
            write_u8(buffer, e.width, off_start + 0x02)
            write_u8(buffer, e.bprow, off_start + 0x03)
            buffer[off_start + 0x04 : off_start + FONT_DAT_ENTRY_LEN] = e.data

        return buffer
