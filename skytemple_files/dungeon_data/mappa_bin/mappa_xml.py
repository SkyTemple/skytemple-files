"""
Imports and exports data from/to XML and mappa floor models.
This can also handle partial data in the XML!
"""
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
from xml.etree.ElementTree import Element

from skytemple_files.common.xml_util import XmlValidateError
from skytemple_files.dungeon_data.mappa_bin import XML_FLOOR_LAYOUT, XML_MONSTER_LIST, XML_TRAP_LIST, XML_ITEM_LIST, \
    XML_ITEM_LIST__TYPE__FLOOR, XML_ITEM_LIST__TYPE__SHOP, XML_ITEM_LIST__TYPE__MONSTER_HOUSE, \
    XML_ITEM_LIST__TYPE__BURIED, XML_ITEM_LIST__TYPE__UNK1, XML_ITEM_LIST__TYPE__UNK2, XML_ITEM_LIST__TYPE
from skytemple_files.dungeon_data.mappa_bin.floor import MappaFloor
from skytemple_files.dungeon_data.mappa_bin.floor_layout import MappaFloorLayout
from skytemple_files.dungeon_data.mappa_bin.item_list import MappaItemList
from skytemple_files.dungeon_data.mappa_bin.monster import MappaMonster
from skytemple_files.dungeon_data.mappa_bin.trap_list import MappaTrapList
from skytemple_files.common.i18n_util import f, _


def mappa_floor_xml_export(floor: MappaFloor, export_layout=True, export_monsters=True, export_traps=True,
                           export_floor_items=True, export_shop_items=True, export_monster_house_items=True,
                           export_buried_items=True, export_unk1_items=True, export_unk2_items=True) -> Element:
    """Exports the requested data of the mappa floor as XML."""
    return floor.to_xml(export_layout=export_layout, export_monsters=export_monsters, export_traps=export_traps,
                        export_floor_items=export_floor_items, export_shop_items=export_shop_items,
                        export_monster_house_items=export_monster_house_items, export_buried_items=export_buried_items,
                        export_unk1_items=export_unk1_items, export_unk2_items=export_unk2_items)


def mappa_floor_xml_import(xml: Element, floor: MappaFloor):
    """Imports all data available in the mappa floor XML into the given model."""
    for child in xml:
        if child.tag == XML_FLOOR_LAYOUT:
            floor_number_before = floor.layout.floor_number
            floor.layout = MappaFloorLayout.from_xml(child)
            floor.layout.floor_number = floor_number_before
        elif child.tag == XML_MONSTER_LIST:
            monsters = []
            for monster in child:
                monsters.append(MappaMonster.from_xml(monster))
            floor.monsters = monsters
        elif child.tag == XML_TRAP_LIST:
            floor.traps = MappaTrapList.from_xml(child)
        elif child.tag == XML_ITEM_LIST and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__FLOOR:
            floor.floor_items = MappaItemList.from_xml(child)
        elif child.tag == XML_ITEM_LIST and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__SHOP:
            floor.shop_items = MappaItemList.from_xml(child)
        elif child.tag == XML_ITEM_LIST and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__MONSTER_HOUSE:
            floor.monster_house_items = MappaItemList.from_xml(child)
        elif child.tag == XML_ITEM_LIST and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__BURIED:
            floor.buried_items = MappaItemList.from_xml(child)
        elif child.tag == XML_ITEM_LIST and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__UNK1:
            floor.unk_items1 = MappaItemList.from_xml(child)
        elif child.tag == XML_ITEM_LIST and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__UNK2:
            floor.unk_items2 = MappaItemList.from_xml(child)
        else:
            raise XmlValidateError(f(_('Floor parsing: Unexpected {child.tag}')))

