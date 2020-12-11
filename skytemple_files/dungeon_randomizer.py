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
    0: MappaFloorSecondaryTerrainType.NONE,
    1: MappaFloorSecondaryTerrainType.NONE,
    170: MappaFloorSecondaryTerrainType.NONE,
    2: MappaFloorSecondaryTerrainType.NONE,
    3: MappaFloorSecondaryTerrainType.NONE,
    171: MappaFloorSecondaryTerrainType.NONE,
    4: MappaFloorSecondaryTerrainType.NONE,
    5: MappaFloorSecondaryTerrainType.NONE,
    6: MappaFloorSecondaryTerrainType.NONE,
    7: MappaFloorSecondaryTerrainType.NONE,
    8: MappaFloorSecondaryTerrainType.NONE,
    9: MappaFloorSecondaryTerrainType.NONE,
    10: MappaFloorSecondaryTerrainType.NONE,
    11: MappaFloorSecondaryTerrainType.NONE,
    12: MappaFloorSecondaryTerrainType.NONE,
    172: MappaFloorSecondaryTerrainType.NONE,
    14: MappaFloorSecondaryTerrainType.NONE,
    15: MappaFloorSecondaryTerrainType.NONE,
    173: MappaFloorSecondaryTerrainType.NONE,
    17: MappaFloorSecondaryTerrainType.HAS_1,
    18: MappaFloorSecondaryTerrainType.NONE,
    19: MappaFloorSecondaryTerrainType.NONE,
    20: MappaFloorSecondaryTerrainType.NONE,
    174: MappaFloorSecondaryTerrainType.NONE,
    22: MappaFloorSecondaryTerrainType.NONE,
    23: MappaFloorSecondaryTerrainType.NONE,
    24: MappaFloorSecondaryTerrainType.NONE,
    175: MappaFloorSecondaryTerrainType.NONE,
    26: MappaFloorSecondaryTerrainType.NONE,
    27: MappaFloorSecondaryTerrainType.NONE,
    28: MappaFloorSecondaryTerrainType.NONE,
    29: MappaFloorSecondaryTerrainType.NONE,
    30: MappaFloorSecondaryTerrainType.NONE,
    31: MappaFloorSecondaryTerrainType.NONE,
    176: MappaFloorSecondaryTerrainType.NONE,
    33: MappaFloorSecondaryTerrainType.NONE,
    34: MappaFloorSecondaryTerrainType.NONE,
    35: MappaFloorSecondaryTerrainType.NONE,
    36: MappaFloorSecondaryTerrainType.NONE,
    37: MappaFloorSecondaryTerrainType.NONE,
    38: MappaFloorSecondaryTerrainType.NONE,
    39: MappaFloorSecondaryTerrainType.NONE,
    40: MappaFloorSecondaryTerrainType.HAS_10,
    177: MappaFloorSecondaryTerrainType.NONE,
    42: MappaFloorSecondaryTerrainType.NONE,
    43: MappaFloorSecondaryTerrainType.NONE,
    178: MappaFloorSecondaryTerrainType.NONE,
    45: MappaFloorSecondaryTerrainType.NONE,
    46: MappaFloorSecondaryTerrainType.NONE,
    179: MappaFloorSecondaryTerrainType.NONE,
    48: MappaFloorSecondaryTerrainType.NONE,
    180: MappaFloorSecondaryTerrainType.NONE,
    113: MappaFloorSecondaryTerrainType.NONE,
    119: MappaFloorSecondaryTerrainType.NONE,
    106: MappaFloorSecondaryTerrainType.NONE,
    118: MappaFloorSecondaryTerrainType.HAS_10,
    51: MappaFloorSecondaryTerrainType.NONE,
    52: MappaFloorSecondaryTerrainType.NONE,
    50: MappaFloorSecondaryTerrainType.NONE,
    108: MappaFloorSecondaryTerrainType.NONE,
    62: MappaFloorSecondaryTerrainType.NONE,
    61: MappaFloorSecondaryTerrainType.NONE,
    91: MappaFloorSecondaryTerrainType.NONE,
    96: MappaFloorSecondaryTerrainType.NONE,
    103: MappaFloorSecondaryTerrainType.NONE,
    88: MappaFloorSecondaryTerrainType.NONE,
    85: MappaFloorSecondaryTerrainType.NONE,
    82: MappaFloorSecondaryTerrainType.NONE,
    111: MappaFloorSecondaryTerrainType.HAS_10,
    123: MappaFloorSecondaryTerrainType.NONE,
    125: MappaFloorSecondaryTerrainType.NONE,
    59: MappaFloorSecondaryTerrainType.NONE,
    90: MappaFloorSecondaryTerrainType.NONE,
    65: MappaFloorSecondaryTerrainType.NONE,
    102: MappaFloorSecondaryTerrainType.NONE,
    105: MappaFloorSecondaryTerrainType.NONE,
    99: MappaFloorSecondaryTerrainType.NONE,
    126: MappaFloorSecondaryTerrainType.NONE,
    49: MappaFloorSecondaryTerrainType.NONE,
    127: MappaFloorSecondaryTerrainType.HAS_1,
    181: MappaFloorSecondaryTerrainType.NONE,
    69: MappaFloorSecondaryTerrainType.NONE,
    109: MappaFloorSecondaryTerrainType.NONE,
    74: MappaFloorSecondaryTerrainType.NONE,
    101: MappaFloorSecondaryTerrainType.NONE,
    81: MappaFloorSecondaryTerrainType.NONE,
    104: MappaFloorSecondaryTerrainType.NONE,
    68: MappaFloorSecondaryTerrainType.NONE,
    87: MappaFloorSecondaryTerrainType.NONE,
    79: MappaFloorSecondaryTerrainType.NONE,
    84: MappaFloorSecondaryTerrainType.NONE,
    112: MappaFloorSecondaryTerrainType.NONE,
    57: MappaFloorSecondaryTerrainType.NONE,
    58: MappaFloorSecondaryTerrainType.NONE,
    182: MappaFloorSecondaryTerrainType.NONE,
    117: MappaFloorSecondaryTerrainType.NONE,
    53: MappaFloorSecondaryTerrainType.NONE,
    54: MappaFloorSecondaryTerrainType.NONE,
    55: MappaFloorSecondaryTerrainType.NONE,
    56: MappaFloorSecondaryTerrainType.NONE,
    124: MappaFloorSecondaryTerrainType.NONE,
    63: MappaFloorSecondaryTerrainType.NONE,
    64: MappaFloorSecondaryTerrainType.NONE,
    25: MappaFloorSecondaryTerrainType.NONE,
    16: MappaFloorSecondaryTerrainType.NONE,
    114: MappaFloorSecondaryTerrainType.NONE,
    83: MappaFloorSecondaryTerrainType.NONE,
    115: MappaFloorSecondaryTerrainType.NONE,
    116: MappaFloorSecondaryTerrainType.NONE,
    97: MappaFloorSecondaryTerrainType.NONE,
    76: MappaFloorSecondaryTerrainType.NONE,
    67: MappaFloorSecondaryTerrainType.NONE,
    75: MappaFloorSecondaryTerrainType.NONE,
    110: MappaFloorSecondaryTerrainType.NONE,
    66: MappaFloorSecondaryTerrainType.NONE,
    142: MappaFloorSecondaryTerrainType.NONE,
    143: MappaFloorSecondaryTerrainType.NONE,
    94: MappaFloorSecondaryTerrainType.NONE,
    32: MappaFloorSecondaryTerrainType.NONE,
    195: MappaFloorSecondaryTerrainType.NONE,
    80: MappaFloorSecondaryTerrainType.NONE,
    184: MappaFloorSecondaryTerrainType.NONE,
    198: MappaFloorSecondaryTerrainType.NONE,
    128: MappaFloorSecondaryTerrainType.NONE,
    185: MappaFloorSecondaryTerrainType.NONE,
    132: MappaFloorSecondaryTerrainType.NONE,
    186: MappaFloorSecondaryTerrainType.NONE,
    133: MappaFloorSecondaryTerrainType.NONE,
    134: MappaFloorSecondaryTerrainType.NONE,
    135: MappaFloorSecondaryTerrainType.NONE,
    187: MappaFloorSecondaryTerrainType.NONE,
    136: MappaFloorSecondaryTerrainType.NONE,
    137: MappaFloorSecondaryTerrainType.NONE,
    138: MappaFloorSecondaryTerrainType.NONE,
    188: MappaFloorSecondaryTerrainType.NONE,
    139: MappaFloorSecondaryTerrainType.NONE,
    140: MappaFloorSecondaryTerrainType.NONE,
    141: MappaFloorSecondaryTerrainType.NONE,
    189: MappaFloorSecondaryTerrainType.NONE,
    44: MappaFloorSecondaryTerrainType.NONE,
    129: MappaFloorSecondaryTerrainType.NONE,
    190: MappaFloorSecondaryTerrainType.NONE,
    122: MappaFloorSecondaryTerrainType.NONE,
    130: MappaFloorSecondaryTerrainType.NONE,
    131: MappaFloorSecondaryTerrainType.NONE,
    191: MappaFloorSecondaryTerrainType.NONE,
    192: MappaFloorSecondaryTerrainType.NONE,
    193: MappaFloorSecondaryTerrainType.NONE,
    194: MappaFloorSecondaryTerrainType.NONE,
    78: MappaFloorSecondaryTerrainType.NONE,
    89: MappaFloorSecondaryTerrainType.NONE
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
