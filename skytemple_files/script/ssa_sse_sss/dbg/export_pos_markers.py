"""Testing script, that exports all position marks."""
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
import io

from ndspy.rom import NintendoDSRom

from skytemple_files.common.script_util import load_script_files, SCRIPT_DIR
from skytemple_files.common.util import get_rom_folder
from skytemple_files.script.ssa_sse_sss.handler import SsaHandler
from skytemple_files.script.ssb.handler import SsbHandler

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')


def main():
    os.makedirs(output_dir, exist_ok=True)

    rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

    script_info = load_script_files(get_rom_folder(rom, SCRIPT_DIR))

    for script_map in script_info['maps'].values():
        if script_map['enter_sse'] is not None:
            process(rom, SCRIPT_DIR + '/' + script_map['name'] + '/', script_map['enter_sse'], script_map['enter_ssbs'])
        for ssa, ssb in script_map['ssas']:
            process(rom, SCRIPT_DIR + '/' + script_map['name'] + '/', ssa, [ssb])
        for sss, ssb in script_map['subscripts'].items():
            process(rom, SCRIPT_DIR + '/' + script_map['name'] + '/', sss, ssb)


def process(rom, base_path, ssa_file_name, ssb_file_name):
    ssa = SsaHandler.deserialize(rom.getFileByName(base_path + ssa_file_name))
    filtered_markers = ssa.position_markers
    #filtered_markers = [x for x in ssa.position_markers if
    #                    not (x.unk8 == 1  and x.unkA == 1  and x.unkC == 1 and x.unkE == 0) and
    #                    not (x.unk8 == 32 and x.unkA == 24 and x.unkC == 3 and x.unkE == 2)]
    if len(filtered_markers) <= 0:
        return
    ssbss = []
    #ssbss = [SsbHandler.deserialize(rom.getFileByName(base_path + ssb)).to_ssb_script()[0] for ssb in ssb_file_name]
    print(f"{base_path + ssa_file_name}:")
    for i, pos_marker in enumerate(filtered_markers):
        print(f"@({pos_marker.pos.x_relative}[{pos_marker.pos.x_offset}], "
              f"{pos_marker.pos.y_relative}[{pos_marker.pos.y_offset}) "
              f"{pos_marker.unk8}-{pos_marker.unkA}-{pos_marker.unkC}-{pos_marker.unkE}")
        found = False
        for ssbs in ssbss:
            arg_seq = f'{pos_marker.pos.x_offset}, {pos_marker.pos.y_offset}, {pos_marker.pos.x_relative}, {pos_marker.pos.y_relative}'
            for num, line in enumerate(io.StringIO(ssbs)):
                if arg_seq in line:
                    print(line.rstrip('\n'))
                    found = True
        if not found:
            print(">> NOT FOUND.")



if __name__ == '__main__':
    main()
