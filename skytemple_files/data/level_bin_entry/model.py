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
from skytemple_files.common.util import *


LEVEL_BIN_ENTRY_LEVEL_LEN = 12


class LevelEntry(AutoString):
    def __init__(
            self, experience_required: int, hp_growth: int,
            attack_growth: int, special_attack_growth: int,
            defense_growth: int, special_defense_growth: int, null: int
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
            self.levels.append(LevelEntry(
                read_sintle(chunk, 0, 4),
                read_uintle(chunk, 4, 2),
                read_uintle(chunk, 6),
                read_uintle(chunk, 7),
                read_uintle(chunk, 8),
                read_uintle(chunk, 9),
                read_uintle(chunk, 10, 2)
            ))

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
