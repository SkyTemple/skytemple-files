#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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
from enum import Enum


class SwdlLfoDest(Enum):
    NONE = 0
    PITCH = 1
    VOLUME = 2
    PAN = 3
    FILTER = 4


class SwdlWshape(Enum):
    NULL = 0
    SQUARE = 1
    TRIANGLE = 2
    SINUS = 3
    UNK4 = 4
    SAW = 5
    NOISE = 6
    RANDOM = 7
