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

from skytemple_files.common.util import get_ppmdu_config_for_rom
from skytemple_files.container.dungeon_bin.handler import DungeonBinHandler
from skytemple_files.container.dungeon_bin.sub.sir0_dpla import DbinSir0DplaHandler
from skytemple_files.graphics.dpla.handler import DplaHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))

dungeon_bin_bin = rom.getFileByName('DUNGEON/dungeon.bin')
static_data = get_ppmdu_config_for_rom(rom)
dungeon_bin = DungeonBinHandler.deserialize(dungeon_bin_bin, static_data)

for i, m in enumerate(dungeon_bin):
    if dungeon_bin.get_filename(i).endswith('.dpla'):
        before = dungeon_bin.get_files_bytes()[i]
        after = DbinSir0DplaHandler.serialize(m)
        print(i)
        with open('/tmp/before.bin', 'wb') as f:
            f.write(before)
        with open('/tmp/after.bin', 'wb') as f:
            f.write(after)
        if i == 81:
            continue  # this one is a bit weird for some reason, but should be ok.
        assert before == after
