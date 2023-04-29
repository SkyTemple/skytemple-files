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

from abc import abstractmethod
from typing import List, Optional, Protocol, Sequence, TypeVar, runtime_checkable

from PIL import Image
from range_typed_integers import u8, u16

from skytemple_files.graphics.bpa.protocol import BpaProtocol
from skytemple_files.graphics.bpc.protocol import BpcProtocol
from skytemple_files.graphics.bpl.protocol import BplProtocol

P = TypeVar("P", bound=BpaProtocol)
C = TypeVar("C", bound=BpcProtocol, contravariant=True)
L = TypeVar("L", bound=BplProtocol, contravariant=True)


@runtime_checkable
class BmaProtocol(Protocol[P, C, L]):
    map_width_camera: u8
    map_height_camera: u8
    # ALL game maps have the same values here. Changing them does nothing,
    # so the game seems to be hardcoded to 3x3.
    tiling_width: u8
    tiling_height: u8
    # Map width & height in chunks, so map.map_width_camera / map.tiling_width
    # The only maps this is not true for are G01P08A. S01P01B, S15P05A, S15P05B, it seems they
    # are missing one tile in width (32x instead of 33x)
    # The game doesn't seem to care if this value is off by less than 3 (tiling_w/h).
    # But NOTE that this has consequences for the collision and unknown data layers! See notes at collision
    # below!
    map_width_chunks: u8
    map_height_chunks: u8
    # Through tests against the BPC, it was determined that unk5 is the number of layers:
    # It seems to be ignored by the game, however
    number_of_layers: u16
    # Some kind of boolean flag? Seems to control if there is a third data block between
    # layer data and collision - Seems to be related to NPC conversations, see below.
    unk6: u16
    # Some maps weirdly have 0x02 here and then have two collision layers, but they always seem redundant?
    number_of_collision_layers: u16

    layer0: Sequence[int]
    layer1: Optional[Sequence[int]]

    # if unk6:
    unknown_data_block: Optional[Sequence[int]]
    # if number_of_collision_layers > 0:
    collision: Optional[Sequence[bool]]
    # if number_of_collision_layers > 1:
    collision2: Optional[Sequence[bool]]

    @abstractmethod
    def __init__(self, data: bytes):
        ...

    @abstractmethod
    def to_pil_single_layer(
        self,
        bpc: C,
        palettes: Sequence[Sequence[int]],
        bpas: Sequence[Optional[P]],
        layer: int,
    ) -> Image.Image:
        """
        Converts one layer of the map into an image. The exported image has the same format as expected by from_pil.
        Exported is a single frame.

        The list of bpas must be the one contained in the bg_list. It needs to contain 8 slots, with empty
        slots being None.

        0: lower layer
        1: upper layer

        Example, of how to export and then import again using images:
            >>> l_upper = bma.to_pil_single_layer(bpc, bpl.palettes, bpas, 1)
            >>> l_lower = bma.to_pil_single_layer(bpc, bpl.palettes, bpas, 0)
            >>> bma.from_pil(bpc, bpl, l_lower, l_upper)
        """
        ...

    @abstractmethod
    def to_pil(
        self,
        bpc: C,
        bpl: L,
        bpas: List[Optional[P]],
        include_collision: bool = True,
        include_unknown_data_block: bool = True,
        pal_ani: bool = True,
        single_frame: bool = False,
    ) -> List[Image.Image]:
        """
        Converts the entire map into an image, as shown in the game. Each PIL image in the list returned is one
        frame. The palettes argument can be retrieved from the map's BPL (bpl.palettes).

        The method does not care about frame speeds. Each step of animation is simply returned as a new image,
        so if BPAs use different frame speeds, this is ignored; they effectively run at the same speed.
        If BPAs are using a different amount of frames per tile, the length of returned list of images will be the lowest
        common multiple of the different frame lengths.

        If pal_ani=True, then also includes palette animations.

        The list of bpas must be the one contained in the bg_list. It needs to contain 8 slots, with empty
        slots being None.
        """
        ...

    @abstractmethod
    def from_pil(
        self,
        bpc: C,
        bpl: L,
        lower_img: Optional[Image.Image] = None,
        upper_img: Optional[Image.Image] = None,
        force_import: bool = False,
        how_many_palettes_lower_layer: int = 16,
    ) -> None:
        """
        Import an entire map from one or two images (for each layer).
        Changes all tiles, tilemappings and chunks in the BPC and re-writes the two layer mappings of the BMA.
        Imports the palettes of the image to the BPL.
        The palettes of the images passed into this method must either identical or can be merged.
        The how_many_palettes_lower_layer parameter controls how many palettes
        from the lower layer image will then be used.

        The passed PIL will be split into separate tiles and the tile's palette index in the tile mapping for this
        coordinate is determined by the first pixel value of each tile in the PIL. The PIL
        must have a palette containing up to 16 sub-palettes with 16 colors each (256 colors).

        If a pixel in a tile uses a color outside of it's 16 color range, an error is thrown or
        the color is replaced with 0 of the palette (transparent). This is controlled by
        the force_import flag.
        The force_import option may be ignored by implementations, in that case the color is always just
        replaced with 0.

        Does not import animations. BPA tiles must be manually mapped to the tilemappings of the BPC after the import.
        BPL palette animations are not modified.

        The input images must have the same dimensions as the BMA (same dimensions as to_pil_single_layer would export).
        The input image can have a different number of layers, than the BMA. BPC and BMA layers are changed accordingly.

        BMA collision and data layer are not modified.
        """
        ...

    @abstractmethod
    def remove_upper_layer(self) -> None:
        """Remove the upper layer. Silently does nothing when it doesn't exist."""
        ...

    @abstractmethod
    def add_upper_layer(self) -> None:
        """Add an upper layer. Silently does nothing when it already exists."""
        ...

    @abstractmethod
    def resize(
        self,
        new_width_chunks: int,
        new_height_chunks: int,
        new_width_camera: int,
        new_height_camera: int,
    ) -> None:
        """
        Change the dimensions of the map. Existing tiles and chunks will keep their position in the grid.
        If the size is reduced, all tiles and chunks that are moved out of the new dimension box are removed.
        """
        ...

    @abstractmethod
    def place_chunk(self, layer_id: int, x: int, y: int, chunk_index: int) -> None:
        """Place the chunk with the given ID at the X and Y position. No error checking is done."""
        ...

    @abstractmethod
    def place_collision(
        self, collision_layer_id: int, x: int, y: int, is_solid: bool
    ) -> None:
        """Set the collision at the X and Y position. No error checking is done."""
        ...

    @abstractmethod
    def place_data(self, x: int, y: int, data: int) -> None:
        """Set data at the X and Y position. No error checking is done."""
        ...

    @abstractmethod
    def deepcopy(self) -> "BmaProtocol":
        """Perform a deep copy of self."""
        ...
