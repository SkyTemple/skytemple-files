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
from decimal import Decimal
from typing import List

from xml.etree import ElementTree

from ndspy.rom import NintendoDSRom

from skytemple_files.dungeon_data.mappa_bin.handler import MappaBinHandler
from skytemple_files.dungeon_data.mappa_bin.item_list import MappaItemCategory, GUARANTEED

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(output_dir, exist_ok=True)

#rom = NintendoDSRom.fromFile(os.path.join(base_dir, '/tmp/x.nds'))
rom = NintendoDSRom.fromFile('/tmp/test.nds')

with open('/home/marco/dev/skytemple/skytemple/ppmd_statsutil/sky_rom/data/BALANCE/mappa_s.bin', 'rb') as f:
    rom.setFileByName('BALANCE/mappa_s.bin', f.read())
    rom.saveToFile('/tmp/test2.nds')

mappa_bin = rom.getFileByName('BALANCE/mappa_s.bin')
mappa = MappaBinHandler.deserialize(mappa_bin)

items = []
lens_monsters = []
tilesets = set()

for fl in mappa.floor_lists:
    for floor in fl:
        for monster in floor.monsters:
            assert monster.weight == monster.weight2
        tilesets.add(floor.layout.water_density)
        items.append(floor.monster_house_items)
        items.append(floor.shop_items)
        items.append(floor.buried_items)
        items.append(floor.floor_items)
        items.append(floor.unk_items1)
        items.append(floor.unk_items2)

item_list_with_guaranteed_items = []
for item_list in items:
    has_guaranteed = False
    for category in item_list.categories.values():
        if category == GUARANTEED:
            has_guaranteed = True
            break
    for item in item_list.items.values():
        if item == GUARANTEED:
            has_guaranteed = True
            break
    if has_guaranteed:
        item_list_with_guaranteed_items.append(item_list)



print(".")


for monster in mappa.floor_lists[4][2].monsters:
    print(monster)
