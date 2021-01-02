"""Converts FontSir0 models back into the binary format used by the game"""
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
from typing import Optional

from skytemple_files.common.util import *
from skytemple_files.graphics.colvec import *
from skytemple_files.graphics.colvec.model import Colvec


class ColvecWriter:
    def __init__(self, model: Colvec):
        self.model = model

    def write(self) -> Tuple[bytes, List[int], Optional[int]]:
        pointer_offsets = []
        header_pointer = 0
        buffer = bytearray()
        for colormap in self.model.colormaps:
            palette_buffer = bytearray(COLVEC_DATA_LEN)
            j = 0
            for i, p in enumerate(colormap):
                write_uintle(palette_buffer, p, j)
                j += 1
                if i % 3 == 2:
                    # Insert the fourth color
                    write_uintle(palette_buffer, 0xff, j)
                    j += 1
            assert j == len(palette_buffer)
            buffer += palette_buffer
        return buffer, pointer_offsets, header_pointer
