"""Converts ItemSP models back into the binary format used by the game"""
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


from range_typed_integers import u32

from skytemple_files.data.item_s_p.model import ItemSP


class ItemSPWriter:
    def __init__(self, model: ItemSP):
        self.model = model

    def write(self) -> tuple[bytes, list[u32], u32 | None]:
        pointer_offsets: list[u32] = []
        header_offset = u32(0)
        data = bytearray(0)
        for i in self.model.item_list:
            data += i.to_bytes()
        return bytes(data), pointer_offsets, header_offset
