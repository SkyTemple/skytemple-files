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
    Pmd2ScriptDirection,
)
from skytemple_files.common.util import AutoString
from skytemple_files.graphics.bpc import BPC_TILE_DIM

logger = logging.getLogger(__name__)


TILE_SIZE = 8
ACTOR_DEFAULT_HITBOX_W = 2 * BPC_TILE_DIM
ACTOR_DEFAULT_HITBOX_H = 1 * BPC_TILE_DIM


class SsaPosition(AutoString):
    scriptdata: Pmd2ScriptData
    x_relative: u16
    y_relative: u16
    x_offset: u16
    y_offset: u16
    direction: Pmd2ScriptDirection | None

    def __init__(
        self,
        scriptdata: Pmd2ScriptData,
        x_pos: u16,
        y_pos: u16,
        x_offset: u16,
        y_offset: u16,
        direction: u16 | None = None,
    ):
        """
        Common SSA position specification. Direction is optional if not applicable.
        """
        self.x_relative = x_pos
        self.y_relative = y_pos

        self.x_offset = x_offset
        self.y_offset = y_offset

        self.direction = None
        if direction is not None:
            try:
                self.direction = scriptdata.directions__by_ssa_id[direction]
            except KeyError:
                logger.warning(f"Unknown direction id: {direction}")
                self.direction = Pmd2ScriptDirection(direction, "UNKNOWN")

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        self_dir = None
        other_dir = None
        if self.direction is not None:
            self_dir = self.direction.ssa_id
        if other.direction is not None:
            other_dir = other.direction.ssa_id
        return (
            self.x_relative == other.x_relative
            and self.y_relative == other.y_relative
            and self.x_offset == other.x_offset
            and self.y_offset == other.y_offset
            and self_dir == other_dir
        )
