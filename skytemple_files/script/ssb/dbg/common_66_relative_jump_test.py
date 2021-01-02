"""Testing script for testing a SSB file."""
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
from skytemple_files.common.util import get_rom_folder, get_files_from_rom_with_extension
from skytemple_files.script.ssb.handler import SsbHandler


def main():
    output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
    os.makedirs(output_dir, exist_ok=True)

    rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

    file_name = 'SCRIPT/COMMON/unionall.ssb'

    # Files that don't work right now:
    print(file_name)

    bin_before = rom.getFileByName(file_name)
    ssb = SsbHandler.deserialize(bin_before)

    target_point = 0x11BF

    for i, ops in enumerate(ssb.routine_ops):
        print(f">>> Routine {i}:")
        for op in ops:
            offset = target_point - op.offset
            offset_two = target_point - int.from_bytes(op.offset.to_bytes(2, byteorder='little', signed=False), byteorder='little', signed=True)
            for param in op.params:
                if param == offset or param == offset_two:
                    print(f"{op.offset:10x}: ({op.op_code.id:3}) {op.op_code.name:45} - {', '.join(hex(x) for x in op.params)}")


if __name__ == '__main__':
    main()
