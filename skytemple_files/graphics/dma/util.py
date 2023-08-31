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
from typing import List, Union

from skytemple_files.graphics.dma.protocol import DmaNeighbor


def get_tile_neighbors(
    wall_matrix: List[List[Union[int, bool]]],
    x,
    y,
    self_is_wall_or_water: bool,
    treat_outside_as_wall=False,
):
    """Return the neighbor bit map for the given 3x3 matrix.
    1 means there is a wall / water. Out of bounds is read as floor, unless treat_outside_as_wall,
    then it's water/wall."""
    ns = 0
    if treat_outside_as_wall:
        # we enlarge the matrix and add a 1 chunk-sized border
        x += 1
        y += 1
        wall_matrix = (
            [[1] * (len(wall_matrix[0]) + 2)]
            + [[1] + l + [1] for l in wall_matrix]
            + [[1] * (len(wall_matrix[0]) + 2)]
        )
    # SOUTH
    if y + 1 < len(wall_matrix) and wall_matrix[y + 1][x]:
        ns += DmaNeighbor.SOUTH
    # SOUTH_EAST
    if (
        y + 1 < len(wall_matrix)
        and x + 1 < len(wall_matrix[y + 1])
        and wall_matrix[y + 1][x + 1]
    ):
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
