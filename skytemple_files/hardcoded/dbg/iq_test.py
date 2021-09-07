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
import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import get_ppmdu_config_for_rom, get_binary_from_rom_ppmdu
from skytemple_files.hardcoded.iq import HardcodedIq

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
rom_us = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us_unpatched.nds'))
rom_eu = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
ppmdu_us = get_ppmdu_config_for_rom(rom_us)
ppmdu_eu = get_ppmdu_config_for_rom(rom_eu)
arm9_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries['arm9.bin'])
arm9_eu = get_binary_from_rom_ppmdu(rom_eu, ppmdu_us.binaries['arm9.bin'])
ov10_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries['overlay/overlay_0010.bin'])
ov10_eu = get_binary_from_rom_ppmdu(rom_eu, ppmdu_us.binaries['overlay/overlay_0010.bin'])
ov29_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries['overlay/overlay_0029.bin'])
ov29_eu = get_binary_from_rom_ppmdu(rom_eu, ppmdu_us.binaries['overlay/overlay_0029.bin'])


def test(getter, setter, ov_us, ov_eu, set_test=True, **kwargs):
    v = getter(ov_eu, ppmdu_eu, **kwargs)
    assert getter(ov_us, ppmdu_us, **kwargs) == v
    if set_test:
        setter(123, ov_us, ppmdu_us, **kwargs)
        setter(124, ov_eu, ppmdu_eu, **kwargs)
        assert getter(ov_us, ppmdu_us, **kwargs) == 123
        assert getter(ov_eu, ppmdu_eu, **kwargs) == 124
    else:
        setter(v, ov_us, ppmdu_us, **kwargs)
        setter(v, ov_eu, ppmdu_eu, **kwargs)
        assert getter(ov_us, ppmdu_us, **kwargs) == v
        assert getter(ov_eu, ppmdu_eu, **kwargs) == v


test(
    HardcodedIq.get_min_iq_for_exclusive_move_user,
    HardcodedIq.set_min_iq_for_exclusive_move_user,
    arm9_us, arm9_eu
)
test(
    HardcodedIq.get_min_iq_for_item_master,
    HardcodedIq.set_min_iq_for_item_master,
    arm9_us, arm9_eu
)
test(
    HardcodedIq.get_intimidator_chance,
    HardcodedIq.set_intimidator_chance,
    ov10_us, ov10_eu
)
test(
    HardcodedIq.get_gummi_iq_gains,
    HardcodedIq.set_gummi_iq_gains,
    arm9_us, arm9_eu, set_test=False, add_types_patch_applied=False
)
test(
    HardcodedIq.get_gummi_belly_heal,
    HardcodedIq.set_gummi_belly_heal,
    arm9_us, arm9_eu, set_test=False, add_types_patch_applied=False
)
test(
    HardcodedIq.get_iq_skills,
    HardcodedIq.set_iq_skills,
    arm9_us, arm9_eu, set_test=False
)
