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
from abc import abstractmethod
from typing import Protocol, TypeVar, Sequence, Tuple

from PIL import Image

from skytemple_files.common.protocol import TilemapEntryProtocol
from skytemple_files.graphics.dpci.protocol import DpciProtocol

CI = TypeVar("CI", bound=DpciProtocol, contravariant=True)


class DpcProtocol(Protocol[CI]):
    chunks: Sequence[Sequence[TilemapEntryProtocol]]

    @abstractmethod
    def __init__(self, data: bytes):
        ...

    @abstractmethod
    def chunks_to_pil(
        self, dpci: CI, palettes: Sequence[Sequence[int]], width_in_mtiles=16
    ) -> Image.Image:
        """
        Convert all chunks of the DPC to one big PIL image.
        The chunks are all placed next to each other.
        The resulting image has one large palette with all palettes merged together.

        To be used with the DPCI file for this dungeon.
        To get the palettes, use the data from the DPL file for this dungeon:

        >>> dpc.chunks_to_pil(dpci, dpl.palettes)

        """
        ...

    @abstractmethod
    def single_chunk_to_pil(
        self, chunk_idx, dpci: CI, palettes: Sequence[Sequence[int]]
    ) -> Image.Image:
        """
        Convert a single chunk of the DPC into a PIL image. For general notes, see chunks_to_pil.
        """
        ...

    @abstractmethod
    def pil_to_chunks(
        self, image: Image.Image, force_import=True
    ) -> Tuple[Sequence[bytes], Sequence[Sequence[int]]]:
        """
        Imports chunks. Format same as for chunks_to_pil.
        Replaces tile mappings and returns the new tiles for storing them in a DPCI and the palettes
        for storing in a DPL.

        The PIL must have a palette containing the 16 sub-palettes with 16 colors each (256 colors).

        If a pixel in a tile uses a color outside of it's 16 color range, an error is thrown or
        the color is replaced with 0 of the palette (transparent). This is controlled by
        the force_import flag.
        """
        ...

    @abstractmethod
    def import_tile_mappings(
        self,
        tile_mappings: Sequence[Sequence[TilemapEntryProtocol]],
        contains_null_chunk=False,
        correct_tile_ids=True,
    ):
        """
        Replace the tile mappings of the specified layer.
        If contains_null_tile is False, the null chunk is added to the list, at the beginning.

        If correct_tile_ids is True, then the tile id of tile_mappings is also increased by one. Use this,
        if you previously used import_tiles with contains_null_tile=False
        """
        ...
