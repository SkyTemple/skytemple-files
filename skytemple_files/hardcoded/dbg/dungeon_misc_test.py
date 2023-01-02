#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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
# mypy: ignore-errors
from __future__ import annotations

import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import (
    get_binary_from_rom_ppmdu,
    get_ppmdu_config_for_rom,
)
from skytemple_files.hardcoded.dungeon_misc import HardcodedDungeonMisc

base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
rom_us = NintendoDSRom.fromFile(os.path.join(base_dir, "skyworkcopy_us.nds"))
rom_eu = NintendoDSRom.fromFile(os.path.join(base_dir, "skyworkcopy.nds"))
ppmdu_us = get_ppmdu_config_for_rom(rom_us)
ppmdu_eu = get_ppmdu_config_for_rom(rom_eu)
arm9_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries["arm9.bin"])
arm9_eu = get_binary_from_rom_ppmdu(rom_eu, ppmdu_us.binaries["arm9.bin"])
ov10_us = get_binary_from_rom_ppmdu(
    rom_us, ppmdu_us.binaries["overlay/overlay_0010.bin"]
)
ov10_eu = get_binary_from_rom_ppmdu(
    rom_eu, ppmdu_us.binaries["overlay/overlay_0010.bin"]
)
ov29_us = get_binary_from_rom_ppmdu(
    rom_us, ppmdu_us.binaries["overlay/overlay_0029.bin"]
)
ov29_eu = get_binary_from_rom_ppmdu(
    rom_eu, ppmdu_us.binaries["overlay/overlay_0029.bin"]
)


def test(getter, setter, expected_value, ov_us, ov_eu):
    assert getter(ov_us, ppmdu_us) == expected_value
    assert getter(ov_eu, ppmdu_eu) == expected_value
    setter(123, ov_us, ppmdu_us)
    setter(124, ov_eu, ppmdu_eu)
    assert getter(ov_us, ppmdu_us) == 123
    assert getter(ov_eu, ppmdu_eu) == 124


test(
    HardcodedDungeonMisc.get_burn_damage_delay,
    HardcodedDungeonMisc.set_burn_damage_delay,
    50,
    ov10_us,
    ov10_eu,
)
test(
    HardcodedDungeonMisc.get_poison_damage_delay,
    HardcodedDungeonMisc.set_poison_damage_delay,
    20,
    ov10_us,
    ov10_eu,
)
test(
    HardcodedDungeonMisc.get_bad_poison_damage_delay,
    HardcodedDungeonMisc.set_bad_poison_damage_delay,
    5,
    ov10_us,
    ov10_eu,
)
test(
    HardcodedDungeonMisc.get_ginseng_increase_by_3_chance,
    HardcodedDungeonMisc.set_ginseng_increase_by_3_chance,
    12,
    ov10_us,
    ov10_eu,
)
test(
    HardcodedDungeonMisc.get_belly_loss_walk_through_walls,
    HardcodedDungeonMisc.set_belly_loss_walk_through_walls,
    5,
    ov29_us,
    ov29_eu,
)
test(
    HardcodedDungeonMisc.get_belly_loss_1000ile_walk_through_walls,
    HardcodedDungeonMisc.set_belly_loss_1000ile_walk_through_walls,
    0,
    ov29_us,
    ov29_eu,
)
