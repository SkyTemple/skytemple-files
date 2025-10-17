#  Copyright 2020-2025 SkyTemple Contributors
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

from range_typed_integers import i16, u16

from skytemple_files.common.util import AutoString
from skytemple_files.script.ssa_sse_sss.position import SsaPosition


class SsaPerformer(AutoString):
    type: u16
    hitbox_w: i16
    hitbox_h: i16
    pos: SsaPosition
    unk10: i16
    unk12: i16

    def __init__(
        self,
        type: u16,
        hitbox_w: i16,
        hitbox_h: i16,
        pos: SsaPosition,
        unk10: i16,
        unk12: i16,
    ):
        # TODO: This is an enum: An enum value from 0 to 5 that dictates what entity will be picked to be this performer.
        self.type: int = type
        self.hitbox_w = hitbox_w
        self.hitbox_h = hitbox_h
        self.pos = pos
        self.unk10 = unk10
        self.unk12 = unk12
