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
from skytemple_files.hardcoded.main_menu_music import HardcodedMainMenuMusic

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
rom_us = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))
rom_eu = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
ppmdu_us = get_ppmdu_config_for_rom(rom_us)
ppmdu_eu = get_ppmdu_config_for_rom(rom_eu)
ov00_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries['overlay/overlay_0000.bin'])
ov00_eu = get_binary_from_rom_ppmdu(rom_eu, ppmdu_us.binaries['overlay/overlay_0000.bin'])
ov09_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries['overlay/overlay_0009.bin'])
ov09_eu = get_binary_from_rom_ppmdu(rom_eu, ppmdu_us.binaries['overlay/overlay_0009.bin'])

print(HardcodedMainMenuMusic.get_main_menu_music(ov00_us, ppmdu_us, ov09_us))
print(HardcodedMainMenuMusic.get_main_menu_music(ov00_eu, ppmdu_eu, ov09_eu))

HardcodedMainMenuMusic.set_main_menu_music(123, ov00_us, ppmdu_us, ov09_us)
HardcodedMainMenuMusic.set_main_menu_music(4, ov00_eu, ppmdu_eu, ov09_eu)

print(HardcodedMainMenuMusic.get_main_menu_music(ov00_us, ppmdu_us, ov09_us))
print(HardcodedMainMenuMusic.get_main_menu_music(ov00_eu, ppmdu_eu, ov09_eu))
