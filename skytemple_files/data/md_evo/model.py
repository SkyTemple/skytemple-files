#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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
from __future__ import annotations

from typing import List

from range_typed_integers import u8_checked, u16_checked, u16, i16

from skytemple_files.common.util import (
    AutoString,
    read_u16,
    read_i16,
    write_u16,
    write_i16,
    read_u32,
    write_u8,
)
from skytemple_files.data.md_evo import MEVO_ENTRY_LENGTH, MEVO_STATS_LENGTH


class MdEvoEntry(AutoString):
    evos: List[u16]
    eggs: List[u16]

    def __init__(self, data: bytes):
        nb_evos = read_u16(data, 0)
        self.evos = []
        for x in range(2, nb_evos * 2 + 2, 2):
            self.evos.append(read_u16(data, x))
        nb_eggs = read_u16(data, 0x12)
        self.eggs = []
        for x in range(0x14, nb_eggs * 2 + 0x14, 2):
            self.eggs.append(read_u16(data, x))

    def to_bytes(self):
        mevo_data = bytearray(MEVO_ENTRY_LENGTH)
        write_u16(mevo_data, u16_checked(len(self.evos)), 0)
        for j, x in enumerate(self.evos):
            write_u16(mevo_data, x, j * 2 + 2)
        write_u8(mevo_data, u8_checked(len(self.eggs)), 0x12)
        for j, x in enumerate(self.eggs):
            write_u16(mevo_data, x, j * 2 + 0x14)
        return mevo_data


class MdEvoStats(AutoString):
    hp_bonus: i16
    atk_bonus: i16
    spatk_bonus: i16
    def_bonus: i16
    spdef_bonus: i16

    def __init__(self, data: bytes):
        self.hp_bonus = read_i16(data, 0)
        self.atk_bonus = read_i16(data, 2)
        self.spatk_bonus = read_i16(data, 4)
        self.def_bonus = read_i16(data, 6)
        self.spdef_bonus = read_i16(data, 8)

    def to_bytes(self):
        mevo_data = bytearray(MEVO_STATS_LENGTH)
        write_i16(mevo_data, self.hp_bonus, 0)
        write_i16(mevo_data, self.atk_bonus, 2)
        write_i16(mevo_data, self.spatk_bonus, 4)
        write_i16(mevo_data, self.def_bonus, 6)
        write_i16(mevo_data, self.spdef_bonus, 8)
        return mevo_data


class MdEvo(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        limit = read_u32(data, 0)
        self.evo_entries = []
        for x in range(4, limit, MEVO_ENTRY_LENGTH):
            self.evo_entries.append(MdEvoEntry(data[x : x + MEVO_ENTRY_LENGTH]))
        self.evo_stats = []
        for x in range(limit, len(data), MEVO_STATS_LENGTH):
            self.evo_stats.append(MdEvoStats(data[x : x + MEVO_STATS_LENGTH]))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MdEvo):
            return False
        return (
            self.evo_entries == other.evo_entries and self.evo_stats == other.evo_stats
        )
