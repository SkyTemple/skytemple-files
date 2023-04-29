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

from itertools import chain
from typing import Optional, List, Tuple

from range_typed_integers import u32_checked, u32

from skytemple_files.common.util import (
    AutoString,
    write_u32,
    read_u32,
)
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.dungeon_data.mappa_bin._python_impl.floor import (
    MappaFloor,
    StubMappaFloor,
)
from skytemple_files.dungeon_data.mappa_bin._python_impl.floor_layout import (
    MappaFloorLayout,
)
from skytemple_files.dungeon_data.mappa_bin._python_impl.item_list import MappaItemList
from skytemple_files.dungeon_data.mappa_bin._python_impl.monster import MappaMonster
from skytemple_files.dungeon_data.mappa_bin._python_impl.trap_list import MappaTrapList
from skytemple_files.dungeon_data.mappa_bin.protocol import MappaBinProtocol

FLOOR_IDX_ENTRY_LEN = 18


class MappaBinReadContainer:
    def __init__(self, data: bytes, header_start: int):
        self.data = data
        self.dungeon_list_index_start = read_u32(data, header_start + 0x00)
        self.floor_layout_data_start = read_u32(data, header_start + 0x04)
        self.item_spawn_list_index_start = read_u32(data, header_start + 0x08)
        self.monster_spawn_list_index_start = read_u32(data, header_start + 0x0C)
        self.trap_spawn_list_index_start = read_u32(data, header_start + 0x10)

        # assert self.dungeon_list_index_start % 4 == 0
        # assert self.floor_layout_data_start % 4 == 0
        # assert self.item_spawn_list_index_start % 4 == 0
        # assert self.monster_spawn_list_index_start % 4 == 0
        # assert self.trap_spawn_list_index_start % 4 == 0

        self.read_cache = {}  # type: ignore


class MappaBin(MappaBinProtocol[MappaFloor], Sir0Serializable, AutoString):
    floor_lists: List[List[MappaFloor]]

    def __init__(self, floor_lists: List[List[MappaFloor]]):
        self.floor_lists = floor_lists

    def add_floor_list(self, floor_list: List[MappaFloor]):
        self.floor_lists.append(floor_list)

    def remove_floor_list(self, index: int):
        del self.floor_lists[index]

    def add_floor_to_floor_list(self, floor_list_index: int, floor: MappaFloor):
        self.floor_lists[floor_list_index].append(floor)

    def insert_floor_in_floor_list(
        self, floor_list_index: int, insert_index: int, floor: MappaFloor
    ):
        self.floor_lists[floor_list_index].insert(insert_index, floor)

    def remove_floor_from_floor_list(self, floor_list_index: int, floor_index: int):
        del self.floor_lists[floor_list_index][floor_index]

    def sir0_serialize_parts(self) -> Tuple[bytes, List[u32], Optional[u32]]:
        """Returns the content and the offsets to the pointers and the sub-header pointer, for Sir0 serialization."""
        pointer_offsets = []

        (
            floor_lists,
            floor_layouts,
            monster_lists,
            trap_lists,
            item_lists,
        ) = self.minimize()
        # Floor list data
        data = bytearray(sum((len(floor_list) + 1) * 18 for floor_list in floor_lists))
        cursor = 0
        for floor_list in floor_lists:
            cursor += 18  # null floor
            for floor in floor_list:
                data[cursor : cursor + 18] = floor.to_mappa()
                cursor += 18
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0x00 for _ in range(0, 16 - (len(data) % 16)))
        # Floor list LUT
        start_floor_list_lut = u32_checked(len(data))
        floor_list_lut = bytearray(4 * len(floor_lists))
        cursor_floor_data = u32(0)
        for i, floor_list in enumerate(floor_lists):
            pointer_offsets.append(u32_checked(start_floor_list_lut + i * 4))
            write_u32(floor_list_lut, cursor_floor_data, i * 4)
            cursor_floor_data = u32_checked(
                cursor_floor_data + (len(floor_list) + 1) * 18
            )
        data += floor_list_lut
        # Padding
        if len(data) % 4 != 0:
            data += bytes(0xAA for _ in range(0, 4 - (len(data) % 4)))
        # Floor layout data
        start_floor_layout_data = u32_checked(len(data))
        layout_data = bytearray(32 * len(floor_layouts))
        for i, layout in enumerate(floor_layouts):
            layout_data[i * 32 : (i + 1) * 32] = layout.to_mappa()
        data += layout_data
        # Padding
        if len(data) % 4 != 0:
            data += bytes(0xAA for _ in range(0, 4 - (len(data) % 4)))
        # Monster spawn data
        monster_data_start = len(data)
        monster_data = bytearray(
            sum((len(monsters) + 1) * 8 for monsters in monster_lists)
        )
        monster_data_cursor = 0
        monster_data_pointer = []
        for i, monster_list in enumerate(monster_lists):
            monster_data_pointer.append(
                u32_checked(monster_data_start + monster_data_cursor)
            )

            single_monster_list_data = bytes(
                chain.from_iterable(monster.to_mappa() for monster in monster_list)
            ) + bytes(8)
            len_single = len(single_monster_list_data)
            monster_data[
                monster_data_cursor : monster_data_cursor + len_single
            ] = single_monster_list_data
            monster_data_cursor += len_single
        data += monster_data
        # Padding
        if len(data) % 4 != 0:
            data += bytes(0xAA for _ in range(0, 4 - (len(data) % 4)))
        # Monster spawn LUT
        start_monster_lut = u32_checked(len(data))
        monster_lut = bytearray(4 * len(monster_data_pointer))
        for i, pnt in enumerate(monster_data_pointer):
            pointer_offsets.append(u32_checked(start_monster_lut + i * 4))
            write_u32(monster_lut, pnt, i * 4)
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
            trap_data_pointer.append(u32_checked(trap_data_start + trap_data_cursor))
            single_trap_list_data = trap_list.to_mappa()

            len_single = len(single_trap_list_data)
            assert len_single == 50
            trap_data[
                trap_data_cursor : trap_data_cursor + len_single
            ] = single_trap_list_data
            trap_data_cursor += len_single
        assert trap_data_cursor == len(trap_lists) * 50
        data += trap_data
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        # Trap lists LUT
        start_traps_lut = u32_checked(len(data))
        trap_lut = bytearray(4 * len(trap_data_pointer))
        for i, pnt in enumerate(trap_data_pointer):
            pointer_offsets.append(u32_checked(start_traps_lut + i * 4))
            write_u32(trap_lut, pnt, i * 4)
        data += trap_lut
        # Item spawn lists data
        item_data_start = len(data)
        # TODO: I don't need to explain why a fixed size here per list is flawed.
        item_data = bytearray((len(item_lists) * 500))
        item_data_cursor = 0
        item_data_pointer = []
        for item_list in item_lists:
            item_data_pointer.append(u32_checked(item_data_start + item_data_cursor))

            single_item_list_data = item_list.to_mappa()
            len_single = len(single_item_list_data)
            assert item_data_cursor + len_single < len(item_data)
            item_data[
                item_data_cursor : item_data_cursor + len_single
            ] = single_item_list_data
            item_data_cursor += len_single
        data += item_data[:item_data_cursor]
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        # Item spawn lists LUT
        start_items_lut = u32_checked(len(data))
        item_list_lut = bytearray(4 * len(item_data_pointer))
        for i, pnt in enumerate(item_data_pointer):
            pointer_offsets.append(u32_checked(start_items_lut + i * 4))
            write_u32(item_list_lut, pnt, i * 4)
        data += item_list_lut
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        # Sub-header
        data_pointer = u32_checked(len(data))
        subheader = bytearray(4 * 5)
        pointer_offsets.append(u32_checked(data_pointer + 0x00))
        write_u32(subheader, start_floor_list_lut, 0x00)
        pointer_offsets.append(u32_checked(data_pointer + 0x04))
        write_u32(subheader, start_floor_layout_data, 0x04)
        pointer_offsets.append(u32_checked(data_pointer + 0x08))
        write_u32(subheader, start_items_lut, 0x08)
        pointer_offsets.append(u32_checked(data_pointer + 0x0C))
        write_u32(subheader, start_monster_lut, 0x0C)
        pointer_offsets.append(u32_checked(data_pointer + 0x10))
        write_u32(subheader, start_traps_lut, 0x10)
        data += subheader

        return data, pointer_offsets, data_pointer

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: u32,
    ) -> "MappaBin":
        return cls(
            cls._read_floor_list(
                MappaBinReadContainer(
                    content_data,
                    data_pointer,
                )
            )
        )

    @classmethod
    def _read_floor_list(cls, read: MappaBinReadContainer):
        start = read.dungeon_list_index_start
        end = read.floor_layout_data_start
        dungeons = []
        for i in range(start, end, 4):
            dungeons.append(cls._read_floors(read, read_u32(read.data, i)))
        return dungeons

    @classmethod
    def _read_floors(cls, read: MappaBinReadContainer, pointer: int):
        # The zeroth floor is just nulls, we omit it.
        empty = bytes(FLOOR_IDX_ENTRY_LEN)
        assert (
            read.data[pointer : pointer + FLOOR_IDX_ENTRY_LEN] == empty
        ), "The first floor of a dungeon must be a null floor."
        floors = []
        pointer += FLOOR_IDX_ENTRY_LEN
        floor_data = read.data[pointer : pointer + FLOOR_IDX_ENTRY_LEN]
        while floor_data != empty:
            floors.append(MappaFloor.from_mappa(read, floor_data))
            pointer += FLOOR_IDX_ENTRY_LEN
            floor_data = read.data[pointer : pointer + FLOOR_IDX_ENTRY_LEN]
            if pointer > read.dungeon_list_index_start - FLOOR_IDX_ENTRY_LEN:
                break
        return floors

    def minimize(
        self,
    ) -> Tuple[
        List[List[StubMappaFloor]],
        List[MappaFloorLayout],
        List[List[MappaMonster]],
        List[MappaTrapList],
        List[MappaItemList],
    ]:
        """
        Collects a list of floors, that references indices in other lists, like stored in the mappa files.
        If two floors use the same exact data for something, they will be pointing to the same index in the lists,
        there are no duplicates.
        Returned are all lists.
        TODO: Performance could be improved here, by using more efficient lookup mechanisms.
        """
        floor_lists: List[List[StubMappaFloor]] = []
        floor_layouts: List[MappaFloorLayout] = []
        monster_lists: List[List[MappaMonster]] = []
        trap_lists: List[MappaTrapList] = []
        item_lists: List[MappaItemList] = []
        for floor_list in self.floor_lists:
            stub_floor_list = []
            for floor in floor_list:
                # Layout
                layout_idx = self._find_if_not_exists_insert(
                    floor_layouts, floor.layout
                )
                # Monsters
                monsters_idx = self._find_if_not_exists_insert(
                    monster_lists, floor.monsters
                )
                # Traps
                traps_idx = self._find_if_not_exists_insert(trap_lists, floor.traps)
                # Floor items
                floor_items_idx = self._find_if_not_exists_insert(
                    item_lists, floor.floor_items
                )
                # Shop items
                shop_items_idx = self._find_if_not_exists_insert(
                    item_lists, floor.shop_items
                )
                # Monster house items
                monster_house_items_idx = self._find_if_not_exists_insert(
                    item_lists, floor.monster_house_items
                )
                # Buried items
                buried_items_idx = self._find_if_not_exists_insert(
                    item_lists, floor.buried_items
                )
                # Unk items 1
                unk_items1_idx = self._find_if_not_exists_insert(
                    item_lists, floor.unk_items1
                )
                # Unk items 2
                unk_items2_idx = self._find_if_not_exists_insert(
                    item_lists, floor.unk_items2
                )

                stub_floor_list.append(
                    StubMappaFloor(
                        layout_idx,
                        monsters_idx,
                        traps_idx,
                        floor_items_idx,
                        shop_items_idx,
                        monster_house_items_idx,
                        buried_items_idx,
                        unk_items1_idx,
                        unk_items2_idx,
                    )
                )

            floor_lists.append(stub_floor_list)

        return floor_lists, floor_layouts, monster_lists, trap_lists, item_lists

    @staticmethod
    def _find_if_not_exists_insert(lst, elem):
        try:
            index = lst.index(elem)
        except ValueError:
            index = len(lst)
            lst.append(elem)
        return index

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MappaBin):
            return False
        return self.floor_lists == other.floor_lists
