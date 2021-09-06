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
import csv
import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_ppmdu_config_for_rom, get_binary_from_rom_ppmdu
from skytemple_files.hardcoded.dungeons import HardcodedDungeons

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
rom_us = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us_unpatched.nds'))
ppmdu_us = get_ppmdu_config_for_rom(rom_us)
arm9_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries['arm9.bin'])
ov10_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries['overlay/overlay_0010.bin'])
rom_eu = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
ppmdu_eu = get_ppmdu_config_for_rom(rom_eu)
ov10_eu = get_binary_from_rom_ppmdu(rom_eu, ppmdu_eu.binaries['overlay/overlay_0010.bin'])

# TilesetProperties
lst = HardcodedDungeons.get_tileset_properties(ov10_us, ppmdu_us)
for i, e in enumerate(lst):
    print(i, ': ', e)
HardcodedDungeons.set_tileset_properties(lst, ov10_us, ppmdu_us)
assert lst == HardcodedDungeons.get_tileset_properties(ov10_us, ppmdu_us)
assert lst == HardcodedDungeons.get_tileset_properties(ov10_eu, ppmdu_eu)

# IMPORT HELP USING THE PMD SPREADSHEET
info = """Beach Cave,Rock Slide,Rock,Cringe
Beach Cave Pit,Rock Slide,Rock,Cringe
Drenched Bluff,Rock Slide,Rock,Cringe
Mt. Bristle,Rock Slide,Rock,Cringe
Mt. Bristle Peak,Rock Slide,Rock,Cringe
Waterfall Cave,Rock Slide,Rock,Cringe
Apple Woods,Seed Bomb,Grass,Sleep
Craggy Coast,Rock Slide,Rock,Cringe
Side Path,Rock Slide,Rock,Cringe
Mt. Horn,Rock Slide,Rock,Cringe
Rock Path,Rock Slide,Rock,Cringe
Foggy Forest,Seed Bomb,Grass,Sleep
Forest Path,Seed Bomb,Grass,Sleep
Steam Cave,Rock Slide,Rock,Cringe
Upper Steam Cave,Rock Slide,Rock,Cringe
Steam Cave Peak,Rock Slide,Rock,Cringe
Amp Plains,Rock Slide,Rock,Cringe
Far Amp Plains,Rock Slide,Rock,Cringe
Amp Clearing,Rock Slide,Rock,Cringe
Northern Desert,Earthquake,Ground,Accuracy -1
Quicksand Cave,Earthquake,Ground,Accuracy -1
Quicksand Pit,Earthquake,Ground,Accuracy -1
Underground Lake,Rock Slide,Rock,Cringe
Crystal Cave,Ice Beam,Ice,Freeze
Crystal Crossing,Ice Beam,Ice,Freeze
Crystal Lake,Ice Beam,Ice,Freeze
Chasm Cave,Rock Slide,Rock,Cringe
Dark Hill,Rock Slide,Rock,Cringe
Sealed Ruin,Rock Slide,Rock,Cringe
Deep Sealed Ruin,Rock Slide,Rock,Cringe
Sealed Ruin Pit,Rock Slide,Rock,Cringe
Dusk Forest,Seed Bomb,Grass,Sleep
Deep Dusk Forest,Seed Bomb,Grass,Sleep
Treeshroud Forest,Seed Bomb,Grass,Sleep
Brine Cave,Earthquake,Ground,Accuracy -1
Lower Brine Cave,Earthquake,Ground,Accuracy -1
Brine Cave Pit,Rock Slide,Rock,Cringe
Hidden Land,Seed Bomb,Grass,Sleep
Hidden Highland,Seed Bomb,Grass,Sleep
Old Ruins,Tri Attack,Normal,Paralysis
XTemporal Tower,Tri Attack,Normal,Paralysis
XTemporal Spire,Tri Attack,Normal,Paralysis
XTemporal Pinnacle,Earthquake,Ground,Accuracy -1
Mystifying Forest,Seed Bomb,Grass,Sleep
Mystifying Forest Clearing,Earthquake,Ground,Accuracy -1
Blizzard Island,Blizzard,Ice,Freeze
Crevice Cave,Ice Beam,Ice,Freeze
Lower Crevice Cave,Ice Beam,Ice,Freeze
Crevice Cave Pit,Ice Beam,Ice,Freeze
Surrounded Sea,Hydro Pump,Water,Attack -1
Miracle Sea,Hydro Pump,Water,Attack -1
Deep Miracle Sea,Hydro Pump,Water,Attack -1
Miracle Seabed,Hydro Pump,Water,Attack -1
Ice Aegis Cave,Rock Slide,Rock,Cringe
Regice Chamber,Rock Slide,Rock,Cringe
Rock Aegis Cave,Rock Slide,Rock,Cringe
Regirock Chamber,Rock Slide,Rock,Cringe
Steel Aegis Cave,Rock Slide,Rock,Cringe
Registeel Chamber,Rock Slide,Rock,Cringe
Aegis Cave Pit,Rock Slide,Rock,Cringe
Regigigas Chamber,Tri Attack,Normal,Paralysis
Mt. Travail,Rock Slide,Rock,Cringe
The Nightmare,Mud Bomb,Ground,Speed -1
Spacial Rift,Mud Bomb,Ground,Speed -1
Deep Spacial Rift,Mud Bomb,Ground,Speed -1
Spacial Rift Bottom,Mud Bomb,Ground,Speed -1
Dark Crater,Earthquake,Ground,Accuracy -1
Deep Dark Crater,Earthquake,Ground,Accuracy -1
Dark Crater Pit,Earthquake,Ground,Accuracy -1
Concealed Ruins,Tri Attack,Normal,Paralysis
Marine Resort,Seed Bomb,Grass,Sleep
Bottomless Sea,Hydro Pump,Water,Attack -1
Bottomless Sea Depths,Hydro Pump,Water,Attack -1
Shimmer Desert,Earthquake,Ground,Accuracy -1
Shimmer Desert Pit,Earthquake,Ground,Accuracy -1
Mt. Avalanche,Ice Beam,Ice,Freeze
Mt. Avalanche Peak,Ice Beam,Ice,Freeze
Giant Volcano,Rock Slide,Rock,Cringe
Giant Volcano Peak,Rock Slide,Rock,Cringe
World Abyss,Rock Slide,Rock,Cringe
World Abyss Pit,Mud Bomb,Ground,Speed -1
Sky Stairway,Ice Beam,Ice,Freeze
Sky Stairway Apex,Ice Beam,Ice,Freeze
Mystery Jungle,Seed Bomb,Grass,Sleep
Deep Mystery Jungle,Mud Bomb,Ground,Speed -1
Serenity River,Hydro Pump,Water,Attack -1
Landslide Cave,Rock Slide,Rock,Cringe
Lush Prairie,Seed Bomb,Grass,Sleep
Tiny Meadow,Seed Bomb,Grass,Sleep
Labyrinth Cave,Rock Slide,Rock,Cringe
Oran Forest,Seed Bomb,Grass,Sleep
Lake Afar,Hydro Pump,Water,Attack -1
Happy Outlook,Tri Attack,Normal,Paralysis
Mt. Mistral,Rock Slide,Rock,Cringe
Shimmer Hill,Rock Slide,Rock,Cringe
Lost Wilderness,Earthquake,Ground,Accuracy -1
Midnight Forest,Seed Bomb,Grass,Sleep
Oblivion Forest,Seed Bomb,Grass,Sleep
Treacherous Waters,Ice Beam,Ice,Freeze
Southeastern Islands,Earthquake,Ground,Accuracy -1
Inferno Cave,Rock Slide,Rock,Cringe
1st Station Pass,Seed Bomb,Grass,Sleep
2nd Station Pass,Seed Bomb,Grass,Sleep
3rd Station Pass,Rock Slide,Rock,Cringe
4th Station Pass,Seed Bomb,Grass,Sleep
5th Station Pass,Seed Bomb,Grass,Sleep
6th Station Pass,Rock Slide,Rock,Cringe
7th Station Pass,Blizzard,Ice,Freeze
8th Station Pass,Blizzard,Ice,Freeze
9th Station Pass,Rock Slide,Rock,Cringe
Sky Peak Summit Pass,Rock Slide,Rock,Cringe
5th Station Clearing,Seed Bomb,Grass,Sleep
#Sky Peak Summit,Mud Bomb,Ground,Speed -1
Star Cave,Ice Beam,Ice,Freeze
#Deep Star Cave,Ice Beam,Ice,Freeze
Star Cave Depths,Ice Beam,Ice,Freeze
Star Cave Pit,Rock Slide,Rock,Cringe
Murky Forest,Seed Bomb,Grass,Sleep
Eastern Cave,Rock Slide,Rock,Cringe
Fortune Ravine,Rock Slide,Rock,Cringe
Fortune Ravine Depths,Rock Slide,Rock,Cringe
Fortune Ravine Pit,Rock Slide,Rock,Cringe
Barren Valley,Rock Slide,Rock,Cringe
Deep Barren Valley,Rock Slide,Rock,Cringe
Barren Valley Clearing,Rock Slide,Rock,Cringe
Dark Wasteland,Earthquake,Ground,Accuracy -1
Temporal Tower,Tri Attack,Normal,Paralysis
Temporal Spire,Tri Attack,Normal,Paralysis
Dusk Forest,Seed Bomb,Grass,Sleep
Black Swamp,Seed Bomb,Grass,Sleep
Spacial Cliffs,Rock Slide,Rock,Cringe
Dark Ice Mountain,Ice Beam,Ice,Freeze
Dark Ice Mountain Peak,Ice Beam,Ice,Freeze
Icicle Forest,Ice Beam,Ice,Freeze
Vast Ice Mountain,Ice Beam,Ice,Freeze
Vast Ice Mountain Peak,Ice Beam,Ice,Freeze
Vast Ice Mountain Pinnacle,Ice Beam,Ice,Freeze
Southern Jungle,Seed Bomb,Grass,Sleep
Boulder Quarry,Rock Slide,Rock,Cringe
Deep Boulder Quarry,Rock Slide,Rock,Cringe
Boulder Quarry Clearing,Rock Slide,Rock,Cringe
Right Cave Path,Ice Beam,Ice,Freeze
Left Cave Path,Tri Attack,Normal,Paralysis
Limestone Cavern,Rock Slide,Rock,Cringe
Deep Limestone Cavern,Rock Slide,Rock,Cringe
Limestone Cavern Depths,Rock Slide,Rock,Cringe
Spring Cave,Rock Slide,Rock,Cringe
Upper Spring Cave,Rock Slide,Rock,Cringe
Middle Spring Cave,Rock Slide,Rock,Cringe
Lower Spring Cave,Rock Slide,Rock,Cringe
Spring Cave Depths,Rock Slide,Rock,Cringe
Spring Cave Pit,Rock Slide,Rock,Cringe
Little Plains,Seed Bomb,Grass,Sleep
Mt. Clear,Seed Bomb,Grass,Sleep
Challenge River,Hydro Pump,Water,Attack -1
Trial Forest,Seed Bomb,Grass,Sleep
Guiding Sea,Hydro Pump,Water,Attack -1
Hidden Shopkeeper Village,Seed Bomb,Grass,Sleep
Normal/Fly Maze,Rock Slide,Rock,Cringe
Dark/Fire Maze,Rock Slide,Rock,Cringe
Rock/Water Maze,Ice Beam,Ice,Freeze
Grass Maze,Seed Bomb,Grass,Sleep
Elec/Steel Maze,Tri Attack,Normal,Paralysis
Ice/Ground Maze,Blizzard,Ice,Freeze
Fight/Psych Maze,Tri Attack,Normal,Paralysis
Poison/Bug Maze,Earthquake,Ground,Accuracy -1
Dragon Maze,Rock Slide,Rock,Cringe
Ghost Maze,Tri Attack,Normal,Paralysis"""

dungeon_name_map = {}
str_blk = ppmdu_us.string_index_data.string_blocks['Dungeon Names (Main)']
string = FileType.STR.deserialize(rom_us.getFileByName('MESSAGE/text_e.str'))
mappa = FileType.MAPPA_BIN.deserialize(rom_us.getFileByName('BALANCE/mappa_s.bin'))
dungeons = HardcodedDungeons.get_dungeon_list(arm9_us, ppmdu_us)
for i, idx in enumerate(range(str_blk.begin, str_blk.end)):
    dungeon_name_map[string.strings[idx]] = i
for dungeon_name, nature_power, camouflage, secret_power in csv.reader(info.splitlines()):
    try:
        dungeon_idx = dungeon_name_map[dungeon_name]
    except KeyError:
        print(f"dungeon {dungeon_name} not found.")
        continue
    if dungeon_idx > 179:
        continue
    dungeon = dungeons[dungeon_idx]
    tileset_id = mappa.floor_lists[dungeon.mappa_index][dungeon.start_after].layout.tileset_id
    entry = lst[tileset_id]
    assert entry.camouflage_type.print_name == camouflage, f"{dungeon_name}, {tileset_id}: Camouflage ({entry.camouflage_type}) must be {camouflage}"
    if tileset_id != 133:
        assert entry.secret_power_effect.print_name == secret_power, f"{dungeon_name}, {tileset_id}: Secret Power ({entry.secret_power_effect}) must be {secret_power}"
    assert entry.nature_power_move_entry.print_name == nature_power, f"{dungeon_name}, {tileset_id}: Nature Power ({entry.nature_power_move_entry}) must be {nature_power}"
