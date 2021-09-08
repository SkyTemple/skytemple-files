#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
import random
from enum import Enum, auto
from typing import List, Optional, Union

from dungeon_eos.DungeonAlgorithm import Properties, StaticParam, ReturnData, DungeonData, generate_floor
from dungeon_eos.RandomGen import RandomGenerator
from skytemple_files.dungeon_data.mappa_bin.floor_layout import MappaFloorLayout
from skytemple_files.graphics.dma.model import DmaType


class RandomGenProperties:
    def __init__(self, gen_type, mul, count, seed_old_t0, seed_t0, add_t1, use_seed_t1, seeds_t1):
        self.gen_type = gen_type
        self.mul = mul
        self.count = count
        self.seed_old_t0 = seed_old_t0
        self.seed_t0 = seed_t0
        self.add_t1 = add_t1
        self.use_seed_t1 = use_seed_t1
        self.seeds_t1 = seeds_t1

    @classmethod
    def default(cls, rng: random.Random = None) -> 'RandomGenProperties':
        if rng is None:
            rng = random
        return cls(
            0,
            0x5d588b65,
            1,
            rng.randrange(1 << 32),
            rng.randrange(1 << 32),
            0x269ec3,
            4,
            [rng.randrange(1 << 32) for i in range(5)]
        )


class TileType(Enum):
    GENERIC = auto()
    PLAYER_SPAWN = auto()
    STAIRS = auto()
    ENEMY = auto()
    TRAP = auto()
    BURIED_ITEM = auto()
    ITEM = auto()


class RoomType(Enum):
    NORMAL = auto()
    MONSTER_HOUSE = auto()
    KECLEON_SHOP = auto()


class Tile:
    def __init__(self, terrain: DmaType, room_index: int, typ=TileType.GENERIC, room=RoomType.NORMAL):
        self.terrain = terrain
        self.room_index = room_index
        self.typ = typ
        self.room_type = room

    def __str__(self):
        if self.typ == TileType.PLAYER_SPAWN:
            return '!'
        if self.typ == TileType.STAIRS:
            return '>'
        if self.typ == TileType.ENEMY:
            return 'Ö'
        if self.typ == TileType.TRAP:
            return '+'
        if self.typ == TileType.BURIED_ITEM:
            return 'i'
        if self.typ == TileType.ITEM:
            return 'I'
        if self.terrain == DmaType.WALL:
            return 'X'
        if self.terrain == DmaType.WATER:
            return '~'
        if self.room_type == RoomType.KECLEON_SHOP:
            return 'K'
        if self.room_type == RoomType.MONSTER_HOUSE:
            return 'M'
        if self.room_index == 255:
            return ' '
        return str(self.room_index)


SIZE_X = 32
SIZE_Y = 56


class DungeonFloorGenerator:
    def __init__(self,
                 unknown_dungeon_chance_patch_applied=False, fix_dead_end_error=False, fix_outer_room_error=False,
                 gen_properties: RandomGenProperties=None
                 ):
        self.unknown_dungeon_chance_patch_applied = unknown_dungeon_chance_patch_applied
        self.fix_dead_end_error = fix_dead_end_error
        self.fix_outer_room_error = fix_outer_room_error
        self.gen_properties = gen_properties
        if self.gen_properties is None:
            self.gen_properties = RandomGenProperties.default()

    def generate(self, floor_layout: MappaFloorLayout, max_retries=1, flat=False) -> Union[List[List[Tile]], List[Tile], None]:
        """
        Returns a dungeon floor matrix (Tile matrix SIZE_Y x SIZE_X).
        Returns None if no valid floor could be generated after max_retries attempts.
        """
        RandomGenerator.gen_type = self.gen_properties.gen_type
        RandomGenerator.mul = self.gen_properties.mul
        RandomGenerator.count = self.gen_properties.count
        RandomGenerator.seed_old_t0 = self.gen_properties.seed_old_t0
        RandomGenerator.seed_t0 = self.gen_properties.seed_t0
        RandomGenerator.add_t1 = self.gen_properties.add_t1
        RandomGenerator.use_seed_t1 = self.gen_properties.use_seed_t1
        RandomGenerator.seeds_t1 = self.gen_properties.seeds_t1

        Properties.layout = floor_layout.structure.value
        Properties.mh_chance = floor_layout.monster_house_chance
        Properties.kecleon_chance = floor_layout.kecleon_shop_chance
        Properties.middle_room_secondary = floor_layout.secondary_terrain.value
        Properties.nb_rooms = floor_layout.room_density
        Properties.bit_flags = floor_layout.terrain_settings.to_mappa()
        Properties.floor_connectivity = floor_layout.floor_connectivity
        Properties.maze_chance = floor_layout.unusued_chance
        Properties.dead_end = int(floor_layout.dead_ends)
        Properties.extra_hallways = floor_layout.extra_hallway_density
        Properties.secondary_density = floor_layout.water_density
        Properties.enemy_density = floor_layout.initial_enemy_density
        Properties.item_density = floor_layout.item_density
        Properties.buried_item_density = floor_layout.buried_item_density
        Properties.trap_density = floor_layout.trap_density
        StaticParam.PATCH_APPLIED = int(self.unknown_dungeon_chance_patch_applied)
        StaticParam.FIX_DEAD_END_ERROR = int(self.fix_dead_end_error)
        StaticParam.FIX_OUTER_ROOM_ERROR = int(self.fix_outer_room_error)
        StaticParam.SHOW_ERROR = 0

        for x in range(max_retries):
            generate_floor()
            if ReturnData.invalid_generation:
                print("Unsafe generation parameters")
                break

        if ReturnData.invalid_generation:
            return None

        tiles_grid = []
        for y in range(32):
            if not flat:
                tiles_row = []
                tiles_grid.append(tiles_row)
            else:
                tiles_row = tiles_grid
            for x in range(56):
                terrain_idx = DungeonData.list_tiles[x][y].terrain_flags & 0x3
                if terrain_idx == 0:
                    dma_type = DmaType.WALL
                if terrain_idx == 1:
                    dma_type = DmaType.FLOOR
                if terrain_idx == 2:
                    dma_type = DmaType.WATER
                tile = Tile(dma_type, DungeonData.list_tiles[x][y].room_index)
                tiles_row.append(tile)
                if DungeonData.player_spawn_x == x and DungeonData.player_spawn_y == y:
                    tile.typ = TileType.PLAYER_SPAWN
                elif DungeonData.stairs_spawn_x == x and DungeonData.stairs_spawn_y == y:
                    tile.typ = TileType.STAIRS
                elif DungeonData.list_tiles[x][y].spawn_flags & 0x8:
                    tile.typ = TileType.ENEMY
                elif DungeonData.list_tiles[x][y].spawn_flags & 0x4:
                    tile.typ = TileType.TRAP
                elif DungeonData.list_tiles[x][y].spawn_flags & 0x2:
                    if DungeonData.list_tiles[x][y].terrain_flags & 0x3 == 0:
                        tile.typ = TileType.BURIED_ITEM
                    else:
                        tile.typ = TileType.ITEM

                if terrain_idx == 1:
                    if DungeonData.list_tiles[x][y].terrain_flags & 0x40:
                        tile.room_type = RoomType.MONSTER_HOUSE
                    elif DungeonData.list_tiles[x][y].terrain_flags & 0x20:
                        tile.room_type = RoomType.KECLEON_SHOP

        return tiles_grid
