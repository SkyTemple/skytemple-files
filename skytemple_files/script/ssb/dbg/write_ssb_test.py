"""Tests if the SSB writer is working, by simple loading the scripts and writing them back and checking if same."""
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

from ndspy.rom import NintendoDSRom

from skytemple_files.common.script_util import load_script_files, SCRIPT_DIR
from skytemple_files.common.util import get_rom_folder, get_files_from_rom_with_extension
from skytemple_files.script.ssb.handler import SsbHandler
from skytemple_files.script.ssb.header import SsbHeaderEu


def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

    rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

    for file_name in get_files_from_rom_with_extension(rom, 'ssb'):
        print(file_name)

        bin_before = rom.getFileByName(file_name)
        ssb_before = SsbHandler.deserialize(bin_before)

        bin_after = SsbHandler.serialize(ssb_before)
        after_header = SsbHeaderEu(bin_after)

        print("Header before:")
        print(str(ssb_before._header))
        print("Header after:")
        print(str(after_header))

        ssb_after = SsbHandler.deserialize(bin_after)

        assert(ssb_before._header.number_of_strings == ssb_after._header.number_of_strings)
        assert(ssb_before._header.const_table_length == ssb_after._header.const_table_length)
        assert(ssb_before._header.constant_strings_start == ssb_after._header.constant_strings_start)
        assert(ssb_before._header.data_offset == ssb_after._header.data_offset)
        assert(ssb_before._header.number_of_constants == ssb_after._header.number_of_constants)
        assert(ssb_before._header.string_table_lengths == ssb_after._header.string_table_lengths)
        assert(ssb_before.routine_info == ssb_after.routine_info)
        assert(ssb_before.routine_ops == ssb_after.routine_ops)
        assert(ssb_before.constants == ssb_after.constants)
        assert(ssb_before.strings == ssb_after.strings)
        assert(len(bin_before) == len(bin_after))
        assert(bin_before == bin_after)


if __name__ == '__main__':
    main()
