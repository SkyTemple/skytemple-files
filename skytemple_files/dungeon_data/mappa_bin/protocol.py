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

from abc import abstractmethod
from enum import Enum
from typing import (
    Protocol,
    TypeVar,
    Sequence,
    List,
    Optional,
    Dict,
    Union,
    MutableSequence,
)

from range_typed_integers import u16, u8, i16, i8

from skytemple_files.common.i18n_util import _
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable


CMD_SKIP = 0x7530
GUARANTEED = 0xFFFF
MAX_ITEM_ID = 363
MAX_CAT_IDS = 0xF
POKE_ID = 183
DUMMY_MD_INDEX = 0x229
LEVEL_MULTIPLIER = 512
# Actually GUARANTEED or a weight between 0 and MAX_WEIGHT.
Probability = int


_MappaFloorStructureType = u8
_MappaFloorWeather = u8
_MappaFloorDarknessLevel = u8
_MappaTrapType = u8
_MappaItemCategory = int
_MappaItem = int


class MappaFloorStructureType(Enum):
    MEDIUM_LARGE = 0, _("Medium Large")  # Max 6x4
    SMALL = 1, _("Small")  # Max 2x3
    SINGLE_MONSTER_HOUSE = 2, _("Single Monster House")
    RING = 3, _("Ring")  # Outer ring with 8 rooms inside in a 4 x 2 shape
    CROSSROADS = 4, _(
        "Crossroads"
    )  # Crossroads (3 rooms at the top, 3 at the bottom, 2 on each side)
    TWO_ROOMS_ONE_MH = 5, _(
        "Two Rooms, One Monster House"
    )  # Two rooms, one is a monster house
    LINE = 6, _("Line")  # 1 horizontal line with 5 rooms in a row
    CROSS = 7, _("Cross")  # 5 rooms: up, down, left, right, center
    SMALL_MEDIUM = 8, _("Small Medium")  # Max. 4x2
    BETTLE = 9, _("Beetle")  # 1 big room in the center with 3 a on each side
    OUTER_ROOMS = 10, _(
        "Outer Rooms"
    )  # All the rooms are in the map borders, none in the center (Max 6x4)
    MEDIUM = 11, _("Medium")  # Max 3x3
    MEDIUM_LARGE_12 = 12, _("Medium Large (12)")  # Max 6x4
    MEDIUM_LARGE_13 = 13, _("Medium Large (13)")  # Max 6x4
    MEDIUM_LARGE_14 = 14, _("Medium Large (14)")  # Max 6x4
    MEDIUM_LARGE_15 = 15, _("Medium Large (15)")  # Max 6x4

    @property
    def print_name(self):
        return self._print_name_

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, print_name: Optional[str] = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self):
        return self._print_name_

    def __repr__(self):
        return f"MappaFloorStructureType.{self.name}"


class MappaFloorWeather(Enum):
    CLEAR = 0, _("Clear")
    SUNNY = 1, _("Sunny")
    SANDSTORM = 2, _("Sandstorm")
    CLOUDY = 3, _("Cloudy")
    RAINY = 4, _("Rainy")
    HAIL = 5, _("Hail")
    FOG = 6, _("Fog")
    SNOW = 7, _("Snow")
    RANDOM = 8, _("Random")

    @property
    def print_name(self):
        return self._print_name_

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, print_name: Optional[str] = None):
        self._print_name_ = print_name

    def __str__(self):
        return self._print_name_

    def __repr__(self):
        return f"MappaFloorWeather.{self.name}"


class MappaFloorDarknessLevel(Enum):
    NO_DARKNESS = 0, _("No darkness")
    HEAVY_DARKNESS = 1, _("1-tile vision (Heavy darkness)")
    LIGHT_DARKNESS = 2, _("2-tile vision (Light darkness)")
    THREE_TILE = 3, _("3-tile vision")
    FOUR_TILE = 4, _("4-tile vision")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, print_name: Optional[str] = None):
        self._print_name_ = print_name

    def __str__(self):
        return self._print_name_

    def __repr__(self):
        return f"MappaFloorDarknessLevel.{self.name}"

    @property
    def print_name(self):
        return self._print_name_


class MappaTrapType(Enum):
    UNUSED = 0, _("Unused")
    MUD_TRAP = 1, _("Mud Trap")
    STICKY_TRAP = 2, _("Sticky Trap")
    GRIMY_TRAP = 3, _("Grimy Trap")
    SUMMON_TRAP = 4, _("Summon Trap")
    PITFALL_TRAP = 5, _("Pitfall Trap")
    WARP_TRAP = 6, _("Warp Trap")
    GUST_TRAP = 7, _("Gust Trap")
    SPIN_TRAP = 8, _("Spin Trap")
    SLUMBER_TRAP = 9, _("Slumber Trap")
    SLOW_TRAP = 10, _("Slow Trap")
    SEAL_TRAP = 11, _("Seal Trap")
    POISON_TRAP = 12, _("Poison Trap")
    SELFDESTRUCT_TRAP = 13, _("Selfdestruct Trap")
    EXPLOSION_TRAP = 14, _("Explosion Trap")
    PP_ZERO_TRAP = 15, _("Pp Zero Trap")
    CHESTNUT_TRAP = 16, _("Chestnut Trap")
    WONDER_TILE = 17, _("Wonder Tile")
    POKEMON_TRAP = 18, _("Pokemon Trap")
    SPIKED_TILE = 19, _("Spiked Tile")
    STEALTH_ROCK = 20, _("Stealth Rock")
    TOXIC_SPIKES = 21, _("Toxic Spikes")
    TRIP_TRAP = 22, _("Trip Trap")
    RANDOM_TRAP = 23, _("Random Trap")
    GRUDGE_TRAP = 24, _("Grudge Trap")

    @property
    def print_name(self):
        return self._print_name_

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, print_name: Optional[str] = None):
        self._print_name_ = print_name

    def __str__(self):
        return self._print_name_

    def __repr__(self):
        return f"MappaTrapType.{self.name}"


class MappaTrapListProtocol(Protocol):
    weights: Dict[_MappaTrapType, u16]

    @abstractmethod
    def __init__(self, weights: Union[List[u16], Dict[_MappaTrapType, u16]]):
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...


class MappaMonsterProtocol(Protocol):
    level: u8
    main_spawn_weight: u16
    monster_house_spawn_weight: u16
    md_index: u16

    @abstractmethod
    def __init__(
        self,
        level: u8,
        main_spawn_weight: u16,
        monster_house_spawn_weight: u16,
        md_index: u16,
    ):
        self.level = level
        self.main_spawn_weight = main_spawn_weight
        self.monster_house_spawn_weight = monster_house_spawn_weight
        self.md_index = md_index

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...


class MappaItemListProtocol(Protocol):
    categories: Dict[_MappaItemCategory, Probability]
    items: Dict[_MappaItem, Probability]

    @abstractmethod
    def __init__(
        self,
        categories: Dict[_MappaItemCategory, Probability],
        items: Dict[_MappaItem, Probability],
    ):
        ...

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes, pointer: int) -> MappaItemListProtocol:
        ...

    @abstractmethod
    def to_bytes(self) -> bytes:
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...


class MappaFloorTerrainSettingsProtocol(Protocol):
    has_secondary_terrain: bool
    unk1: bool
    generate_imperfect_rooms: bool
    unk3: bool
    unk4: bool
    unk5: bool
    unk6: bool
    unk7: bool

    @abstractmethod
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
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...


TS = TypeVar("TS", bound=MappaFloorTerrainSettingsProtocol)


class MappaFloorLayoutProtocol(Protocol[TS]):
    structure: _MappaFloorStructureType
    room_density: i8
    tileset_id: u8
    music_id: u8
    weather: _MappaFloorWeather
    floor_connectivity: u8
    initial_enemy_density: i8
    kecleon_shop_chance: u8
    monster_house_chance: u8
    unused_chance: u8
    sticky_item_chance: u8
    dead_ends: bool
    secondary_terrain: u8
    terrain_settings: TS
    unk_e: bool
    item_density: u8
    trap_density: u8
    floor_number: u8
    fixed_floor_id: u8
    extra_hallway_density: u8
    buried_item_density: u8
    water_density: u8
    darkness_level: _MappaFloorDarknessLevel
    max_coin_amount: int
    kecleon_shop_item_positions: u8
    empty_monster_house_chance: u8
    unk_hidden_stairs: u8
    hidden_stairs_spawn_chance: u8
    enemy_iq: u16
    iq_booster_boost: i16

    @abstractmethod
    def __init__(
        self,
        structure: _MappaFloorStructureType,
        room_density: i8,
        tileset_id: u8,
        music_id: u8,
        weather: _MappaFloorWeather,
        floor_connectivity: u8,
        initial_enemy_density: i8,
        kecleon_shop_chance: u8,
        monster_house_chance: u8,
        unused_chance: u8,
        sticky_item_chance: u8,
        dead_ends: bool,
        secondary_terrain: u8,
        terrain_settings: TS,
        unk_e: bool,
        item_density: u8,
        trap_density: u8,
        floor_number: u8,
        fixed_floor_id: u8,
        extra_hallway_density: u8,
        buried_item_density: u8,
        water_density: u8,
        darkness_level: _MappaFloorDarknessLevel,
        max_coin_amount: int,
        kecleon_shop_item_positions: u8,
        empty_monster_house_chance: u8,
        unk_hidden_stairs: u8,
        hidden_stairs_spawn_chance: u8,
        enemy_iq: u16,
        iq_booster_boost: i16,
    ):
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...


L = TypeVar("L", bound=MappaFloorLayoutProtocol)
M = TypeVar("M", bound=MappaMonsterProtocol)
TL = TypeVar("TL", bound=MappaTrapListProtocol)
IL = TypeVar("IL", bound=MappaItemListProtocol)


class MappaFloorProtocol(Protocol[L, M, TL, IL]):
    layout: L
    monsters: MutableSequence[M]
    traps: TL
    floor_items: IL
    shop_items: IL
    monster_house_items: IL
    buried_items: IL
    unk_items1: IL
    unk_items2: IL

    @classmethod
    @abstractmethod
    def __init__(
        self,
        layout: L,
        monsters: List[M],
        traps: TL,
        floor_items: IL,
        shop_items: IL,
        monster_house_items: IL,
        buried_items: IL,
        unk_items1: IL,
        unk_items2: IL,
    ):
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...


F = TypeVar("F", bound=MappaFloorProtocol)


class MappaBinProtocol(Sir0Serializable, Protocol[F]):
    floor_lists: Sequence[Sequence[F]]

    @abstractmethod
    def __init__(self, floor_lists: List[List[F]]):
        ...

    @abstractmethod
    def add_floor_list(self, floor_list: List[F]):
        ...

    @abstractmethod
    def remove_floor_list(self, index: int):
        ...

    @abstractmethod
    def add_floor_to_floor_list(self, floor_list_index: int, floor: F):
        ...

    @abstractmethod
    def insert_floor_in_floor_list(
        self, floor_list_index: int, insert_index: int, floor: F
    ):
        ...

    @abstractmethod
    def remove_floor_from_floor_list(self, floor_list_index: int, floor_index: int):
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...
