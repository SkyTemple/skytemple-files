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

from range_typed_integers import i32, u16, u8

from skytemple_files.common.util import AutoString, read_i32, read_u16, read_u8, chunks

LEVEL_BIN_ENTRY_LEVEL_LEN = 12


class LevelEntry(AutoString):
    experience_required: i32
    hp_growth: u16
    attack_growth: u8
    special_attack_growth: u8
    defense_growth: u8
    special_defense_growth: u8
    null: u16

    def __init__(
        self,
        experience_required: i32,
        hp_growth: u16,
        attack_growth: u8,
        special_attack_growth: u8,
        defense_growth: u8,
        special_defense_growth: u8,
        null: u16,
    ):
        self.experience_required = experience_required
        self.hp_growth = hp_growth
        self.attack_growth = attack_growth
        self.special_attack_growth = special_attack_growth
        self.defense_growth = defense_growth
        self.special_defense_growth = special_defense_growth
        self.null = null
        assert self.null == 0


class LevelBinEntry(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        self.levels = []

        for chunk in chunks(data, LEVEL_BIN_ENTRY_LEVEL_LEN):
            self.levels.append(
                LevelEntry(
                    read_i32(chunk, 0),
                    read_u16(chunk, 4),
                    read_u8(chunk, 6),
                    read_u8(chunk, 7),
                    read_u8(chunk, 8),
                    read_u8(chunk, 9),
                    read_u16(chunk, 10),
                )
            )

    def __len__(self):
        return len(self.levels)

    def __getitem__(self, key):
        return self.levels[key]

    def __setitem__(self, key, value):
        self.levels[key] = value

    def __delitem__(self, key):
        del self.levels[key]

    def __iter__(self):
        return iter(self.levels)
