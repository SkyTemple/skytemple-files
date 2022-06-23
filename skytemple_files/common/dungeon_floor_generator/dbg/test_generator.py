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
# mypy: ignore-errors
from __future__ import annotations

from random import choice, randrange

from skytemple_files.common.dungeon_floor_generator.generator import (
    DungeonFloorGenerator,
)
from skytemple_files.dungeon_data.mappa_bin.floor_layout import (
    MappaFloorDarknessLevel,
    MappaFloorLayout,
    MappaFloorStructureType,
    MappaFloorTerrainSettings,
    MappaFloorWeather,
)

layout = MappaFloorLayout(
    structure=MappaFloorStructureType.MEDIUM_LARGE,
    room_density=randrange(3, 21),
    tileset_id=65,
    music_id=99,  # Sky Peak Forest
    weather=MappaFloorWeather.CLEAR,
    floor_connectivity=randrange(5, 51),
    initial_enemy_density=randrange(1, 4),
    kecleon_shop_chance=randrange(0, 101),
    monster_house_chance=randrange(0, 41),
    unusued_chance=randrange(0, 101),
    sticky_item_chance=15,
    dead_ends=True,
    secondary_terrain=choice([1, 10, 0]),
    terrain_settings=MappaFloorTerrainSettings(
        True, False, True, False, False, False, False, False
    ),
    unk_e=choice((True, False)),
    item_density=randrange(0, 11),
    trap_density=randrange(0, 16),
    floor_number=0,
    fixed_floor_id=0,
    extra_hallway_density=randrange(0, 36),
    buried_item_density=randrange(0, 11),
    water_density=randrange(11, 41),
    darkness_level=choice(list(MappaFloorDarknessLevel)),
    max_coin_amount=randrange(0, 181) * 5,
    kecleon_shop_item_positions=randrange(0, 14),
    empty_monster_house_chance=randrange(0, 101),
    unk_hidden_stairs=choice((0, 255)),
    hidden_stairs_spawn_chance=randrange(0, 101),
    enemy_iq=randrange(1, 601),
    iq_booster_allowed=choice((True, False)),
)

tiles = DungeonFloorGenerator(unknown_dungeon_chance_patch_applied=True).generate(
    layout
)

for y in tiles:
    for c in y:
        print(str(c), end="")
    print()
