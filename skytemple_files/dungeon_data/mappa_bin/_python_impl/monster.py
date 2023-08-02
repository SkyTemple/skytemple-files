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

from typing import TYPE_CHECKING, List

from range_typed_integers import u8, u16

from skytemple_files.common.util import (
    AutoString,
    read_u16,
    write_u16,
)
from skytemple_files.dungeon_data.mappa_bin.protocol import (
    MappaMonsterProtocol,
    LEVEL_MULTIPLIER,
)

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin._python_impl.model import (
        MappaBinReadContainer,
    )


class MappaMonster(MappaMonsterProtocol, AutoString):
    level: u8
    main_spawn_weight: u16
    monster_house_spawn_weight: u16
    md_index: u16

    def __init__(
        self,
        level: u8,
        main_spawn_weight: u16,
        monster_house_spawn_weight: u16,
        md_index: u16,
    ):
        self.level = level
        self.main_spawn_weight = main_spawn_weight
        self.monster_house_spawn_weight = monster_house_spawn_weight
        self.md_index = md_index

    @classmethod
    def list_from_mappa(
        cls, read: "MappaBinReadContainer", pointer: int
    ) -> List["MappaMonster"]:
        monsters = []
        while not cls._is_end_of_entries(read.data, pointer):
            monsters.append(
                MappaMonster(
                    u8(read_u16(read.data, pointer + 0) // LEVEL_MULTIPLIER),
                    read_u16(read.data, pointer + 2),
                    read_u16(read.data, pointer + 4),
                    read_u16(read.data, pointer + 6),
                )
            )
            pointer += 8
        return monsters

    def to_mappa(self):
        data = bytearray(8)
        write_u16(data, u16(self.level * LEVEL_MULTIPLIER), 0x00)
        write_u16(data, self.main_spawn_weight, 0x02)
        write_u16(data, self.monster_house_spawn_weight, 0x04)
        write_u16(data, self.md_index, 0x06)
        return data

    @classmethod
    def _is_end_of_entries(cls, data: bytes, pointer):
        return read_u16(data, pointer + 6) == 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MappaMonster):
            return False
        return (
            self.md_index == other.md_index
            and self.level == other.level
            and self.main_spawn_weight == other.main_spawn_weight
            and self.monster_house_spawn_weight == other.monster_house_spawn_weight
        )
