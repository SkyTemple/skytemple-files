#  Copyright 2020 Parakoopa
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
import warnings
from enum import Enum
from typing import Union, Tuple

from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptData
from skytemple_files.common.util import AutoString


class Direction(Enum):
    """SSA Direction"""
    DOWN = 1
    DOWN_LEFT = 2
    LEFT = 3
    UP_LEFT = 4
    UP = 5
    UP_RIGHT = 6
    RIGHT = 7
    DOWN_RIGHT = 8


class SsaPosition(AutoString):
    def __init__(self, scriptdata: Pmd2ScriptData, x_pos, y_pos, x_offset, y_offset, direction=None):
        """
        Common SSA position specification. Direction is optional if not applicable.
        """
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.x_offset = x_offset
        self.y_offset = y_offset

        self.direction: Union[Tuple[int, str], None] = None
        if direction is not None:
            try:
                self.direction = (direction, scriptdata.directions__by_id[direction])
            except KeyError:
                warnings.warn(f"[SsaActor]: Unknown direction id: {direction}")
                self.direction = (direction, 'UNKNOWN')
