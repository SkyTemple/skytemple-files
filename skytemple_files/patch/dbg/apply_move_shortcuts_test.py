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

from skytemple_files.common.util import get_ppmdu_config_for_rom, create_file_in_rom, set_binary_in_rom_ppmdu
from skytemple_files.patch.patches import Patcher

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
    os.makedirs(out_dir, exist_ok=True)

    in_rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
    patcher = Patcher(in_rom, get_ppmdu_config_for_rom(in_rom))
    assert not patcher.is_applied('MoveShortcuts')

    patcher.apply('MoveShortcuts')

    assert patcher.is_applied('MoveShortcuts')
    in_rom.saveToFile(os.path.join(out_dir, 'patched.nds'))
