"""Testing script for testing a SSE/SSA and SSS file of the 'Crossroads' map."""
#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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
from skytemple_files.script.ssa_sse_sss.handler import SsaHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

script_info = load_script_files(get_rom_folder(rom, SCRIPT_DIR))

map_name = 'G01P02A'
sse_name = SCRIPT_DIR + '/' + map_name + '/' + 'enter.sse'

bin_before = rom.getFileByName(sse_name)
sse = SsaHandler.deserialize(bin_before)

print("=====================")
print(f"--- enter.sse ---")
print(f"Header: {sse.header}")
print(f"LayerList:")
for i, l in enumerate(sse.layer_list):
    print(f"    Layer {i}:")
    print(f"        Actors:")
    for e in l.actors:
        print(f"            {e}")
    print(f"        Objects:")
    for e in l.objects:
        print(f"            {e}")
    print(f"        Performers:")
    for e in l.performers:
        print(f"            {e}")
    print(f"        Events:")
    for e in l.events:
        print(f"            {e}")
    print(f"        Unk10:")
    for e in l.unk10s:
        print(f"            {e}")
print(f"Triggers:")
for e in sse.triggers:
    print(f"    {e}")
print(f"PositionMarkers:")
for e in sse.position_markers:
    print(f"    {e}")

#bin_after = SsaHandler.serialize(ssa)
#assert bin_before == bin_after
