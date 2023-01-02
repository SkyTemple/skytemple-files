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
from __future__ import annotations

import os

from ndspy.rom import NintendoDSRom

from skytemple_files.dungeon_data.fixed_bin.handler import FixedBinHandler

output_dir = os.path.join(os.path.dirname(__file__), "dbg_output")
os.makedirs(output_dir, exist_ok=True)

rom = NintendoDSRom.fromFile("/home/marco/dev/skytemple/skytemple/skyworkcopy.nds")

fixed_bin = rom.getFileByName("BALANCE/fixed.bin")
fixed = FixedBinHandler.deserialize(fixed_bin)
fixed_bin_after = FixedBinHandler.serialize(fixed)

with open(os.path.join(output_dir, "before.bin"), "wb") as f:
    f.write(fixed_bin)

with open(os.path.join(output_dir, "after.bin"), "wb") as f:
    f.write(fixed_bin_after)

assert fixed_bin == fixed_bin_after
print("ok!")
