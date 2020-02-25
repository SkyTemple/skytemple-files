"""Testing script for testing a SSB file."""
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

from skytemple_files.common.script_util import load_script_files, SCRIPT_DIR
from skytemple_files.common.util import get_rom_folder
from skytemple_files.script.ssb.handler import SsbHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

script_info = load_script_files(get_rom_folder(rom, SCRIPT_DIR))

map_name = 'D01P11A'
ssb_name = SCRIPT_DIR + '/' + map_name + '/' + 'm24p1101.ssb'

bin_before = rom.getFileByName(ssb_name)
ssb = SsbHandler.deserialize(bin_before)

print(ssb.header)
print(f"number_of_routines: {len(ssb.routine_info)}")
print(f"constants: {ssb.constants}")
print(f"strings: {ssb.strings}")
print(ssb.routine_info)
for ops in ssb.routine_ops:
    print(">>> Routine:")
    op_cursor = 0
    for op in ops:
        print(f"{op_cursor:10}: {op}")
        op_cursor += 2 + len(op.params) * 2