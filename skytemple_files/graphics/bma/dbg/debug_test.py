"""Debugging import problems"""
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

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom_vanilla = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
rom_modified = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))

bin_vanilla = rom_vanilla.getFileByName('MAP_BG/s05p01a.bma')

with open('/tmp/before.bin', 'wb') as f:
    f.write(bin_vanilla)

bin_modified = rom_modified.getFileByName('MAP_BG/s05p01a.bma')

with open('/tmp/after.bin', 'wb') as f:
    f.write(bin_modified)
