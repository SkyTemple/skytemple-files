"""Converts ItemP models back into the binary format used by the game"""
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
from typing import Optional, Dict

from skytemple_files.common.util import *
from skytemple_files.container.sir0.sir0_util import encode_sir0_pointer_offsets
from skytemple_files.data.item_p.model import ItemP
from skytemple_files.data.item_p import *

class ItemPWriter:
    def __init__(self, model: ItemP):
        self.model = model

    def write(self) -> Tuple[bytes, List[int], Optional[int]]:
        pointer_offsets: List[int] = []
        header_offset = 0
        data = bytearray(0)
        for i in self.model.item_list:
            data += i.to_bytes()
        return bytes(data), pointer_offsets, header_offset
