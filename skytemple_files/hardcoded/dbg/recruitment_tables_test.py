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
from skytemple_files.hardcoded.recruitment_tables import HardcodedRecruitmentTables

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
rom_us = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))
ppmdu_us = get_ppmdu_config_for_rom(rom_us)
ov11_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries['overlay/overlay_0011.bin'])

species = HardcodedRecruitmentTables.get_monster_species_list(ov11_us, ppmdu_us)
level = HardcodedRecruitmentTables.get_monster_levels_list(ov11_us, ppmdu_us)
location = HardcodedRecruitmentTables.get_monster_locations_list(ov11_us, ppmdu_us)

for i, (e_species, e_level, e_location) in enumerate(zip(species, level, location)):
    print(i, e_species, e_level, e_location)
    
# Try setting and see if still same.
HardcodedRecruitmentTables.set_monster_species_list(species, ov11_us, ppmdu_us)
assert species == HardcodedRecruitmentTables.get_monster_species_list(ov11_us, ppmdu_us)

HardcodedRecruitmentTables.set_monster_levels_list(level, ov11_us, ppmdu_us)
assert level == HardcodedRecruitmentTables.get_monster_levels_list(ov11_us, ppmdu_us)

HardcodedRecruitmentTables.set_monster_locations_list(location, ov11_us, ppmdu_us)
assert location == HardcodedRecruitmentTables.get_monster_locations_list(ov11_us, ppmdu_us)
