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
from typing import Union, Tuple

from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptData, Pmd2ScriptDirection
from skytemple_files.common.util import AutoString
from skytemple_files.graphics.bpc.model import BPC_TILE_DIM

logger = logging.getLogger(__name__)


TILE_SIZE = 8
ACTOR_DEFAULT_HITBOX_W = 2 * BPC_TILE_DIM
ACTOR_DEFAULT_HITBOX_H = 1 * BPC_TILE_DIM


class SsaPosition(AutoString):
    def __init__(self, scriptdata: Pmd2ScriptData, x_pos, y_pos, x_offset, y_offset, direction=None):
        """
        Common SSA position specification. Direction is optional if not applicable.
        """
        self.x_relative = x_pos
        self.y_relative = y_pos

        self.x_offset = x_offset
        self.y_offset = y_offset

        self.direction: Union[Pmd2ScriptDirection, None] = None
        if direction is not None:
            try:
                self.direction = scriptdata.directions__by_ssa_id[direction]
            except KeyError:
                logger.warning(f"Unknown direction id: {direction}")
                self.direction = Pmd2ScriptDirection(direction, 'UNKNOWN')

    @property
    def x_absolute(self):
        offset = 0
        if self.x_offset >= 2:
            offset = 4
        return self.x_relative * TILE_SIZE + offset

    @property
    def y_absolute(self):
        offset = 0
        if self.y_offset >= 2:
            offset = 4
        return self.y_relative * TILE_SIZE + offset
