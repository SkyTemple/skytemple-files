"""Converts MappaBin models back into the binary format used by the game"""
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
from itertools import chain
from typing import Optional

from skytemple_files.common.util import *
from skytemple_files.dungeon_data.mappa_bin.item_list import GUARANTEED
from skytemple_files.dungeon_data.mappa_bin.model import MappaBin
from skytemple_files.dungeon_data.mappa_bin.trap_list import MappaTrapType

HIGHEST_MAX_WEIGHT = 10000


class MappaBinWriter:
    def __init__(self, model: MappaBin):
        self.model = model

    def write(self) -> Tuple[bytes, List[int], Optional[int]]:
        """Returns the content and the offsets to the pointers and the sub-header pointer, for Sir0 serialization."""
        pointer_offsets = []
        
        floor_lists, floor_layouts, monster_lists, trap_lists, item_lists = self.model.minimize()
        # Floor list data
        data = bytearray(sum((len(floor_list) + 1) * 18 for floor_list in floor_lists))
        cursor = 0
        for floor_list in floor_lists:
            cursor += 18  # null floor
            for floor in floor_list:
                data[cursor:cursor+18] = floor.to_mappa()
                cursor += 18
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0x00 for _ in range(0, 16 - (len(data) % 16)))
        # Floor list LUT
        start_floor_list_lut = len(data)
        floor_list_lut = bytearray(4 * len(floor_lists))
        cursor_floor_data = 0
        for i, floor_list in enumerate(floor_lists):
            pointer_offsets.append(start_floor_list_lut + i * 4)
            write_uintle(floor_list_lut, cursor_floor_data, i * 4, 4)
            cursor_floor_data += (len(floor_list) + 1) * 18
        data += floor_list_lut
        # Padding
        if len(data) % 4 != 0:
            data += bytes(0xAA for _ in range(0, 4 - (len(data) % 4)))
        # Floor layout data
        start_floor_layout_data = len(data)
        layout_data = bytearray(32 * len(floor_layouts))
        for i, layout in enumerate(floor_layouts):
            layout_data[i * 32: (i + 1) * 32] = layout.to_mappa()
        data += layout_data
        # Padding
        if len(data) % 4 != 0:
            data += bytes(0xAA for _ in range(0, 4 - (len(data) % 4)))
        # Monster spawn data
        monster_data_start = len(data)
        monster_data = bytearray(sum((len(monsters) + 1) * 8 for monsters in monster_lists))
        monster_data_cursor = 0
        monster_data_pointer = []
        for i, monster_list in enumerate(monster_lists):
            monster_data_pointer.append(monster_data_start + monster_data_cursor)

            single_monster_list_data = bytes(chain.from_iterable(monster.to_mappa() for monster in monster_list)) + bytes(8)
            len_single = len(single_monster_list_data)
            monster_data[monster_data_cursor:monster_data_cursor+len_single] = single_monster_list_data
            monster_data_cursor += len_single
        data += monster_data
        # Padding
        if len(data) % 4 != 0:
            data += bytes(0xAA for _ in range(0, 4 - (len(data) % 4)))
        # Monster spawn LUT
        start_monster_lut = len(data)
        monster_lut = bytearray(4 * len(monster_data_pointer))
        for i, pnt in enumerate(monster_data_pointer):
            pointer_offsets.append(start_monster_lut + i * 4)
            write_uintle(monster_lut, pnt, i * 4, 4)
        data += monster_lut
        # Padding
        if len(data) % 4 != 0:
            data += bytes(0xAA for _ in range(0, 4 - (len(data) % 4)))
        # Trap lists data
        trap_data_start = len(data)
        trap_data = bytearray(len(trap_lists) * 50)
        trap_data_cursor = 0
        trap_data_pointer = []
        for trap_list in trap_lists:
            trap_data_pointer.append(trap_data_start + trap_data_cursor)
            single_trap_list_data = trap_list.to_mappa()

            len_single = len(single_trap_list_data)
            assert len_single == 50
            trap_data[trap_data_cursor:trap_data_cursor+len_single] = single_trap_list_data
            trap_data_cursor += len_single
        assert trap_data_cursor == len(trap_lists) * 50
        data += trap_data
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        # Trap lists LUT
        start_traps_lut = len(data)
        trap_lut = bytearray(4 * len(trap_data_pointer))
        for i, pnt in enumerate(trap_data_pointer):
            pointer_offsets.append(start_traps_lut + i * 4)
            write_uintle(trap_lut, pnt, i * 4, 4)
        data += trap_lut
        # Item spawn lists data
        item_data_start = len(data)
        # TODO: I don't need to explain why a fixed size here per list is flawed.
        item_data = bytearray((len(item_lists) * 500))
        item_data_cursor = 0
        item_data_pointer = []
        for item_list in item_lists:
            item_data_pointer.append(item_data_start + item_data_cursor)

            single_item_list_data = item_list.to_mappa()
            len_single = len(single_item_list_data)
            assert item_data_cursor + len_single < len(item_data)
            item_data[item_data_cursor:item_data_cursor+len_single] = single_item_list_data
            item_data_cursor += len_single
        data += item_data[:item_data_cursor]
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        # Item spawn lists LUT
        start_items_lut = len(data)
        item_list_lut = bytearray(4 * len(item_data_pointer))
        for i, pnt in enumerate(item_data_pointer):
            pointer_offsets.append(start_items_lut + i * 4)
            write_uintle(item_list_lut, pnt, i * 4, 4)
        data += item_list_lut
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        # Sub-header
        data_pointer = len(data)
        subheader = bytearray(4 * 5)
        pointer_offsets.append(data_pointer + 0x00)
        write_uintle(subheader, start_floor_list_lut, 0x00, 4)
        pointer_offsets.append(data_pointer + 0x04)
        write_uintle(subheader, start_floor_layout_data, 0x04, 4)
        pointer_offsets.append(data_pointer + 0x08)
        write_uintle(subheader, start_items_lut, 0x08, 4)
        pointer_offsets.append(data_pointer + 0x0C)
        write_uintle(subheader, start_monster_lut, 0x0C, 4)
        pointer_offsets.append(data_pointer + 0x10)
        write_uintle(subheader, start_traps_lut, 0x10, 4)
        data += subheader

        return data, pointer_offsets, data_pointer
