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
from typing import TYPE_CHECKING, List

from skytemple_files.common.util import read_uintle, AutoString

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin.model import MappaBinReadContainer
DUMMY_MD_INDEX = 0x229
LEVEL_MULTIPLIER = 512


class MappaMonster(AutoString):
    def __init__(self, level: int, spawn_weight: int, spawn_weight2: int, md_index: id):
        self.level = level
        self.spawn_weight = spawn_weight
        self.spawn_weight2 = spawn_weight2
        self.md_index = md_index

    @classmethod
    def list_from_mappa(cls, read: 'MappaBinReadContainer', pointer: int) -> List['MappaMonster']:
        monsters = []
        while not cls._is_dummy_entry(read.data, pointer):
            monsters.append(MappaMonster(
                int(read_uintle(read.data, pointer + 0, 2) / LEVEL_MULTIPLIER),
                read_uintle(read.data, pointer + 2, 2),
                read_uintle(read.data, pointer + 4, 2),
                read_uintle(read.data, pointer + 6, 2),
            ))
            pointer += 8
        return monsters

    @classmethod
    def _is_dummy_entry(cls, data: memoryview, pointer):
        return read_uintle(data, pointer + 6, 2) == DUMMY_MD_INDEX
