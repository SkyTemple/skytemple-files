"""Module for editing hardcoded data for the dungeons."""
#  Copyright 2020 Parakoopa
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
from typing import List

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_uintle, write_uintle, AutoString


class DungeonDefinition(AutoString):
    def __init__(self, number_floors: int, mappa_index: int, start_after: int, number_floors_in_group: int):
        self.number_floors = number_floors
        self.mappa_index = mappa_index
        self.start_after = start_after
        self.number_floors_in_group = number_floors_in_group

    def __eq__(self, other):
        if not isinstance(other, DungeonDefinition):
            return False
        return self.number_floors == other.number_floors and \
               self.mappa_index == other.mappa_index and \
               self.start_after == other.start_after and \
               self.number_floors_in_group == other.number_floors_in_group


class HardcodedDungeons:
    @staticmethod
    def get_dungeon_list(arm9bin: bytes, config: Pmd2Data) -> List[DungeonDefinition]:
        """Returns the list of dungeon definitions."""
        block = config.binaries['arm9.bin'].blocks['DungeonList']
        lst = []
        for i in range(block.begin, block.end, 4):
            lst.append(DungeonDefinition(
                read_uintle(arm9bin, i),
                read_uintle(arm9bin, i + 1),
                read_uintle(arm9bin, i + 2),
                read_uintle(arm9bin, i + 3),
            ))
        return lst

    @staticmethod
    def set_dungeon_list(value: List[DungeonDefinition], arm9bin: bytearray, config: Pmd2Data):
        """
        Sets the dungeon definitions.
        The length of the list must exactly match the original ROM's length (see get_dungeon_list).
        """
        block = config.binaries['arm9.bin'].blocks['DungeonList']
        expected_length = int((block.end - block.begin) / 4)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            arm9bin[block.begin + i * 4:block.begin + (i + 1) * 4] = bytes([
                entry.number_floors, entry.mappa_index, entry.start_after, entry.number_floors_in_group
            ])
