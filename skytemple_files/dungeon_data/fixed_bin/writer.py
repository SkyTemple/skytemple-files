"""Converts FixedBin models back into the binary format used by the game"""
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


from range_typed_integers import u32_checked, u32

from skytemple_files.common.util import write_u32
from skytemple_files.dungeon_data.fixed_bin.model import FixedBin


class FixedBinWriter:
    def __init__(self, model: FixedBin):
        self.model = model

    def write(self) -> tuple[bytes, list[u32], u32 | None]:
        """Returns the content and the offsets to the pointers and the sub-header pointer, for Sir0 serialization."""
        fixed_floors = bytearray()
        pointers = []
        for floor in self.model.fixed_floors:
            pointers.append(u32_checked(len(fixed_floors)))
            fixed_floors += floor.to_bytes()

        # Padding
        if len(fixed_floors) % 4 != 0:
            fixed_floors += bytes(0xAA for _ in range(0, 4 - (len(fixed_floors) % 4)))

        header_buffer = bytearray((len(self.model.fixed_floors) + 1) * 4)
        pointer_offsets = []
        i = 0
        for i, pointer in enumerate(pointers):
            pointer_offsets.append(u32(len(fixed_floors) + i * 4))
            write_u32(header_buffer, pointer, i * 4)
        write_u32(header_buffer, u32(0xAAAAAAAA), (i + 1) * 4)

        return fixed_floors + header_buffer, pointer_offsets, u32(len(fixed_floors))
