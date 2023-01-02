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

SUBENTRIES = 40  # Subentries of one 80 byte TOC entry
SUBENTRY_LEN = 4  # Length of the subentry pointers
KAO_IMG_PAL_B_SIZE = 48  # Size of KaoImage palette block in bytes (16*3)
KAO_IMG_PIXEL_DEPTH = 4  # one byte in a kao image are two pixels
KAO_IMG_METAPIXELS_DIM = (
    8  # How many pixels build a meta-pixel / tile per dim. (8x8)=48
)
KAO_IMG_IMG_DIM = (
    5  # How many meta-pixels / tiles build an image per dimension (5x5)=25
)
KAO_FILE_BYTE_ALIGNMENT = (
    16  # The size of the kao file has to be divisble by this number of bytes
)
