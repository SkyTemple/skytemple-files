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
from typing import Sequence, Protocol

from PIL import Image


class DpciProtocol(Protocol):
    tiles: Sequence[bytes]

    @abstractmethod
    def __init__(self, data: bytes):
        ...

    @abstractmethod
    def tiles_to_pil(
        self, palettes: Sequence[Sequence[int]], width_in_tiles=20, palette_index=0
    ) -> Image.Image:
        """
        Convert all individual tiles of the DPCI into one PIL image.
        The image contains all tiles next to each other, the image width is tile_width tiles.
        The resulting image has one large palette with all palettes merged together.

        palettes is a list of 16 16 color palettes.
        The tiles are exported with the first palette in the list of palettes.
        The result image contains a palette that consists of all palettes merged together.
        """
        ...

    @abstractmethod
    def pil_to_tiles(self, image: Image.Image):
        """
        Imports tiles that are in a format as described in the documentation for tiles_to_pil.
        """
        ...

    @abstractmethod
    def import_tiles(self, tiles: Sequence[bytearray], contains_null_tile=False):
        """
        Replace the tiles.
        If contains_null_tile is False, the null tile is added to the list, at the beginning.
        """
        ...
