"""Exports all DPCIs from the dungeon.bin"""
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
from skytemple_files.graphics.dpci.model import Dpci
from skytemple_files.graphics.dpl.model import Dpl

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(os.path.join(output_dir, 'raw'), exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))

dungeon_bin_bin = rom.getFileByName('DUNGEON/dungeon.bin')
static_data = get_ppmdu_config_for_rom(rom)
dungeon_bin = DungeonBinHandler.deserialize(dungeon_bin_bin, static_data)

for i, file in enumerate(dungeon_bin):
    fn = dungeon_bin.get_filename(i)
    if fn.endswith('.dpci'):
        file: Dpci
        pal_file: Dpl = dungeon_bin.get(fn.replace('.dpci', '.dpl'))
        print(fn)
        file.tiles_to_pil(pal_file.palettes).save(os.path.join(output_dir, fn + '.png'))
