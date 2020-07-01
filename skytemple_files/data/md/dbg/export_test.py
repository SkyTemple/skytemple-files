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

from skytemple_files.common.types.file_types import FileType
from skytemple_files.data.md.handler import MdHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
md_bin = rom.getFileByName('BALANCE/monster.md')
md_model = MdHandler.deserialize(md_bin)

unknames = ["unk31", "unk1", "unk17", "unk18", "unk19", "unk20", "unk21", "unk27", "unk28", "unk29", "unk30"]
for unkname in unknames:
    unks = {}
    strings = FileType.STR.deserialize(rom.getFileByName('MESSAGE/text_e.str'))

    for entry in md_model:
        v = getattr(entry, unkname)
        if v not in unks:
            unks[v] = []
        unks[v].append(strings.strings[8736 + entry.md_index_base])

    print("=========================")
    print(unkname)
    for k, v in unks.items():
        print(k, f" (count {len(v)}:", v)
