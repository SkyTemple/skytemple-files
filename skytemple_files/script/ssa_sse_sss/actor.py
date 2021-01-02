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
import logging
import warnings

from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptData, Pmd2ScriptEntity
from skytemple_files.common.util import AutoString
from skytemple_files.script.ssa_sse_sss.position import SsaPosition
logger = logging.getLogger(__name__)


class SsaActor(AutoString):
    def __init__(self, scriptdata: Pmd2ScriptData, actor_id, pos: SsaPosition, script_id, unkE):
        try:
            self.actor = scriptdata.level_entities__by_id[actor_id]
        except KeyError:
            logger.warning(f"Unknown actor id: {actor_id}")
            self.actor = Pmd2ScriptEntity(actor_id, 0, 'UNKNOWN', 0, 0, 0)
        self.pos = pos
        self.script_id = script_id
        self.unkE = unkE
