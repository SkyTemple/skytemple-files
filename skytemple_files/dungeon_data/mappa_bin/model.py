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
from xml.etree.ElementTree import Element

from skytemple_files.common.ppmdu_config.dungeon_data import Pmd2DungeonItem, Pmd2DungeonData
from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.xml_util import XmlSerializable, validate_xml_tag
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.dungeon_data.mappa_bin import XML_MAPPA, XML_FLOOR_LIST, XML_FLOOR
from skytemple_files.dungeon_data.mappa_bin.floor import MappaFloor, StubMappaFloor
from skytemple_files.dungeon_data.mappa_bin.floor_layout import MappaFloorLayout
from skytemple_files.dungeon_data.mappa_bin.item_list import MappaItemList
from skytemple_files.dungeon_data.mappa_bin.monster import MappaMonster
from skytemple_files.dungeon_data.mappa_bin.trap_list import MappaTrapList

FLOOR_IDX_ENTRY_LEN = 18


class MappaBinReadContainer:
    def __init__(self, data: bytes, header_start: int, items: List[Pmd2DungeonItem]):
        self.data = data
        self.dungeon_list_index_start = read_uintle(data, header_start + 0x00, 4)
        self.floor_layout_data_start = read_uintle(data, header_start + 0x04, 4)
        self.item_spawn_list_index_start = read_uintle(data, header_start + 0x08, 4)
        self.monster_spawn_list_index_start = read_uintle(data, header_start + 0x0C, 4)
        self.trap_spawn_list_index_start = read_uintle(data, header_start + 0x10, 4)

        #assert self.dungeon_list_index_start % 4 == 0
        #assert self.floor_layout_data_start % 4 == 0
        #assert self.item_spawn_list_index_start % 4 == 0
        #assert self.monster_spawn_list_index_start % 4 == 0
        #assert self.trap_spawn_list_index_start % 4 == 0

        self.items = items
        self.read_cache = {}


class MappaBin(Sir0Serializable, XmlSerializable):

    def __init__(self, floor_lists: List[List[MappaFloor]]):
        self.floor_lists = floor_lists

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.dungeon_data.mappa_bin.writer import MappaBinWriter
        return MappaBinWriter(self).write()

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int, static_data: Optional[Pmd2Data] = None) -> 'MappaBin':
        if static_data is None:
            raise ValueError("MappaBin needs Pmd2Data to initialize.")
        return cls(cls._read_floor_list(MappaBinReadContainer(
            content_data, data_pointer, static_data.dungeon_data.items
        )))

    @classmethod
    def _read_floor_list(cls, read: MappaBinReadContainer):
        start = read.dungeon_list_index_start
        end = read.floor_layout_data_start
        dungeons = []
        for i in range(start, end, 4):
            dungeons.append(cls._read_floors(read, read_uintle(read.data, i, 4)))
        return dungeons

    @classmethod
    def _read_floors(cls, read: MappaBinReadContainer, pointer):
        # The zeroth floor is just nulls, we omit it.
        empty = bytes(FLOOR_IDX_ENTRY_LEN)
        assert read.data[pointer:pointer + FLOOR_IDX_ENTRY_LEN] == empty, \
            "The first floor of a dungeon must be a null floor."
        floors = []
        pointer += FLOOR_IDX_ENTRY_LEN
        floor_data = read.data[pointer:pointer + FLOOR_IDX_ENTRY_LEN]
        while floor_data != empty:
            floors.append(MappaFloor.from_mappa(read, floor_data))
            pointer += FLOOR_IDX_ENTRY_LEN
            floor_data = read.data[pointer:pointer + FLOOR_IDX_ENTRY_LEN]
            if pointer > read.dungeon_list_index_start - FLOOR_IDX_ENTRY_LEN:
                break
        return floors

    def to_xml(self) -> Element:
        mappa_xml = Element(XML_MAPPA)
        for i, floor_list in enumerate(self.floor_lists):
            floor_list_xml = Element(XML_FLOOR_LIST)
            for floor in floor_list:
                floor_xml = floor.to_xml()
                validate_xml_tag(floor_xml, XML_FLOOR)
                floor_list_xml.append(floor_xml)
            mappa_xml.append(floor_list_xml)
        return mappa_xml

    @classmethod
    def from_xml(cls, ele: Element) -> 'MappaBin':
        validate_xml_tag(ele, XML_MAPPA)
        floor_lists = []
        for x_floor_list in ele:
            floor_list = []
            validate_xml_tag(x_floor_list, XML_FLOOR_LIST)
            for x_floor in x_floor_list:
                floor_list.append(MappaFloor.from_xml(x_floor))
            floor_lists.append(floor_list)
        return cls(floor_lists)

    def minimize(self) -> Tuple[
        List[List[StubMappaFloor]], List[MappaFloorLayout], List[List[MappaMonster]],
        List[MappaTrapList], List[MappaItemList]
    ]:
        """
        Collects a list of floors, that references indices in other lists, like stored in the mappa files.
        If two floors use the same exact data for something, they will be pointing to the same index in the lists,
        there are no duplicates.
        Returned are all lists.
        TODO: Performance could be improved here, by using more efficient lookup mechanisms.
        """
        floor_lists = []
        floor_layouts = []
        monster_lists = []
        trap_lists = []
        item_lists = []
        for floor_list in self.floor_lists:
            stub_floor_list = []
            for floor in floor_list:
                # Layout
                layout_idx = self._find_if_not_exists_insert(floor_layouts, floor.layout)
                # Monsters
                monsters_idx = self._find_if_not_exists_insert(monster_lists, floor.monsters)
                # Traps
                traps_idx = self._find_if_not_exists_insert(trap_lists, floor.traps)
                # Floor items
                floor_items_idx = self._find_if_not_exists_insert(item_lists, floor.floor_items)
                # Shop items
                shop_items_idx = self._find_if_not_exists_insert(item_lists, floor.shop_items)
                # Monster house items
                monster_house_items_idx = self._find_if_not_exists_insert(item_lists, floor.monster_house_items)
                # Buried items
                buried_items_idx = self._find_if_not_exists_insert(item_lists, floor.buried_items)
                # Unk items 1
                unk_items1_idx = self._find_if_not_exists_insert(item_lists, floor.unk_items1)
                # Unk items 2
                unk_items2_idx = self._find_if_not_exists_insert(item_lists, floor.unk_items2)

                stub_floor_list.append(StubMappaFloor(
                    layout_idx, monsters_idx, traps_idx, floor_items_idx, shop_items_idx,
                    monster_house_items_idx, buried_items_idx, unk_items1_idx, unk_items2_idx
                ))

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

    def __eq__(self, other):
        if not isinstance(other, MappaBin):
            return False
        return self.floor_lists == other.floor_lists
