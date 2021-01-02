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
from skytemple_files.script.lsd.handler import LsdHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

script_info = load_script_files(get_rom_folder(rom, SCRIPT_DIR))

for map_name, map in script_info['maps'].items():
    if map['lsd'] is not None:
        lsd_name = SCRIPT_DIR + '/' + map_name + '/' + map['lsd']

        bin_before = rom.getFileByName(lsd_name)
        lsd = LsdHandler.deserialize(bin_before)

        print(f"{lsd_name}: {lsd.entries}")

        bin_after = LsdHandler.serialize(lsd)
        assert bin_before == bin_after
