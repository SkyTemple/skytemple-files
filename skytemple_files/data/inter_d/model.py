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

from enum import Enum, auto

from skytemple_files.common.util import *
from skytemple_files.common.i18n_util import _


class InterDEntryType(Enum):
    ALWAYS = 0x00, _('Always')
    FNSET  = 0x01, _('Flag Not Set')
    FSET   = 0x02, _('Flag Set')
    SCNEQ  = 0x03, _('Scenario Equals')
    SCNBE  = 0x04, _('Scenario Below or Equal')
    SCNGE  = 0x05, _('Scenario Greater or Equal')
    
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: int, explanation: str
    ):
        self.explanation = explanation
    
class InterDEntry(AutoString):
    def __init__(self, data: bytes = bytes(6)):
        self.floor = read_uintle(data, 0, 1)
        self.ent_type = InterDEntryType(read_uintle(data, 1, 1))
        self.game_var_id = read_uintle(data, 2, 2)
        self.param1 = read_uintle(data, 4, 1)
        self.param2 = read_uintle(data, 5, 1)

    def to_bytes(self) -> bytes:
        data = bytearray(6)
        write_uintle(data, self.floor, 0, 1)
        write_uintle(data, self.ent_type.value, 1, 1)
        write_uintle(data, self.game_var_id, 2, 2)
        write_uintle(data, self.param1, 4, 1)
        write_uintle(data, self.param2, 5, 1)
        return bytes(data)
    
class InterD(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.list_dungeons = []
        limit = read_uintle(data, 0, 4)
        prev = read_uintle(data, 4, 2)
        for x in range(6, limit, 2):
            cur = read_uintle(data, x, 2)
            self.list_dungeons.append([])
            for y in range(limit+prev*6, limit+cur*6, 6):
                self.list_dungeons[-1].append(InterDEntry(data[y:y+6]))
            prev = cur

    def __eq__(self, other):
        if not isinstance(other, InterD):
            return False
        return self.list_dungeons == other.list_dungeons
