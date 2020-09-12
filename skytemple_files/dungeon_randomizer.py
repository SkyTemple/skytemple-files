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
from collections import OrderedDict
from random import randrange, choice, sample, shuffle
from typing import List

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.dungeon_data import Pmd2DungeonItem
from skytemple_files.common.types.file_types import FileType
from skytemple_files.dungeon_data.mappa_bin import MAX_WEIGHT
from skytemple_files.dungeon_data.mappa_bin.floor import MappaFloor
from skytemple_files.dungeon_data.mappa_bin.floor_layout import MappaFloorLayout, MappaFloorStructureType, \
    MappaFloorSecondaryTerrainType, MappaFloorWeather, MappaFloorTerrainSettings, MappaFloorDarknessLevel
from skytemple_files.dungeon_data.mappa_bin.item_list import MappaItemCategory, MappaItemList, MAX_ITEM_ID
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

# 383, 384 -> Kecleons
KECLEON_MD_INDEX = 383
DISALLOWED_MD_IDS = [KECLEON_MD_INDEX, 384]
ALLOWED_MD_IDS = [x for x in range(1, 537) if x not in DISALLOWED_MD_IDS]
MONSTER_LEVEL_VARIANCE = 3

# Invalid items:
DISALLOWED_ITEM_IDS = [11, 12, 98, 113, 114, 138, 166, 175, 176, 177, 181, 184, 185, 198, 205, 219, 224, 226, 236, 258,
                       259, 293, 294, 295, 296, 297, 298, 299, 300, 324, 339, 345, 349, 353, 360, 361]
ALLOWED_ITEM_IDS = [x for x in range(1, MAX_ITEM_ID) if x not in DISALLOWED_ITEM_IDS]
ALLOWED_ITEM_CATS = [
    MappaItemCategory.THROWN_PIERCE,
    MappaItemCategory.THROWN_ROCK,
    MappaItemCategory.BERRIES_SEEDS_VITAMINS,
    MappaItemCategory.FOODS_GUMMIES,
    MappaItemCategory.HOLD,
    MappaItemCategory.TMS,
    MappaItemCategory.ORBS,
    MappaItemCategory.OTHER
]

MAX_TRAP_LISTS = 100
MAX_ITEM_LISTS = 150
MIN_MONSTERS_PER_LIST = 5
MAX_MONSTERS_PER_LIST = 30  # 48 is theoretical limit [=max used by vanilla game]
#MIN_ITEMS_PER_LIST = 20
#MAX_ITEMS_PER_LIST = 100  # 196 is theoretical limit [=max used by vanilla game]
MIN_ITEMS_PER_CAT = 4
MAX_ITEMS_PER_CAT = 18


def ranks(sample):
    """
    Return the ranks of each element in an integer sample.
    """
    indices = sorted(range(len(sample)), key=lambda i: sample[i])
    return sorted(indices, key=lambda i: indices[i])


def sample_with_minimum_distance(n, k, d):
    """
    Sample of k elements from range(n), with a minimum distance d.
    """
    smpl = sample(range(n-(k-1)*(d-1)), k)
    return [s + (d-1)*r for s, r in zip(smpl, ranks(smpl))]


def random_weights(k):
    """
    Returns k random weights, with relative equal distance, in a range of *0.75-*1
    """
    smallest_possible_d = int(MAX_WEIGHT / k)
    d = int(smallest_possible_d * (randrange(75, 100) / 100))
    # We actually subtract the d and add it later to all of the items, to make the first entry also a bit more likely
    weights = [w + d for w in sample_with_minimum_distance(MAX_WEIGHT - d, k, d)]
    # The last weight needs to have 10000
    highest_index = weights.index(max(weights))
    weights[highest_index] = MAX_WEIGHT
    return weights


def can_be_randomized(floor: MappaFloor):
    # We don't randomize fixed floors
    return floor.layout.fixed_floor_id == 0


def randomize_layout(original_layout: MappaFloorLayout):
    tileset = choice(ALLOWED_TILESET_IDS)
    structure = choice(list(MappaFloorStructureType))
    # Make Monster Houses less likely by re-rolling 50% of the time when it happens
    if structure == MappaFloorStructureType.SINGLE_MONSTER_HOUSE or structure == MappaFloorStructureType.TWO_ROOMS_ONE_MH:
        if choice((True, False)):
            structure = choice(list(MappaFloorStructureType))
    return MappaFloorLayout(
        structure=structure,
        room_density=randrange(3, 21),
        tileset_id=tileset,
        music_id=randrange(1, 118),
        weather=choice(list(MappaFloorWeather)),
        floor_connectivity=randrange(5, 51),
        initial_enemy_density=randrange(1, 14),
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
    md_ids = sorted(set(choice(ALLOWED_MD_IDS) for _ in range(0, randrange(MIN_MONSTERS_PER_LIST, MAX_MONSTERS_PER_LIST + 1))))
    weights = sorted(random_weights(len(md_ids)))
    for md_id, weight in zip(md_ids, weights):
        level = min(100, max(1, randrange(min_level - MONSTER_LEVEL_VARIANCE, max_level + MONSTER_LEVEL_VARIANCE + 1)))
        monsters.append(MappaMonster(level, weight, weight, md_id))

    # Add Kecleon and Dummy
    monsters.append(MappaMonster(42, 0, 0, KECLEON_MD_INDEX))
    monsters.append(MappaMonster(1, 0, 0, DUMMY_MD_INDEX))

    return sorted(monsters, key=lambda m: m.md_index)


def randomize_traps():
    # Unusued trap + 24 traps
    ws = sorted(random_weights(24))
    return MappaTrapList([0] + ws)


def randomize_items():
    categories = {}
    items = OrderedDict()
    cats_as_list = list(ALLOWED_ITEM_CATS)

    # 1/8 chance for money to get a chance
    if choice([True] + [False] * 7):
        cats_as_list.append(MappaItemCategory.POKE)

    # 1/8 chance for Link Box to get a chance
    if choice([True] + [False] * 7):
        cats_as_list.append(MappaItemCategory.LINK_BOX)

    weights = sorted(random_weights(len(cats_as_list)))
    for i, cat in enumerate(cats_as_list):
        categories[cat] = weights[i]

        # TODO: Work with .item_ids() instead, since there are some exceptions (see foods/vitamins).
        if cat.number_of_items is not None:
            allowed_cat_item_ids = [x for x in ALLOWED_ITEM_IDS if x in
                                    range(cat.first_item_id, cat.first_item_id + cat.number_of_items)]
            upper_limit = min(MAX_ITEMS_PER_CAT, len(allowed_cat_item_ids))
            if upper_limit <= MIN_ITEMS_PER_CAT:
                n_items = MIN_ITEMS_PER_CAT
            else:
                n_items = randrange(MIN_ITEMS_PER_CAT, upper_limit)
            cat_item_ids = sorted(set(
                (choice(allowed_cat_item_ids) for _ in range(0, n_items))
            ))
            cat_weights = sorted(random_weights(len(cat_item_ids)))

            for item_id, weight in zip(cat_item_ids, cat_weights):
                items[Pmd2DungeonItem(item_id, '???')] = weight

    return MappaItemList(categories, OrderedDict(sorted(items.items(), key=lambda i: i[0].id)))


def randomize(mappa: MappaBin, trap_lists: List[MappaTrapList], item_lists: List[MappaItemList]):
    for floor_list in mappa.floor_lists:
        for floor in floor_list:
            if can_be_randomized(floor):
                floor.layout = randomize_layout(floor.layout)
                floor.monsters = randomize_monsters(
                    min(m.level for m in floor.monsters if m.weight > 0),
                    max(m.level for m in floor.monsters if m.weight > 0)
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
