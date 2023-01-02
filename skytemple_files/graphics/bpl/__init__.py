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

# Length of a palette in colors. Color 0 is auto-generated (transparent)
BPL_PAL_LEN = 15
# Actual colors in an image, (including the color 0)
BPL_IMG_PAL_LEN = BPL_PAL_LEN + 1
# Maximum number of palettes
BPL_MAX_PAL = 16
# Maximum number of normal palettes
BPL_NORMAL_MAX_PAL = 14
# Number of color bytes per palette entry. Fourth is always 0x00.
BPL_PAL_ENTRY_LEN = 4
# Size of a single palette in bytes
BPL_PAL_SIZE = BPL_PAL_LEN * BPL_PAL_ENTRY_LEN
BPL_COL_INDEX_ENTRY_LEN = 4
# The value of the fourth color
BPL_FOURTH_COLOR = 0x00
