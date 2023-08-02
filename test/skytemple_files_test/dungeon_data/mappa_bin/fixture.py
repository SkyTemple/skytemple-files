#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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

from typing import List, Dict, Union, Tuple, Optional, Sequence

from range_typed_integers import u16, u8, i8, i16, u32

from skytemple_files.common.util import AutoString
from skytemple_files.dungeon_data.mappa_bin.protocol import MappaTrapListProtocol, Probability, MappaMonsterProtocol, \
    MappaItemListProtocol, MappaFloorTerrainSettingsProtocol, MappaFloorLayoutProtocol, MappaFloorProtocol, \
    MappaBinProtocol, F


def eq_mappa_trap_list_protocol(one: MappaTrapListProtocol, two: MappaTrapListProtocol) -> bool:
    return one.weights == two.weights


class MappaTrapListStub(MappaTrapListProtocol, AutoString):
    weights: Dict[u8, u16]

    def __init__(self, weights: Union[List[u16], Dict[u8, u16]]):
        if isinstance(weights, list):
            if len(weights) != 25:
                raise ValueError(
                    "MappaTrapListStub constructor needs a weight value for all of the 25 traps."
                )
            self.weights = {}
            for i, value in enumerate(weights):
                self.weights[u8(i)] = value
        elif isinstance(weights, dict):
            self.weights = weights
            if set(self.weights.keys()) != set(range(0, 25)):
                raise ValueError(
                    "MappaTrapListStub constructor needs a weight value for all of the 25 traps."
                )
        else:
            raise ValueError(f"Invalid type for MappaTrapListStub {type(weights)}")

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()


def eq_mappa_monster_list_protocol(one: Sequence[MappaMonsterProtocol], two: Sequence[MappaMonsterProtocol]) -> bool:
    if len(one) != len(two):
        return False
    for x, y in zip(one, two):
        if not eq_mappa_monster_protocol(x, y):
            return False
    return True


def eq_mappa_monster_protocol(one: MappaMonsterProtocol, two: MappaMonsterProtocol) -> bool:
    return (
        one.level == two.level and
        one.main_spawn_weight == two.main_spawn_weight and
        one.monster_house_spawn_weight == two.monster_house_spawn_weight and
        one.md_index == two.md_index
    )


class MappaMonsterStub(MappaMonsterProtocol, AutoString):
    level: u8
    main_spawn_weight: u16
    monster_house_spawn_weight: u16
    md_index: u16

    def __init__(self, level: u8, main_spawn_weight: u16, monster_house_spawn_weight: u16, md_index: u16):
        self.level = level
        self.main_spawn_weight = main_spawn_weight
        self.monster_house_spawn_weight = monster_house_spawn_weight
        self.md_index = md_index

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()


def eq_mappa_item_list_protocol(one: MappaItemListProtocol, two: MappaItemListProtocol) -> bool:
    return (
        one.categories == two.categories and
        one.items == two.items
    )


class MappaItemListStub(MappaItemListProtocol, AutoString):
    categories: Dict[int, Probability]
    items: Dict[int, Probability]

    def __init__(
        self,
        categories: Dict[int, Probability],
        items: Dict[int, Probability],
    ):
        self.categories = categories
        self.items = items

    @classmethod
    def from_bytes(cls, data: bytes, pointer: int) -> MappaItemListProtocol:
        raise NotImplementedError()

    def to_bytes(self) -> bytes:
        raise NotImplementedError()

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()


def eq_mappa_floor_terrain_settings_protocol(one: MappaFloorTerrainSettingsProtocol, two: MappaFloorTerrainSettingsProtocol) -> bool:
    return (
        one.has_secondary_terrain == two.has_secondary_terrain and
        one.unk1 == two.unk1 and
        one.generate_imperfect_rooms == two.generate_imperfect_rooms and
        one.unk3 == two.unk3 and
        one.unk4 == two.unk4 and
        one.unk5 == two.unk5 and
        one.unk6 == two.unk6 and
        one.unk7 == two.unk7
    )


class MappaFloorTerrainSettingsStub(MappaFloorTerrainSettingsProtocol, AutoString):
    has_secondary_terrain: bool
    unk1: bool
    generate_imperfect_rooms: bool
    unk3: bool
    unk4: bool
    unk5: bool
    unk6: bool
    unk7: bool

    def __init__(
        self,
        has_secondary_terrain: bool,
        unk1: bool,
        generate_imperfect_rooms: bool,
        unk3: bool,
        unk4: bool,
        unk5: bool,
        unk6: bool,
        unk7: bool,
    ):
        self.unk7 = unk7
        self.unk6 = unk6
        self.unk5 = unk5
        self.unk4 = unk4
        self.unk3 = unk3
        self.generate_imperfect_rooms = generate_imperfect_rooms
        self.unk1 = unk1
        self.has_secondary_terrain = has_secondary_terrain

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()


def eq_mappa_floor_layout_protocol(one: MappaFloorLayoutProtocol, two: MappaFloorLayoutProtocol) -> bool:
    return (
        one.structure == two.structure and
        one.room_density == two.room_density and
        one.tileset_id == two.tileset_id and
        one.music_id == two.music_id and
        one.weather == two.weather and
        one.floor_connectivity == two.floor_connectivity and
        one.initial_enemy_density == two.initial_enemy_density and
        one.kecleon_shop_chance == two.kecleon_shop_chance and
        one.monster_house_chance == two.monster_house_chance and
        one.unused_chance == two.unused_chance and
        one.sticky_item_chance == two.sticky_item_chance and
        one.dead_ends == two.dead_ends and
        one.secondary_terrain == two.secondary_terrain and
        eq_mappa_floor_terrain_settings_protocol(one.terrain_settings, two.terrain_settings) and
        one.unk_e == two.unk_e and
        one.item_density == two.item_density and
        one.trap_density == two.trap_density and
        one.floor_number == two.floor_number and
        one.fixed_floor_id == two.fixed_floor_id and
        one.extra_hallway_density == two.extra_hallway_density and
        one.buried_item_density == two.buried_item_density and
        one.water_density == two.water_density and
        one.darkness_level == two.darkness_level and
        # Coin amounts don't need to be equal, but they do need to result in the same value
        # when converted to the raw value and back
        # (it's up to the implementors to decide how they want to store this information in the model)
        (one.max_coin_amount // 5 * 5) == (two.max_coin_amount // 5 * 5) and
        one.kecleon_shop_item_positions == two.kecleon_shop_item_positions and
        one.empty_monster_house_chance == two.empty_monster_house_chance and
        one.unk_hidden_stairs == two.unk_hidden_stairs and
        one.hidden_stairs_spawn_chance == two.hidden_stairs_spawn_chance and
        one.enemy_iq == two.enemy_iq and
        one.iq_booster_boost == two.iq_booster_boost
    )


class MappaFloorLayoutStub(MappaFloorLayoutProtocol, AutoString):
    structure: u8
    room_density: i8
    tileset_id: u8
    music_id: u8
    weather: u8
    floor_connectivity: u8
    initial_enemy_density: i8
    kecleon_shop_chance: u8
    monster_house_chance: u8
    unused_chance: u8
    sticky_item_chance: u8
    dead_ends: bool
    secondary_terrain: u8
    terrain_settings: MappaFloorTerrainSettingsStub
    unk_e: bool
    item_density: u8
    trap_density: u8
    floor_number: u8
    fixed_floor_id: u8
    extra_hallway_density: u8
    buried_item_density: u8
    water_density: u8
    darkness_level: u8
    max_coin_amount: int
    kecleon_shop_item_positions: u8
    empty_monster_house_chance: u8
    unk_hidden_stairs: u8
    hidden_stairs_spawn_chance: u8
    enemy_iq: u16
    iq_booster_boost: i16

    def __init__(
        self,
        structure: u8,
        room_density: i8,
        tileset_id: u8,
        music_id: u8,
        weather: u8,
        floor_connectivity: u8,
        initial_enemy_density: i8,
        kecleon_shop_chance: u8,
        monster_house_chance: u8,
        unused_chance: u8,
        sticky_item_chance: u8,
        dead_ends: bool,
        secondary_terrain: u8,
        terrain_settings: MappaFloorTerrainSettingsStub,
        unk_e: bool,
        item_density: u8,
        trap_density: u8,
        floor_number: u8,
        fixed_floor_id: u8,
        extra_hallway_density: u8,
        buried_item_density: u8,
        water_density: u8,
        darkness_level: u8,
        max_coin_amount: int,
        kecleon_shop_item_positions: u8,
        empty_monster_house_chance: u8,
        unk_hidden_stairs: u8,
        hidden_stairs_spawn_chance: u8,
        enemy_iq: u16,
        iq_booster_boost: i16,
    ):
        self.structure = structure
        self.room_density = room_density
        self.tileset_id = tileset_id
        self.music_id = music_id
        self.weather = weather
        self.floor_connectivity = floor_connectivity
        self.initial_enemy_density = initial_enemy_density
        self.kecleon_shop_chance = kecleon_shop_chance
        self.monster_house_chance = monster_house_chance
        self.unused_chance = unused_chance
        self.sticky_item_chance = sticky_item_chance
        self.dead_ends = dead_ends
        self.secondary_terrain = secondary_terrain
        self.terrain_settings = terrain_settings
        self.unk_e = unk_e
        self.item_density = item_density
        self.trap_density = trap_density
        self.floor_number = floor_number
        self.fixed_floor_id = fixed_floor_id
        self.extra_hallway_density = extra_hallway_density
        self.buried_item_density = buried_item_density
        self.water_density = water_density
        self.darkness_level = darkness_level
        self.max_coin_amount = max_coin_amount
        self.kecleon_shop_item_positions = kecleon_shop_item_positions
        self.empty_monster_house_chance = empty_monster_house_chance
        self.unk_hidden_stairs = unk_hidden_stairs
        self.hidden_stairs_spawn_chance = hidden_stairs_spawn_chance
        self.enemy_iq = enemy_iq
        self.iq_booster_boost = iq_booster_boost

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()


def eq_mappa_floor_protocol(one: MappaFloorProtocol, two: MappaFloorProtocol) -> bool:
    return (
        eq_mappa_floor_layout_protocol(one.layout, two.layout) and
        eq_mappa_monster_list_protocol(one.monsters, two.monsters) and
        eq_mappa_trap_list_protocol(one.traps, two.traps) and
        eq_mappa_item_list_protocol(one.floor_items, two.floor_items) and
        eq_mappa_item_list_protocol(one.shop_items, two.shop_items) and
        eq_mappa_item_list_protocol(one.monster_house_items, two.monster_house_items) and
        eq_mappa_item_list_protocol(one.buried_items, two.buried_items) and
        eq_mappa_item_list_protocol(one.unk_items1, two.unk_items1) and
        eq_mappa_item_list_protocol(one.unk_items2, two.unk_items2)
    )


class MappaFloorStub(MappaFloorProtocol, AutoString):
    layout: MappaFloorLayoutStub
    monsters: List[MappaMonsterStub]
    traps: MappaTrapListStub
    floor_items: MappaItemListStub
    shop_items: MappaItemListStub
    monster_house_items: MappaItemListStub
    buried_items: MappaItemListStub
    unk_items1: MappaItemListStub
    unk_items2: MappaItemListStub

    def __init__(
        self,
        layout: MappaFloorLayoutStub,
        monsters: List[MappaMonsterStub],
        traps: MappaTrapListStub,
        floor_items: MappaItemListStub,
        shop_items: MappaItemListStub,
        monster_house_items: MappaItemListStub,
        buried_items: MappaItemListStub,
        unk_items1: MappaItemListStub,
        unk_items2: MappaItemListStub,
    ):
        self.layout = layout
        self.monsters = monsters
        self.traps = traps
        self.floor_items = floor_items
        self.shop_items = shop_items
        self.monster_house_items = monster_house_items
        self.buried_items = buried_items
        self.unk_items1 = unk_items1
        self.unk_items2 = unk_items2

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()


def eq_mappa_protocol(one: MappaBinProtocol, two: MappaBinProtocol) -> bool:
    if len(one.floor_lists) != len(two.floor_lists):
        return False
    for x, y in zip(one.floor_lists, two.floor_lists):
        if len(x) != len(y):
            return False
        for xx, yy in zip(x, y):
            if not eq_mappa_floor_protocol(xx, yy):
                return False
    return True


class MappaBinStub(MappaBinProtocol, AutoString):
    floor_lists: List[List[MappaFloorStub]]

    def __init__(self, floor_lists: List[List[MappaFloorStub]]):
        ...

    def add_floor_list(self, floor_list: List[MappaFloorStub]):
        raise NotImplementedError()

    def remove_floor_list(self, index: int):
        raise NotImplementedError()

    def add_floor_to_floor_list(self, floor_list_index: int, floor: MappaFloorStub):
        raise NotImplementedError()

    def insert_floor_in_floor_list(self, floor_list_index: int, insert_index: int, floor: F):
        pass

    def remove_floor_from_floor_list(self, floor_list_index: int, floor_index: int):
        raise NotImplementedError()

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()
    
    def sir0_serialize_parts(self) -> Tuple[bytes, List[u32], Optional[u32]]:
        raise NotImplementedError()

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: u32) -> MappaBinStub:
        raise NotImplementedError()
