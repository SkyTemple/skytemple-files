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

from enum import Enum
from typing import List

from range_typed_integers import u8, u16

from skytemple_files.common.i18n_util import _
from skytemple_files.common.util import (
    AutoString,
    read_u8,
    read_u16,
    write_u16,
    read_u32,
    write_u8,
)


class InterDEntryType(Enum):
    ALWAYS = 0x00, _("Always")
    FNSET = 0x01, _("Flag Not Set")
    FSET = 0x02, _("Flag Set")
    SCNEQ = 0x03, _("Scenario Equals")
    SCNBE = 0x04, _("Scenario Below or Equal")
    SCNGE = 0x05, _("Scenario Greater or Equal")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, explanation: str):
        self.explanation = explanation


class InterDEntry(AutoString):
    floor: u8
    continue_music: bool
    ent_type: InterDEntryType
    game_var_id: u16
    param1: u8
    param2: u8

    def __init__(self, data: bytes = bytes(6)):
        floor_attrib = read_u8(data, 0)
        self.floor = u8(floor_attrib & 0x7F)
        self.continue_music = bool(floor_attrib & 0x80)
        self.ent_type = InterDEntryType(read_u8(data, 1))  # type: ignore
        self.game_var_id = read_u16(data, 2)
        self.param1 = read_u8(data, 4)
        self.param2 = read_u8(data, 5)

    def to_bytes(self) -> bytes:
        data = bytearray(6)
        write_u8(data, u8((self.floor & 0x7F) + (int(self.continue_music) << 7)), 0)
        write_u8(data, self.ent_type.value, 1)
        write_u16(data, self.game_var_id, 2)
        write_u8(data, self.param1, 4)
        write_u8(data, self.param2, 5)
        return bytes(data)


class InterD(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.list_dungeons: List[List[InterDEntry]] = []
        limit = read_u32(data, 0)
        prev = read_u16(data, 4)
        for x in range(6, limit, 2):
            cur = read_u16(data, x)
            self.list_dungeons.append([])
            for y in range(limit + prev * 6, limit + cur * 6, 6):
                self.list_dungeons[-1].append(InterDEntry(data[y : y + 6]))
            prev = cur

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, InterD):
            return False
        return self.list_dungeons == other.list_dungeons
