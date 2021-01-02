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

from skytemple_files.dungeon_data.mappa_bin.handler import MappaBinHandler

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(output_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us_unpatched.nds'))

mappa_bin = rom.getFileByName('BALANCE/mappa_s.bin')
mappa = MappaBinHandler.deserialize(mappa_bin)

mappa_after_bin = MappaBinHandler.serialize(mappa)

with open('/tmp/before.bin', 'wb') as f:
    f.write(mappa_bin)

with open('/tmp/after.bin', 'wb') as f:
    f.write(mappa_after_bin)

mappa_after = MappaBinHandler.deserialize(mappa_after_bin)
for i_fl in range(0, len(mappa.floor_lists)):
    for i in range(0, len(mappa.floor_lists[i_fl])):
        assert mappa.floor_lists[i_fl][i].layout == mappa_after.floor_lists[i_fl][i].layout
        assert mappa.floor_lists[i_fl][i].monsters == mappa_after.floor_lists[i_fl][i].monsters
        assert mappa.floor_lists[i_fl][i].traps == mappa_after.floor_lists[i_fl][i].traps
        assert mappa.floor_lists[i_fl][i].floor_items == mappa_after.floor_lists[i_fl][i].floor_items
        assert mappa.floor_lists[i_fl][i].shop_items == mappa_after.floor_lists[i_fl][i].shop_items
        assert mappa.floor_lists[i_fl][i].buried_items == mappa_after.floor_lists[i_fl][i].buried_items
        assert mappa.floor_lists[i_fl][i].monster_house_items == mappa_after.floor_lists[i_fl][i].monster_house_items
        assert mappa.floor_lists[i_fl][i].unk_items1 == mappa_after.floor_lists[i_fl][i].unk_items1
        assert mappa.floor_lists[i_fl][i].unk_items2 == mappa_after.floor_lists[i_fl][i].unk_items2
assert mappa == mappa_after
assert len(mappa_bin) % 16 == 0
assert len(mappa_after_bin) % 16 == 0

rom.setFileByName('BALANCE/mappa_s.bin', mappa_after_bin)
rom.saveToFile(os.path.join(output_dir, 'mappa_save_test.nds'))

