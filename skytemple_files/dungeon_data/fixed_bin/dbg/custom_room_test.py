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

from skytemple_files.common.util import get_ppmdu_config_for_rom, get_binary_from_rom_ppmdu, set_binary_in_rom_ppmdu
from skytemple_files.dungeon_data.fixed_bin.handler import FixedBinHandler
from skytemple_files.dungeon_data.fixed_bin.model import TileRule, TileRuleType, EntityRule
from skytemple_files.hardcoded.fixed_floor import HardcodedFixedFloorTables, EntitySpawnEntry, ItemSpawn, \
    MonsterSpawn, TileSpawn

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(output_dir, exist_ok=True)

rom = NintendoDSRom.fromFile('/home/marco/dev/skytemple/skytemple/skyworkcopy.nds')
static_data = get_ppmdu_config_for_rom(rom)

fixed_bin = rom.getFileByName('BALANCE/fixed.bin')
fixed = FixedBinHandler.deserialize(fixed_bin, static_data=static_data)

ov29 = get_binary_from_rom_ppmdu(rom, static_data.binaries['overlay/overlay_0029.bin'])
ov10 = get_binary_from_rom_ppmdu(rom, static_data.binaries['overlay/overlay_0010.bin'])

entity_table = HardcodedFixedFloorTables.get_entity_spawn_table(ov29, static_data)
item_table = HardcodedFixedFloorTables.get_item_spawn_list(ov29, static_data)
tile_table = HardcodedFixedFloorTables.get_tile_spawn_list(ov29, static_data)
monster_table = HardcodedFixedFloorTables.get_monster_spawn_list(ov29, static_data)
monster_stats_table = HardcodedFixedFloorTables.get_monster_spawn_stats_table(ov10, static_data)

T = TileRule
WH = TileRuleType.WALL_HALLWAY
FR = TileRuleType.FLOOR_ROOM
WZ = TileRuleType.WARP_ZONE
SR = TileRuleType.SECONDARY_ROOM
FH = TileRuleType.FLOOR_HALLWAY
K1 = TileRuleType.FL_WA_ROOM_FLAG_0C
K2 = TileRuleType.FL_WA_ROOM_FLAG_0D
LS = TileRuleType.LEADER_SPAWN
# ITEM1 + Monster
entity_table[1].monster_id = 1
entity_table[1].item_id = 1
entity_table[1].tile_id = 0
item_table[1] = ItemSpawn(1, 0, 0, 0)
monster_table[1] = MonsterSpawn(321, 1, 0xA)
ITEM1 = EntityRule(1, static_data.script_data.directions__by_name['Left'])
# ITEM2
entity_table[2].monster_id = 0
entity_table[2].item_id = 2
entity_table[2].tile_id = 1
item_table[2] = ItemSpawn(2, 0, 0, 0)
tile_table[1] = TileSpawn(1, 1, 0, 0b1000)
ITEM2 = EntityRule(2)
# ITEM3
entity_table[3].monster_id = 0
entity_table[3].item_id = 3
entity_table[3].tile_id = 2
item_table[3] = ItemSpawn(3, 0, 0, 0)
tile_table[2] = TileSpawn(2, 2, 0, 0b0100000)
ITEM3 = EntityRule(3)
# ITEM4
entity_table[4].monster_id = 0
entity_table[4].item_id = 4
entity_table[4].tile_id = 3
item_table[4] = ItemSpawn(4, 0, 0, 0)
tile_table[3] = TileSpawn(3, 0, 0, 0b0000001)
ITEM4 = EntityRule(4)
# ITEM5
entity_table[5].monster_id = 0
entity_table[5].item_id = 5
entity_table[5].tile_id = 4
item_table[5] = ItemSpawn(115, 0, 0, 0)
tile_table[4] = TileSpawn(0, 0, 0xFF, 0)
ITEM5 = EntityRule(5)
# MONS1
entity_table[6].monster_id = 2
entity_table[6].item_id = 0
entity_table[6].tile_id = 5
monster_table[2] = MonsterSpawn(412, 1, 0xA)
tile_table[5] = TileSpawn(0, 3, 0, 0b0000010)
MONS1 = EntityRule(6, static_data.script_data.directions__by_name['DownRight'])
# MONS2
entity_table[7].monster_id = 3
entity_table[7].item_id = 0
entity_table[7].tile_id = 66
monster_table[3] = MonsterSpawn(178, 1, 0x6)
tile_table[5] = TileSpawn(0xFF, 0xFF, 0, 0b0000100)
MONS2 = EntityRule(7, static_data.script_data.directions__by_name['DownLeft'])

fixed.fixed_floors[1].width = 8
fixed.fixed_floors[1].height = 8

fixed.fixed_floors[1].actions = [
    T(WH), T(WH), T(WH), T(WH), T(WH), T(WH), T(WH), T(WH),
    T(WH), T(FR), T(FR), T(FR), T(FR), T(FR), T(WZ), T(WH),
    T(WH), ITEM1, T(SR), MONS1, MONS2, T(SR), ITEM2, T(WH),
    T(WH), ITEM3, T(SR), T(FR), T(FR), T(SR), ITEM4, T(WH),
    T(WH), T(FR), T(FR), T(FR), T(FR), T(FR), T(FR), T(WH),
    T(WH), T(WH), T(WH), T(K1), T(FH), T(K2), T(WH), T(WH),
    T(WH), T(FH), T(FH), ITEM5, T(FH), T(FH), T(FH), T(WH),
    T(WH), T(LS), T(WH), T(WH), T(WH), T(WH), T(WH), T(WH)
]

ov29_before = bytes(ov29)
HardcodedFixedFloorTables.set_item_spawn_list(ov29, item_table, static_data)
HardcodedFixedFloorTables.set_tile_spawn_list(ov29, tile_table, static_data)
HardcodedFixedFloorTables.set_monster_spawn_list(ov29, monster_table, static_data)
HardcodedFixedFloorTables.set_entity_spawn_table(ov29, entity_table, static_data)
set_binary_in_rom_ppmdu(rom, static_data.binaries['overlay/overlay_0029.bin'], ov29)

assert ov29_before != get_binary_from_rom_ppmdu(rom, static_data.binaries['overlay/overlay_0029.bin'])
assert item_table == HardcodedFixedFloorTables.get_item_spawn_list(ov29, static_data)
assert monster_table == HardcodedFixedFloorTables.get_monster_spawn_list(ov29, static_data)
assert tile_table == HardcodedFixedFloorTables.get_tile_spawn_list(ov29, static_data)
assert entity_table == HardcodedFixedFloorTables.get_entity_spawn_table(ov29, static_data)

fixed_bin_after = FixedBinHandler.serialize(fixed)
assert fixed_bin != fixed_bin_after
rom.setFileByName('BALANCE/fixed.bin', fixed_bin_after)
rom.saveToFile(os.path.join(output_dir, 'test_fixed_floor.nds'))

assert get_binary_from_rom_ppmdu(
    NintendoDSRom.fromFile(os.path.join(output_dir, 'test_fixed_floor.nds')), static_data.binaries['overlay/overlay_0029.bin']
) != ov29_before
