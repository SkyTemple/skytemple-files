"""Converts LevelBinEntry models back into the binary format used by the game"""
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
from skytemple_files.data.level_bin_entry.model import LevelBinEntry, LEVEL_BIN_ENTRY_LEVEL_LEN


class LevelBinEntryWriter:
    def __init__(self, model: LevelBinEntry):
        self.model = model

    def write(self) -> bytes:
        data = bytearray(LEVEL_BIN_ENTRY_LEVEL_LEN * len(self.model.levels))
        for i, level in enumerate(self.model.levels):
            write_sintle(data, level.experience_required,    i * LEVEL_BIN_ENTRY_LEVEL_LEN + 0x0, 4)
            write_uintle(data, level.hp_growth,              i * LEVEL_BIN_ENTRY_LEVEL_LEN + 0x4, 2)
            write_uintle(data, level.attack_growth,          i * LEVEL_BIN_ENTRY_LEVEL_LEN + 0x6, 1)
            write_uintle(data, level.special_attack_growth,  i * LEVEL_BIN_ENTRY_LEVEL_LEN + 0x7, 1)
            write_uintle(data, level.defense_growth,         i * LEVEL_BIN_ENTRY_LEVEL_LEN + 0x8, 1)
            write_uintle(data, level.special_defense_growth, i * LEVEL_BIN_ENTRY_LEVEL_LEN + 0x9, 1)
            write_uintle(data, level.null,                   i * LEVEL_BIN_ENTRY_LEVEL_LEN + 0xA, 2)
        return data
