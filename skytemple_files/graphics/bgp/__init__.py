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

from range_typed_integers import u8

BGP_RES_WIDTH = 256
BGP_RES_HEIGHT = 192
BGP_HEADER_LENGTH = 32
BGP_PAL_ENTRY_LEN = 4
BGP_PAL_UNKNOWN4_COLOR_VAL = u8(0x80)
# The palette is actually a list of smaller palettes. Each palette has this many colors:
BGP_PAL_NUMBER_COLORS = 16
# The maximum number of palettes supported
BGP_MAX_PAL = 16
BGP_TILEMAP_ENTRY_BYTELEN = 2
BGP_PIXEL_BITLEN = 4
BGP_TILE_DIM = 8
BGP_RES_WIDTH_IN_TILES = int(BGP_RES_WIDTH / BGP_TILE_DIM)
BGP_RES_HEIGHT_IN_TILES = int(BGP_RES_HEIGHT / BGP_TILE_DIM)
BGP_TOTAL_NUMBER_TILES = BGP_RES_WIDTH_IN_TILES * BGP_RES_HEIGHT_IN_TILES
# All BPGs have this many tiles and tilemapping entries for some reason
BGP_TOTAL_NUMBER_TILES_ACTUALLY = 1024
# NOTE: Tile 0 is always 0x0. <- THIS
