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
import os
from xml.dom import minidom
from xml.etree.ElementTree import Element

from xml.etree import ElementTree

from ndspy.rom import NintendoDSRom

from skytemple_files.dungeon_data.mappa_bin import XML_FLOOR_LIST
from skytemple_files.dungeon_data.mappa_bin.handler import MappaBinHandler
from skytemple_files.dungeon_data.mappa_bin.mappa_xml import mappa_floor_xml_export, mappa_floor_xml_import
from skytemple_files.dungeon_data.mappa_bin.model import MappaBin

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(output_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, '4261 - Pokemon Mystery Dungeon Explorers of Sky (U)(Xenophobia).nds'))

mappa_bin = rom.getFileByName('BALANCE/mappa_s.bin')
mappa = MappaBinHandler.deserialize(mappa_bin)
assert mappa == MappaBinHandler.deserialize(mappa_bin)


def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def write_xml(xml, fn):
    with open(os.path.join(output_dir, fn), 'w') as f:
        f.write(prettify(xml))


def test_eql_switch(to_test, if_false, if_true, cond):
    if cond:
        assert to_test == if_true
        return
    assert to_test == if_false


def test_partial(floor_to_import_into, source_floor, xml_fn, layout, monsters, traps, floor_items, shop_items,
                 monster_house_items, unk1_items, unk2_items, buried_items):
    xml = ElementTree.parse(os.path.join(output_dir, xml_fn))
    layout_before = floor_to_import_into.layout
    monsters_before = floor_to_import_into.monsters
    traps_before = floor_to_import_into.traps
    floor_items_before = floor_to_import_into.floor_items
    shop_items_before = floor_to_import_into.shop_items
    monster_house_items_before = floor_to_import_into.monster_house_items
    unk_items1_before = floor_to_import_into.unk_items1
    unk_items2_before = floor_to_import_into.unk_items2
    buried_items_before = floor_to_import_into.buried_items
    mappa_floor_xml_import(xml.getroot(), floor_to_import_into)
    test_eql_switch(floor_to_import_into.layout, layout_before, source_floor.layout, layout)
    test_eql_switch(floor_to_import_into.monsters, monsters_before, source_floor.monsters, monsters)
    test_eql_switch(floor_to_import_into.traps, traps_before, source_floor.traps, traps)
    test_eql_switch(floor_to_import_into.floor_items, floor_items_before, source_floor.floor_items, floor_items)
    test_eql_switch(floor_to_import_into.shop_items, shop_items_before, source_floor.shop_items, shop_items)
    test_eql_switch(floor_to_import_into.monster_house_items, monster_house_items_before, source_floor.monster_house_items, monster_house_items)
    test_eql_switch(floor_to_import_into.unk_items1, unk_items1_before, source_floor.unk_items1, unk1_items)
    test_eql_switch(floor_to_import_into.unk_items2, unk_items2_before, source_floor.unk_items2, unk2_items)
    test_eql_switch(floor_to_import_into.buried_items, buried_items_before, source_floor.buried_items, buried_items)


# Test built-in model full export
"""
for i, floor_list in enumerate(mappa.floor_lists):
    print(i)
    floor_list_xml = Element(XML_FLOOR_LIST)
    for floor in floor_list:
        floor_xml = floor.to_xml()
        floor_list_xml.append(floor_xml)
    write_xml(floor_list_xml, f'floor_list{i}.xml')
"""

# Test partial export functions with Beach Cave floor 1
floor = mappa.floor_lists[1][0]

# Layout only
write_xml(mappa_floor_xml_export(
    floor,
    export_layout=True, export_monsters=False, export_traps=False,
    export_floor_items=False, export_shop_items=False, export_monster_house_items=False,
    export_unk1_items=False, export_unk2_items=False, export_buried_items=False
), 'bc1_layout.xml')
# Monsters only
write_xml(mappa_floor_xml_export(
    floor,
    export_layout=False, export_monsters=True, export_traps=False,
    export_floor_items=False, export_shop_items=False, export_monster_house_items=False,
    export_unk1_items=False, export_unk2_items=False, export_buried_items=False
), 'bc1_monsters.xml')
# Traps only
write_xml(mappa_floor_xml_export(
    floor,
    export_layout=False, export_monsters=False, export_traps=True,
    export_floor_items=False, export_shop_items=False, export_monster_house_items=False,
    export_unk1_items=False, export_unk2_items=False, export_buried_items=False
), 'bc1_traps.xml')
# Floor items only
write_xml(mappa_floor_xml_export(
    floor,
    export_layout=False, export_monsters=False, export_traps=False,
    export_floor_items=True, export_shop_items=False, export_monster_house_items=False,
    export_unk1_items=False, export_unk2_items=False, export_buried_items=False
), 'bc1_floor_items.xml')
# Shop items and monsters
write_xml(mappa_floor_xml_export(
    floor,
    export_layout=False, export_monsters=True, export_traps=False,
    export_floor_items=False, export_shop_items=True, export_monster_house_items=False,
    export_unk1_items=False, export_unk2_items=False, export_buried_items=False
), 'bc1_shop_items_monsters.xml')
# Full
write_xml(mappa_floor_xml_export(
    floor
), 'bc1.xml')

# TODO test partial import
floor_to_import_into = mappa.floor_lists[0][0]


test_partial(floor_to_import_into, floor, 'bc1_layout.xml',
             layout=True, monsters=False, traps=False,
             floor_items=False, shop_items=False, monster_house_items=False,
             unk1_items=False, unk2_items=False, buried_items=False
)
test_partial(floor_to_import_into, floor, 'bc1_monsters.xml',
             layout=False, monsters=True, traps=False,
             floor_items=False, shop_items=False, monster_house_items=False,
             unk1_items=False, unk2_items=False, buried_items=False
)
test_partial(floor_to_import_into, floor, 'bc1_traps.xml',
             layout=False, monsters=False, traps=False,
             floor_items=False, shop_items=False, monster_house_items=False,
             unk1_items=False, unk2_items=False, buried_items=False
)
test_partial(floor_to_import_into, floor, 'bc1_floor_items.xml',
             layout=False, monsters=False, traps=False,
             floor_items=True, shop_items=False, monster_house_items=False,
             unk1_items=False, unk2_items=False, buried_items=False
)
test_partial(floor_to_import_into, floor, 'bc1_shop_items_monsters.xml',
             layout=False, monsters=True, traps=False,
             floor_items=False, shop_items=True, monster_house_items=False,
             unk1_items=False, unk2_items=False, buried_items=False
)
test_partial(floor_to_import_into, floor, 'bc1.xml',
             layout=True, monsters=True, traps=True,
             floor_items=True, shop_items=True, monster_house_items=True,
             unk1_items=True, unk2_items=False, buried_items=True
)


#assert mappa == MappaBin.from_xml(xml)
