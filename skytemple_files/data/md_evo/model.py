#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
from skytemple_files.common.i18n_util import _
from skytemple_files.data.md_evo import *


class MdEvoEntry(AutoString):
    def __init__(self, data: bytes):
        nb_evos = read_uintle(data, 0, 2)
        self.evos = []
        for x in range(2, nb_evos*2+2, 2):
            self.evos.append(read_uintle(data, x, 2))
        nb_eggs = read_uintle(data, 0x12, 2)
        self.eggs = []
        for x in range(0x14, nb_eggs*2+0x14, 2):
            self.eggs.append(read_uintle(data, x, 2))
    def to_bytes(self):
        mevo_data = bytearray(MEVO_ENTRY_LENGTH)
        write_uintle(mevo_data, len(self.evos), 0, 2)
        for j,x in enumerate(self.evos):
            write_uintle(mevo_data, x, j*2+2, 2)
        write_uintle(mevo_data, len(self.eggs), 0x12, 2)
        for j,x in enumerate(self.eggs):
            write_uintle(mevo_data, x, j*2+0x14, 2)
        return mevo_data

class MdEvoStats(AutoString):
    def __init__(self, data: bytes):
        self.hp_bonus = read_sintle(data, 0, 2)
        self.atk_bonus = read_sintle(data, 2, 2)
        self.spatk_bonus = read_sintle(data, 4, 2)
        self.def_bonus = read_sintle(data, 6, 2)
        self.spdef_bonus = read_sintle(data, 8, 2)
    def to_bytes(self):
        mevo_data = bytearray(MEVO_STATS_LENGTH)
        write_sintle(mevo_data, self.hp_bonus, 0, 2)
        write_sintle(mevo_data, self.atk_bonus, 2, 2)
        write_sintle(mevo_data, self.spatk_bonus, 4, 2)
        write_sintle(mevo_data, self.def_bonus, 6, 2)
        write_sintle(mevo_data, self.spdef_bonus, 8, 2)
        return mevo_data


class MdEvo(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        limit = read_uintle(data, 0, 4)
        self.evo_entries = []
        for x in range(4, limit, MEVO_ENTRY_LENGTH):
            self.evo_entries.append(MdEvoEntry(data[x:x+MEVO_ENTRY_LENGTH]))
        self.evo_stats = []
        for x in range(limit, len(data), MEVO_STATS_LENGTH):
            self.evo_stats.append(MdEvoStats(data[x:x+MEVO_STATS_LENGTH]))
    
    def __eq__(self, other):
        if not isinstance(other, MdEvo):
            return False
        return self.evo_entries == other.evo_entries and \
               self.evo_stats == other.evo_stats
