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

from skytemple_files.common.util import *
from skytemple_files.common.xml_util import XmlSerializable, validate_xml_tag, XmlValidateError
from skytemple_files.dungeon_data.mappa_bin import XML_FLOOR_LAYOUT, XML_FLOOR, XML_TRAP_LIST, XML_MONSTER, \
    XML_MONSTER_LIST, XML_ITEM_LIST, XML_ITEM_LIST__TYPE, XML_ITEM_LIST__TYPE__FLOOR, XML_ITEM_LIST__TYPE__SHOP, \
    XML_ITEM_LIST__TYPE__MONSTER_HOUSE, XML_ITEM_LIST__TYPE__BURIED, XML_ITEM_LIST__TYPE__UNK1, \
    XML_ITEM_LIST__TYPE__UNK2
from skytemple_files.dungeon_data.mappa_bin.floor_layout import MappaFloorLayout
from skytemple_files.dungeon_data.mappa_bin.item_list import MappaItemList
from skytemple_files.dungeon_data.mappa_bin.monster import MappaMonster
from skytemple_files.dungeon_data.mappa_bin.trap_list import MappaTrapList
from skytemple_files.common.i18n_util import f, _

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin.model import MappaBinReadContainer


class StubMappaFloor:
    """A mappa floor that only referneces an index for all of it's data."""
    def __init__(
        self, layout_idx: int, monsters_idx: int, traps_idx: int, floor_items_idx: int,
        shop_items_idx: int, monster_house_items_idx: int, buried_items_idx: int,
        unk_items1_idx: int, unk_items2_idx: int
    ):
        self.layout_idx: int = layout_idx
        self.monsters_idx: int = monsters_idx
        self.traps_idx: int = traps_idx
        self.floor_items_idx: int = floor_items_idx
        self.shop_items_idx: int = shop_items_idx
        self.monster_house_items_idx: int = monster_house_items_idx
        self.buried_items_idx: int = buried_items_idx
        self.unk_items1_idx: int = unk_items1_idx
        self.unk_items2_idx: int = unk_items2_idx

    def to_mappa(self) -> bytes:
        data = bytearray(18)
        write_uintle(data, self.layout_idx, 0x00, 2)
        write_uintle(data, self.monsters_idx, 0x02, 2)
        write_uintle(data, self.traps_idx, 0x04, 2)
        write_uintle(data, self.floor_items_idx, 0x06, 2)
        write_uintle(data, self.shop_items_idx, 0x08, 2)
        write_uintle(data, self.monster_house_items_idx, 0x0A, 2)
        write_uintle(data, self.buried_items_idx, 0x0C, 2)
        write_uintle(data, self.unk_items1_idx, 0x0E, 2)
        write_uintle(data, self.unk_items2_idx, 0x10, 2)
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
                read.floor_layout_data_start + 32 * read_uintle(floor_data, 0x00, 2),
                lambda pnt: MappaFloorLayout.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.monster_spawn_list_index_start, read_uintle(floor_data, 0x02, 2)),
                lambda pnt: MappaMonster.list_from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.trap_spawn_list_index_start, read_uintle(floor_data, 0x04, 2)),
                lambda pnt: MappaTrapList.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.item_spawn_list_index_start, read_uintle(floor_data, 0x06, 2)),
                lambda pnt: MappaItemList.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.item_spawn_list_index_start, read_uintle(floor_data, 0x08, 2)),
                lambda pnt: MappaItemList.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.item_spawn_list_index_start, read_uintle(floor_data, 0x0A, 2)),
                lambda pnt: MappaItemList.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.item_spawn_list_index_start, read_uintle(floor_data, 0x0C, 2)),
                lambda pnt: MappaItemList.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.item_spawn_list_index_start, read_uintle(floor_data, 0x0E, 2)),
                lambda pnt: MappaItemList.from_mappa(read, pnt)
            ),
            cls._from_cache(
                read,
                cls._read_pointer(read.data, read.item_spawn_list_index_start, read_uintle(floor_data, 0x10, 2)),
                lambda pnt: MappaItemList.from_mappa(read, pnt)
            )
        )

    @staticmethod
    def _read_pointer(data: bytes, start, index):
        return read_uintle(data, start + (4 * index), 4)

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

    def __eq__(self, other):
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
