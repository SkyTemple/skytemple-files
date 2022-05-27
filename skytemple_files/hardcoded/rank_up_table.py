#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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

from range_typed_integers import u32

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_u32, write_u32, AutoString, CheckedIntWrites

ENTRY_LEN = 16


class Rank(AutoString, CheckedIntWrites):
    rank_name_str: u32
    points_needed_next: u32
    storage_capacity: u32
    item_awarded: u32

    def __init__(self, rank_name_str: u32, points_needed_next: u32, storage_capacity: u32, item_awarded: u32):
        self.rank_name_str = rank_name_str
        self.points_needed_next = points_needed_next
        self.storage_capacity = storage_capacity
        self.item_awarded = item_awarded

    def to_bytes(self) -> bytes:
        buffer = bytearray(ENTRY_LEN)
        write_u32(buffer, self.rank_name_str, 0x00)
        write_u32(buffer, self.points_needed_next, 0x04)
        write_u32(buffer, self.storage_capacity, 0x08)
        write_u32(buffer, self.item_awarded, 0x0C)
        return buffer

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rank):
            return False
        return self.rank_name_str == other.rank_name_str and self.points_needed_next == other.points_needed_next \
                and self.storage_capacity == other.storage_capacity and self.item_awarded == other.item_awarded


class HardcodedRankUpTable:
    @classmethod
    def get_rank_up_table(cls, arm9bin: bytes, config: Pmd2Data) -> List[Rank]:
        """Returns the list of ranks in the game."""
        block = config.binaries['arm9.bin'].symbols['RankUpTable']
        lst = []
        for i in range(block.begin, block.end, ENTRY_LEN):
            lst.append(Rank(
                read_u32(arm9bin, i + 0x00),
                read_u32(arm9bin, i + 0x04),
                read_u32(arm9bin, i + 0x08),
                read_u32(arm9bin, i + 0x0C)
            ))
        return lst

    @classmethod
    def set_rank_up_table(cls, value: List[Rank], arm9bin: bytearray, config: Pmd2Data) -> None:
        """
        Sets the list of ranks in the game.
        The length of the list must exactly match the original ROM's length (see get_rank_up_table).
        """
        block = config.binaries['arm9.bin'].symbols['RankUpTable']
        expected_length = int((block.end - block.begin) / ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            arm9bin[block.begin + (i * ENTRY_LEN):block.begin + ((i + 1) * ENTRY_LEN)] = entry.to_bytes()
