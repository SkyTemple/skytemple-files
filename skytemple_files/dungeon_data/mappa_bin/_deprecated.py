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
import logging
import warnings
from enum import Enum
from typing import Optional, List

from skytemple_files.common.i18n_util import _

_WARNMSG = "MappaItemCategory is deprecated. Use Pmd2DungeonData's item_categories attribute instead. " \
           "This deprecated class will provide dynamically generated values from the default " \
           "EU XML configuration."
_defconf = None


def _gdefconf():
    from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
    global _defconf
    if _defconf is None:
        _defconf = Pmd2XmlReader.load_default().dungeon_data.item_categories
    return _defconf


logger = logging.getLogger(__name__)


class MappaItemCategory(Enum):
    """:deprecated: Use Pmd2DungeonData's item_categories attribute instead."""
    warnings.warn(_WARNMSG, category=DeprecationWarning, stacklevel=2)
    logger.warning(_WARNMSG)
    THROWN_PIERCE = 0, -1, 0, list(_gdefconf()[0].items), [], _(_gdefconf()[0].name)
    THROWN_ROCK = 1, -1, 0, list(_gdefconf()[1].items), [], _(_gdefconf()[1].name)
    BERRIES_SEEDS_VITAMINS = 2, -1, 0, list(_gdefconf()[2].items), [], _(_gdefconf()[2].name)
    FOODS_GUMMIES = 3, -1, 0, list(_gdefconf()[3].items), [], _(_gdefconf()[3].name)
    HOLD = 4, -1, 0, list(_gdefconf()[4].items), [], _(_gdefconf()[4].name)
    TMS = 5, -1, 0, list(_gdefconf()[5].items), [], _(_gdefconf()[5].name)
    POKE = 6, -1, 0, list(_gdefconf()[6].items), [], _(_gdefconf()[6].name)
    UNK7 = 7, -1, 0, list(_gdefconf()[7].items), [], _(_gdefconf()[7].name)
    OTHER = 8, -1, 0, list(_gdefconf()[8].items), [], _(_gdefconf()[8].name)
    ORBS = 9, -1, 0, list(_gdefconf()[9].items), [], _(_gdefconf()[9].name)
    LINK_BOX = 10, -1, 0, list(_gdefconf()[10].items), [], _(_gdefconf()[10].name)
    UNKB = 11, -1, 0, list(_gdefconf()[11].items), [], _(_gdefconf()[11].name)
    UNKC = 12, -1, 0, list(_gdefconf()[12].items), [], _(_gdefconf()[12].name)
    UNKD = 13, -1, 0, list(_gdefconf()[13].items), [], _(_gdefconf()[13].name)
    UNKE = 14, -1, 0, list(_gdefconf()[14].items), [], _(_gdefconf()[14].name)
    UNKF = 15, -1, 0, list(_gdefconf()[15].items), [], _(_gdefconf()[15].name)

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: int, first_item_id: Optional[int], number_of_items: Optional[int],
            excluded_item_ids: List[int], extra_item_ids: List[int], name_localized: str
    ):
        self.first_item_id = first_item_id
        self.number_of_items = number_of_items
        self.excluded_item_ids = excluded_item_ids
        self.extra_item_ids = extra_item_ids
        self.name_localized = name_localized

    def is_item_in_cat(self, item_id: int):
        return item_id in self.extra_item_ids or (
                self.first_item_id <= item_id < self.first_item_id + self.number_of_items
                and item_id not in self.excluded_item_ids
        )

    def item_ids(self):
        return [
                   x for x in range(self.first_item_id, self.first_item_id + self.number_of_items)
                   if x not in self.excluded_item_ids
               ] + self.extra_item_ids

    @property
    def print_name(self):
        return self.name_localized