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
from skytemple_files.hardcoded.dungeon_music import HardcodedDungeonMusic

base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
rom_us = NintendoDSRom.fromFile(os.path.join(base_dir, "skyworkcopy_us.nds"))
rom_eu = NintendoDSRom.fromFile(os.path.join(base_dir, "skyworkcopy.nds"))
ppmdu_us = get_ppmdu_config_for_rom(rom_us)
ppmdu_eu = get_ppmdu_config_for_rom(rom_eu)
ov10_us = get_binary_from_rom_ppmdu(
    rom_us, ppmdu_us.binaries["overlay/overlay_0010.bin"]
)
ov10_eu = get_binary_from_rom_ppmdu(
    rom_eu, ppmdu_us.binaries["overlay/overlay_0010.bin"]
)

for x in HardcodedDungeonMusic.get_music_list(ov10_us, ppmdu_us):
    print(x)
print("===")
for x in HardcodedDungeonMusic.get_music_list(ov10_eu, ppmdu_eu):
    print(x)
print("===")
print("===")
print("===")
print("===")
for x in HardcodedDungeonMusic.get_random_music_list(ov10_us, ppmdu_us):
    print(x)
print("===")
for x in HardcodedDungeonMusic.get_random_music_list(ov10_eu, ppmdu_eu):
    print(x)
