"""
Imports and exports data from/to XML and mappa floor models.
This can also handle partial data in the XML!
"""
#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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

from typing import Dict, no_type_check, TypedDict, List, Optional
from xml.etree.ElementTree import Element

from range_typed_integers import i8_checked, u8_checked, u16_checked, i16_checked, u8

from skytemple_files.common.i18n_util import _, f
from skytemple_files.common.ppmdu_config.dungeon_data import Pmd2DungeonItemCategory
from skytemple_files.common.xml_util import (
    XmlValidateError,
    validate_xml_tag,
    validate_xml_attribs,
)
from skytemple_files.dungeon_data.mappa_bin import (
    XML_TRAP_LIST,
    XML_ITEM_LIST__TYPE__MONSTER_HOUSE,
    XML_ITEM_LIST,
    XML_FLOOR_LAYOUT__NUMBER,
    XML_ITEM_LIST__TYPE__SHOP,
    XML_TRAP__WEIGHT,
    XML_FLOOR_LAYOUT__WEATHER,
    XML_FLOOR,
    XML_FLOOR_LAYOUT__GENSET__EXTRA_HALLWAY_DENSITY,
    XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_TYPE,
    XML_FLOOR_LAYOUT__CHANCES,
    XML_FLOOR_LAYOUT__GENSET__FLOOR_CONNECTIVITY,
    XML_FLOOR_LAYOUT__MISCSET__ENEMY_IQ,
    XML_ITEM__WEIGHT,
    XML_FLOOR_LAYOUT__GENSET__INITIAL_ENEMY_DENSITY,
    XML_FLOOR_LAYOUT__FIXED_FLOOR_ID,
    XML_MONSTER__WEIGHT,
    XML_ITEM_LIST__TYPE,
    XML_ITEM__ID,
    XML_FLOOR_LAYOUT__TERRAINSET,
    XML_FLOOR_LIST,
    XML_ITEM_LIST__TYPE__UNK1,
    XML_FLOOR_LAYOUT__GENSET__TRAP_DENSITY,
    XML_CATEGORY__WEIGHT,
    XML_FLOOR_LAYOUT__CHANCES__MONSTER_HOUSE,
    XML_FLOOR_LAYOUT__MISCSET__IQ_BOOSTER_BOOST,
    XML_FLOOR_LAYOUT__CHANCES__UNUSED,
    XML_FLOOR_LAYOUT__GENSET__WATER_DENSITY,
    XML_FLOOR_LAYOUT__GENSET__MAX_COIN_AMOUNT,
    XML_FLOOR_LAYOUT__TERRAINSET__IMPERFECT_ROOMS,
    XML_ITEM_LIST__TYPE__FLOOR,
    XML_FLOOR_LAYOUT__STRUCTURE,
    XML_FLOOR_LAYOUT__TERRAINSET__UNK3,
    XML_FLOOR_LAYOUT__BGM,
    XML_FLOOR_LAYOUT__TERRAINSET__UNK1,
    XML_ITEM_LIST__TYPE__BURIED,
    XML_FLOOR_LAYOUT__TERRAINSET__UNK5,
    XML_FLOOR_LAYOUT__GENSET__BURIED_ITEM_DENSITY,
    XML_MAPPA,
    XML_FLOOR_LAYOUT__MISCSET,
    XML_ITEM_LIST__TYPE__UNK2,
    XML_FLOOR_LAYOUT__MISCSET__UNKE,
    XML_CATEGORY__NAME,
    XML_FLOOR_LAYOUT__MISCSET__KECLEON_SHOP_ITEM_POSITIONS,
    XML_FLOOR_LAYOUT__CHANCES__SHOP,
    XML_MONSTER,
    XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_USED,
    XML_FLOOR_LAYOUT__CHANCES__HIDDEN_STAIRS,
    XML_FLOOR_LAYOUT__CHANCES__STICKY_ITEM,
    XML_MONSTER__WEIGHT2,
    XML_FLOOR_LAYOUT__DARKNESS_LEVEL,
    XML_FLOOR_LAYOUT__GENSET__ROOM_DENSITY,
    XML_FLOOR_LAYOUT__TERRAINSET__UNK6,
    XML_MONSTER_LIST,
    XML_FLOOR_LAYOUT,
    XML_FLOOR_LAYOUT__TERRAINSET__UNK4,
    XML_TRAP__NAME,
    XML_FLOOR_LAYOUT__CHANCES__EMPTY_MONSTER_HOUSE,
    XML_FLOOR_LAYOUT__TERRAINSET__UNK7,
    XML_ITEM,
    XML_TRAP,
    XML_MONSTER__MD_INDEX,
    XML_FLOOR_LAYOUT__GENSET__ITEM_DENSITY,
    XML_FLOOR_LAYOUT__GENSET__DEAD_ENDS,
    XML_FLOOR_LAYOUT__TILESET,
    XML_FLOOR_LAYOUT__GENSET,
    XML_MONSTER__LEVEL,
    XML_FLOOR_LAYOUT__MISCSET__UNK_HIDDEN_STAIRS,
    XML_CATEGORY,
)
from skytemple_files.dungeon_data.mappa_bin.handler import MappaBinHandler
from skytemple_files.dungeon_data.mappa_bin.protocol import (
    MappaBinProtocol,
    MappaFloorProtocol,
    MappaFloorLayoutProtocol,
    MappaFloorStructureType,
    MappaFloorWeather,
    MappaFloorDarknessLevel,
    MappaMonsterProtocol,
    MappaTrapListProtocol,
    MappaTrapType,
    MappaItemListProtocol,
    GUARANTEED,
)


def mappa_to_xml(mappa: MappaBinProtocol) -> Element:
    mappa_xml = Element(XML_MAPPA)
    for i, floor_list in enumerate(mappa.floor_lists):
        floor_list_xml = Element(XML_FLOOR_LIST)
        for floor in floor_list:
            floor_xml = floor.to_xml()
            validate_xml_tag(floor_xml, XML_FLOOR)
            floor_list_xml.append(floor_xml)
        mappa_xml.append(floor_list_xml)
    return mappa_xml


def mappa_from_xml(
    ele: Element, items: Dict[str, Pmd2DungeonItemCategory]
) -> MappaBinProtocol:
    validate_xml_tag(ele, XML_MAPPA)
    floor_lists = []
    for x_floor_list in ele:
        floor_list = []
        validate_xml_tag(x_floor_list, XML_FLOOR_LIST)
        for x_floor in x_floor_list:
            floor_list.append(mappa_floor_from_xml(x_floor, items))
        floor_lists.append(floor_list)
    return MappaBinHandler.get_model_cls()(floor_lists)


def mappa_floor_to_xml(
    floor: MappaFloorProtocol,
    items_desc: Dict[int, Pmd2DungeonItemCategory],
    export_layout=True,
    export_monsters=True,
    export_traps=True,
    export_floor_items=True,
    export_shop_items=True,
    export_monster_house_items=True,
    export_buried_items=True,
    export_unk1_items=True,
    export_unk2_items=True,
) -> Element:
    floor_xml = Element(XML_FLOOR)

    if export_layout:
        layout_xml = mappa_floor_layout_to_xml(floor.layout)
        validate_xml_tag(layout_xml, XML_FLOOR_LAYOUT)
        floor_xml.append(layout_xml)

    if export_monsters:
        monsters_xml = Element(XML_MONSTER_LIST)
        for monster in floor.monsters:
            monster_xml = mappa_monster_to_xml(monster)
            validate_xml_tag(monster_xml, XML_MONSTER)
            monsters_xml.append(monster_xml)
        floor_xml.append(monsters_xml)

    if export_traps:
        traps_xml = mappa_trap_list_to_xml(floor.traps)
        validate_xml_tag(traps_xml, XML_TRAP_LIST)
        floor_xml.append(traps_xml)

    if export_floor_items:
        floor_items_xml = mappa_item_list_to_xml(floor.floor_items, items_desc)
        validate_xml_tag(floor_items_xml, XML_ITEM_LIST)
        floor_items_xml.set(XML_ITEM_LIST__TYPE, XML_ITEM_LIST__TYPE__FLOOR)
        floor_xml.append(floor_items_xml)

    if export_shop_items:
        shop_items_xml = mappa_item_list_to_xml(floor.shop_items, items_desc)
        validate_xml_tag(shop_items_xml, XML_ITEM_LIST)
        shop_items_xml.set(XML_ITEM_LIST__TYPE, XML_ITEM_LIST__TYPE__SHOP)
        floor_xml.append(shop_items_xml)

    if export_monster_house_items:
        monster_house_items_xml = mappa_item_list_to_xml(
            floor.monster_house_items, items_desc
        )
        validate_xml_tag(monster_house_items_xml, XML_ITEM_LIST)
        monster_house_items_xml.set(
            XML_ITEM_LIST__TYPE, XML_ITEM_LIST__TYPE__MONSTER_HOUSE
        )
        floor_xml.append(monster_house_items_xml)

    if export_buried_items:
        buried_items_xml = mappa_item_list_to_xml(floor.buried_items, items_desc)
        validate_xml_tag(buried_items_xml, XML_ITEM_LIST)
        buried_items_xml.set(XML_ITEM_LIST__TYPE, XML_ITEM_LIST__TYPE__BURIED)
        floor_xml.append(buried_items_xml)

    if export_unk1_items:
        unk_items1_xml = mappa_item_list_to_xml(floor.unk_items1, items_desc)
        validate_xml_tag(unk_items1_xml, XML_ITEM_LIST)
        unk_items1_xml.set(XML_ITEM_LIST__TYPE, XML_ITEM_LIST__TYPE__UNK1)
        floor_xml.append(unk_items1_xml)

    if export_unk2_items:
        unk_items2_xml = mappa_item_list_to_xml(floor.unk_items2, items_desc)
        validate_xml_tag(unk_items2_xml, XML_ITEM_LIST)
        unk_items2_xml.set(XML_ITEM_LIST__TYPE, XML_ITEM_LIST__TYPE__UNK2)
        floor_xml.append(unk_items2_xml)

    return floor_xml


class MappaFloorFromXmlDict(TypedDict):
    layout: Optional[MappaFloorLayoutProtocol]
    monsters: Optional[List[MappaMonsterProtocol]]
    traps: Optional[MappaTrapListProtocol]
    floor_items: Optional[MappaItemListProtocol]
    shop_items: Optional[MappaItemListProtocol]
    monster_house_items: Optional[MappaItemListProtocol]
    buried_items: Optional[MappaItemListProtocol]
    unk_items1: Optional[MappaItemListProtocol]
    unk_items2: Optional[MappaItemListProtocol]


def mappa_floor_from_xml(
    ele: Element, items: Dict[str, Pmd2DungeonItemCategory]
) -> MappaFloorProtocol:
    data: MappaFloorFromXmlDict = {
        "layout": None,
        "monsters": None,
        "traps": None,
        "floor_items": None,
        "shop_items": None,
        "monster_house_items": None,
        "buried_items": None,
        "unk_items1": None,
        "unk_items2": None,
    }
    for child in ele:
        if child.tag == XML_FLOOR_LAYOUT and data["layout"] is None:
            data["layout"] = mappa_floor_layout_from_xml(child)
        elif child.tag == XML_MONSTER_LIST and data["monsters"] is None:
            monsters = []
            for monster in child:
                monsters.append(mappa_monster_from_xml(monster))
            data["monsters"] = monsters
        elif child.tag == XML_TRAP_LIST and data["traps"] is None:
            data["traps"] = mappa_trap_list_from_xml(child)
        elif (
            child.tag == XML_ITEM_LIST
            and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__FLOOR
            and data["floor_items"] is None
        ):
            data["floor_items"] = mappa_item_list_from_xml(child, items)
        elif (
            child.tag == XML_ITEM_LIST
            and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__SHOP
            and data["shop_items"] is None
        ):
            data["shop_items"] = mappa_item_list_from_xml(child, items)
        elif (
            child.tag == XML_ITEM_LIST
            and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__MONSTER_HOUSE
            and data["monster_house_items"] is None
        ):
            data["monster_house_items"] = mappa_item_list_from_xml(child, items)
        elif (
            child.tag == XML_ITEM_LIST
            and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__BURIED
            and data["buried_items"] is None
        ):
            data["buried_items"] = mappa_item_list_from_xml(child, items)
        elif (
            child.tag == XML_ITEM_LIST
            and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__UNK1
            and data["unk_items1"] is None
        ):
            data["unk_items1"] = mappa_item_list_from_xml(child, items)
        elif (
            child.tag == XML_ITEM_LIST
            and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__UNK2
            and data["unk_items2"] is None
        ):
            data["unk_items2"] = mappa_item_list_from_xml(child, items)
        else:
            raise XmlValidateError(f(_("Floor parsing: Unexpected {child.tag}")))

    for k, v in data.items():
        if v is None:
            raise XmlValidateError(f(_("Missing {k} for Floor data.")))

    return MappaBinHandler.get_floor_model()(**data)  # type: ignore


def mappa_floor_xml_import(
    xml: Element, floor: MappaFloorProtocol, items: Dict[str, Pmd2DungeonItemCategory]
):
    """Imports all data available in the mappa floor XML into the given model."""
    for child in xml:
        if child.tag == XML_FLOOR_LAYOUT:
            floor_number_before = floor.layout.floor_number
            floor.layout = mappa_floor_layout_from_xml(child)
            floor.layout.floor_number = floor_number_before
        elif child.tag == XML_MONSTER_LIST:
            monsters = []
            for monster in child:
                monsters.append(mappa_monster_from_xml(monster))
            floor.monsters = monsters
        elif child.tag == XML_TRAP_LIST:
            floor.traps = mappa_trap_list_from_xml(child)
        elif (
            child.tag == XML_ITEM_LIST
            and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__FLOOR
        ):
            floor.floor_items = mappa_item_list_from_xml(child, items)
        elif (
            child.tag == XML_ITEM_LIST
            and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__SHOP
        ):
            floor.shop_items = mappa_item_list_from_xml(child, items)
        elif (
            child.tag == XML_ITEM_LIST
            and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__MONSTER_HOUSE
        ):
            floor.monster_house_items = mappa_item_list_from_xml(child, items)
        elif (
            child.tag == XML_ITEM_LIST
            and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__BURIED
        ):
            floor.buried_items = mappa_item_list_from_xml(child, items)
        elif (
            child.tag == XML_ITEM_LIST
            and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__UNK1
        ):
            floor.unk_items1 = mappa_item_list_from_xml(child, items)
        elif (
            child.tag == XML_ITEM_LIST
            and child.get(XML_ITEM_LIST__TYPE) == XML_ITEM_LIST__TYPE__UNK2
        ):
            floor.unk_items2 = mappa_item_list_from_xml(child, items)
        else:
            raise XmlValidateError(f(_("Floor parsing: Unexpected {child.tag}")))


def mappa_floor_layout_to_xml(mfl: MappaFloorLayoutProtocol) -> Element:
    xml_layout = Element(
        XML_FLOOR_LAYOUT,
        {
            XML_FLOOR_LAYOUT__STRUCTURE: MappaFloorStructureType(mfl.structure).name,
            XML_FLOOR_LAYOUT__TILESET: str(mfl.tileset_id),
            XML_FLOOR_LAYOUT__BGM: str(mfl.music_id),
            XML_FLOOR_LAYOUT__WEATHER: MappaFloorWeather(mfl.weather).name,
            XML_FLOOR_LAYOUT__NUMBER: str(mfl.floor_number),
            XML_FLOOR_LAYOUT__FIXED_FLOOR_ID: str(mfl.fixed_floor_id),
            XML_FLOOR_LAYOUT__DARKNESS_LEVEL: MappaFloorDarknessLevel(
                mfl.darkness_level
            ).name,
        },
    )
    xml_generator_settings = Element(
        XML_FLOOR_LAYOUT__GENSET,
        {
            XML_FLOOR_LAYOUT__GENSET__ROOM_DENSITY: str(mfl.room_density),
            XML_FLOOR_LAYOUT__GENSET__FLOOR_CONNECTIVITY: str(mfl.floor_connectivity),
            XML_FLOOR_LAYOUT__GENSET__INITIAL_ENEMY_DENSITY: str(
                mfl.initial_enemy_density
            ),
            XML_FLOOR_LAYOUT__GENSET__DEAD_ENDS: str(int(mfl.dead_ends)),
            XML_FLOOR_LAYOUT__GENSET__ITEM_DENSITY: str(mfl.item_density),
            XML_FLOOR_LAYOUT__GENSET__TRAP_DENSITY: str(mfl.trap_density),
            XML_FLOOR_LAYOUT__GENSET__EXTRA_HALLWAY_DENSITY: str(
                mfl.extra_hallway_density
            ),
            XML_FLOOR_LAYOUT__GENSET__BURIED_ITEM_DENSITY: str(mfl.buried_item_density),
            XML_FLOOR_LAYOUT__GENSET__WATER_DENSITY: str(mfl.water_density),
            XML_FLOOR_LAYOUT__GENSET__MAX_COIN_AMOUNT: str(mfl.max_coin_amount),
        },
    )
    xml_chances = Element(
        XML_FLOOR_LAYOUT__CHANCES,
        {
            XML_FLOOR_LAYOUT__CHANCES__SHOP: str(mfl.kecleon_shop_chance),
            XML_FLOOR_LAYOUT__CHANCES__MONSTER_HOUSE: str(mfl.monster_house_chance),
            XML_FLOOR_LAYOUT__CHANCES__UNUSED: str(mfl.unused_chance),
            XML_FLOOR_LAYOUT__CHANCES__STICKY_ITEM: str(mfl.sticky_item_chance),
            XML_FLOOR_LAYOUT__CHANCES__EMPTY_MONSTER_HOUSE: str(
                mfl.empty_monster_house_chance
            ),
            XML_FLOOR_LAYOUT__CHANCES__HIDDEN_STAIRS: str(
                mfl.hidden_stairs_spawn_chance
            ),
        },
    )
    xml_terrain_settings = Element(
        XML_FLOOR_LAYOUT__TERRAINSET,
        {
            XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_USED: str(
                int(mfl.terrain_settings.has_secondary_terrain)
            ),
            XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_TYPE: str(mfl.secondary_terrain),
            XML_FLOOR_LAYOUT__TERRAINSET__IMPERFECT_ROOMS: str(
                int(mfl.terrain_settings.generate_imperfect_rooms)
            ),
            XML_FLOOR_LAYOUT__TERRAINSET__UNK1: str(int(mfl.terrain_settings.unk1)),
            XML_FLOOR_LAYOUT__TERRAINSET__UNK3: str(int(mfl.terrain_settings.unk3)),
            XML_FLOOR_LAYOUT__TERRAINSET__UNK4: str(int(mfl.terrain_settings.unk4)),
            XML_FLOOR_LAYOUT__TERRAINSET__UNK5: str(int(mfl.terrain_settings.unk5)),
            XML_FLOOR_LAYOUT__TERRAINSET__UNK6: str(int(mfl.terrain_settings.unk6)),
            XML_FLOOR_LAYOUT__TERRAINSET__UNK7: str(int(mfl.terrain_settings.unk7)),
        },
    )
    xml_misc = Element(
        XML_FLOOR_LAYOUT__MISCSET,
        {
            XML_FLOOR_LAYOUT__MISCSET__UNKE: str(int(mfl.unk_e)),
            XML_FLOOR_LAYOUT__MISCSET__KECLEON_SHOP_ITEM_POSITIONS: str(
                mfl.kecleon_shop_item_positions
            ),
            XML_FLOOR_LAYOUT__MISCSET__UNK_HIDDEN_STAIRS: str(mfl.unk_hidden_stairs),
            XML_FLOOR_LAYOUT__MISCSET__ENEMY_IQ: str(mfl.enemy_iq),
            XML_FLOOR_LAYOUT__MISCSET__IQ_BOOSTER_BOOST: str(mfl.iq_booster_boost),
        },
    )

    xml_layout.append(xml_generator_settings)
    xml_layout.append(xml_chances)
    xml_layout.append(xml_terrain_settings)
    xml_layout.append(xml_misc)

    return xml_layout


@no_type_check
def mappa_floor_layout_from_xml(ele: Element) -> MappaFloorLayoutProtocol:
    validate_xml_tag(ele, XML_FLOOR_LAYOUT)
    generator_settings = None
    chances = None
    terrain_settings = None
    misc = None
    for child in ele:
        if child.tag == XML_FLOOR_LAYOUT__GENSET:
            generator_settings = child
        elif child.tag == XML_FLOOR_LAYOUT__CHANCES:
            chances = child
        elif child.tag == XML_FLOOR_LAYOUT__TERRAINSET:
            terrain_settings = child
        elif child.tag == XML_FLOOR_LAYOUT__MISCSET:
            misc = child
        else:
            raise XmlValidateError(
                f(_("Unexpected sub-node for {XML_FLOOR_LAYOUT}: {child.tag}"))
            )

    if generator_settings is None:
        raise XmlValidateError(
            f(_("{XML_FLOOR_LAYOUT__GENSET} missing for {XML_FLOOR_LAYOUT}."))
        )

    if chances is None:
        raise XmlValidateError(
            f(_("{XML_FLOOR_LAYOUT__CHANCES} missing for {XML_FLOOR_LAYOUT}."))
        )

    if terrain_settings is None:
        raise XmlValidateError(
            f(_("{XML_FLOOR_LAYOUT__TERRAINSET} missing for {XML_FLOOR_LAYOUT}."))
        )

    if misc is None:
        raise XmlValidateError(
            f(_("{XML_FLOOR_LAYOUT__MISCSET} missing for {XML_FLOOR_LAYOUT}."))
        )

    validate_xml_attribs(
        ele,
        [
            XML_FLOOR_LAYOUT__STRUCTURE,
            XML_FLOOR_LAYOUT__TILESET,
            XML_FLOOR_LAYOUT__BGM,
            XML_FLOOR_LAYOUT__WEATHER,
            XML_FLOOR_LAYOUT__NUMBER,
            XML_FLOOR_LAYOUT__FIXED_FLOOR_ID,
            XML_FLOOR_LAYOUT__DARKNESS_LEVEL,
        ],
    )

    validate_xml_attribs(
        generator_settings,
        [
            XML_FLOOR_LAYOUT__GENSET__ROOM_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__FLOOR_CONNECTIVITY,
            XML_FLOOR_LAYOUT__GENSET__INITIAL_ENEMY_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__DEAD_ENDS,
            XML_FLOOR_LAYOUT__GENSET__ITEM_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__TRAP_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__EXTRA_HALLWAY_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__BURIED_ITEM_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__WATER_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__MAX_COIN_AMOUNT,
        ],
    )

    validate_xml_attribs(
        chances,
        [
            XML_FLOOR_LAYOUT__CHANCES__SHOP,
            XML_FLOOR_LAYOUT__CHANCES__MONSTER_HOUSE,
            XML_FLOOR_LAYOUT__CHANCES__UNUSED,
            XML_FLOOR_LAYOUT__CHANCES__STICKY_ITEM,
            XML_FLOOR_LAYOUT__CHANCES__EMPTY_MONSTER_HOUSE,
            XML_FLOOR_LAYOUT__CHANCES__HIDDEN_STAIRS,
        ],
    )

    validate_xml_attribs(
        terrain_settings,
        [
            XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_USED,
            XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_TYPE,
            XML_FLOOR_LAYOUT__TERRAINSET__IMPERFECT_ROOMS,
            XML_FLOOR_LAYOUT__TERRAINSET__UNK1,
            XML_FLOOR_LAYOUT__TERRAINSET__UNK3,
            XML_FLOOR_LAYOUT__TERRAINSET__UNK4,
            XML_FLOOR_LAYOUT__TERRAINSET__UNK5,
            XML_FLOOR_LAYOUT__TERRAINSET__UNK6,
            XML_FLOOR_LAYOUT__TERRAINSET__UNK7,
        ],
    )

    validate_xml_attribs(
        misc,
        [
            XML_FLOOR_LAYOUT__MISCSET__UNKE,
            XML_FLOOR_LAYOUT__MISCSET__KECLEON_SHOP_ITEM_POSITIONS,
            XML_FLOOR_LAYOUT__MISCSET__UNK_HIDDEN_STAIRS,
            XML_FLOOR_LAYOUT__MISCSET__ENEMY_IQ,
            XML_FLOOR_LAYOUT__MISCSET__IQ_BOOSTER_BOOST,
        ],
    )

    if not hasattr(MappaFloorStructureType, ele.get(XML_FLOOR_LAYOUT__STRUCTURE)):
        raise XmlValidateError(
            f(_("Invalid structure type {ele.get(XML_FLOOR_LAYOUT__STRUCTURE)}"))
        )
    structure = u8(
        getattr(MappaFloorStructureType, ele.get(XML_FLOOR_LAYOUT__STRUCTURE)).value
    )

    if not hasattr(MappaFloorWeather, ele.get(XML_FLOOR_LAYOUT__WEATHER)):
        raise XmlValidateError(
            f(_("Invalid weather type {ele.get(XML_FLOOR_LAYOUT__WEATHER)}"))
        )
    weather = u8(getattr(MappaFloorWeather, ele.get(XML_FLOOR_LAYOUT__WEATHER)).value)

    if not hasattr(MappaFloorDarknessLevel, ele.get(XML_FLOOR_LAYOUT__DARKNESS_LEVEL)):
        raise XmlValidateError(
            f(
                _(
                    "Invalid darkness level type {ele.get(XML_FLOOR_LAYOUT__DARKNESS_LEVEL)}"
                )
            )
        )
    darkness_level = u8(
        getattr(
            MappaFloorDarknessLevel, ele.get(XML_FLOOR_LAYOUT__DARKNESS_LEVEL)
        ).value
    )

    return MappaBinHandler.get_floor_layout_model()(
        structure=structure,
        room_density=i8_checked(
            int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__ROOM_DENSITY))
        ),
        tileset_id=u8_checked(int(ele.get(XML_FLOOR_LAYOUT__TILESET))),
        music_id=u8_checked(int(ele.get(XML_FLOOR_LAYOUT__BGM))),
        weather=weather,
        floor_connectivity=u8_checked(
            int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__FLOOR_CONNECTIVITY))
        ),
        initial_enemy_density=i8_checked(
            int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__INITIAL_ENEMY_DENSITY))
        ),
        kecleon_shop_chance=u8_checked(
            int(chances.get(XML_FLOOR_LAYOUT__CHANCES__SHOP))
        ),
        monster_house_chance=u8_checked(
            int(chances.get(XML_FLOOR_LAYOUT__CHANCES__MONSTER_HOUSE))
        ),
        unused_chance=u8_checked(int(chances.get(XML_FLOOR_LAYOUT__CHANCES__UNUSED))),
        sticky_item_chance=u8_checked(
            int(chances.get(XML_FLOOR_LAYOUT__CHANCES__STICKY_ITEM))
        ),
        dead_ends=bool(
            int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__DEAD_ENDS))
        ),
        secondary_terrain=u8_checked(
            int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_TYPE))
        ),
        terrain_settings=MappaBinHandler.get_terrain_settings_model()(
            has_secondary_terrain=bool(
                int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_USED))
            ),
            unk1=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__UNK1))),
            generate_imperfect_rooms=bool(
                int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__IMPERFECT_ROOMS))
            ),
            unk3=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__UNK3))),
            unk4=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__UNK4))),
            unk5=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__UNK5))),
            unk6=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__UNK6))),
            unk7=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__UNK7))),
        ),
        unk_e=bool(int(misc.get(XML_FLOOR_LAYOUT__MISCSET__UNKE))),
        item_density=u8_checked(
            int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__ITEM_DENSITY))
        ),
        trap_density=u8_checked(
            int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__TRAP_DENSITY))
        ),
        floor_number=u8_checked(int(ele.get(XML_FLOOR_LAYOUT__NUMBER))),
        fixed_floor_id=u8_checked(int(ele.get(XML_FLOOR_LAYOUT__FIXED_FLOOR_ID))),
        extra_hallway_density=u8_checked(
            int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__EXTRA_HALLWAY_DENSITY))
        ),
        buried_item_density=u8_checked(
            int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__BURIED_ITEM_DENSITY))
        ),
        water_density=u8_checked(
            int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__WATER_DENSITY))
        ),
        darkness_level=darkness_level,
        max_coin_amount=int(
            generator_settings.get(XML_FLOOR_LAYOUT__GENSET__MAX_COIN_AMOUNT)
        ),
        kecleon_shop_item_positions=u8_checked(
            int(misc.get(XML_FLOOR_LAYOUT__MISCSET__KECLEON_SHOP_ITEM_POSITIONS))
        ),
        empty_monster_house_chance=u8_checked(
            int(chances.get(XML_FLOOR_LAYOUT__CHANCES__EMPTY_MONSTER_HOUSE))
        ),
        unk_hidden_stairs=u8_checked(
            int(misc.get(XML_FLOOR_LAYOUT__MISCSET__UNK_HIDDEN_STAIRS))
        ),
        hidden_stairs_spawn_chance=u8_checked(
            int(chances.get(XML_FLOOR_LAYOUT__CHANCES__HIDDEN_STAIRS))
        ),
        enemy_iq=u16_checked(int(misc.get(XML_FLOOR_LAYOUT__MISCSET__ENEMY_IQ))),
        iq_booster_boost=i16_checked(
            int(misc.get(XML_FLOOR_LAYOUT__MISCSET__IQ_BOOSTER_BOOST))
        ),
    )


def mappa_monster_to_xml(monster: MappaMonsterProtocol) -> Element:
    return Element(
        XML_MONSTER,
        {
            XML_MONSTER__LEVEL: str(monster.level),
            XML_MONSTER__WEIGHT: str(monster.main_spawn_weight),
            XML_MONSTER__WEIGHT2: str(monster.monster_house_spawn_weight),
            XML_MONSTER__MD_INDEX: str(monster.md_index),
        },
    )


@no_type_check
def mappa_monster_from_xml(ele: Element) -> MappaMonsterProtocol:
    validate_xml_tag(ele, XML_MONSTER)
    validate_xml_attribs(
        ele,
        [
            XML_MONSTER__LEVEL,
            XML_MONSTER__WEIGHT,
            XML_MONSTER__WEIGHT2,
            XML_MONSTER__MD_INDEX,
        ],
    )
    return MappaBinHandler.get_monster_model()(
        u8_checked(int(ele.get(XML_MONSTER__LEVEL))),
        u16_checked(int(ele.get(XML_MONSTER__WEIGHT))),
        u16_checked(int(ele.get(XML_MONSTER__WEIGHT2))),
        u16_checked(int(ele.get(XML_MONSTER__MD_INDEX))),
    )


def mappa_trap_list_to_xml(trap_list: MappaTrapListProtocol) -> Element:
    xml_trap_list = Element(XML_TRAP_LIST)
    for trap, weight in trap_list.weights.items():
        xml_trap_list.append(
            Element(
                XML_TRAP,
                {
                    XML_TRAP__NAME: MappaTrapType(trap).name,
                    XML_TRAP__WEIGHT: str(weight),
                },
            )
        )
    return xml_trap_list


def mappa_trap_list_from_xml(ele: Element) -> MappaTrapListProtocol:
    validate_xml_tag(ele, XML_TRAP_LIST)
    weights = {}
    for child in ele:
        validate_xml_tag(child, XML_TRAP)
        validate_xml_attribs(child, [XML_TRAP__NAME, XML_TRAP__WEIGHT])
        name = child.get(XML_TRAP__NAME)
        assert name is not None
        if not hasattr(MappaTrapType, name):
            raise XmlValidateError(f(_("Unknown trap {name}.")))
        weights[getattr(MappaTrapType, name).value] = u16_checked(
            int(child.get(XML_TRAP__WEIGHT))  # type: ignore
        )
    try:
        return MappaBinHandler.get_trap_list_model()(weights)
    except ValueError as ex:
        raise XmlValidateError(
            _("Trap lists need an entry for all of the 25 traps")
        ) from ex


def mappa_item_list_to_xml(
    item_list: MappaItemListProtocol, items_desc: Dict[int, Pmd2DungeonItemCategory]
) -> Element:
    xml_item_list = Element(XML_ITEM_LIST)
    for category, probability in item_list.categories.items():
        weight = "GUARANTEED" if probability == GUARANTEED else str(probability)
        xml_category = Element(
            XML_CATEGORY,
            {
                XML_CATEGORY__NAME: items_desc[category].name,
                XML_CATEGORY__WEIGHT: str(weight),
            },
        )
        xml_item_list.append(xml_category)
    for item, probability in item_list.items.items():
        weight = "GUARANTEED" if probability == GUARANTEED else str(probability)
        xml_item = Element(
            XML_ITEM, {XML_ITEM__ID: str(item), XML_ITEM__WEIGHT: str(weight)}
        )
        xml_item_list.append(xml_item)

    return xml_item_list


def mappa_item_list_from_xml(
    ele: Element, items_desc: Dict[str, Pmd2DungeonItemCategory]
) -> MappaItemListProtocol:
    validate_xml_tag(ele, XML_ITEM_LIST)
    categories = {}
    items = {}
    for child in ele:
        if child.tag == XML_CATEGORY:
            validate_xml_attribs(child, [XML_CATEGORY__NAME, XML_CATEGORY__WEIGHT])
            name = child.get(XML_CATEGORY__NAME)
            if name not in items_desc:
                raise XmlValidateError(f"Unknown item category {name}.")
            assert name is not None
            weight_str = child.get(XML_CATEGORY__WEIGHT)
            assert weight_str is not None
            weight = int(weight_str) if weight_str != "GUARANTEED" else GUARANTEED
            categories[items_desc[name].value] = weight
        elif child.tag == XML_ITEM:
            validate_xml_attribs(child, [XML_ITEM__ID, XML_ITEM__WEIGHT])
            weight_str = child.get(XML_ITEM__WEIGHT)
            assert weight_str is not None
            weight = int(weight_str) if weight_str != "GUARANTEED" else GUARANTEED
            items[int(child.get(XML_ITEM__ID))] = weight  # type: ignore
        else:
            raise XmlValidateError(
                f"Unexpected sub-node for {XML_ITEM_LIST}: {child.tag}"
            )
    return MappaBinHandler.get_item_list_model()(categories, items)
