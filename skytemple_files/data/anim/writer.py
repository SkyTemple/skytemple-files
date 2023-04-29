"""Converts WazaP models back into the binary format used by the game"""
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

import typing

from range_typed_integers import u32_checked

from skytemple_files.common.util import write_u32
from skytemple_files.data.anim import HEADER_SIZE
from skytemple_files.data.anim.model import Anim


class AnimWriter:
    def __init__(self, model: Anim):
        self.model = model

    @typing.no_type_check
    def write(self) -> bytes:
        data = bytearray(HEADER_SIZE)
        write_u32(data, u32_checked(len(data)), 0)
        for e in self.model.trap_table:
            data += e.to_bytes()
        write_u32(data, u32_checked(len(data)), 4)
        for e in self.model.item_table:
            data += e.to_bytes()
        write_u32(data, u32_checked(len(data)), 8)
        for e in self.model.move_table:
            data += e.to_bytes()
        write_u32(data, u32_checked(len(data)), 12)
        for e in self.model.general_table:
            data += e.to_bytes()
        write_u32(data, u32_checked(len(data)), 16)
        for e in self.model.special_move_table:
            data += e.to_bytes()
        return bytes(data)
