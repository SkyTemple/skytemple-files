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
from decimal import Decimal
from enum import Enum
from typing import Dict, Union
from xml.etree.ElementTree import Element

from skytemple_files.common.ppmdu_config.dungeon_data import Pmd2DungeonItem
from skytemple_files.common.util import *
from skytemple_files.common.xml_util import XmlSerializable, validate_xml_tag, XmlValidateError, validate_xml_attribs
from skytemple_files.dungeon_data.mappa_bin import XML_ITEM_LIST, XML_CATEGORY, XML_CATEGORY__NAME, \
    XML_CATEGORY__CHANCE, XML_ITEM__ID, XML_ITEM__CHANCE, XML_ITEM

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin.model import MappaBinReadContainer


CMD_SKIP = 0x7530
GUARANTEED = 0xFFFF
MAX_ITEM_ID = 362
# Actually GUARANTEED or a Decimal. Literals are only supported for Python 3.8+ so we do it like this.
Probability = Union[int, Decimal]


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


class MappaItemList(AutoString, XmlSerializable):
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
                    chance = Decimal(val) / Decimal(100)
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
        self._write_skip(data, current_id, 0x10)
        current_id = 0
        for item, val in sorted(self.items.items(), key=lambda it: it[0].id):
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
            chance = 'GUARANTEED' if probability == GUARANTEED else str(probability)
            xml_category = Element(XML_CATEGORY, {
                XML_CATEGORY__NAME: category.name,
                XML_CATEGORY__CHANCE: str(chance)
            })
            xml_item_list.append(xml_category)
        for item, probability in self.items.items():
            chance = 'GUARANTEED' if probability == GUARANTEED else str(probability)
            xml_item = Element(XML_ITEM, {
                XML_ITEM__ID: str(item.id),
                XML_ITEM__CHANCE: str(chance)
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
                validate_xml_attribs(child, [XML_CATEGORY__NAME, XML_CATEGORY__CHANCE])
                name = child.get(XML_CATEGORY__NAME)
                if not hasattr(MappaItemCategory, name):
                    raise XmlValidateError(f"Unknown item category {name}.")
                chance_str = child.get(XML_CATEGORY__CHANCE)
                chance = Decimal(chance_str) if chance_str != 'GUARANTEED' else GUARANTEED
                categories[getattr(MappaItemCategory, name)] = chance
            elif child.tag == XML_ITEM:
                validate_xml_attribs(child, [XML_ITEM__ID, XML_ITEM__CHANCE])
                chance_str = child.get(XML_ITEM__CHANCE)
                chance = Decimal(chance_str) if chance_str != 'GUARANTEED' else GUARANTEED
                items[Pmd2DungeonItem(int(child.get(XML_ITEM__ID)), '???')] = chance
            else:
                raise XmlValidateError(f"Unexpected sub-node for {XML_ITEM_LIST}: {child.tag}")
        return cls(categories, items)

    def __eq__(self, other):
        if not isinstance(other, MappaItemList):
            return False
        return self.categories == other.categories and self.items == other.items

    def _write_skip(self, data: bytearray, current_id: int, target_id: int):
        data += (target_id - current_id + CMD_SKIP).to_bytes(2, 'little', signed=False)
        return target_id

    def _write_probability(self, data: bytearray, probability: Probability):
        if probability == GUARANTEED:
            data += probability.to_bytes(2, 'little', signed=False)
        else:
            data += int(probability * 100).to_bytes(2, 'little', signed=False)
