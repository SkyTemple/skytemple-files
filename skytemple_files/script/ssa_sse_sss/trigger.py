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

import logging

from range_typed_integers import u16

from skytemple_files.common.ppmdu_config.script_data import (
    Pmd2ScriptData,
    Pmd2ScriptRoutine,
)
from skytemple_files.common.util import AutoString

logger = logging.getLogger(__name__)


class SsaTrigger(AutoString):
    """NOTE: This is called Event in SkyTemple. Trigger is the historic name from reverse engineering."""

    coroutine: Pmd2ScriptRoutine
    unk2: u16
    unk3: u16
    script_id: u16

    def __init__(
        self,
        scriptdata: Pmd2ScriptData,
        coroutine_id: u16,
        unk2: u16,
        unk3: u16,
        script_id: u16,
    ):
        try:
            self.coroutine = scriptdata.common_routine_info__by_id[coroutine_id]
        except KeyError:
            logger.warning(f"Unknown coroutine id: {coroutine_id}")
            self.coroutine = Pmd2ScriptRoutine(coroutine_id, 0, "UNKNOWN")
        self.unk2 = unk2
        self.unk3 = unk3
        self.script_id = script_id
