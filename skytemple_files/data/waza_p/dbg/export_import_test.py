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
from skytemple_files.data.waza_p.writer import WazaPWriter

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
waza_p_bin = rom.getFileByName('BALANCE/waza_p.bin')
waza_p = FileType.WAZA_P.deserialize(waza_p_bin)
sir0_pointers_before = FileType.SIR0.deserialize(waza_p_bin).content_pointer_offsets

print("Moves")
for i, move in enumerate(waza_p.moves):
    print(i, move)
print("Learnsets")
for learnset in waza_p.learnsets:
    print(learnset)

sir0_pointers_after = WazaPWriter(waza_p).write()[1]
bin_after = FileType.WAZA_P.serialize(waza_p)

with open('/tmp/before.bin', 'wb') as f:
    f.write(waza_p_bin)

with open('/tmp/after.bin', 'wb') as f:
    f.write(bin_after)

#assert sir0_pointers_before == sir0_pointers_after
assert FileType.WAZA_P.deserialize(bin_after) == waza_p
