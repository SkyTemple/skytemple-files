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

from range_typed_integers import i16, u8, u16

from skytemple_files.common.ppmdu_config.script_data import (
    Pmd2ScriptData,
    Pmd2ScriptObject,
)
from skytemple_files.common.util import AutoString
from skytemple_files.script.ssa_sse_sss.position import SsaPosition

logger = logging.getLogger(__name__)


class SsaObject(AutoString):
    object_id: Pmd2ScriptObject
    hitbox_w: i16
    hitbox_h: i16
    pos: SsaPosition
    script_id: i16
    unk12: i16

    def __init__(
        self,
        scriptdata: Pmd2ScriptData,
        object_id: u16,
        htibox_w: i16,
        hitbox_h: i16,
        pos: SsaPosition,
        script_id: i16,
        unk12: i16,
    ):
        try:
            self.object = scriptdata.objects__by_id[object_id]
        except KeyError:
            logger.warning(f"Unknown object id: {object_id}")
            self.object = Pmd2ScriptObject(object_id, u16(0), u16(0), u8(0), "UNKNOWN")
        self.hitbox_w = htibox_w
        self.hitbox_h = hitbox_h
        self.pos = pos
        self.script_id = script_id
        self.unk12 = unk12
