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

from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from skytemple_files.data.item_p.writer import ItemPWriter
from skytemple_files.dungeon_data.mappa_bin.item_list import MappaItemCategory

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
item_p_bin = rom.getFileByName('BALANCE/item_p.bin')
item_p = FileType.ITEM_P.deserialize(item_p_bin)

cats = {x: [] for x in MappaItemCategory}

for idx, entry in enumerate(item_p.item_list):
    cats[entry.category_enum()].append(idx)

for cat, items in cats.items():
    print(f'<Category id="{cat.value}" name="{cat.name_localized}">')
    for item in items:
        print(f'  <Item>{item}</Item>')
    print(f'</Category>')

assert MappaItemCategory.UNKC == MappaItemCategory.UNKC
