#  Copyright 2020 Parakoopa
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
from skytemple_files.dungeon_data.mappa_bin.floor_layout import MappaFloorLayout
from skytemple_files.dungeon_data.mappa_bin.item_list import MappaItemList
from skytemple_files.dungeon_data.mappa_bin.monster_list import MappaMonsterList
from skytemple_files.dungeon_data.mappa_bin.trap_list import MappaTrapList

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin.model import MappaBinReadContainer


class MappaFloor:
    def __init__(
        self, layout: MappaFloorLayout, monsters: MappaMonsterList, traps: MappaTrapList, floor_items: MappaItemList,
        shop_items: MappaItemList, monster_house_items: MappaItemList, buried_items: MappaItemList,
        unk_items1: MappaItemList, unk_items2: MappaItemList
    ):
        self.id: int  # ID in dungeon
        self.layout: MappaFloorLayout = layout
        self.monsters: MappaMonsterList = monsters
        self.traps: MappaTrapList = traps
        self.floor_items: MappaItemList = floor_items
        self.shop_items: MappaItemList = shop_items
        self.monster_house_items: MappaItemList = monster_house_items
        self.buried_items: MappaItemList = buried_items
        self.unk_items1: MappaItemList = unk_items1
        self.unk_items2: MappaItemList = unk_items2

    @classmethod
    def from_mappa(cls, read: 'MappaBinReadContainer', floor_data: bytes) -> 'MappaFloor':
        return cls(
            MappaFloorLayout.from_mappa(
                read, cls._read_pointer(read.data, read.floor_layout_data_start, read_uintle(floor_data, 0x00, 2))
            ),
            MappaMonsterList.from_mappa(
                read, cls._read_pointer(read.data, read.monster_spawn_list_index_start, read_uintle(floor_data, 0x02, 2))
            ),
            MappaTrapList.from_mappa(
                read, cls._read_pointer(read.data, read.trap_spawn_list_index_start, read_uintle(floor_data, 0x04, 2))
            ),
            MappaItemList.from_mappa(
                read, cls._read_pointer(read.data, read.item_spawn_list_index_start, read_uintle(floor_data, 0x06, 2))
            ),
            MappaItemList.from_mappa(
                read, cls._read_pointer(read.data, read.item_spawn_list_index_start, read_uintle(floor_data, 0x08, 2))
            ),
            MappaItemList.from_mappa(
                read, cls._read_pointer(read.data, read.item_spawn_list_index_start, read_uintle(floor_data, 0x0A, 2))
            ),
            MappaItemList.from_mappa(
                read, cls._read_pointer(read.data, read.item_spawn_list_index_start, read_uintle(floor_data, 0x0C, 2))
            ),
            MappaItemList.from_mappa(
                read, cls._read_pointer(read.data, read.item_spawn_list_index_start, read_uintle(floor_data, 0x0E, 2))
            ),
            MappaItemList.from_mappa(
                read, cls._read_pointer(read.data, read.item_spawn_list_index_start, read_uintle(floor_data, 0x10, 2))
            )
        )

    @staticmethod
    def _read_pointer(data: bytes, start, index):
        print(index)
        return read_uintle(data, start + (4 * index))
