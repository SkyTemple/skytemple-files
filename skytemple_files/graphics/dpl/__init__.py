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
