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

from typing import List

from range_typed_integers import u8

from skytemple_files.common.util import iter_bytes, write_u8
from skytemple_files.graphics.dpl import (
    DPL_PAL_LEN,
    DPL_PAL_ENTRY_LEN,
    DPL_FOURTH_COLOR,
)
from skytemple_files.graphics.dpl.protocol import DplProtocol


class Dpl(DplProtocol):
    """
    This palette file contains a single raw RGBx palette.
    The model chunks the colors in 16-color palettes.
    """

    def __init__(self, data: bytes):
        self.palettes: List[List[int]] = []
        assert len(data) / 4 % 1 == 0
        pal = []
        for i, (r, g, b, x) in enumerate(iter_bytes(data, DPL_PAL_ENTRY_LEN)):
            pal.append(r)
            pal.append(g)
            pal.append(b)
            assert (
                x == DPL_FOURTH_COLOR
            )  # just in case it isn't... then we'd have a real alpha channel
            if i % DPL_PAL_LEN == DPL_PAL_LEN - 1:
                self.palettes.append(pal)
                pal = []
        if len(pal) > 0:
            self.palettes.append(pal)

    def to_bytes(self):
        data = bytearray(len(self.palettes) * DPL_PAL_LEN * DPL_PAL_ENTRY_LEN)
        cursor = 0
        for pal in self.palettes:
            for i, col in enumerate(pal):
                write_u8(data, u8(col), cursor)
                cursor += 1
                if i % 3 == 2:
                    write_u8(data, u8(DPL_FOURTH_COLOR), cursor)
                    cursor += 1
        return data
