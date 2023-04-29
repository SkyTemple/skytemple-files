"""Converts MappaGBin models back into the binary format used by the game"""
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

from range_typed_integers import u32_checked, u32

from skytemple_files.common.util import write_u32
from skytemple_files.dungeon_data.mappa_g_bin.model import MappaGBin


class MappaGBinWriter:
    def __init__(self, model: MappaGBin):
        self.model = model
        self.data = None
        self.bytes_written = 0

    def write(self) -> Tuple[bytes, List[u32], Optional[u32]]:
        """Returns the content and the offsets to the pointers and the sub-header pointer, for Sir0 serialization."""
        pointer_offsets: List[u32] = []

        floor_lists, floor_layouts = self.model.minimize()
        # Floor list data
        data = bytearray(sum((len(floor_list) + 1) * 4 for floor_list in floor_lists))
        cursor = 0
        for floor_list in floor_lists:
            cursor += 4  # null floor
            for floor in floor_list:
                data[cursor : cursor + 4] = floor.to_mappa()
                cursor += 4
        # Floor list LUT
        start_floor_list_lut = u32_checked(len(data))
        floor_list_lut = bytearray(4 * len(floor_lists))
        cursor_floor_data = u32(0)
        for i, floor_list in enumerate(floor_lists):
            pointer_offsets.append(u32(start_floor_list_lut + i * 4))
            write_u32(floor_list_lut, cursor_floor_data, i * 4)
            cursor_floor_data = u32_checked(
                cursor_floor_data + (len(floor_list) + 1) * 4
            )
        data += floor_list_lut
        # Floor layout data
        start_floor_layout_data = u32_checked(len(data))
        layout_data = bytearray(4 * len(floor_layouts))
        for i, layout in enumerate(floor_layouts):
            layout_data[i * 4 : (i + 1) * 4] = layout.to_mappa()
        data += layout_data
        # Sub-header
        data_pointer = u32(len(data))
        subheader = bytearray(8)
        pointer_offsets.append(u32(data_pointer + 0x00))
        write_u32(subheader, start_floor_list_lut, 0x00)
        pointer_offsets.append(u32(data_pointer + 0x04))
        write_u32(subheader, start_floor_layout_data, 0x04)
        data += subheader

        return data, pointer_offsets, data_pointer
