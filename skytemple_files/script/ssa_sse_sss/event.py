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

from range_typed_integers import u16

from skytemple_files.common.util import AutoString
from skytemple_files.script.ssa_sse_sss import TRIGGER_ENTRY_LEN
from skytemple_files.script.ssa_sse_sss.position import SsaPosition

INVALID_TRIGGER = 99999


class SsaEvent(AutoString):
    """NOTE: This is called Trigger in SkyTemple. Event is the historic name from reverse engineering."""

    trigger_width: u16
    trigger_height: u16
    trigger_pointer: int
    trigger_table_start: u16
    pos: SsaPosition
    unkE: u16

    def __init__(
        self,
        trigger_width: u16,
        trigger_height: u16,
        trigger_pointer: int,
        trigger_table_start: u16,
        pos: SsaPosition,
        unkE: u16,
    ):
        self.trigger_width = trigger_width
        self.trigger_height = trigger_height
        # If the table start is 0, switch to "set id mode"
        if trigger_table_start == 0:
            self.trigger_id = trigger_pointer
        else:
            try:
                self.trigger_id = (
                    trigger_pointer - trigger_table_start
                ) // TRIGGER_ENTRY_LEN
            except TypeError:
                # If this fails, this event has somehow no trigger assigned.
                self.trigger_id = INVALID_TRIGGER
        # direction must be none!
        self.pos = pos
        self.unkE = unkE

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return (
            self.trigger_id == other.trigger_id
            and self.trigger_width == other.trigger_width
            and self.trigger_height == other.trigger_height
            and self.pos == other.pos
            and self.unkE == other.unkE
        )
