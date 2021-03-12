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

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
item_p_bin = rom.getFileByName('BALANCE/item_p.bin')
item_p = FileType.ITEM_P.deserialize(item_p_bin)
sir0_pointers_before = FileType.SIR0.deserialize(item_p_bin).content_pointer_offsets

sir0_pointers_after = ItemPWriter(item_p).write()[1]
bin_after = FileType.ITEM_P.serialize(item_p)

with open('/tmp/before.bin', 'wb') as f:
    f.write(item_p_bin)

with open('/tmp/after.bin', 'wb') as f:
    f.write(bin_after)

assert sir0_pointers_before == sir0_pointers_after
assert FileType.ITEM_P.deserialize(bin_after) == item_p
