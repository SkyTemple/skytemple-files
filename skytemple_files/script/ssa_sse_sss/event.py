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
from skytemple_files.common.util import AutoString
from skytemple_files.script.ssa_sse_sss import TRIGGER_ENTRY_LEN
from skytemple_files.script.ssa_sse_sss.position import SsaPosition


class SsaEvent(AutoString):
    def __init__(self, trigger_width, trigger_height, trigger_pointer, trigger_table_start, pos: SsaPosition, unkE):
        self.trigger_width = trigger_width
        self.trigger_height = trigger_height
        # If the table start is 0, switch to "set id mode"
        if trigger_table_start == 0:
            self.trigger_id = trigger_pointer
        else:
            self.trigger_id = int((trigger_pointer - trigger_table_start) / TRIGGER_ENTRY_LEN)
        # direction must be none!
        self.pos = pos
        self.unkE = unkE
