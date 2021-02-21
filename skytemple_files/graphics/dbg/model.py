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
from typing import List

from skytemple_files.common.tiled_image import from_pil, search_for_chunk, TilemapEntry
from skytemple_files.common.util import read_uintle, write_uintle, chunks
from skytemple_files.graphics.dpc.model import Dpc, DPC_TILING_DIM
from skytemple_files.graphics.dpci.model import Dpci, DPCI_TILE_DIM
from skytemple_files.graphics.dpl.model import Dpl, DPL_PAL_LEN, DPL_MAX_PAL
from skytemple_files.common.i18n_util import f, _

try:
    from PIL import Image
except ImportError:
    from pil import Image

DBG_TILING_DIM = 3
DBG_CHUNK_WIDTH = 24
DBG_WIDTH_AND_HEIGHT = 32


class Dbg:
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.mappings = []
        for pos in range(0, len(data), 2):
            self.mappings.append(read_uintle(data, pos, 2))

    def to_pil(
            self, dpc: Dpc, dpci: Dpci, palettes: List[List[int]]
    ) -> Image.Image:
        width_and_height_map = DBG_WIDTH_AND_HEIGHT * DBG_CHUNK_WIDTH

        chunks = dpc.chunks_to_pil(dpci, palettes, 1)
        fimg = Image.new('P', (width_and_height_map, width_and_height_map))
        fimg.putpalette(chunks.getpalette())

        for i, mt_idx in enumerate(self.mappings):
            x = i % DBG_WIDTH_AND_HEIGHT
            y = math.floor(i / DBG_WIDTH_AND_HEIGHT)
            fimg.paste(
                chunks.crop((0, mt_idx * DBG_CHUNK_WIDTH, DBG_CHUNK_WIDTH, mt_idx * DBG_CHUNK_WIDTH + DBG_CHUNK_WIDTH)),
                (x * DBG_CHUNK_WIDTH, y * DBG_CHUNK_WIDTH)
            )

        return fimg

    def from_pil(
            self, dpc: Dpc, dpci: Dpci, dpl: Dpl, img: Image.Image, force_import=False
    ):
        """
        Import an entire background from an image.
        Changes all tiles, tile mappings and chunks in the DPC/DPCI and re-writes the mappings of the DBG.
        Imports the palettes of the image to the DPL.

        The passed PIL will be split into separate tiles and the tile's palette index in the tile mapping for this
        coordinate is determined by the first pixel value of each tile in the PIL. The PIL
        must have a palette containing up to 16 sub-palettes with 16 colors each (256 colors).

        If a pixel in a tile uses a color outside of it's 16 color range, an error is thrown or
        the color is replaced with 0 of the palette (transparent). This is controlled by
        the force_import flag.

        The input images must have the same dimensions as the DBG (same dimensions as to_pil_single_layer would export).
        """
        expected_width = DBG_TILING_DIM * DBG_WIDTH_AND_HEIGHT * DPCI_TILE_DIM
        expected_height = DBG_TILING_DIM * DBG_WIDTH_AND_HEIGHT * DPCI_TILE_DIM
        if img.width != expected_width:
            raise ValueError(f(_("Can not import map background: Width of image must match the expected width: "
                                 "{expected_width}px")))
        if img.height != expected_height:
            raise ValueError(f(_("Can not import map background: Height of image must match the expected height: "
                                "{expected_height}px")))

        # Import tiles, tile mappings and chunks mappings
        tiles, all_possible_tile_mappings, palettes = from_pil(
            img, DPL_PAL_LEN, 16, DPCI_TILE_DIM,
            img.width, img.height, 3, 3, force_import
        )
        # Remove any extra colors
        palettes = palettes[:DPL_MAX_PAL]

        dpci.import_tiles(tiles)

        # Build a new list of chunks / tile mappings for the DPC based on repeating chunks
        # in the imported image. Generate chunk mappings.
        chunk_mappings = []
        chunk_mappings_counter = 1
        tile_mappings = []
        tiles_in_chunk = DBG_TILING_DIM * DBG_TILING_DIM
        for chk_fst_tile_idx in range(0, DBG_WIDTH_AND_HEIGHT * DBG_WIDTH_AND_HEIGHT * tiles_in_chunk, tiles_in_chunk):
            chunk = all_possible_tile_mappings[chk_fst_tile_idx:chk_fst_tile_idx+tiles_in_chunk]
            start_of_existing_chunk = search_for_chunk(chunk, tile_mappings)
            if start_of_existing_chunk is not None:
                chunk_mappings.append(int(start_of_existing_chunk / tiles_in_chunk) + 1)
            else:
                tile_mappings += chunk
                chunk_mappings.append(chunk_mappings_counter)
                chunk_mappings_counter += 1

        dpc.import_tile_mappings(list(chunks(tile_mappings, DPC_TILING_DIM * DPC_TILING_DIM)))
        self.mappings = chunk_mappings

        # Import palettes
        dpl.palettes = palettes

    def to_bytes(self):
        buffer = bytearray(2 * len(self.mappings))
        for i, m in enumerate(self.mappings):
            write_uintle(buffer, m, i * 2, 2)
        return buffer

    def __eq__(self, other):
        if not isinstance(other, Dbg):
            return False
        return self.mappings == other.mappings
