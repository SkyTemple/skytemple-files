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
from typing import Dict, Union

from skytemple_files.common.ppmdu_config.dungeon_data import Pmd2DungeonItem
from skytemple_files.common.util import *

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin.model import MappaBinReadContainer


CMD_SKIP = 0x7530
GUARANTEED = 0xFFFF
MAX_ITEM_ID = 362
# Actually GUARANTEED or a float. Literals are only supported for Python 3.8+ so we do it like this.
Probability = Union[int, float]


class MappaItemCategory(Enum):
    THROWN_PIERCE = 0
    THROWN_ROCK = 1
    BERRIES_SEEDS_VITAMINS = 2
    FOODS_GUMMIES = 3
    HOLD = 4
    TMS = 5
    ORBS = 6
    UNK7 = 7
    OTHER = 8
    UNK9 = 9
    LINK_BOX = 0xA
    UNKB = 0xB
    UNKC = 0xC
    UNKD = 0xD
    UNKE = 0xE
    UNKF = 0xF


class MappaItemList(AutoString):
    def __init__(self, categories: Dict[MappaItemCategory, Probability], items: Dict[Pmd2DungeonItem, Probability]):
        self.categories = categories
        self.items = items

    @classmethod
    def from_mappa(cls, read: 'MappaBinReadContainer', pointer: int):
        processing_categories = True
        item_or_cat_id = 0

        items = {}
        categories = {}

        while item_or_cat_id <= MAX_ITEM_ID:
            val = read_uintle(read.data, pointer, 2)
            skip = val > CMD_SKIP

            if skip:
                item_or_cat_id += val - CMD_SKIP
            else:
                if val == GUARANTEED:
                    chance = 100
                else:
                    chance = val / 100
                if processing_categories:
                    categories[MappaItemCategory(item_or_cat_id)] = chance
                else:
                    items[read.items[item_or_cat_id]] = chance
                item_or_cat_id += 1
            if item_or_cat_id >= 0xF and processing_categories:
                processing_categories = False
                item_or_cat_id -= 0x10
            pointer += 2

        return MappaItemList(categories, items)
