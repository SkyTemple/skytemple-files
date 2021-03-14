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
from skytemple_files.data.item_s_p.writer import ItemSPWriter

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
item_sp_bin = rom.getFileByName('BALANCE/item_s_p.bin')
item_sp = FileType.ITEM_SP.deserialize(item_sp_bin)
sir0_pointers_before = FileType.SIR0.deserialize(item_sp_bin).content_pointer_offsets

sir0_pointers_after = ItemSPWriter(item_sp).write()[1]
bin_after = FileType.ITEM_SP.serialize(item_sp)

with open('/tmp/before.bin', 'wb') as f:
    f.write(item_sp_bin)

with open('/tmp/after.bin', 'wb') as f:
    f.write(bin_after)

for entry in item_sp.item_list:
    print(entry)

assert sir0_pointers_before == sir0_pointers_after
assert FileType.ITEM_SP.deserialize(bin_after) == item_sp
