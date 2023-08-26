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

import math
from typing import List, Sequence

from PIL import Image
from range_typed_integers import u16

from skytemple_files.common.i18n_util import _, f
from skytemple_files.common.protocol import TilemapEntryProtocol
from skytemple_files.common.tiled_image import from_pil, search_for_chunk
from skytemple_files.common.util import (
    chunks,
    read_u16,
    write_u16,
)
from skytemple_files.graphics.dbg import (
    DBG_TILING_DIM,
    DBG_CHUNK_WIDTH,
    DBG_WIDTH_AND_HEIGHT,
)
from skytemple_files.graphics.dbg.protocol import DbgProtocol
from skytemple_files.graphics.dpc._model import Dpc
from skytemple_files.graphics.dpc import DPC_TILING_DIM
from skytemple_files.graphics.dpci._model import Dpci
from skytemple_files.graphics.dpci import DPCI_TILE_DIM
from skytemple_files.graphics.dpl._model import Dpl
from skytemple_files.graphics.dpl import DPL_PAL_LEN, DPL_MAX_PAL
from skytemple_files.user_error import UserValueError


class Dbg(DbgProtocol[Dpc, Dpci, Dpl]):
    mappings: List[u16]

    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.mappings = []
        for pos in range(0, len(data), 2):
            self.mappings.append(read_u16(data, pos))

    def place_chunk(self, x: int, y: int, chunk_index: int) -> None:
        dbg_index = y * DBG_WIDTH_AND_HEIGHT + x
        self.mappings[dbg_index] = u16(chunk_index)

    def to_pil(
        self, dpc: Dpc, dpci: Dpci, palettes: Sequence[Sequence[int]]
    ) -> Image.Image:
        width_and_height_map = DBG_WIDTH_AND_HEIGHT * DBG_CHUNK_WIDTH

        chunks = dpc.chunks_to_pil(dpci, palettes, 1)
        fimg = Image.new("P", (width_and_height_map, width_and_height_map))
        fimg.putpalette(chunks.getpalette())  # type: ignore

        for i, mt_idx in enumerate(self.mappings):
            x = i % DBG_WIDTH_AND_HEIGHT
            y = math.floor(i / DBG_WIDTH_AND_HEIGHT)
            fimg.paste(
                chunks.crop(
                    (
                        0,
                        mt_idx * DBG_CHUNK_WIDTH,
                        DBG_CHUNK_WIDTH,
                        mt_idx * DBG_CHUNK_WIDTH + DBG_CHUNK_WIDTH,
                    )
                ),
                (x * DBG_CHUNK_WIDTH, y * DBG_CHUNK_WIDTH),
            )

        return fimg

    def from_pil(
        self,
        dpc: Dpc,
        dpci: Dpci,
        dpl: Dpl,
        img: Image.Image,
        force_import: bool = False,
    ) -> None:
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
            raise UserValueError(
                f(
                    _(
                        "Can not import map background: Width of image must match the expected width: "
                        "{expected_width}px"
                    )
                )
            )
        if img.height != expected_height:
            raise UserValueError(
                f(
                    _(
                        "Can not import map background: Height of image must match the expected height: "
                        "{expected_height}px"
                    )
                )
            )

        # Import tiles, tile mappings and chunks mappings
        tiles, all_possible_tile_mappings, palettes = from_pil(
            img,
            DPL_PAL_LEN,
            16,
            DPCI_TILE_DIM,
            img.width,
            img.height,
            3,
            3,
            force_import,
        )
        # Remove any extra colors
        palettes = palettes[:DPL_MAX_PAL]

        dpci.import_tiles(tiles)

        # Build a new list of chunks / tile mappings for the DPC based on repeating chunks
        # in the imported image. Generate chunk mappings.
        chunk_mappings = []
        chunk_mappings_counter = 1
        tile_mappings: List[TilemapEntryProtocol] = []
        tiles_in_chunk = DBG_TILING_DIM * DBG_TILING_DIM
        for chk_fst_tile_idx in range(
            0,
            DBG_WIDTH_AND_HEIGHT * DBG_WIDTH_AND_HEIGHT * tiles_in_chunk,
            tiles_in_chunk,
        ):
            chunk = all_possible_tile_mappings[
                chk_fst_tile_idx : chk_fst_tile_idx + tiles_in_chunk
            ]
            start_of_existing_chunk = search_for_chunk(chunk, tile_mappings)
            if start_of_existing_chunk is not None:
                chunk_mappings.append(
                    u16(int(start_of_existing_chunk / tiles_in_chunk) + 1)
                )
            else:
                tile_mappings += chunk
                chunk_mappings.append(u16(chunk_mappings_counter))
                chunk_mappings_counter += 1

        dpc.import_tile_mappings(list(chunks(tile_mappings, DPC_TILING_DIM * DPC_TILING_DIM)))  # type: ignore
        self.mappings = chunk_mappings

        # Import palettes
        dpl.palettes = palettes

    def to_bytes(self) -> bytes:
        buffer = bytearray(2 * len(self.mappings))
        for i, m in enumerate(self.mappings):
            write_u16(buffer, m, i * 2)
        return buffer

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dbg):
            return False
        return self.mappings == other.mappings
