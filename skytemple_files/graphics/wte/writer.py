"""Converts Wte models back into the binary format used by the game"""
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
from typing import Optional

from skytemple_files.common.util import *
from skytemple_files.graphics.wte.model import Wte, MAGIC_NUMBER


class WteWriter:
    def __init__(self, model: Wte):
        self.model = model

    def write(self) -> Tuple[bytes, List[int], Optional[int]]:
        pointer_offsets = []
        buffer = bytearray()

        # Image data
        image_pointer = len(buffer)
        buffer += self.model.image_data
        # Padding
        if len(buffer) % 16 != 0:
            buffer += bytes(0 for _ in range(0, 16 - (len(buffer) % 16)))

        # Palette
        palette_pointer = len(buffer)
        palette_buffer = bytearray(len(self.model.palette) + int(len(self.model.palette) / 3))
        j = 0
        for i, p in enumerate(self.model.palette):
            write_uintle(palette_buffer, p, j)
            j += 1
            if i % 3 == 2:
                # Insert the fourth color
                write_uintle(palette_buffer, 0x80, j)
                j += 1
        assert j == len(palette_buffer)
        buffer += palette_buffer

        # Header
        # We don't really know how many 0s the game wants but better to many than too few...
        header = bytearray(0x34)
        header[0:4] = MAGIC_NUMBER
        pointer_offsets.append(len(buffer) + 0x04)
        write_uintle(header, image_pointer, 0x04, 4)
        write_uintle(header, len(self.model.image_data), 0x08, 4)
        write_uintle(header, self.model.actual_dim, 0x0C, 1)
        write_uintle(header, self.model.image_type.value, 0x0D, 1)
        write_uintle(header, self.model.unk10, 0x10, 4)
        write_uintle(header, self.model.width, 0x14, 2)
        write_uintle(header, self.model.height, 0x16, 2)
        pointer_offsets.append(len(buffer) + 0x18)
        write_uintle(header, palette_pointer, 0x18, 4)
        write_uintle(header, int(len(self.model.palette) / 3), 0x1C, 4)

        header_pointer = len(buffer)
        buffer += header

        return buffer, pointer_offsets, header_pointer
