"""Replaces the P** of dungeon tileset 1 with dungeon tileset 2."""
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
import itertools
import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import get_ppmdu_config_for_rom
from skytemple_files.container.dungeon_bin.handler import DungeonBinHandler
from skytemple_files.graphics.dma.model import Dma
from skytemple_files.graphics.dpc.model import Dpc
from skytemple_files.graphics.dpci.model import Dpci
from skytemple_files.graphics.dpl.model import Dpl
from skytemple_files.graphics.dpla.model import Dpla

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(os.path.join(output_dir), exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))

dungeon_bin_bin = rom.getFileByName('DUNGEON/dungeon.bin')
static_data = get_ppmdu_config_for_rom(rom)
dungeon_bin = DungeonBinHandler.deserialize(dungeon_bin_bin, static_data)

dungeon_bin.set('dungeon1.dpl', dungeon_bin.get('dungeon2.dpl'))
dungeon_bin.set('dungeon1.dpla', dungeon_bin.get('dungeon2.dpla'))
dungeon_bin.set('dungeon1.dpci', dungeon_bin.get('dungeon2.dpci'))
dungeon_bin.set('dungeon1.dpc', dungeon_bin.get('dungeon2.dpc'))
dungeon_bin.set('dungeon1.dma', dungeon_bin.get('dungeon2.dma'))

dungeon_bin_bin_after = DungeonBinHandler.serialize(dungeon_bin)
rom.setFileByName('DUNGEON/dungeon.bin', dungeon_bin_bin_after)

# Check if we can open them again
dungeon_bin_bin = rom.getFileByName('DUNGEON/dungeon.bin')
dungeon_bin.get('dungeon1.dpl')
dungeon_bin.get('dungeon1.dpla')
dungeon_bin.get('dungeon1.dpci')
dungeon_bin.get('dungeon1.dpc')
dungeon_bin.get('dungeon1.dma')

rom.saveToFile(os.path.join(output_dir, 'changed.nds'))

