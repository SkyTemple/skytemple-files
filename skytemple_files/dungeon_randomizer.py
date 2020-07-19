#!/usr/bin/env python3
"""
This is a sample Python CLI script that uses SkyTemple Files to randomize data on dungeon floors.

Currently there are no settings. To run:

$ python3 dungeon_randomizer.py input_rom_name.nds output_rom_name.nds

It randomizes almost everything. Pokémon levels are randomized in a range of +/-3 of the normal min/max level Pokémon
on that floor.

This is also an example on how to use the following file handlers:
- MAPPA_BIN
"""
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
import argparse
import os
import statistics
from decimal import Decimal
from random import randrange, choice
from typing import List

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.dungeon_data import Pmd2DungeonItem
from skytemple_files.common.types.file_types import FileType
from skytemple_files.dungeon_data.mappa_bin.floor import MappaFloor
from skytemple_files.dungeon_data.mappa_bin.floor_layout import MappaFloorLayout, MappaFloorStructureType, \
    MappaFloorSecondaryTerrainType, MappaFloorWeather, MappaFloorTerrainSettings, MappaFloorDarknessLevel
from skytemple_files.dungeon_data.mappa_bin.item_list import MappaItemCategory, MappaItemList
from skytemple_files.dungeon_data.mappa_bin.model import MappaBin
from skytemple_files.dungeon_data.mappa_bin.monster import MappaMonster, DUMMY_MD_INDEX
from skytemple_files.dungeon_data.mappa_bin.trap_list import MappaTrapList

SECONDARY_TERRAIN_TILESET_MAP = {
    0: MappaFloorSecondaryTerrainType.WATER,
    1: MappaFloorSecondaryTerrainType.WATER,
    170: MappaFloorSecondaryTerrainType.WATER,
    2: MappaFloorSecondaryTerrainType.WATER,
    3: MappaFloorSecondaryTerrainType.WATER,
    171: MappaFloorSecondaryTerrainType.WATER,
    4: MappaFloorSecondaryTerrainType.WATER,
    5: MappaFloorSecondaryTerrainType.WATER,
    6: MappaFloorSecondaryTerrainType.WATER,
    7: MappaFloorSecondaryTerrainType.WATER,
    8: MappaFloorSecondaryTerrainType.WATER,
    9: MappaFloorSecondaryTerrainType.WATER,
    10: MappaFloorSecondaryTerrainType.WATER,
    11: MappaFloorSecondaryTerrainType.WATER,
    12: MappaFloorSecondaryTerrainType.WATER,
    172: MappaFloorSecondaryTerrainType.WATER,
    14: MappaFloorSecondaryTerrainType.WATER,
    15: MappaFloorSecondaryTerrainType.WATER,
    173: MappaFloorSecondaryTerrainType.WATER,
    17: MappaFloorSecondaryTerrainType.LAVA,
    18: MappaFloorSecondaryTerrainType.WATER,
    19: MappaFloorSecondaryTerrainType.WATER,
    20: MappaFloorSecondaryTerrainType.WATER,
    174: MappaFloorSecondaryTerrainType.WATER,
    22: MappaFloorSecondaryTerrainType.WATER,
    23: MappaFloorSecondaryTerrainType.WATER,
    24: MappaFloorSecondaryTerrainType.WATER,
    175: MappaFloorSecondaryTerrainType.WATER,
    26: MappaFloorSecondaryTerrainType.WATER,
    27: MappaFloorSecondaryTerrainType.WATER,
    28: MappaFloorSecondaryTerrainType.WATER,
    29: MappaFloorSecondaryTerrainType.WATER,
    30: MappaFloorSecondaryTerrainType.WATER,
    31: MappaFloorSecondaryTerrainType.WATER,
    176: MappaFloorSecondaryTerrainType.WATER,
    33: MappaFloorSecondaryTerrainType.WATER,
    34: MappaFloorSecondaryTerrainType.WATER,
    35: MappaFloorSecondaryTerrainType.WATER,
    36: MappaFloorSecondaryTerrainType.WATER,
    37: MappaFloorSecondaryTerrainType.WATER,
    38: MappaFloorSecondaryTerrainType.WATER,
    39: MappaFloorSecondaryTerrainType.WATER,
    40: MappaFloorSecondaryTerrainType.VOID,
    177: MappaFloorSecondaryTerrainType.WATER,
    42: MappaFloorSecondaryTerrainType.WATER,
    43: MappaFloorSecondaryTerrainType.WATER,
    178: MappaFloorSecondaryTerrainType.WATER,
    45: MappaFloorSecondaryTerrainType.WATER,
    46: MappaFloorSecondaryTerrainType.WATER,
    179: MappaFloorSecondaryTerrainType.WATER,
    48: MappaFloorSecondaryTerrainType.WATER,
    180: MappaFloorSecondaryTerrainType.WATER,
    113: MappaFloorSecondaryTerrainType.WATER,
    119: MappaFloorSecondaryTerrainType.WATER,
    106: MappaFloorSecondaryTerrainType.WATER,
    118: MappaFloorSecondaryTerrainType.VOID,
    51: MappaFloorSecondaryTerrainType.WATER,
    52: MappaFloorSecondaryTerrainType.WATER,
    50: MappaFloorSecondaryTerrainType.WATER,
    108: MappaFloorSecondaryTerrainType.WATER,
    62: MappaFloorSecondaryTerrainType.WATER,
    61: MappaFloorSecondaryTerrainType.WATER,
    91: MappaFloorSecondaryTerrainType.WATER,
    96: MappaFloorSecondaryTerrainType.WATER,
    103: MappaFloorSecondaryTerrainType.WATER,
    88: MappaFloorSecondaryTerrainType.WATER,
    85: MappaFloorSecondaryTerrainType.WATER,
    82: MappaFloorSecondaryTerrainType.WATER,
    111: MappaFloorSecondaryTerrainType.VOID,
    123: MappaFloorSecondaryTerrainType.WATER,
    125: MappaFloorSecondaryTerrainType.WATER,
    59: MappaFloorSecondaryTerrainType.WATER,
    90: MappaFloorSecondaryTerrainType.WATER,
    65: MappaFloorSecondaryTerrainType.WATER,
    102: MappaFloorSecondaryTerrainType.WATER,
    105: MappaFloorSecondaryTerrainType.WATER,
    99: MappaFloorSecondaryTerrainType.WATER,
    126: MappaFloorSecondaryTerrainType.WATER,
    49: MappaFloorSecondaryTerrainType.WATER,
    127: MappaFloorSecondaryTerrainType.LAVA,
    181: MappaFloorSecondaryTerrainType.WATER,
    69: MappaFloorSecondaryTerrainType.WATER,
    109: MappaFloorSecondaryTerrainType.WATER,
    74: MappaFloorSecondaryTerrainType.WATER,
    101: MappaFloorSecondaryTerrainType.WATER,
    81: MappaFloorSecondaryTerrainType.WATER,
    104: MappaFloorSecondaryTerrainType.WATER,
    68: MappaFloorSecondaryTerrainType.WATER,
    87: MappaFloorSecondaryTerrainType.WATER,
    79: MappaFloorSecondaryTerrainType.WATER,
    84: MappaFloorSecondaryTerrainType.WATER,
    112: MappaFloorSecondaryTerrainType.WATER,
    57: MappaFloorSecondaryTerrainType.WATER,
    58: MappaFloorSecondaryTerrainType.WATER,
    182: MappaFloorSecondaryTerrainType.WATER,
    117: MappaFloorSecondaryTerrainType.WATER,
    53: MappaFloorSecondaryTerrainType.WATER,
    54: MappaFloorSecondaryTerrainType.WATER,
    55: MappaFloorSecondaryTerrainType.WATER,
    56: MappaFloorSecondaryTerrainType.WATER,
    124: MappaFloorSecondaryTerrainType.WATER,
    63: MappaFloorSecondaryTerrainType.WATER,
    64: MappaFloorSecondaryTerrainType.WATER,
    25: MappaFloorSecondaryTerrainType.WATER,
    16: MappaFloorSecondaryTerrainType.WATER,
    114: MappaFloorSecondaryTerrainType.WATER,
    83: MappaFloorSecondaryTerrainType.WATER,
    115: MappaFloorSecondaryTerrainType.WATER,
    116: MappaFloorSecondaryTerrainType.WATER,
    97: MappaFloorSecondaryTerrainType.WATER,
    76: MappaFloorSecondaryTerrainType.WATER,
    67: MappaFloorSecondaryTerrainType.WATER,
    75: MappaFloorSecondaryTerrainType.WATER,
    110: MappaFloorSecondaryTerrainType.WATER,
    66: MappaFloorSecondaryTerrainType.WATER,
    142: MappaFloorSecondaryTerrainType.WATER,
    143: MappaFloorSecondaryTerrainType.WATER,
    94: MappaFloorSecondaryTerrainType.WATER,
    32: MappaFloorSecondaryTerrainType.WATER,
    195: MappaFloorSecondaryTerrainType.WATER,
    80: MappaFloorSecondaryTerrainType.WATER,
    184: MappaFloorSecondaryTerrainType.WATER,
    198: MappaFloorSecondaryTerrainType.WATER,
    128: MappaFloorSecondaryTerrainType.WATER,
    185: MappaFloorSecondaryTerrainType.WATER,
    132: MappaFloorSecondaryTerrainType.WATER,
    186: MappaFloorSecondaryTerrainType.WATER,
    133: MappaFloorSecondaryTerrainType.WATER,
    134: MappaFloorSecondaryTerrainType.WATER,
    135: MappaFloorSecondaryTerrainType.WATER,
    187: MappaFloorSecondaryTerrainType.WATER,
    136: MappaFloorSecondaryTerrainType.WATER,
    137: MappaFloorSecondaryTerrainType.WATER,
    138: MappaFloorSecondaryTerrainType.WATER,
    188: MappaFloorSecondaryTerrainType.WATER,
    139: MappaFloorSecondaryTerrainType.WATER,
    140: MappaFloorSecondaryTerrainType.WATER,
    141: MappaFloorSecondaryTerrainType.WATER,
    189: MappaFloorSecondaryTerrainType.WATER,
    44: MappaFloorSecondaryTerrainType.WATER,
    129: MappaFloorSecondaryTerrainType.WATER,
    190: MappaFloorSecondaryTerrainType.WATER,
    122: MappaFloorSecondaryTerrainType.WATER,
    130: MappaFloorSecondaryTerrainType.WATER,
    131: MappaFloorSecondaryTerrainType.WATER,
    191: MappaFloorSecondaryTerrainType.WATER,
    192: MappaFloorSecondaryTerrainType.WATER,
    193: MappaFloorSecondaryTerrainType.WATER,
    194: MappaFloorSecondaryTerrainType.WATER,
    78: MappaFloorSecondaryTerrainType.WATER,
    89: MappaFloorSecondaryTerrainType.WATER
}
# TODO: Tileset IDS > 169 seem to be using MapBGs to render?
ALLOWED_TILESET_IDS = [k for k in SECONDARY_TERRAIN_TILESET_MAP.keys() if k < 170]
ALLOWED_MD_IDS = range(1, 537)
ALLOWED_ITEM_IDS = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
    34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62,
    63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91,
    92, 93, 94, 95, 96, 97, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 115, 116, 117, 118, 119,
    120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 139, 140, 141, 142, 143,
    144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 167,
    168, 169, 170, 171, 172, 173, 174, 178, 179, 180, 182, 183, 186, 187, 188, 189, 190, 191, 192, 193, 195, 196, 197,
    199, 200, 201, 202, 203, 204, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 220, 221, 222, 223,
    225, 227, 228, 229, 230, 231, 232, 233, 234, 235, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249,
    250, 251, 252, 253, 254, 255, 256, 257, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274,
    275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 301, 302, 303, 304, 305,
    306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 325, 326, 327, 328, 329,
    330, 331, 332, 333, 334, 335, 336, 337, 338, 340, 341, 342, 343, 344, 346, 347, 348, 350, 351, 352, 354, 355, 356,
    357, 358, 359, 362
]
MAX_TRAP_LISTS = 100
MAX_ITEM_LISTS = 150


def random_decimal(start, stop):
    return Decimal(randrange(start * 100, stop * 100)) / 100


def can_be_randomized(floor: MappaFloor):
    # We don't randomize fixed floors
    return floor.layout.fixed_floor_id == 0


def randomize_layout(original_layout: MappaFloorLayout):
    tileset = choice(ALLOWED_TILESET_IDS)
    return MappaFloorLayout(
        structure=choice(list(MappaFloorStructureType)),
        room_density=randrange(3, 21),
        tileset_id=tileset,
        music_id=randrange(0, 118),
        weather=choice(list(MappaFloorWeather)),
        floor_connectivity=randrange(5, 51),
        initial_enemy_density=randrange(0, 14),
        kecleon_shop_chance=randrange(0, 101),
        monster_house_chance=randrange(0, 101),
        unusued_chance=randrange(0, 101),
        sticky_item_chance=randrange(0, 101),
        dead_ends=choice((True, False)),
        secondary_terrain=SECONDARY_TERRAIN_TILESET_MAP[tileset],
        terrain_settings=MappaFloorTerrainSettings(
            choice((True, False)), False, choice((True, False)), False, False, False, False, False
        ),
        unk_e=choice((True, False)),
        item_density=randrange(0, 11),
        trap_density=randrange(0, 16),
        floor_number=original_layout.floor_number,
        fixed_floor_id=original_layout.fixed_floor_id,
        extra_hallway_density=randrange(0, 36),
        buried_item_density=randrange(0, 11),
        water_density=randrange(0, 41),
        darkness_level=choice(list(MappaFloorDarknessLevel)),
        max_coin_amount=randrange(0, 181) * 5,
        kecleon_shop_item_positions=randrange(0, 14),
        empty_monster_house_chance=randrange(0, 101),
        unk_hidden_stairs=choice((0, 255)),
        hidden_stairs_spawn_chance=randrange(0, 101),
        enemy_iq=randrange(1, 601),
        iq_booster_allowed=choice((True, False))
    )


def randomize_monsters(min_level, max_level):
    monsters = []
    for _ in range(0, randrange(0, 21)):
        level = min(100, max(1, randrange(min_level - 3, max_level + 3)))
        weight = random_decimal(5, 101)
        monsters.append(MappaMonster(level, weight, weight, choice(ALLOWED_MD_IDS)))

    # Add Kecleon and Dummy
    monsters.append(MappaMonster(42, 0, 0, 383))
    monsters.append(MappaMonster(1, 0, 0, DUMMY_MD_INDEX))

    return monsters


def randomize_traps():
    chances = []
    for _ in range(0, 25):
        chances.append(random_decimal(0, 101))
    return MappaTrapList(chances)


def randomize_items():
    categories = {}
    items = {}
    for cat in MappaItemCategory:
        categories[cat] = random_decimal(35, 101)

    for _ in range(0, randrange(1, 150)):
        # We could maybe override previous values here, but that's okay.
        items[Pmd2DungeonItem(choice(ALLOWED_ITEM_IDS), '???')] = random_decimal(5, 101)

    # Add coins
    items[Pmd2DungeonItem(183, '???')] = random_decimal(0, 101)
    return MappaItemList(categories, items)


def randomize(mappa: MappaBin, trap_lists: List[MappaTrapList], item_lists: List[MappaItemList]):
    for floor_list in mappa.floor_lists:
        for floor in floor_list:
            if can_be_randomized(floor):
                floor.layout = randomize_layout(floor.layout)
                floor.monsters = randomize_monsters(
                    min(m.level for m in floor.monsters if m.chance > 0),
                    max(m.level for m in floor.monsters if m.chance > 0)
                )
                floor.traps = choice(trap_lists)
                floor.floor_items = choice(item_lists)
                floor.buried_items = choice(item_lists)
                floor.shop_items = choice(item_lists)
                floor.monster_house_items = choice(item_lists)
                floor.unk_items1 = choice(item_lists)
                floor.unk_items2 = choice(item_lists)


def run_main(rom_path, output_rom_path):
    print("Loading ROM...")
    rom = NintendoDSRom.fromFile(rom_path)
    mappa_before = rom.getFileByName('BALANCE/mappa_s.bin')
    mappa = FileType.MAPPA_BIN.deserialize(mappa_before)

    print("Randomizing items and traps...")
    trap_lists = []
    item_lists = []
    for _ in range(0, MAX_TRAP_LISTS):
        trap_lists.append(randomize_traps())
    for _ in range(0, MAX_ITEM_LISTS):
        item_lists.append(randomize_items())
    print("Randomizing Pokémon, floors and layouts...")
    randomize(mappa, trap_lists, item_lists)

    print("Saving to ROM...")
    mappa_after = FileType.MAPPA_BIN.serialize(mappa)
    rom.setFileByName('BALANCE/mappa_s.bin', mappa_after)

    print(f"Saving output ROM to {output_rom_path}...")
    rom.saveToFile(output_rom_path)

    print("Success!")
    print(f"Size BALANCE/mappa_s.bin before: {len(mappa_before)}")
    print(f"Size BALANCE/mappa_s.bin after: {len(mappa_after)}")


def main():
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(description="""Randomize the dungeon floors in PMD EoS.

    Currently there are no settings.

    It randomizes almost everything. Pokémon levels are randomized in a range of +/-3.

        """, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input_rom', metavar='INPUT_ROM',
                        help='Path to the input ROM file.')
    parser.add_argument('output_rom', metavar='OUTPUT_ROM',
                        help='Path where the randomized output ROM should be saved.')

    args = parser.parse_args()

    run_main(args.input_rom, args.output_rom)


if __name__ == '__main__':
    main()
