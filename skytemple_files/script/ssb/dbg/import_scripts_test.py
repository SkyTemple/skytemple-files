"""Import ssb files from a rom directory back into the game."""
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


def main(rom_file, directory):
    rom = NintendoDSRom.fromFile(rom_file)

    for file_name in get_files_from_rom_with_extension(rom, 'ssb'):
        if os.path.exists(os.path.join(directory, file_name)):
            print(file_name)

            with open(os.path.join(directory, file_name), 'rb') as f:
                rom.setFileByName(file_name, f.read())

    rom.saveToFile(rom_file)


if __name__ == '__main__':
    rom_file = sys.argv[1]
    directory = sys.argv[2]
    main(rom_file, directory)
