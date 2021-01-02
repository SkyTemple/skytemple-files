"""Converts Wtu models back into the binary format used by the game"""
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
from skytemple_files.graphics.wtu.model import Wtu, MAGIC_NUMBER, WTU_ENTRY_LEN


class WtuWriter:
    def __init__(self, model: Wtu):
        self.model = model

    def write(self) -> bytes:
        buffer = bytearray(self.model.header_size + WTU_ENTRY_LEN * len(self.model.entries))
        buffer[0:4] = MAGIC_NUMBER
        write_uintle(buffer, len(self.model.entries), 0x4, 4)
        write_uintle(buffer, self.model.image_mode, 0x8, 4)
        write_uintle(buffer, self.model.header_size, 0xC, 4)

        for i, e in enumerate(self.model.entries):
            write_uintle(buffer, e.x, self.model.header_size + (i * WTU_ENTRY_LEN) + 0x00, 2)
            write_uintle(buffer, e.y, self.model.header_size + (i * WTU_ENTRY_LEN) + 0x02, 2)
            write_uintle(buffer, e.width, self.model.header_size + (i * WTU_ENTRY_LEN) + 0x04, 2)
            write_uintle(buffer, e.height, self.model.header_size + (i * WTU_ENTRY_LEN) + 0x06, 2)

        return buffer
