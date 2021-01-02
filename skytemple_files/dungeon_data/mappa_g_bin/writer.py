"""Converts MappaGBin models back into the binary format used by the game"""
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
from skytemple_files.dungeon_data.mappa_g_bin.model import MappaGBin


class MappaGBinWriter:
    def __init__(self, model: MappaGBin):
        self.model = model
        self.data = None
        self.bytes_written = 0

    def write(self) -> Tuple[bytes, List[int], Optional[int]]:
        """Returns the content and the offsets to the pointers and the sub-header pointer, for Sir0 serialization."""
        pointer_offsets = []

        floor_lists, floor_layouts = self.model.minimize()
        # Floor list data
        data = bytearray(sum((len(floor_list) + 1) * 4 for floor_list in floor_lists))
        cursor = 0
        for floor_list in floor_lists:
            cursor += 4  # null floor
            for floor in floor_list:
                data[cursor:cursor + 4] = floor.to_mappa()
                cursor += 4
        # Floor list LUT
        start_floor_list_lut = len(data)
        floor_list_lut = bytearray(4 * len(floor_lists))
        cursor_floor_data = 0
        for i, floor_list in enumerate(floor_lists):
            pointer_offsets.append(start_floor_list_lut + i * 4)
            write_uintle(floor_list_lut, cursor_floor_data, i * 4, 4)
            cursor_floor_data += (len(floor_list) + 1) * 4
        data += floor_list_lut
        # Floor layout data
        start_floor_layout_data = len(data)
        layout_data = bytearray(4 * len(floor_layouts))
        for i, layout in enumerate(floor_layouts):
            layout_data[i * 4: (i + 1) * 4] = layout.to_mappa()
        data += layout_data
        # Sub-header
        data_pointer = len(data)
        subheader = bytearray(8)
        pointer_offsets.append(data_pointer + 0x00)
        write_uintle(subheader, start_floor_list_lut, 0x00, 4)
        pointer_offsets.append(data_pointer + 0x04)
        write_uintle(subheader, start_floor_layout_data, 0x04, 4)
        data += subheader

        return data, pointer_offsets, data_pointer
