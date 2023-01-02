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
from skytemple_files.hardcoded.ground_dungeon_tilesets import (
    HardcodedGroundDungeonTilesets,
)

base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
rom = NintendoDSRom.fromFile(os.path.join(base_dir, "skyworkcopy.nds"))
ppmdu = get_ppmdu_config_for_rom(rom)

l = HardcodedGroundDungeonTilesets.get_ground_dungeon_tilesets(
    get_binary_from_rom_ppmdu(rom, ppmdu.binaries["overlay/overlay_0011.bin"]), ppmdu
)
for i, d in enumerate(l):
    print(i, d)
