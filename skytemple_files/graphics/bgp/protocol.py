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
from typing import Protocol, Sequence

from PIL import Image

from skytemple_files.common.protocol import TilemapEntryProtocol


class BgpProtocol(Protocol):
    palettes: Sequence[Sequence[int]] = []
    tiles: Sequence[bytearray] = []
    tilemap: Sequence[TilemapEntryProtocol] = []

    @abstractmethod
    def __init__(self, data: bytes):
        ...

    @abstractmethod
    def to_pil(self, ignore_flip_bits=False) -> Image.Image:
        """
        Convert all tiles of the BGP to one big PIL image.
        The resulting image has one large palette with 256 colors.
        If ignore_flip_bits is set, tiles are not flipped.

        The image returned will have the size 256x192.
        """
        ...

    @abstractmethod
    def from_pil(self, pil: Image.Image, force_import=False) -> None:
        """
        Modify the image data in the BGP by importing the passed PIL.
        The passed PIL will be split into separate tiles and the tile's palette index
        is determined by the first pixel value of each tile in the PIL. The PIL
        must have a palette containing the 16 sub-palettes with 16 colors each (256 colors).

        If a pixel in a tile uses a color outside of it's 16 color range, an error is thrown or
        the color is replaced with 0 of the palette (transparent). This is controlled by
        the force_import flag.

        The image must have the size 256x192.
        """
        ...
