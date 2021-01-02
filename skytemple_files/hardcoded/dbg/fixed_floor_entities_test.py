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
from skytemple_files.hardcoded.fixed_floor import HardcodedFixedFloorTables

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
ppmdu = get_ppmdu_config_for_rom(rom)

ov29 = get_binary_from_rom_ppmdu(rom, ppmdu.binaries['overlay/overlay_0029.bin'])
ov10 = get_binary_from_rom_ppmdu(rom, ppmdu.binaries['overlay/overlay_0010.bin'])


def print_and_test(binary, getter, setter):
    values = getter(binary, ppmdu)

    for i, val in enumerate(values):
        print(i, val)

    # Try setting and see if still same.
    setter(binary, values, ppmdu)
    assert values == getter(binary, ppmdu)

print_and_test(
    ov29,
    HardcodedFixedFloorTables.get_entity_spawn_table,
    HardcodedFixedFloorTables.set_entity_spawn_table
)

print_and_test(
    ov29,
    HardcodedFixedFloorTables.get_item_spawn_list,
    HardcodedFixedFloorTables.set_item_spawn_list
)

print_and_test(
    ov29,
    HardcodedFixedFloorTables.get_monster_spawn_list,
    HardcodedFixedFloorTables.set_monster_spawn_list
)

print_and_test(
    ov29,
    HardcodedFixedFloorTables.get_tile_spawn_list,
    HardcodedFixedFloorTables.set_tile_spawn_list
)

print_and_test(
    ov10,
    HardcodedFixedFloorTables.get_monster_spawn_stats_table,
    HardcodedFixedFloorTables.set_monster_spawn_stats_table
)

print_and_test(
    ov10,
    HardcodedFixedFloorTables.get_fixed_floor_properties,
    HardcodedFixedFloorTables.set_fixed_floor_properties
)

print_and_test(
    ov29,
    HardcodedFixedFloorTables.get_fixed_floor_overrides,
    HardcodedFixedFloorTables.set_fixed_floor_overrides
)
