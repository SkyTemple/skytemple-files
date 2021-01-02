"""Module for editing the hardcoded table mapping of ground levels to dungeon tilesets."""
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
from typing import List

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_uintle, write_uintle, AutoString


class GroundTilesetMapping(AutoString):
    def __init__(self, ground_level: int, dungeon_tileset: int, unk2: int, unk3: int):
        self.ground_level = ground_level
        self.dungeon_id = dungeon_tileset
        self.unk2 = unk2  # TODO: Rename in floor_id
        self.unk3 = unk3

    def __eq__(self, other):
        if not isinstance(other, GroundTilesetMapping):
            return False
        return self.ground_level == other.ground_level and \
               self.dungeon_id == other.dungeon_id and \
               self.unk2 == other.unk2 and \
               self.unk3 == other.unk3

    def to_bytes(self) -> bytes:
        return self.ground_level.to_bytes(2, 'little', signed=False) + \
               self.dungeon_id.to_bytes(1, 'little', signed=False) + \
               self.unk2.to_bytes(1, 'little', signed=False) + \
               self.unk3.to_bytes(4, 'little', signed=False)


class HardcodedGroundDungeonTilesets:
    @staticmethod
    def get_ground_dungeon_tilesets(overlay11bin: bytes, config: Pmd2Data) -> List[GroundTilesetMapping]:
        """Returns the list."""
        block = config.binaries['overlay/overlay_0011.bin'].blocks['LevelTilemapList']
        lst = []
        for i in range(block.begin, block.end, 8):
            lst.append(GroundTilesetMapping(
                read_uintle(overlay11bin, i, 2),
                read_uintle(overlay11bin, i + 2, 1),
                read_uintle(overlay11bin, i + 3, 1),
                read_uintle(overlay11bin, i + 4, 4),
            ))
        return lst

    @staticmethod
    def set_ground_dungeon_tilesets(value: List[GroundTilesetMapping], overlay11bin: bytearray, config: Pmd2Data):
        """
        Sets the  list.
        The length of the list must exactly match the original ROM's length (see get_dungeon_list).
        """
        block = config.binaries['overlay/overlay_0011.bin'].blocks['LevelTilemapList']
        expected_length = int((block.end - block.begin) / 8)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            overlay11bin[block.begin + i * 8:block.begin + (i + 1) * 8] = entry.to_bytes()
