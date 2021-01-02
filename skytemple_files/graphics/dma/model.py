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
import math
from enum import Enum

try:
    from PIL import Image
except ImportError:
    from pil import Image

from skytemple_files.common.util import *
from skytemple_files.graphics.dpc.model import Dpc, DPC_TILING_DIM
from skytemple_files.graphics.dpci.model import Dpci, DPCI_TILE_DIM


class DmaType(Enum):
    WALL = 0
    WATER = 1
    FLOOR = 2


class DmaExtraType(Enum):
    FLOOR1 = 0
    WALL_OR_VOID = 1
    FLOOR2 = 2


class DmaNeighbor:
    SOUTH = 0x01
    SOUTH_EAST = 0x02
    EAST = 0x04
    NORTH_EAST = 0x08
    NORTH = 0x10
    NORTH_WEST = 0x20
    WEST = 0x40
    SOUTH_WEST = 0x80


class Dma:
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        # Come in pair of three. So: i = floor(i/3)
        # First two:
        # 00 -> Wall
        # 01 -> Water
        # 10 -> Floor
        # 11 -> Extra
        # Rest: SouthWest West NorthWest North NorthEast East SouthEast South
        self.chunk_mappings = list(data)

    def get(self, get_type: DmaType, neighbors_same: int) -> List[int]:
        """
        Returns all three variations (chunk ids) set for this dungeon tile configuration.
        neighbors_same is a bitfield with the bits for the directions set to 1 if the neighbor at this
        position has the same type as the tile at this position.
        TIP: For neighbors_same, use the bit flags in DmaNeighbor.
        """
        # Wall
        high_two = 0
        if get_type == DmaType.WATER:
            high_two = 0x100
        elif get_type == DmaType.FLOOR:
            high_two = 0x200
        idx = high_two + neighbors_same
        return self.chunk_mappings[(idx * 3):(idx * 3) + 3]

    def get_extra(self, extra_type: DmaExtraType) -> List[int]:
        """
        Returns a few extra chunk variations for the given type.
        How they are used exactly by the game is currently not know,
        this interface could change if we find out.
        """
        cms = []
        for i in range(0x300 * 3, len(self.chunk_mappings)):
            if i % 3 == extra_type.value:
                cms.append(self.chunk_mappings[i])
        return cms

    def set(self, get_type: DmaType, neighbors_same: int, variation_index: int, value: int):
        """
        Sets the mapping for the given configuration and the given variation of it.
        """
        # Wall
        high_two = 0
        if get_type == DmaType.WATER:
            high_two = 0x100
        elif get_type == DmaType.FLOOR:
            high_two = 0x200
        idx = high_two + neighbors_same
        self.chunk_mappings[(idx * 3) + variation_index] = value

    def set_extra(self, extra_type: DmaExtraType, index: int, value: int):
        """
        Sets and extra tile entry.
        """
        self.chunk_mappings[(0x300 * 3) + extra_type.value + (3 * index)] = value

    def to_pil(
            self, dpc: Dpc, dpci: Dpci, palettes: List[List[int]]
    ) -> Image.Image:
        """
        For debugging only, the output image contains some labels, etc. Use get(...) instead to
        get a chunk mapping and then render that chunk by extracting it from the image returned by
        bpc.chunks_to_pil(...)

        Converts the chunks of the DMA into an image. Works like bpc.chunks_to_pil,
        but uses the chunk mappings stored in this file to place them instead.
        """

        # We don't render all possibilities of course...
        possibilities_to_render = [[
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ], [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ], [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ], [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ], [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]
        ]]
        # For each possibility we need 11x4 chunks (incl. 1 space line and three variations, with spacing)
        # This means for all two types we need 24x4 (incl. 2 spacing) per possibility
        # Possibilities are rendered down
        # For the extra tiles we need 16x1, in total 16x6 (incl. spacing and one spacing before)
        chunk_dim = DPC_TILING_DIM * DPCI_TILE_DIM

        width = 24 * chunk_dim
        height = (4 * len(possibilities_to_render) + 6) * chunk_dim

        chunks = dpc.chunks_to_pil(dpci, palettes, 1)

        fimg = Image.new('P', (width, height))
        fimg.putpalette(chunks.getpalette())

        def paste(chunk_index, x, y):
            fimg.paste(
                chunks.crop((0, chunk_index * chunk_dim, chunk_dim, chunk_index * chunk_dim + chunk_dim)),
                (x * chunk_dim, y * chunk_dim)
            )

        x_cursor = 0

        for solid_type in (DmaType.WALL, DmaType.WATER):
            y_cursor = 0
            for possibility in possibilities_to_render:
                for y, row in enumerate(possibility):
                    for x, solid in enumerate(row):
                        ctype = solid_type if solid else DmaType.FLOOR
                        solid_neighbors = self.get_tile_neighbors(possibility, x, y, bool(solid))
                        for iv, variation in enumerate(self.get(ctype, solid_neighbors)):
                            paste(variation, x_cursor + (4 * iv) + x, y_cursor + y)
                y_cursor += 4
            x_cursor += 13

        for extra_type in (DmaExtraType.FLOOR1, DmaExtraType.WALL_OR_VOID, DmaExtraType.FLOOR2):
            for x, variation in enumerate(self.get_extra(extra_type)):
                paste(variation, x, y_cursor)
            y_cursor += 2

        return fimg

    @staticmethod
    def get_tile_neighbors(wall_matrix: List[List[int]], x, y, self_is_wall_or_water: bool, treat_outside_as_wall=False):
        """Return the neighbor bit map for the given 3x3 matrix.
        1 means there is a wall / water. Out of bounds is read as floor, unless treat_outside_as_wall,
        then it's water/wall."""
        ns = 0
        if treat_outside_as_wall:
            # we enlarge the matrix and add a 1 chunk-sized border
            x += 1
            y += 1
            wall_matrix =   [[1] * (len(wall_matrix[0]) + 2)] + \
                            [[1] + l + [1] for l in wall_matrix] + \
                            [[1] * (len(wall_matrix[0]) + 2)]
        # SOUTH
        if y + 1 < len(wall_matrix) and wall_matrix[y + 1][x]:
            ns += DmaNeighbor.SOUTH
        # SOUTH_EAST
        if y + 1 < len(wall_matrix) and x + 1 < len(wall_matrix[y + 1]) and wall_matrix[y + 1][x + 1]:
            ns += DmaNeighbor.SOUTH_EAST
        # EAST
        if x + 1 < len(wall_matrix[y]) and wall_matrix[y][x + 1]:
            ns += DmaNeighbor.EAST
        # NORTH_EAST
        if y - 1 >= 0 and x + 1 < len(wall_matrix[y - 1]) and wall_matrix[y - 1][x + 1]:
            ns += DmaNeighbor.NORTH_EAST
        # NORTH
        if y - 1 >= 0 and wall_matrix[y - 1][x]:
            ns += DmaNeighbor.NORTH
        # NORTH_WEST
        if y - 1 >= 0 and x - 1 >= 0 and wall_matrix[y - 1][x - 1]:
            ns += DmaNeighbor.NORTH_WEST
        # WEST
        if x - 1 >= 0 and wall_matrix[y][x - 1]:
            ns += DmaNeighbor.WEST
        # SOUTH_WEST
        if y + 1 < len(wall_matrix) and x - 1 >= 0 and wall_matrix[y + 1][x - 1]:
            ns += DmaNeighbor.SOUTH_WEST

        if not self_is_wall_or_water:
            # If we are not solid, we need to invert, since we just checked for us being solid.
            ns ^= 0xFF
        return ns

    def to_bytes(self):
        return bytes(self.chunk_mappings)
