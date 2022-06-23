#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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

from skytemple_files.common.util import get_files_from_rom_with_extension
from skytemple_files.data.str.handler import StrHandler

base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")

rom = NintendoDSRom.fromFile(os.path.join(base_dir, "skyworkcopy.nds"))

for filename in get_files_from_rom_with_extension(rom, "str"):
    print("Processing " + filename)

    bin_before = rom.getFileByName(filename)
    strings = StrHandler.deserialize(bin_before)
    bin_after = StrHandler.serialize(strings)

    with open("/tmp/before.bin", "wb") as f:
        f.write(bin_before)

    with open("/tmp/after.bin", "wb") as f:
        f.write(bin_after)

    assert bin_before == bin_after
    # strings.strings[441] = 'ÄÖÜßäéöü'
    strings.strings[441] = "Hi Chat ♪!"
    bin_after2 = StrHandler.serialize(strings)
    print(StrHandler.deserialize(bin_after2).strings[441])
    rom.setFileByName(filename, bin_after2)

rom.saveToFile(os.path.join(base_dir, "skyworkcopy_edit.nds"))
