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
from skytemple_files.common.i18n_util import f, _

try:
    from PIL import Image
except ImportError:
    from pil import Image

from skytemple_files.common.tiled_image import TilemapEntry, to_pil, from_pil
from skytemple_files.common.util import *
from skytemple_files.graphics.dpci.model import Dpci, DPCI_TILE_DIM
from skytemple_files.graphics.dpl.model import DPL_PAL_LEN, DPL_MAX_PAL

DPC_TILING_DIM = 3


class Dpc:
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        all_tilemaps = []
        for bytes2 in iter_bytes(data, 2):
            all_tilemaps.append(TilemapEntry.from_int(read_uintle(bytes2, 0, 2)))
        self.chunks = list(chunks(all_tilemaps, DPC_TILING_DIM * DPC_TILING_DIM))

    def chunks_to_pil(self, dpci: Dpci, palettes: List[List[int]], width_in_mtiles=16) -> Image.Image:
        """
        Convert all chunks of the DPC to one big PIL image.
        The chunks are all placed next to each other.
        The resulting image has one large palette with all palettes merged together.

        To be used with the DPCI file for this dungeon.
        To get the palettes, use the data from the DPL file for this dungeon:

        >>> dpc.chunks_to_pil(dpci, dpl.palettes)

        """
        width = width_in_mtiles * DPC_TILING_DIM * DPCI_TILE_DIM
        height = math.ceil(len(self.chunks) / width_in_mtiles) * DPC_TILING_DIM * DPCI_TILE_DIM
        return to_pil(
            list(itertools.chain.from_iterable(self.chunks)), dpci.tiles, palettes, DPCI_TILE_DIM,
            width, height, DPC_TILING_DIM, DPC_TILING_DIM
        )

    def single_chunk_to_pil(self, chunk_idx, dpci: Dpci, palettes: List[List[int]]):
        """
        Convert a single chunk of the DPC into a PIL image. For general notes, see chunks_to_pil.
        """
        return to_pil(
            self.chunks[chunk_idx], dpci.tiles, palettes, DPCI_TILE_DIM,
            DPCI_TILE_DIM * DPC_TILING_DIM, DPCI_TILE_DIM * DPC_TILING_DIM,
            DPC_TILING_DIM, DPC_TILING_DIM
        )

    def pil_to_chunks(self, image: Image.Image, force_import=True) -> Tuple[List[bytes], List[List[int]]]:
        """
        Imports chunks. Format same as for chunks_to_pil.
        Replaces tile mappings and returns the new tiles for storing them in a DPCI and the palettes
        for storing in a DPL.

        The PIL must have a palette containing the 16 sub-palettes with 16 colors each (256 colors).

        If a pixel in a tile uses a color outside of it's 16 color range, an error is thrown or
        the color is replaced with 0 of the palette (transparent). This is controlled by
        the force_import flag.
        """
        tiles, all_tilemaps, palettes = from_pil(
            image, DPL_PAL_LEN, 16, DPCI_TILE_DIM,
            image.width, image.height, DPC_TILING_DIM, DPC_TILING_DIM, force_import
        )
        # Validate number of palettes
        palettes = palettes[:DPL_MAX_PAL]
        for tm in all_tilemaps:
            if tm.pal_idx > DPL_MAX_PAL - 1:
                raise ValueError(f(_("The image to import can only use the first 12 palettes. "
                                     "Tried to use palette {tm.pal_idx}")))
        self.chunks = list(chunks(all_tilemaps, DPC_TILING_DIM * DPC_TILING_DIM))
        self.re_fill_chunks()
        return tiles, palettes

    def to_bytes(self):
        all_tilemaps = list(itertools.chain.from_iterable(self.chunks))
        data = bytearray(len(all_tilemaps) * 2)
        for i, tm in enumerate(all_tilemaps):
            write_uintle(data, tm.to_int(), i * 2, 2)
        return data

    def import_tile_mappings(
            self, tile_mappings: List[List[TilemapEntry]],
            contains_null_chunk=False, correct_tile_ids=True
    ):
        """
        Replace the tile mappings of the specified layer.
        If contains_null_tile is False, the null chunk is added to the list, at the beginning.

        If correct_tile_ids is True, then the tile id of tile_mappings is also increased by one. Use this,
        if you previously used import_tiles with contains_null_tile=False
        """
        if correct_tile_ids:
            for chunk in tile_mappings:
                for entry in chunk:
                    if not contains_null_chunk:
                        entry.idx += 1
        if not contains_null_chunk:
            tile_mappings = [[TilemapEntry.from_int(0) for _ in range(0, 9)]] + tile_mappings
        self.chunks = tile_mappings
        self.re_fill_chunks()

    def re_fill_chunks(self):
        if len(self.chunks) > 400:
            raise ValueError(_("A dungeon background or tilemap can not have more than 400 chunks."))
        self.chunks += [[TilemapEntry.from_int(0) for _ in range(0, 9)]] * (400 - len(self.chunks))
