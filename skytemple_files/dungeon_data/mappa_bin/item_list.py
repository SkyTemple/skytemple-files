#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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
import logging
from enum import Enum
from typing import Dict, Union, Optional
from xml.etree.ElementTree import Element

from skytemple_files.common.ppmdu_config.dungeon_data import Pmd2DungeonItem, Pmd2DungeonItemCategory
from skytemple_files.common.util import *
from skytemple_files.common.xml_util import XmlSerializable, validate_xml_tag, XmlValidateError, validate_xml_attribs
from skytemple_files.dungeon_data.mappa_bin import XML_ITEM_LIST, XML_CATEGORY, XML_CATEGORY__NAME, \
    XML_CATEGORY__WEIGHT, XML_ITEM__ID, XML_ITEM__WEIGHT, XML_ITEM
from skytemple_files.common.i18n_util import _

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin.model import MappaBinReadContainer
logger = logging.getLogger(__name__)


CMD_SKIP = 0x7530
GUARANTEED = 0xFFFF
MAX_ITEM_ID = 363
POKE_ID = 183
# Actually GUARANTEED or a weight between 0 and MAX_WEIGHT.
Probability = int


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

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: str, first_item_id: Optional[int], number_of_items: Optional[int],
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


class MappaItemList(AutoString, XmlSerializable):
    def __init__(self,
                 categories: Dict[Union[MappaItemCategory, Pmd2DungeonItemCategory], Probability],
                 items: Dict[Pmd2DungeonItem, Probability]):
        self.categories = categories
        self.items = items

    @classmethod
    def from_mappa(cls, read: 'MappaBinReadContainer', pointer: int):
        return cls.from_bytes(read.data, read.items, pointer)
        
    @classmethod
    def from_bytes(cls, data: bytes, item_list: Pmd2DungeonItem, pointer: int):
        processing_categories = True
        item_or_cat_id = 0
        orig_pointer = pointer
        len_read = 0

        items = {}
        categories = {}

        while item_or_cat_id <= MAX_ITEM_ID:
            val = read_uintle(data, pointer, 2)
            len_read += 2
            skip = val > CMD_SKIP and val != GUARANTEED

            if skip:
                item_or_cat_id += val - CMD_SKIP
            else:
                if val == GUARANTEED:
                    weight = GUARANTEED
                else:
                    weight = val
                if processing_categories:
                    # TODO: Switch to Pmd2DungeonItemCategory
                    categories[MappaItemCategory(item_or_cat_id)] = weight
                else:
                    items[item_list[item_or_cat_id]] = weight
                item_or_cat_id += 1
            if item_or_cat_id >= 0xF and processing_categories:
                processing_categories = False
                item_or_cat_id -= 0x10
            pointer += 2

        assert data[orig_pointer:orig_pointer+len_read] == MappaItemList(categories, items).to_mappa()

        return MappaItemList(categories, items)

    def to_mappa(self):
        data = bytearray()
        current_id = 0
        # Start with the categories
        for cat, val in sorted(self.categories.items(), key=lambda it: it[0].value):
            id_cat = cat.value
            if current_id != id_cat:
                current_id = self._write_skip(data, current_id, id_cat)
            self._write_probability(data, val)
            current_id += 1
        # Continue with the items
        sorted_items = sorted(self.items.items(), key=lambda it: it[0].id)
        first_item_id = sorted_items[0][0].id if len(sorted_items) > 0 else 0
        self._write_skip(data, current_id, 0x10 + first_item_id)
        current_id = first_item_id
        for item, val in sorted_items:
            if current_id != item.id:
                current_id = self._write_skip(data, current_id, item.id)
            self._write_probability(data, val)
            current_id += 1
        # Fill up to MAX_ITEM_ID + 1
        self._write_skip(data, current_id, MAX_ITEM_ID + 1)
        return data

    def to_xml(self) -> Element:
        xml_item_list = Element(XML_ITEM_LIST)
        for category, probability in self.categories.items():
            weight = 'GUARANTEED' if probability == GUARANTEED else str(probability)
            xml_category = Element(XML_CATEGORY, {
                XML_CATEGORY__NAME: MappaItemCategory(category.value).name,
                XML_CATEGORY__WEIGHT: str(weight)
            })
            xml_item_list.append(xml_category)
        for item, probability in self.items.items():
            weight = 'GUARANTEED' if probability == GUARANTEED else str(probability)
            xml_item = Element(XML_ITEM, {
                XML_ITEM__ID: str(item.id),
                XML_ITEM__WEIGHT: str(weight)
            })
            xml_item_list.append(xml_item)

        return xml_item_list

    @classmethod
    def from_xml(cls, ele: Element) -> 'XmlSerializable':
        validate_xml_tag(ele, XML_ITEM_LIST)
        categories = {}
        items = {}
        for child in ele:
            if child.tag == XML_CATEGORY:
                validate_xml_attribs(child, [XML_CATEGORY__NAME, XML_CATEGORY__WEIGHT])
                name = child.get(XML_CATEGORY__NAME)
                # TODO: Switch to Pmd2DungeonItemCategory
                if not hasattr(MappaItemCategory, name):
                    raise XmlValidateError(f"Unknown item category {name}.")
                weight_str = child.get(XML_CATEGORY__WEIGHT)
                weight = int(weight_str) if weight_str != 'GUARANTEED' else GUARANTEED
                # TODO: Switch to Pmd2DungeonItemCategory
                categories[getattr(MappaItemCategory, name)] = weight
            elif child.tag == XML_ITEM:
                validate_xml_attribs(child, [XML_ITEM__ID, XML_ITEM__WEIGHT])
                weight_str = child.get(XML_ITEM__WEIGHT)
                weight = int(weight_str) if weight_str != 'GUARANTEED' else GUARANTEED
                items[Pmd2DungeonItem(int(child.get(XML_ITEM__ID)), '???')] = weight
            else:
                raise XmlValidateError(f"Unexpected sub-node for {XML_ITEM_LIST}: {child.tag}")
        return cls(categories, items)

    def __eq__(self, other):
        if not isinstance(other, MappaItemList):
            return False
        return self.categories == other.categories and self.items == other.items

    def _write_skip(self, data: bytearray, current_id: int, target_id: int):
        if current_id != target_id:
            data += (target_id - current_id + CMD_SKIP).to_bytes(2, 'little', signed=False)
        return target_id

    def _write_probability(self, data: bytearray, probability: Probability):
        data += probability.to_bytes(2, 'little', signed=False)
