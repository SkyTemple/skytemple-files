"""This patches the test dungeon to have 5 floors instead and so it overflows into the next dungeon's floors."""
#  Copyright 2020 Parakoopa
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

base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
os.makedirs(output_dir, exist_ok=True)
rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
ARM9_START_DUNGEONS = 0x9e924

assert rom.arm9[ARM9_START_DUNGEONS:ARM9_START_DUNGEONS+4] == bytes([3, 0, 0, 3])
rom.arm9[ARM9_START_DUNGEONS:ARM9_START_DUNGEONS+4] = bytes([5, 0, 0, 5])
rom.saveToFile(os.path.join(output_dir, '5floors.nds'))

rom = NintendoDSRom.fromFile(os.path.join(output_dir, '5floors.nds'))
assert rom.arm9[ARM9_START_DUNGEONS:ARM9_START_DUNGEONS+4] == bytes([5, 0, 0, 5])
