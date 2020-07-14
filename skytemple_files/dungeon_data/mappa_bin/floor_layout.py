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
from enum import Enum
from typing import TYPE_CHECKING

from skytemple_files.common.util import read_uintle

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin.model import MappaBinReadContainer


class MappaFloorStructureType(Enum):
    MEDIUM_LARGE = 0  # Max 6x4
    SMALL = 1  # Max 2x3
    SINGLE_MONSTER_HOUSE = 2
    RING = 3  # Outer ring with 8 rooms inside in a 4 x 2 shape
    CROSSROADS = 4  # Crossroads (3 rooms at the top, 3 at the bottom, 2 on each side)
    TWO_ROOMS_ONE_MH = 5  # Two rooms, one is a monster house
    LINE = 6  # 1 horizontal line with 5 rooms in a row
    CROSS = 7  # 5 rooms: up, down, left, right, center
    SMALL_MEDIUM = 8  # Max. 4x2
    BETTLE = 9  # 1 big room in the center with 3 a on each side
    OUTER_ROOMS = 10  # All the rooms are in the map borders, none in the center (Max 6x4)
    MEDIUM = 11  # Max 3x3
    MEDIUM_LARGE_12 = 12  # Max 6x4
    MEDIUM_LARGE_13 = 13  # Max 6x4
    MEDIUM_LARGE_14 = 14  # Max 6x4
    MEDIUM_LARGE_15 = 15  # Max 6x4


class MappaFloorWeather(Enum):
    CLEAR = 0
    SUNNY = 1
    SANDSTORM = 2
    CLOUDY = 3
    RAINY = 4
    HAIL = 5
    FOG = 6
    SNOW = 7
    RANDOM = 8


class MappaFloorSecondaryTerrainType(Enum):
    NONE = 0
    WATER = 1
    LAVA = 10  # TODO: Check


class MappaFloorTerrainSettings:
    def __init__(
            self, has_secondary_terrain: bool, unk1: bool, generate_imperfect_rooms: bool,
            unk3: bool, unk4: bool, unk5: bool, unk6: bool, unk7: bool
    ):
        self.has_secondary_terrain = has_secondary_terrain
        # Seems unused.
        self.unk1 = unk1
        self.generate_imperfect_rooms = generate_imperfect_rooms
        # These bits might just be fully unused.
        self.unk3 = unk3
        self.unk4 = unk4
        self.unk5 = unk5
        self.unk6 = unk6
        self.unk7 = unk7


class MappaFloorDarknessLevel(Enum):
    NO_DARKNESS = 0
    LIGHT_DARKNESS = 1
    HEAVY_DARKNESS = 2


class MappaFloorLayout:
    def __init__(
            self, *, structure: MappaFloorStructureType, room_density: int, tileset_id: int, music_id: int,
            weather: MappaFloorWeather, floor_connectivity: int, initial_enemy_density: int, kecleon_shop_chance: int,
            monster_house_chance: int, unusued_chance: int, sticky_item_chance: int, dead_ends: bool,
            secondary_terrain: MappaFloorSecondaryTerrainType, terrain_settings: MappaFloorTerrainSettings,
            unk_e: bool, item_density: int, trap_density: int, floor_number: int, fixed_floor_id: int,
            extra_hallway_density: int, buried_item_density: int, water_density: int,
            darkness_level: MappaFloorDarknessLevel, max_coin_amount: int, kecleon_shop_item_positions: int,
            empty_monster_house_chance: int, unk_hidden_stairs: int, hidden_stairs_spawn_chance: int, enemy_iq: int,
            iq_booster_allowed: bool
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
        self.unusued_chance = unusued_chance
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
        self.iq_booster_allowed = iq_booster_allowed

    @classmethod
    def from_mappa(cls, read: 'MappaBinReadContainer', pointer: int):
        terrain_settings_bitflag = read_uintle(read.data, pointer + 0x0D)
        terrain_settings = MappaFloorTerrainSettings(
            *(bool(terrain_settings_bitflag >> i & 1) for i in range(8))
        )
        return cls(
            structure=MappaFloorStructureType(read_uintle(read.data, pointer + 0x00)),
            room_density=read_uintle(read.data, pointer + 0x01),
            tileset_id=read_uintle(read.data, pointer + 0x02),
            music_id=read_uintle(read.data, pointer + 0x03),
            weather=MappaFloorWeather(read_uintle(read.data, pointer + 0x04)),
            floor_connectivity=read_uintle(read.data, pointer + 0x05),
            initial_enemy_density=read_uintle(read.data, pointer + 0x06),
            kecleon_shop_chance=read_uintle(read.data, pointer + 0x07),
            monster_house_chance=read_uintle(read.data, pointer + 0x08),
            unusued_chance=read_uintle(read.data, pointer + 0x09),
            sticky_item_chance=read_uintle(read.data, pointer + 0x0A),
            dead_ends=bool(read_uintle(read.data, pointer + 0x0B)),
            secondary_terrain=MappaFloorSecondaryTerrainType(read_uintle(read.data, pointer + 0x0C)),
            terrain_settings=terrain_settings,
            unk_e=bool(read_uintle(read.data, pointer + 0x0E)),
            item_density=read_uintle(read.data, pointer + 0x0F),
            trap_density=read_uintle(read.data, pointer + 0x10),
            floor_number=read_uintle(read.data, pointer + 0x11),
            fixed_floor_id=read_uintle(read.data, pointer + 0x12),
            extra_hallway_density=read_uintle(read.data, pointer + 0x13),
            buried_item_density=read_uintle(read.data, pointer + 0x14),
            water_density=read_uintle(read.data, pointer + 0x15),
            darkness_level=MappaFloorDarknessLevel(read_uintle(read.data, pointer + 0x16)),
            max_coin_amount=read_uintle(read.data, pointer + 0x17),
            kecleon_shop_item_positions=read_uintle(read.data, pointer + 0x18),
            empty_monster_house_chance=read_uintle(read.data, pointer + 0x19),
            unk_hidden_stairs=read_uintle(read.data, pointer + 0x1A),
            hidden_stairs_spawn_chance=read_uintle(read.data, pointer + 0x1B),
            enemy_iq=read_uintle(read.data, pointer + 0x1C, 2),
            iq_booster_allowed=bool(read_uintle(read.data, pointer + 0x1E))
        )
