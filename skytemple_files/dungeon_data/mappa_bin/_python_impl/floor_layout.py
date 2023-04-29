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

from typing import TYPE_CHECKING

from range_typed_integers import u8, i8, u16, i16

from skytemple_files.common.util import (
    AutoString,
    write_i8,
    read_u8,
    read_u16,
    generate_bitfield,
    read_i16,
    write_u16,
    write_i16,
    write_u8,
    read_i8,
)
from skytemple_files.dungeon_data.mappa_bin.protocol import (
    _MappaFloorWeather,
    _MappaFloorDarknessLevel,
    _MappaFloorStructureType,
    MappaFloorTerrainSettingsProtocol,
    MappaFloorLayoutProtocol,
)

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin._python_impl.model import (
        MappaBinReadContainer,
    )


class MappaFloorTerrainSettings(MappaFloorTerrainSettingsProtocol, AutoString):
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MappaFloorTerrainSettings):
            return False
        return (
            self.has_secondary_terrain == other.has_secondary_terrain
            and self.unk1 == other.unk1
            and self.generate_imperfect_rooms == other.generate_imperfect_rooms
            and self.unk3 == other.unk3
            and self.unk4 == other.unk4
            and self.unk5 == other.unk5
            and self.unk6 == other.unk6
            and self.unk7 == other.unk7
        )

    def to_mappa(self):
        return u8(
            generate_bitfield(
                (
                    self.unk7,
                    self.unk6,
                    self.unk5,
                    self.unk4,
                    self.unk3,
                    self.generate_imperfect_rooms,
                    self.unk1,
                    self.has_secondary_terrain,
                )
            )
        )


class MappaFloorLayout(MappaFloorLayoutProtocol[MappaFloorTerrainSettings], AutoString):
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
    terrain_settings: MappaFloorTerrainSettings
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
        terrain_settings: MappaFloorTerrainSettings,
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
        # If <=0: Disabled
        self.iq_booster_boost = iq_booster_boost

    @classmethod
    def from_mappa(cls, read: "MappaBinReadContainer", pointer: int):
        terrain_settings_bitflag = read_u8(read.data, pointer + 0x0D)
        terrain_settings = MappaFloorTerrainSettings(
            *(bool(terrain_settings_bitflag >> i & 1) for i in range(8))
        )
        return cls(
            structure=read_u8(read.data, pointer + 0x00),
            room_density=read_i8(read.data, pointer + 0x01),
            tileset_id=read_u8(read.data, pointer + 0x02),
            music_id=read_u8(read.data, pointer + 0x03),
            weather=read_u8(read.data, pointer + 0x04),
            floor_connectivity=read_u8(read.data, pointer + 0x05),
            initial_enemy_density=read_i8(read.data, pointer + 0x06),
            kecleon_shop_chance=read_u8(read.data, pointer + 0x07),
            monster_house_chance=read_u8(read.data, pointer + 0x08),
            unused_chance=read_u8(read.data, pointer + 0x09),
            sticky_item_chance=read_u8(read.data, pointer + 0x0A),
            dead_ends=bool(read_u8(read.data, pointer + 0x0B)),
            secondary_terrain=read_u8(read.data, pointer + 0x0C),
            terrain_settings=terrain_settings,
            unk_e=bool(read_u8(read.data, pointer + 0x0E)),
            item_density=read_u8(read.data, pointer + 0x0F),
            trap_density=read_u8(read.data, pointer + 0x10),
            floor_number=read_u8(read.data, pointer + 0x11),
            fixed_floor_id=read_u8(read.data, pointer + 0x12),
            extra_hallway_density=read_u8(read.data, pointer + 0x13),
            buried_item_density=read_u8(read.data, pointer + 0x14),
            water_density=read_u8(read.data, pointer + 0x15),
            darkness_level=read_u8(read.data, pointer + 0x16),
            max_coin_amount=read_u8(read.data, pointer + 0x17) * 5,
            kecleon_shop_item_positions=read_u8(read.data, pointer + 0x18),
            empty_monster_house_chance=read_u8(read.data, pointer + 0x19),
            unk_hidden_stairs=read_u8(read.data, pointer + 0x1A),
            hidden_stairs_spawn_chance=read_u8(read.data, pointer + 0x1B),
            enemy_iq=read_u16(read.data, pointer + 0x1C),
            iq_booster_boost=read_i16(read.data, pointer + 0x1E),
        )

    def to_mappa(self) -> bytes:
        data = bytearray(32)
        write_u8(data, self.structure, 0x00)
        write_i8(data, self.room_density, 0x01)
        write_u8(data, self.tileset_id, 0x02)
        write_u8(data, self.music_id, 0x03)
        write_u8(data, self.weather, 0x04)
        write_u8(data, self.floor_connectivity, 0x05)
        write_i8(data, self.initial_enemy_density, 0x06)
        write_u8(data, self.kecleon_shop_chance, 0x07)
        write_u8(data, self.monster_house_chance, 0x08)
        write_u8(data, self.unused_chance, 0x09)
        write_u8(data, self.sticky_item_chance, 0x0A)
        write_u8(data, u8(int(self.dead_ends)), 0x0B)
        write_u8(data, self.secondary_terrain, 0x0C)
        write_u8(data, self.terrain_settings.to_mappa(), 0x0D)
        write_u8(data, u8(int(self.unk_e)), 0x0E)
        write_u8(data, self.item_density, 0x0F)
        write_u8(data, self.trap_density, 0x10)
        write_u8(data, self.floor_number, 0x11)
        write_u8(data, self.fixed_floor_id, 0x12)
        write_u8(data, self.extra_hallway_density, 0x13)
        write_u8(data, self.buried_item_density, 0x14)
        write_u8(data, self.water_density, 0x15)
        write_u8(data, self.darkness_level, 0x16)
        write_u8(data, u8(self.max_coin_amount // 5), 0x17)
        write_u8(data, self.kecleon_shop_item_positions, 0x18)
        write_u8(data, self.empty_monster_house_chance, 0x19)
        write_u8(data, self.unk_hidden_stairs, 0x1A)
        write_u8(data, self.hidden_stairs_spawn_chance, 0x1B)
        write_u16(data, self.enemy_iq, 0x1C)
        write_i16(data, self.iq_booster_boost, 0x1E)

        return data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MappaFloorLayout):
            return False
        return (
            self.structure == other.structure
            and self.room_density == other.room_density
            and self.tileset_id == other.tileset_id
            and self.music_id == other.music_id
            and self.weather == other.weather
            and self.floor_connectivity == other.floor_connectivity
            and self.initial_enemy_density == other.initial_enemy_density
            and self.kecleon_shop_chance == other.kecleon_shop_chance
            and self.monster_house_chance == other.monster_house_chance
            and self.unused_chance == other.unused_chance
            and self.sticky_item_chance == other.sticky_item_chance
            and self.dead_ends == other.dead_ends
            and self.secondary_terrain == other.secondary_terrain
            and self.terrain_settings == other.terrain_settings
            and self.unk_e == other.unk_e
            and self.item_density == other.item_density
            and self.trap_density == other.trap_density
            and self.floor_number == other.floor_number
            and self.fixed_floor_id == other.fixed_floor_id
            and self.extra_hallway_density == other.extra_hallway_density
            and self.buried_item_density == other.buried_item_density
            and self.water_density == other.water_density
            and self.darkness_level == other.darkness_level
            and self.max_coin_amount == other.max_coin_amount
            and self.kecleon_shop_item_positions == other.kecleon_shop_item_positions
            and self.empty_monster_house_chance == other.empty_monster_house_chance
            and self.unk_hidden_stairs == other.unk_hidden_stairs
            and self.hidden_stairs_spawn_chance == other.hidden_stairs_spawn_chance
            and self.enemy_iq == other.enemy_iq
            and self.iq_booster_boost == other.iq_booster_boost
        )
