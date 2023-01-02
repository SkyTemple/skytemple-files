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

from range_typed_integers import i16, u16

from skytemple_files.common.ppmdu_config.script_data import (
    Pmd2ScriptData,
    Pmd2ScriptEntity,
)
from skytemple_files.common.util import AutoString
from skytemple_files.script.ssa_sse_sss.position import SsaPosition

logger = logging.getLogger(__name__)


class SsaActor(AutoString):
    scriptdata: Pmd2ScriptData
    actor_id: u16
    pos: SsaPosition
    script_id: i16
    unkE: i16

    def __init__(
        self,
        scriptdata: Pmd2ScriptData,
        actor_id: u16,
        pos: SsaPosition,
        script_id: i16,
        unkE: i16,
    ):
        try:
            self.actor = scriptdata.level_entities__by_id[actor_id]
        except KeyError:
            logger.warning(f"Unknown actor id: {actor_id}")
            self.actor = Pmd2ScriptEntity(
                actor_id, u16(0), "UNKNOWN", u16(0), u16(0), u16(0)
            )
        self.pos = pos
        self.script_id = script_id
        self.unkE = unkE
