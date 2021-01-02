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

from skytemple_files.common.util import get_ppmdu_config_for_rom, get_binary_from_rom_ppmdu
from skytemple_files.hardcoded.rank_up_table import HardcodedRankUpTable

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
rom_us = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))
ppmdu_us = get_ppmdu_config_for_rom(rom_us)
arm9_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries['arm9.bin'])

rank_up = HardcodedRankUpTable.get_rank_up_table(arm9_us, ppmdu_us)

for i, rank in enumerate(rank_up):
    print(i, rank)
    
# Try setting and see if still same.
HardcodedRankUpTable.set_rank_up_table(rank_up, arm9_us, ppmdu_us)
assert rank_up == HardcodedRankUpTable.get_rank_up_table(arm9_us, ppmdu_us)
