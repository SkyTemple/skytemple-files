#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
#
import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import get_ppmdu_config_for_rom, get_binary_from_rom_ppmdu
from skytemple_files.patch.patches import Patcher
from skytemple_files.patch.errors import PatchNotConfiguredError

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
    package = os.path.join(os.path.dirname(__file__), 'parameters_test')
    os.makedirs(out_dir, exist_ok=True)
    os.environ['SKYTEMPLE_DEBUG_ARMIPS_OUTPUT'] = 'YES'

    in_rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

    # Load PPMDU config, but remove all data about Patches and LooseBinFiles.
    config = get_ppmdu_config_for_rom(in_rom)
    config.asm_patches_constants.patches = {}
    config.asm_patches_constants.loose_bin_files = {}
    patcher = Patcher(in_rom, config, skip_core_patches=True)

    # Load the package
    patcher.add_pkg(package, False)
    assert not patcher.is_applied('ParametersTest')

    # Missing params
    try:
        patcher.apply('ParametersTest')
    except PatchNotConfiguredError:
        pass
    else:
        assert False, "Must throw PatchNotConfiguredError"

    # Invalid params
    try:
        patcher.apply('ParametersTest', config={
            'int_param': -1,
            'int_param2': 100,
            'int_param3': 1234,
            'select_param': 'HELLO',
            'string_param': 'World'
        })
    except PatchNotConfiguredError as ex:
        assert ex.config_parameter == 'int_param', "Must throw PatchNotConfiguredError for int_param, since it's out of range."
    else:
        assert False, "Must throw PatchNotConfiguredError for validation"
    try:
        patcher.apply('ParametersTest', config={
            'int_param': 1,
            'int_param2': 100,
            'int_param3': 1234,
            'select_param': 'INVALID',
            'string_param': 'World'
        })
    except PatchNotConfiguredError as ex:
        assert ex.config_parameter == 'select_param', "Must throw PatchNotConfiguredError for select_param, since it's an invalid option."
    else:
        assert False, "Must throw PatchNotConfiguredError for validation"

    # Check output!:
    patcher.apply('ParametersTest', config={
        'int_param': 1,
        'int_param2': 100,
        'int_param3': 1234,
        'select_param': 'HELLO',
        'string_param': 'World'
    })
