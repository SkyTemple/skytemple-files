"""Converts Wte models back into the binary format used by the game"""
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

from typing import Optional, Tuple, List

from range_typed_integers import u32_checked, u32, u8

from skytemple_files.common.util import (
    write_u32,
    write_u16,
    write_u8,
)
from skytemple_files.graphics.wte.model import MAGIC_NUMBER, Wte


class WteWriter:
    def __init__(self, model: Wte):
        self.model = model

    def write(self) -> Tuple[bytes, List[u32], Optional[u32]]:
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
        palette_buffer = bytearray(
            len(self.model.palette) + int(len(self.model.palette) / 3)
        )
        j = 0
        for i, p in enumerate(self.model.palette):
            write_u8(palette_buffer, u8(p), j)
            j += 1
            if i % 3 == 2:
                # Insert the fourth color
                write_u8(palette_buffer, u8(0x80), j)
                j += 1
        assert j == len(palette_buffer)
        buffer += palette_buffer

        # Header
        # We don't really know how many 0s the game wants but better to many than too few...
        header = bytearray(0x34)
        header[0:4] = MAGIC_NUMBER
        pointer_offsets.append(u32(len(buffer) + 0x04))
        write_u32(header, u32_checked(image_pointer), 0x04)
        write_u32(header, u32_checked(len(self.model.image_data)), 0x08)
        write_u8(header, self.model.actual_dim, 0x0C)
        write_u8(header, self.model.image_type.value, 0x0D)
        write_u32(header, self.model.unk10, 0x10)
        write_u16(header, self.model.width, 0x14)
        write_u16(header, self.model.height, 0x16)
        pointer_offsets.append(u32(len(buffer) + 0x18))
        write_u32(header, u32_checked(palette_pointer), 0x18)
        write_u32(header, u32_checked(len(self.model.palette) // 3), 0x1C)

        header_pointer = u32(len(buffer))
        buffer += header

        return buffer, pointer_offsets, header_pointer
