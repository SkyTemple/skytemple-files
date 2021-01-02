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

ENTRY_LEN = 16


class Rank(AutoString):
    def __init__(self, rank_name_str: int, points_needed_next: int, storage_capacity: int, item_awarded: int):
        self.rank_name_str = rank_name_str
        self.points_needed_next = points_needed_next
        self.storage_capacity = storage_capacity
        self.item_awarded = item_awarded

    def to_bytes(self) -> bytes:
        buffer = bytearray(ENTRY_LEN)
        write_uintle(buffer, self.rank_name_str, 0x00, 4)
        write_uintle(buffer, self.points_needed_next, 0x04, 4)
        write_uintle(buffer, self.storage_capacity, 0x08, 4)
        write_uintle(buffer, self.item_awarded, 0x0C, 4)
        return buffer

    def __eq__(self, other):
        if not isinstance(other, Rank):
            return False
        return self.rank_name_str == other.rank_name_str and self.points_needed_next == other.points_needed_next \
                and self.storage_capacity == other.storage_capacity and self.item_awarded == other.item_awarded


class HardcodedRankUpTable:
    @classmethod
    def get_rank_up_table(cls, arm9bin: bytes, config: Pmd2Data) -> List[Rank]:
        """Returns the list of ranks in the game."""
        block = config.binaries['arm9.bin'].blocks['RankUpTable']
        lst = []
        for i in range(block.begin, block.end, ENTRY_LEN):
            lst.append(Rank(
                read_uintle(arm9bin, i + 0x00, 4),
                read_uintle(arm9bin, i + 0x04, 4),
                read_uintle(arm9bin, i + 0x08, 4),
                read_uintle(arm9bin, i + 0x0C, 4)
            ))
        return lst

    @classmethod
    def set_rank_up_table(cls, value: List[Rank], arm9bin: bytearray, config: Pmd2Data):
        """
        Sets the list of ranks in the game.
        The length of the list must exactly match the original ROM's length (see get_rank_up_table).
        """
        block = config.binaries['arm9.bin'].blocks['RankUpTable']
        expected_length = int((block.end - block.begin) / ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            arm9bin[block.begin + (i * ENTRY_LEN):block.begin + ((i + 1) * ENTRY_LEN)] = entry.to_bytes()
