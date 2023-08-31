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

from typing import List, Sequence

from PIL import Image

from skytemple_files.common.util import chunks
from skytemple_files.graphics.dma.protocol import DmaType, DmaExtraType, DmaProtocol
from skytemple_files.graphics.dma.util import get_tile_neighbors
from skytemple_files.graphics.dpc._model import Dpc
from skytemple_files.graphics.dpc import DPC_TILING_DIM
from skytemple_files.graphics.dpci._model import Dpci
from skytemple_files.graphics.dpci import DPCI_TILE_DIM


class Dma(DmaProtocol):
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
        self.chunk_mappings: List[int] = list(data)

    def get(self, get_type: int, neighbors_same: int) -> Sequence[int]:
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
        return self.chunk_mappings[(idx * 3) : (idx * 3) + 3]

    def get_extra(self, extra_type: int) -> Sequence[int]:
        """
        Returns a few extra chunk variations for the given type.
        How they are used exactly by the game is currently not know,
        this interface could change if we find out.
        """
        cms = []
        for i in range(0x300 * 3, len(self.chunk_mappings)):
            if i % 3 == extra_type:
                cms.append(self.chunk_mappings[i])
        return cms

    def set(self, get_type: int, neighbors_same: int, variation_index: int, value: int):
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

    def set_extra(self, extra_type: int, index: int, value: int):
        """
        Sets and extra tile entry.
        """
        self.chunk_mappings[(0x300 * 3) + extra_type + (3 * index)] = value

    def to_pil(
        self, dpc: Dpc, dpci: Dpci, palettes: Sequence[Sequence[int]]
    ) -> Image.Image:
        """
        For debugging only, the output image contains some labels, etc. Use get(...) instead to
        get a chunk mapping and then render that chunk by extracting it from the image returned by
        bpc.chunks_to_pil(...)

        Converts the chunks of the DMA into an image. Works like bpc.chunks_to_pil,
        but uses the chunk mappings stored in this file to place them instead.
        """

        # We don't render all possibilities of course...
        possibilities_to_render = [
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
            [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
            [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
            [[1, 0, 1], [0, 1, 0], [1, 0, 1]],
        ]
        # For each possibility we need 11x4 chunks (incl. 1 space line and three variations, with spacing)
        # This means for all two types we need 24x4 (incl. 2 spacing) per possibility
        # Possibilities are rendered down
        # For the extra tiles we need 16x1, in total 16x6 (incl. spacing and one spacing before)
        chunk_dim = DPC_TILING_DIM * DPCI_TILE_DIM

        width = 24 * chunk_dim
        height = (4 * len(possibilities_to_render) + 6) * chunk_dim

        chunks = dpc.chunks_to_pil(dpci, palettes, 1)

        fimg = Image.new("P", (width, height))
        fimg.putpalette(chunks.getpalette())  # type: ignore

        def paste(chunk_index, x, y):
            fimg.paste(
                chunks.crop(
                    (
                        0,
                        chunk_index * chunk_dim,
                        chunk_dim,
                        chunk_index * chunk_dim + chunk_dim,
                    )
                ),
                (x * chunk_dim, y * chunk_dim),
            )

        x_cursor = 0

        for solid_type in (DmaType.WALL, DmaType.WATER):
            y_cursor = 0
            for possibility in possibilities_to_render:
                for y, row in enumerate(possibility):
                    for x, solid in enumerate(row):
                        ctype = solid_type if solid else DmaType.FLOOR
                        solid_neighbors = get_tile_neighbors(
                            possibility, x, y, bool(solid)
                        )
                        for iv, variation in enumerate(
                            self.get(ctype, solid_neighbors)
                        ):
                            paste(variation, x_cursor + (4 * iv) + x, y_cursor + y)
                y_cursor += 4
            x_cursor += 13

        for extra_type in (
            DmaExtraType.FLOOR1,
            DmaExtraType.WALL_OR_VOID,
            DmaExtraType.FLOOR2,
        ):
            for x, variation in enumerate(self.get_extra(extra_type)):
                paste(variation, x, y_cursor)
            y_cursor += 2

        return fimg

    def to_bytes(self):
        return bytes(self.chunk_mappings)
