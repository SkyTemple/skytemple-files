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
from __future__ import annotations

import typing
from xml.etree.ElementTree import Element

from skytemple_files.common.i18n_util import _, f
from skytemple_files.common.util import *
from skytemple_files.common.xml_util import (XmlSerializable, XmlValidateError,
                                             validate_xml_tag)
from skytemple_files.dungeon_data.mappa_bin import (
    XML_FLOOR, XML_FLOOR_LAYOUT, XML_ITEM_LIST, XML_ITEM_LIST__TYPE,
    XML_ITEM_LIST__TYPE__BURIED, XML_ITEM_LIST__TYPE__FLOOR,
    XML_ITEM_LIST__TYPE__MONSTER_HOUSE, XML_ITEM_LIST__TYPE__SHOP,
    XML_ITEM_LIST__TYPE__UNK1, XML_ITEM_LIST__TYPE__UNK2, XML_MONSTER,
    XML_MONSTER_LIST, XML_TRAP_LIST)
from skytemple_files.dungeon_data.mappa_bin.floor_layout import \
    MappaFloorLayout
from skytemple_files.dungeon_data.mappa_bin.item_list import MappaItemList
from skytemple_files.dungeon_data.mappa_bin.monster import MappaMonster
from skytemple_files.dungeon_data.mappa_bin.trap_list import MappaTrapList

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin.model import \
        MappaBinReadContainer


class StubMappaFloor:
    """A mappa floor that only referneces an index for all of it's data."""
    layout_idx: u16
    monsters_idx: u16
    traps_idx: u16
    floor_items_idx: u16
    shop_items_idx: u16
    monster_house_items_idx: u16
    buried_items_idx: u16
    unk_items1_idx: u16
    unk_items2_idx: u16

    def __init__(
        self, layout_idx: u16, monsters_idx: u16, traps_idx: u16, floor_items_idx: u16,
        shop_items_idx: u16, monster_house_items_idx: u16, buried_items_idx: u16,
        unk_items1_idx: u16, unk_items2_idx: u16
    ):
        self.layout_idx = layout_idx
        self.monsters_idx = monsters_idx
        self.traps_idx = traps_idx
        self.floor_items_idx = floor_items_idx
        self.shop_items_idx = shop_items_idx
        self.monster_house_items_idx = monster_house_items_idx
        self.buried_items_idx = buried_items_idx
        self.unk_items1_idx = unk_items1_idx
        self.unk_items2_idx = unk_items2_idx

    def to_mappa(self) -> bytes:
        data = bytearray(18)
        write_u16(data, self.layout_idx, 0x00)
        write_u16(data, self.monsters_idx, 0x02)
        write_u16(data, self.traps_idx, 0x04)
        write_u16(data, self.floor_items_idx, 0x06)
        write_u16(data, self.shop_items_idx, 0x08)
        write_u16(data, self.monster_house_items_idx, 0x0A)
        write_u16(data, self.buried_items_idx, 0x0C)
        write_u16(data, self.unk_items1_idx, 0x0E)
        write_u16(data, self.unk_items2_idx, 0x10)
        if bytes(18) in data:
            raise ValueError(_("Could not save floor: It contains too much empty data.\nThis probably happened "
                               "because a lot of spawn lists are empty.\nPlease check the floors you edited and fill "
                               "them with more data. If you are using the randomizer, check your allowed item list."))
        return data


class MappaFloor(AutoString, XmlSerializable):
    def __init__(
        self, layout: MappaFloorLayout, monsters: List[MappaMonster], traps: MappaTrapList, floor_items: MappaItemList,
        shop_items: MappaItemList, monster_house_items: MappaItemList, buried_items: MappaItemList,
        unk_items1: MappaItemList, unk_items2: MappaItemList
    ):
        self.layout: MappaFloorLayout = layout
        self.monsters: List[MappaMonster] = monsters
        self.traps: MappaTrapList = traps
        self.floor_items: MappaItemList = floor_items
        self.shop_items: MappaItemList = shop_items
        self.monster_house_items: MappaItemList = monster_house_items
        self.buried_items: MappaItemList = buried_items
        self.unk_items1: MappaItemList = unk_items1
        self.unk_items2: MappaItemList = unk_items2

    @classmethod
    def from_mappa(cls, read: 'MappaBinReadContainer', floor_data: bytes) -> 'MappaFloor':
        return cls(
            cls._from_cache(
                read,
                read.floor_layout_data_start + 32 * read_u16(floor_data, 0x00),
                lambda pnt: MappaFloorLayout.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.monster_spawn_list_index_start, read_u16(floor_data, 0x02)),
                lambda pnt: MappaMonster.list_from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.trap_spawn_list_index_start, read_u16(floor_data, 0x04)),
                lambda pnt: MappaTrapList.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.item_spawn_list_index_start, read_u16(floor_data, 0x06)),
                lambda pnt: MappaItemList.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.item_spawn_list_index_start, read_u16(floor_data, 0x08)),
                lambda pnt: MappaItemList.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.item_spawn_list_index_start, read_u16(floor_data, 0x0A)),
                lambda pnt: MappaItemList.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.item_spawn_list_index_start, read_u16(floor_data, 0x0C)),
                lambda pnt: MappaItemList.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.item_spawn_list_index_start, read_u16(floor_data, 0x0E)),
                lambda pnt: MappaItemList.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.item_spawn_list_index_start, read_u16(floor_data, 0x10)),
                lambda pnt: MappaItemList.from_mappa(read, pnt)
            )
        )

    @staticmethod
    def _read_pointer(data: bytes, start, index):
        return read_u32(data, start + (4 * index))

    @staticmethod
    def _from_cache(read, pnt, load_callback):
        # TODO: Caching needs a deep copy
        return load_callback(pnt)

    def to_xml(
            self, export_layout=True, export_monsters=True, export_traps=True,
            export_floor_items=True, export_shop_items=True, export_monster_house_items=True,
            export_buried_items=True, export_unk1_items=True, export_unk2_items=True
    ) -> Element:
        floor_xml = Element(XML_FLOOR)

        if export_layout:
            layout_xml = self.layout.to_xml()
            validate_xml_tag(layout_xml, XML_FLOOR_LAYOUT)
            floor_xml.append(layout_xml)

        if export_monsters:
            monsters_xml = Element(XML_MONSTER_LIST)
            for monster in self.monsters:
                monster_xml = monster.to_xml()
                validate_xml_tag(monster_xml, XML_MONSTER)
                monsters_xml.append(monster_xml)
            floor_xml.append(monsters_xml)

        if export_traps:
            traps_xml = self.traps.to_xml()
            validate_xml_tag(traps_xml, XML_TRAP_LIST)
            floor_xml.append(traps_xml)

        if export_floor_items:
            floor_items_xml = self.floor_items.to_xml()
            validate_xml_tag(floor_items_xml, XML_ITEM_LIST)
            floor_items_xml.set(XML_ITEM_LIST__TYPE, XML_ITEM_LIST__TYPE__FLOOR)
            floor_xml.append(floor_items_xml)

        if export_shop_items:
            shop_items_xml = self.shop_items.to_xml()
            validate_xml_tag(shop_items_xml, XML_ITEM_LIST)
            shop_items_xml.set(XML_ITEM_LIST__TYPE, XML_ITEM_LIST__TYPE__SHOP)
            floor_xml.append(shop_items_xml)

        if export_monster_house_items:
            monster_house_items_xml = self.monster_house_items.to_xml()
            validate_xml_tag(monster_house_items_xml, XML_ITEM_LIST)
            monster_house_items_xml.set(XML_ITEM_LIST__TYPE, XML_ITEM_LIST__TYPE__MONSTER_HOUSE)
            floor_xml.append(monster_house_items_xml)

        if export_buried_items:
            buried_items_xml = self.buried_items.to_xml()
            validate_xml_tag(buried_items_xml, XML_ITEM_LIST)
            buried_items_xml.set(XML_ITEM_LIST__TYPE, XML_ITEM_LIST__TYPE__BURIED)
            floor_xml.append(buried_items_xml)

        if export_unk1_items:
            unk_items1_xml = self.unk_items1.to_xml()
            validate_xml_tag(unk_items1_xml, XML_ITEM_LIST)
            unk_items1_xml.set(XML_ITEM_LIST__TYPE, XML_ITEM_LIST__TYPE__UNK1)
            floor_xml.append(unk_items1_xml)

        if export_unk2_items:
            unk_items2_xml = self.unk_items2.to_xml()
            validate_xml_tag(unk_items2_xml, XML_ITEM_LIST)
            unk_items2_xml.set(XML_ITEM_LIST__TYPE, XML_ITEM_LIST__TYPE__UNK2)
            floor_xml.append(unk_items2_xml)

        return floor_xml

    @classmethod
    @typing.no_type_check
    def from_xml(cls, ele: Element) -> 'MappaFloor':
        data = {
            'layout': None,
            'monsters': None,
            'traps': None,
            'floor_items': None,
            'shop_items': None,
            'monster_house_items': None,
            'buried_items': None,
            'unk_items1': None,
            'unk_items2': None
        }
        for child in ele:
            if child.tag == XML_FLOOR_LAYOUT and data['layout'] is None:
                data['layout'] = MappaFloorLayout.from_xml(child)
            elif child.tag == XML_MONSTER_LIST and data['monsters'] is None:
                monsters = []
                for monster in child:
                    monsters.append(MappaMonster.from_xml(monster))
                data['monsters'] = monsters
            elif child.tag == XML_TRAP_LIST and data['traps'] is None:
                data['traps'] = MappaTrapList.from_xml(child)
            elif child.tag == XML_ITEM_LIST and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__FLOOR and data['floor_items'] is None:
                data['floor_items'] = MappaItemList.from_xml(child)
            elif child.tag == XML_ITEM_LIST and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__SHOP and data['shop_items'] is None:
                data['shop_items'] = MappaItemList.from_xml(child)
            elif child.tag == XML_ITEM_LIST and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__MONSTER_HOUSE and data['monster_house_items'] is None:
                data['monster_house_items'] = MappaItemList.from_xml(child)
            elif child.tag == XML_ITEM_LIST and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__BURIED and data['buried_items'] is None:
                data['buried_items'] = MappaItemList.from_xml(child)
            elif child.tag == XML_ITEM_LIST and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__UNK1 and data['unk_items1'] is None:
                data['unk_items1'] = MappaItemList.from_xml(child)
            elif child.tag == XML_ITEM_LIST and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__UNK2 and data['unk_items2'] is None:
                data['unk_items2'] = MappaItemList.from_xml(child)
            else:
                raise XmlValidateError(f(_('Floor parsing: Unexpected {child.tag}')))

        for k, v in data.items():
            if v is None:
                raise XmlValidateError(f(_('Missing {k} for Floor data.')))

        return cls(**data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MappaFloor):
            return False
        return self.floor_items == other.floor_items \
            and self.layout == other.layout \
            and self.traps == other.traps \
            and self.monsters == other.monsters \
            and self.buried_items == other.buried_items \
            and self.monster_house_items == other.monster_house_items \
            and self.shop_items == other.shop_items \
            and self.unk_items1 == other.unk_items1 \
            and self.unk_items2 == other.unk_items2
