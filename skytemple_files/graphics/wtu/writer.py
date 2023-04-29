"""Converts Wtu models back into the binary format used by the game"""
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

from range_typed_integers import u32_checked

from skytemple_files.common.util import write_u16, write_u32
from skytemple_files.graphics.wtu.model import MAGIC_NUMBER, WTU_ENTRY_LEN, Wtu


class WtuWriter:
    def __init__(self, model: Wtu):
        self.model = model

    def write(self) -> bytes:
        buffer = bytearray(
            self.model.header_size + WTU_ENTRY_LEN * len(self.model.entries)
        )
        buffer[0:4] = MAGIC_NUMBER
        write_u32(buffer, u32_checked(len(self.model.entries)), 0x4)
        write_u32(buffer, self.model.image_mode, 0x8)
        write_u32(buffer, self.model.header_size, 0xC)

        for i, e in enumerate(self.model.entries):
            write_u16(buffer, e.x, self.model.header_size + (i * WTU_ENTRY_LEN) + 0x00)
            write_u16(buffer, e.y, self.model.header_size + (i * WTU_ENTRY_LEN) + 0x02)
            write_u16(
                buffer, e.width, self.model.header_size + (i * WTU_ENTRY_LEN) + 0x04
            )
            write_u16(
                buffer, e.height, self.model.header_size + (i * WTU_ENTRY_LEN) + 0x06
            )

        return buffer
