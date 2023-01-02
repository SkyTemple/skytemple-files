#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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
# mypy: ignore-errors
from __future__ import annotations

import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import (
    get_binary_from_rom_ppmdu,
    get_ppmdu_config_for_rom,
)
from skytemple_files.hardcoded.text_speed import HardcodedTextSpeed

base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
rom_us = NintendoDSRom.fromFile(os.path.join(base_dir, "skyworkcopy_us.nds"))
rom_eu = NintendoDSRom.fromFile(os.path.join(base_dir, "skyworkcopy.nds"))
ppmdu_us = get_ppmdu_config_for_rom(rom_us)
ppmdu_eu = get_ppmdu_config_for_rom(rom_eu)
arm9_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries["arm9.bin"])
arm9_eu = get_binary_from_rom_ppmdu(rom_eu, ppmdu_us.binaries["arm9.bin"])

print(HardcodedTextSpeed.get_text_speed_debug(arm9_us, ppmdu_us))
print(HardcodedTextSpeed.get_text_speed_debug(arm9_eu, ppmdu_eu))

HardcodedTextSpeed.set_text_speed_debug(True, arm9_us, ppmdu_us)
HardcodedTextSpeed.set_text_speed_debug(True, arm9_eu, ppmdu_eu)

print(HardcodedTextSpeed.get_text_speed_debug(arm9_us, ppmdu_us))
print(HardcodedTextSpeed.get_text_speed_debug(arm9_eu, ppmdu_eu))
