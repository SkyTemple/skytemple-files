#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
from skytemple_files.hardcoded.spawn_rate import HardcodedSpawnRate

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
rom_us = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))
rom_eu = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
ppmdu_us = get_ppmdu_config_for_rom(rom_us)
ppmdu_eu = get_ppmdu_config_for_rom(rom_eu)
ov10_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries['overlay/overlay_0010.bin'])
ov10_eu = get_binary_from_rom_ppmdu(rom_eu, ppmdu_us.binaries['overlay/overlay_0010.bin'])

print(HardcodedSpawnRate.get_normal_spawn_rate(ov10_us, ppmdu_us))
print(HardcodedSpawnRate.get_normal_spawn_rate(ov10_eu, ppmdu_eu))
print(HardcodedSpawnRate.get_stolen_spawn_rate(ov10_us, ppmdu_us))
print(HardcodedSpawnRate.get_stolen_spawn_rate(ov10_eu, ppmdu_eu))

HardcodedSpawnRate.set_normal_spawn_rate(123, ov10_us, ppmdu_us)
HardcodedSpawnRate.set_normal_spawn_rate(567, ov10_eu, ppmdu_eu)
HardcodedSpawnRate.set_stolen_spawn_rate(987, ov10_us, ppmdu_us)
HardcodedSpawnRate.set_stolen_spawn_rate(654, ov10_eu, ppmdu_eu)

print(HardcodedSpawnRate.get_normal_spawn_rate(ov10_us, ppmdu_us))
print(HardcodedSpawnRate.get_normal_spawn_rate(ov10_eu, ppmdu_eu))
print(HardcodedSpawnRate.get_stolen_spawn_rate(ov10_us, ppmdu_us))
print(HardcodedSpawnRate.get_stolen_spawn_rate(ov10_eu, ppmdu_eu))
