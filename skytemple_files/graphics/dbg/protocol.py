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
from typing import Protocol, TypeVar, Sequence, runtime_checkable

from PIL import Image

from skytemple_files.graphics.dpc.protocol import DpcProtocol
from skytemple_files.graphics.dpci.protocol import DpciProtocol
from skytemple_files.graphics.dpl.protocol import DplProtocol

C = TypeVar("C", bound=DpcProtocol, contravariant=True)
CI = TypeVar("CI", bound=DpciProtocol, contravariant=True)
L = TypeVar("L", bound=DplProtocol, contravariant=True)


@runtime_checkable
class DbgProtocol(Protocol[C, CI, L]):
    mappings: Sequence[int]

    @abstractmethod
    def __init__(self, data: bytes):
        ...

    @abstractmethod
    def place_chunk(self, x: int, y: int, chunk_index: int) -> None:
        """Place the chunk with the given ID at the X and Y position. No error checking is done."""
        ...

    @abstractmethod
    def to_pil(
        self, dpc: C, dpci: CI, palettes: Sequence[Sequence[int]]
    ) -> Image.Image:
        ...

    @abstractmethod
    def from_pil(
        self, dpc: C, dpci: CI, dpl: L, img: Image.Image, force_import: bool = False
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
        ...
