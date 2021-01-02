"""
This table is stored in ARM9 and has two entries for every Pokémon base form.
- The first one seems to be how many 16x16 tile slots (or 256 byte pixels) the
  Pokémon's sprite will take up.
- The second is unknown, but also related to the sprite size?
"""
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
from skytemple_files.common.util import read_uintle, AutoString

ENTRY_LEN = 2


class MonsterSpriteDataTableEntry(AutoString):
    def __init__(self, sprite_tile_slots: int, unk1: int):
        self.sprite_tile_slots = sprite_tile_slots
        self.unk1 = unk1

    def to_bytes(self) -> bytes:
        return bytes([self.sprite_tile_slots, self.unk1])

    def __eq__(self, other):
        if not isinstance(other, MonsterSpriteDataTableEntry):
            return False
        return self.sprite_tile_slots == other.sprite_tile_slots and self.unk1 == other.unk1


class HardcodedMonsterSpriteDataTable:
    @classmethod
    def get(cls, arm9bin: bytes, config: Pmd2Data) -> List[MonsterSpriteDataTableEntry]:
        """Returns the list."""
        block = config.binaries['arm9.bin'].blocks['MonsterSpriteData']
        lst = []
        for i in range(block.begin, block.end, ENTRY_LEN):
            lst.append(MonsterSpriteDataTableEntry(
                read_uintle(arm9bin, i + 0x00, 1),
                read_uintle(arm9bin, i + 0x01, 1)
            ))
        return lst

    @classmethod
    def set(cls, value: List[MonsterSpriteDataTableEntry], arm9bin: bytearray, config: Pmd2Data):
        """
        Sets the list.
        The length of the list must exactly match the original ROM's length (see get).
        """
        block = config.binaries['arm9.bin'].blocks['MonsterSpriteData']
        expected_length = int((block.end - block.begin) / ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            arm9bin[block.begin + (i * ENTRY_LEN):block.begin + ((i + 1) * ENTRY_LEN)] = entry.to_bytes()
