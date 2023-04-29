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

from typing import TYPE_CHECKING, List

from range_typed_integers import u16

from skytemple_files.common.i18n_util import _
from skytemple_files.common.util import (
    AutoString,
    read_u16,
    write_u16,
    read_u32,
)
from skytemple_files.dungeon_data.mappa_bin._python_impl.floor_layout import (
    MappaFloorLayout,
)
from skytemple_files.dungeon_data.mappa_bin._python_impl.item_list import MappaItemList
from skytemple_files.dungeon_data.mappa_bin._python_impl.monster import MappaMonster
from skytemple_files.dungeon_data.mappa_bin._python_impl.trap_list import MappaTrapList
from skytemple_files.dungeon_data.mappa_bin.protocol import (
    MappaFloorProtocol,
)

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin._python_impl.model import (
        MappaBinReadContainer,
    )


class StubMappaFloor:
    """A mappa floor that only referneces an index for all of it's data."""

    layout_idx: u16
    monsters_idx: u16
    traps_idx: u16
    floor_items_idx: u16
    shop_items_idx: u16
    monster_house_items_idx: u16
    buried_items_idx: u16
    unk_items1_idx: u16
    unk_items2_idx: u16

    def __init__(
        self,
        layout_idx: u16,
        monsters_idx: u16,
        traps_idx: u16,
        floor_items_idx: u16,
        shop_items_idx: u16,
        monster_house_items_idx: u16,
        buried_items_idx: u16,
        unk_items1_idx: u16,
        unk_items2_idx: u16,
    ):
        self.layout_idx = layout_idx
        self.monsters_idx = monsters_idx
        self.traps_idx = traps_idx
        self.floor_items_idx = floor_items_idx
        self.shop_items_idx = shop_items_idx
        self.monster_house_items_idx = monster_house_items_idx
        self.buried_items_idx = buried_items_idx
        self.unk_items1_idx = unk_items1_idx
        self.unk_items2_idx = unk_items2_idx

    def to_mappa(self) -> bytes:
        data = bytearray(18)
        write_u16(data, self.layout_idx, 0x00)
        write_u16(data, self.monsters_idx, 0x02)
        write_u16(data, self.traps_idx, 0x04)
        write_u16(data, self.floor_items_idx, 0x06)
        write_u16(data, self.shop_items_idx, 0x08)
        write_u16(data, self.monster_house_items_idx, 0x0A)
        write_u16(data, self.buried_items_idx, 0x0C)
        write_u16(data, self.unk_items1_idx, 0x0E)
        write_u16(data, self.unk_items2_idx, 0x10)
        if bytes(18) in data:
            raise ValueError(
                _(
                    "Could not save floor: It contains too much empty data.\nThis probably happened "
                    "because a lot of spawn lists are empty.\nPlease check the floors you edited and fill "
                    "them with more data. If you are using the randomizer, check your allowed item list."
                )
            )
        return data


class MappaFloor(
    MappaFloorProtocol[MappaFloorLayout, MappaMonster, MappaTrapList, MappaItemList],
    AutoString,
):
    def __init__(
        self,
        layout: MappaFloorLayout,
        monsters: List[MappaMonster],
        traps: MappaTrapList,
        floor_items: MappaItemList,
        shop_items: MappaItemList,
        monster_house_items: MappaItemList,
        buried_items: MappaItemList,
        unk_items1: MappaItemList,
        unk_items2: MappaItemList,
    ):
        self.layout: MappaFloorLayout = layout
        self.monsters: List[MappaMonster] = monsters
        self.traps: MappaTrapList = traps
        self.floor_items: MappaItemList = floor_items
        self.shop_items: MappaItemList = shop_items
        self.monster_house_items: MappaItemList = monster_house_items
        self.buried_items: MappaItemList = buried_items
        self.unk_items1: MappaItemList = unk_items1
        self.unk_items2: MappaItemList = unk_items2

    @classmethod
    def from_mappa(
        cls, read: "MappaBinReadContainer", floor_data: bytes
    ) -> "MappaFloor":
        return cls(
            cls._from_cache(
                read,
                read.floor_layout_data_start + 32 * read_u16(floor_data, 0x00),
                lambda pnt: MappaFloorLayout.from_mappa(read, pnt),
            ),
            cls._from_cache(
                read,
                cls._read_pointer(
                    read.data,
                    read.monster_spawn_list_index_start,
                    read_u16(floor_data, 0x02),
                ),
                lambda pnt: MappaMonster.list_from_mappa(read, pnt),
            ),
            cls._from_cache(
                read,
                cls._read_pointer(
                    read.data,
                    read.trap_spawn_list_index_start,
                    read_u16(floor_data, 0x04),
                ),
                lambda pnt: MappaTrapList.from_mappa(read, pnt),
            ),
            cls._from_cache(
                read,
                cls._read_pointer(
                    read.data,
                    read.item_spawn_list_index_start,
                    read_u16(floor_data, 0x06),
                ),
                lambda pnt: MappaItemList.from_mappa(read, pnt),
            ),
            cls._from_cache(
                read,
                cls._read_pointer(
                    read.data,
                    read.item_spawn_list_index_start,
                    read_u16(floor_data, 0x08),
                ),
                lambda pnt: MappaItemList.from_mappa(read, pnt),
            ),
            cls._from_cache(
                read,
                cls._read_pointer(
                    read.data,
                    read.item_spawn_list_index_start,
                    read_u16(floor_data, 0x0A),
                ),
                lambda pnt: MappaItemList.from_mappa(read, pnt),
            ),
            cls._from_cache(
                read,
                cls._read_pointer(
                    read.data,
                    read.item_spawn_list_index_start,
                    read_u16(floor_data, 0x0C),
                ),
                lambda pnt: MappaItemList.from_mappa(read, pnt),
            ),
            cls._from_cache(
                read,
                cls._read_pointer(
                    read.data,
                    read.item_spawn_list_index_start,
                    read_u16(floor_data, 0x0E),
                ),
                lambda pnt: MappaItemList.from_mappa(read, pnt),
            ),
            cls._from_cache(
                read,
                cls._read_pointer(
                    read.data,
                    read.item_spawn_list_index_start,
                    read_u16(floor_data, 0x10),
                ),
                lambda pnt: MappaItemList.from_mappa(read, pnt),
            ),
        )

    @staticmethod
    def _read_pointer(data: bytes, start, index):
        return read_u32(data, start + (4 * index))

    @staticmethod
    def _from_cache(read, pnt, load_callback):
        # TODO: Caching needs a deep copy
        return load_callback(pnt)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MappaFloor):
            return False
        return (
            self.floor_items == other.floor_items
            and self.layout == other.layout
            and self.traps == other.traps
            and self.monsters == other.monsters
            and self.buried_items == other.buried_items
            and self.monster_house_items == other.monster_house_items
            and self.shop_items == other.shop_items
            and self.unk_items1 == other.unk_items1
            and self.unk_items2 == other.unk_items2
        )
