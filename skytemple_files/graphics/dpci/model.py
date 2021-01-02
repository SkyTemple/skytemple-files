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
import itertools
import math

try:
    from PIL import Image
except ImportError:
    from pil import Image

from skytemple_files.common.tiled_image import TilemapEntry, to_pil, from_pil
from skytemple_files.common.util import *
from skytemple_files.graphics.dpl.model import DPL_PAL_LEN, DPL_MAX_PAL

DPCI_TILE_DIM = 8


class Dpci:
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        self.tiles = list(iter_bytes(data, int(DPCI_TILE_DIM * DPCI_TILE_DIM / 2)))  # / 2 because 4bpp

    def tiles_to_pil(self, palettes: List[List[int]], width_in_tiles=20, palette_index=0) -> Image.Image:
        """
        Convert all individual tiles of the DPCI into one PIL image.
        The image contains all tiles next to each other, the image width is tile_width tiles.
        The resulting image has one large palette with all palettes merged together.

        palettes is a list of 16 16 color palettes.
        The tiles are exported with the first palette in the list of palettes.
        The result image contains a palette that consists of all palettes merged together.
        """
        # create a dummy tile map containing all the tiles
        tilemap = []
        for i in range(0, len(self.tiles)):
            tilemap.append(TilemapEntry(
                i, False, False, palette_index, True
            ))

        width = width_in_tiles * DPCI_TILE_DIM
        height = math.ceil((len(self.tiles)) / width_in_tiles) * DPCI_TILE_DIM

        return to_pil(
            tilemap, self.tiles, palettes, DPCI_TILE_DIM, width, height
        )

    def pil_to_tiles(self, image: Image.Image):
        """
        Imports tiles that are in a format as described in the documentation for tiles_to_pil.
        """
        self.tiles, _, __ = from_pil(
            image, DPL_PAL_LEN, 16, DPCI_TILE_DIM,
            image.width, image.height, optimize=False
        )

    def to_bytes(self):
        return bytes(itertools.chain.from_iterable(self.tiles))

    def import_tiles(self, tiles: List[bytearray], contains_null_tile=False):
        """
        Replace the tiles.
        If contains_null_tile is False, the null tile is added to the list, at the beginning.
        """
        if not contains_null_tile:
            tiles = [bytearray(int(DPCI_TILE_DIM * DPCI_TILE_DIM / 2))] + tiles
        self.tiles = tiles
