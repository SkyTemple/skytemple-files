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
import os

from ndspy.rom import NintendoDSRom

from skytemple_files.dungeon_data.mappa_bin.handler import MappaBinHandler
from skytemple_files.dungeon_data.mappa_bin.item_list import MappaItemCategory

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(output_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, '/tmp/x.nds'))
#rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))

mappa_bin = rom.getFileByName('BALANCE/mappa_s.bin')
mappa = MappaBinHandler.deserialize(mappa_bin)

items = []
lens_monsters = []

for fl in mappa.floor_lists:
    for floor in fl:
        items.append(floor.monster_house_items)
        items.append(floor.shop_items)
        items.append(floor.buried_items)
        items.append(floor.floor_items)
        items.append(floor.unk_items1)
        items.append(floor.unk_items2)

items_with_link_boxes = 0
for item_list in items:
    if MappaItemCategory.LINK_BOX in item_list.categories:
        items_with_link_boxes += 1

print(len(items), items_with_link_boxes)
