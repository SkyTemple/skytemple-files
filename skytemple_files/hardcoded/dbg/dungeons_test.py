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

from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_ppmdu_config_for_rom, get_binary_from_rom_ppmdu
from skytemple_files.hardcoded.dungeons import HardcodedDungeons

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
rom_us = NintendoDSRom.fromFile('/tmp/rando.nds')
ppmdu_us = get_ppmdu_config_for_rom(rom_us)
arm9_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries['arm9.bin'])

dungeon_list = HardcodedDungeons.get_dungeon_list(arm9_us, ppmdu_us)
for i, d in enumerate(dungeon_list):
    print(i, d)

# 0x35 (53) is used by dungeons >= 0xB4, which are NOT on the list (dojo dungeons).
print(set(range(0, 100)) - set([x.mappa_index for x in dungeon_list]))
# <<< {53}

# End:
# Function that returns the number of floors in a dungeon:
# if ID >= 0xB4 && ID <= 0xBD {
#     return 5
# } else if ID == 0xBE {
#     return 1
# } else if ID >= 0xBF {
#     return 0x30
# } else {
#     Read the value from arm9.bin
# }
# if ID >= 0xB4 && ID <= 0xBD {
#     mappa entry = 35h
#     mappa floor = Current floor + (ID - 0xB4) * 5
# } else if ID == 0xBE {
#     mappa entry = 35h
#     mappa floor = Current floor + 32h
# } else if ID >= 0xBF && ID <= 0xD3 {
#     mappa entry = 35h
#     mappa floor = Current floor + 33h
# } else {
#     mappa entry = (whatever the arm9.bin table says)
#     mappa floor = Current floor + (whatever the arm9.bin table says)
# }
# No, I forgot to say: The function that gets the mappa entry given a dungeon ID returns 0x35 if the ID is >= 0xB4,
# and the one that returns the mappa floor number returns 0 if the ID is >= 0xB4

# Try setting and see if still same.
HardcodedDungeons.set_dungeon_list(dungeon_list, arm9_us, ppmdu_us)
assert dungeon_list == HardcodedDungeons.get_dungeon_list(arm9_us, ppmdu_us)

# DungeonRestrictions
lst = HardcodedDungeons.get_dungeon_restrictions(arm9_us, ppmdu_us)
for e in lst:
    print(e)
HardcodedDungeons.set_dungeon_restrictions(lst, arm9_us, ppmdu_us)
assert lst == HardcodedDungeons.get_dungeon_restrictions(arm9_us, ppmdu_us)

# SecondaryTerrains
lst = HardcodedDungeons.get_secondary_terrains(arm9_us, ppmdu_us)
for e in lst:
    print(e)
HardcodedDungeons.set_secondary_terrains(lst, arm9_us, ppmdu_us)
assert lst == HardcodedDungeons.get_secondary_terrains(arm9_us, ppmdu_us)

# MapMarkerPlacements - TODO: They don't line up with dungeon IDs at all!
lst = HardcodedDungeons.get_marker_placements(arm9_us, ppmdu_us)
str_blk = ppmdu_us.string_index_data.string_blocks['Dungeon Names (Selection)']
dungeon_strs = FileType.STR.deserialize(rom_us.getFileByName('MESSAGE/text_e.str')).strings[str_blk.begin:str_blk.end]
for i, e in enumerate(lst):
    print("--------")
    if len(dungeon_strs) <= i:
        print(f'unk{i}')
    else:
        print(dungeon_strs[i])
    if e.level_id == -1:
        print('n/a')
    else:
        print(ppmdu_us.script_data.level_list__by_id[e.level_id].name)
    print(e.reference_id)
    print("x", e.x, "y", e.y)
HardcodedDungeons.set_marker_placements(lst, arm9_us, ppmdu_us)
assert lst == HardcodedDungeons.get_marker_placements(arm9_us, ppmdu_us)
