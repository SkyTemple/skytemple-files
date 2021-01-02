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
from skytemple_files.common.util import *

# Length of a palette in colors.
DPL_PAL_LEN = 16
# Maximum number of palettes
DPL_MAX_PAL = 12
# Number of color bytes per palette entry. Fourth is always 0x00.
DPL_PAL_ENTRY_LEN = 4
# Size of a single palette in bytes
DPL_PAL_SIZE = DPL_PAL_LEN * DPL_PAL_ENTRY_LEN
# The value of the fourth color
DPL_FOURTH_COLOR = 128


class Dpl:
    """
    This palette file contains a single raw RGBx palette.
    The model chunks the colors in 16-color palettes.
    The model stores the colors as a stream of RGB values:
    [R, G, B, R, G, B...]
    """
    def __init__(self, data: bytes):
        self.palettes = []
        assert len(data) / 4 % 1 == 0
        pal = []
        for i, (r, g, b, x) in enumerate(iter_bytes(data, DPL_PAL_ENTRY_LEN)):
            pal.append(r)
            pal.append(g)
            pal.append(b)
            assert x == DPL_FOURTH_COLOR  # just in case it isn't... then we'd have a real alpha channel
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
                write_uintle(data, col, cursor)
                cursor += 1
                if i % 3 == 2:
                    write_uintle(data, DPL_FOURTH_COLOR, cursor)
                    cursor += 1
        return data
