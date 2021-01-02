"""Tests applying a patch inside a skypatch file."""
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

from skytemple_files.common.util import get_ppmdu_config_for_rom, get_binary_from_rom_ppmdu
from skytemple_files.patch.patches import Patcher

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
    package = os.path.join(os.path.dirname(__file__),
                           '..', '..', '..', 'docs', 'patch_packages', 'example_patch.skypatch')
    os.makedirs(out_dir, exist_ok=True)

    in_rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))

    # Load PPMDU config, but remove all data about Patches and LooseBinFiles.
    config = get_ppmdu_config_for_rom(in_rom)
    config.asm_patches_constants.patches = {}
    config.asm_patches_constants.loose_bin_files = {}

    patcher = Patcher(in_rom, config, skip_core_patches=True)

    # Load the package
    patcher.add_pkg(package)
    assert not patcher.is_applied('ExamplePatch')

    patcher.apply('ExamplePatch')
    with open(os.path.join(out_dir, 'example_patch_ov11.bin'), 'wb') as f:
        f.write(get_binary_from_rom_ppmdu(in_rom, config.binaries['overlay/overlay_0011.bin']))

    assert patcher.is_applied('ExamplePatch')
    in_rom.saveToFile(os.path.join(out_dir, 'patched.nds'))

    # Check if really patched
    out_rom = NintendoDSRom.fromFile(os.path.join(out_dir, 'patched.nds'))
    new_patcher = Patcher(out_rom, get_ppmdu_config_for_rom(out_rom))
    new_patcher.add_pkg(package)
    assert new_patcher.is_applied('ExamplePatch')
