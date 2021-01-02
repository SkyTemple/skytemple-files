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
from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_ppmdu_config_for_rom, get_binary_from_rom_ppmdu
from skytemple_files.dungeon_data.mappa_bin.validator.exception import DungeonTotalFloorCountInvalidError
from skytemple_files.dungeon_data.mappa_bin.validator.validator import DungeonValidator
from skytemple_files.hardcoded.dungeons import HardcodedDungeons

rom = NintendoDSRom.fromFile('../../../../../4261 - Pokemon Mystery Dungeon Explorers of Sky (U)(Xenophobia).nds')
config = get_ppmdu_config_for_rom(rom)

mappa_bin = rom.getFileByName('BALANCE/mappa_s.bin')
mappa = FileType.MAPPA_BIN.deserialize(mappa_bin)

dungeons = HardcodedDungeons.get_dungeon_list(
    get_binary_from_rom_ppmdu(rom, config.binaries['arm9.bin']),
    config
)

for i, dungeon in enumerate(dungeons):
    print(i, dungeon)
print("")

validator = DungeonValidator(mappa.floor_lists)
validator.validate(dungeons)
for e in validator.errors:
    if not isinstance(e, DungeonTotalFloorCountInvalidError):
        print(repr(e))

print("")
print(validator.invalid_dungeons)
