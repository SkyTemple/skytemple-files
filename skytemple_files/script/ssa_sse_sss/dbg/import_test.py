"""Testing script, that tests writing."""
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
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    from pil import Image, ImageDraw, ImageFont
from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.common.script_util import load_script_files, SCRIPT_DIR
from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_rom_folder
from skytemple_files.script.ssa_sse_sss.handler import SsaHandler
from skytemple_files.script.ssa_sse_sss.position import SsaPosition

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

def main():
    os.makedirs(output_dir, exist_ok=True)

    rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

    script_info = load_script_files(get_rom_folder(rom, SCRIPT_DIR))

    for script_map in script_info['maps'].values():
        # Map BGs are NOT *actually* mapped 1:1 to scripts. They are loaded via Opcode. However it turns out, using the BPL name
        # is an easy way to map them.
        if script_map['enter_sse'] is not None:
            process(rom, script_map['name'], SCRIPT_DIR + '/' + script_map['name'] + '/' + script_map['enter_sse'])
        for ssa, _ in script_map['ssas']:
            process(rom, script_map['name'], SCRIPT_DIR + '/' + script_map['name'] + '/' + ssa)
        for sss in script_map['subscripts'].keys():
            process(rom, script_map['name'], SCRIPT_DIR + '/' + script_map['name'] + '/' + sss)


def process(rom, map_name, file_name):
    print(f"Processing {file_name}...")

    bin_before = rom.getFileByName(file_name)
    ssa_before = SsaHandler.deserialize(bin_before)

    bin_after = SsaHandler.serialize(ssa_before)
    ssa_after = SsaHandler.deserialize(bin_after)
    bin_after2 = SsaHandler.serialize(ssa_after)

    with open('/tmp/1.bin', 'wb') as f:
        f.write(bin_before)

    with open('/tmp/2.bin', 'wb') as f:
        f.write(bin_after2)

    assert bin_before == bin_after2


if __name__ == '__main__':
    main()
