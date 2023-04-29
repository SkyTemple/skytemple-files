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
from range_typed_integers import u16

from skytemple_files.common.protocol import TilemapEntryProtocol
from skytemple_files.graphics.bpa.protocol import BpaProtocol


@runtime_checkable
class BpcLayerProtocol(Protocol):
    # The actual number of tiles is one lower
    number_tiles: u16
    # There must be 4 BPAs. (0 for not used)
    bpas: Sequence[u16]
    # NOTE: Incosistent with number_tiles. We are including the null chunk in this count.
    chunk_tilemap_len: u16
    # May also be set from outside after creation:
    tiles: Sequence[bytes]
    tilemap: Sequence[TilemapEntryProtocol]

    @abstractmethod
    def __init__(
        self,
        number_tiles: int,
        bpas: List[int],
        chunk_tilemap_len: int,
        tiles: List[bytes],
        tilemap: List[TilemapEntryProtocol],
    ) -> None:
        ...


T = TypeVar("T", bound=BpcLayerProtocol)
P = TypeVar("P", bound=BpaProtocol)


@runtime_checkable
class BpcProtocol(Protocol[T, P]):
    tiling_width: int
    tiling_height: int
    number_of_layers: int
    layers: Sequence[T]

    @abstractmethod
    def __init__(self, data: bytes, tiling_width: int, tiling_height: int):
        """
        Creates a BPC. A BPC contains two layers of image data. The image data is
        grouped in 8x8 tiles, and these tiles are grouped in {tiling_width}x{tiling_height}
        chunks using a tile mapping.
        These chunks are referenced in the BMA tile to build the actual image.
        The tiling sizes are also stored in the BMA file.
        Each tile mapping is aso asigned a palette number. The palettes are stored in the BPL
        file for the map background and always contain 16 colors.
        """
        ...

    @abstractmethod
    def chunks_to_pil(
        self, layer: int, palettes: Sequence[Sequence[int]], width_in_mtiles: int = 20
    ) -> Image.Image:
        """
        Convert all chunks of the BPC to one big PIL image.
        The chunks are all placed next to each other.
        The resulting image has one large palette with all palettes merged together.

        To get the palettes, use the data from the BPL file for this map background:

        >>> bpc.chunks_to_pil(bpl.palettes)

        The first chunk is a NULL tile. It is always empty, even when re-imported.

        Does NOT export BPA tiles. Chunks that reference BPA tiles are replaced with empty tiles. You will see
        warnings by the tiled_image module when this is the case.
        The mapping to BPA tiles has to be done programmatically using set_tile or set_chunk.

        """
        ...

    @abstractmethod
    def single_chunk_to_pil(
        self, layer: int, chunk_idx: int, palettes: Sequence[Sequence[int]]
    ) -> Image.Image:
        """
        Convert a single chunk of the BPC to one big PIL image. For general notes, see chunks_to_pil.

        Does NOT export BPA tiles. Chunks that reference BPA tiles are replaced with empty tiles.
        """
        ...

    @abstractmethod
    def tiles_to_pil(
        self,
        layer: int,
        palettes: Sequence[Sequence[int]],
        width_in_tiles: int = 20,
        single_palette: Optional[int] = None,
    ) -> Image.Image:
        """
        Convert all individual tiles of the BPC into one PIL image.
        The image contains all tiles next to each other, the image width is tile_width tiles.
        The resulting image has one large palette with all palettes merged together.

        The tiles are exported with the palette of the first placed tile or 0 if tile is not in tilemap,
        for easier editing. The result image contains a palette that consists of all palettes merged together.

        If single_palette is not None, all palettes are exported using the palette no. stored in single_palette.

        The first tile is a NULL tile. It is always empty, even when re-imported.
        """
        ...

    @abstractmethod
    def chunks_animated_to_pil(
        self,
        layer: int,
        palettes: Sequence[Sequence[int]],
        bpas: Sequence[Optional[P]],
        width_in_mtiles: int = 20,
    ) -> List[Image.Image]:
        """
        Exports chunks. For general notes see chunks_to_pil.

        However this method also exports BPA animated tiles referenced in the tilemap. This means it returns
        a set of images containing the chunks, including BPC tiles and BPA tiles. BPA tiles are animated, and
        each image contains one frame of the animation.

        The method does not care about frame speeds. Each step of animation is simply returned as a new image,
        so if BPAs use different frame speeds, this is ignored; they effectively run at the same speed.
        If BPAs are using a different amount of frames per tile, the length of returned list of images will be the lowest
        common denominator of the different frame lengths.

        Does not include palette animations. You can apply them by switching out the palettes of the PIL
        using the information provided by the BPL.

        The list of bpas must be the one contained in the bg_list. It needs to contain 8 slots, with empty
        slots being None.
        """
        ...

    @abstractmethod
    def single_chunk_animated_to_pil(
        self,
        layer: int,
        chunk_idx: int,
        palettes: Sequence[Sequence[int]],
        bpas: Sequence[Optional[P]],
    ) -> List[Image.Image]:
        """
        Exports a single chunk. For general notes see chunks_to_pil. For notes regarding the animation see
        chunks_animated_to_pil.
        """
        ...

    @abstractmethod
    def pil_to_tiles(self, layer: int, image: Image.Image) -> None:
        """
        Imports tiles that are in a format as described in the documentation for tiles_to_pil.
        Tile mappings, chunks and palettes are not updated.
        """
        ...

    @abstractmethod
    def pil_to_chunks(
        self, layer: int, image: Image.Image, force_import: bool = True
    ) -> List[List[int]]:
        """
        Imports chunks. Format same as for chunks_to_pil.
        Replaces tiles, tile mappings and therefor also chunks.
        "Unsets" BPA assignments! BPAs have to be manually re-assigned by using set_tile or set_chunk. BPA
        indices are stored after BPC tile indices.

        The PIL must have a palette containing the 16 sub-palettes with 16 colors each (256 colors).

        If a pixel in a tile uses a color outside of it's 16 color range, an error is thrown or
        the color is replaced with 0 of the palette (transparent). This is controlled by
        the force_import flag.

        Returns the palettes stored in the image for further processing (eg. replacing the BPL palettes).
        """
        ...

    @abstractmethod
    def get_tile(self, layer: int, index: int) -> TilemapEntryProtocol:
        ...

    @abstractmethod
    def set_tile(
        self, layer: int, index: int, tile_mapping: TilemapEntryProtocol
    ) -> None:
        ...

    @abstractmethod
    def get_chunk(self, layer: int, index: int) -> Sequence[TilemapEntryProtocol]:
        ...

    @abstractmethod
    def import_tiles(
        self, layer: int, tiles: List[bytes], contains_null_tile: bool = False
    ) -> None:
        """
        Replace the tiles of the specified layer.
        If contains_null_tile is False, the null tile is added to the list, at the beginning.
        """
        ...

    @abstractmethod
    def import_tile_mappings(
        self,
        layer: int,
        tile_mappings: List[TilemapEntryProtocol],
        contains_null_chunk: bool = False,
        correct_tile_ids: bool = True,
    ) -> None:
        """
        Replace the tile mappings of the specified layer.
        If contains_null_tile is False, the null chunk is added to the list, at the beginning.

        If correct_tile_ids is True, then the tile id of tile_mappings is also increased by one. Use this,
        if you previously used import_tiles with contains_null_tile=False
        """
        ...

    @abstractmethod
    def get_bpas_for_layer(
        self, layer: int, bpas_from_bg_list: Sequence[Optional[P]]
    ) -> List[P]:
        """
        This method returns a list of not None BPAs assigned to the BPC layer from an ordered list of possible candidates.
        What is returned depends on the BPA mapping of the layer.

        The bg_list.dat contains a list of 8 BPAs. The first four are for layer 0, the next four for layer 1.

        This method asserts, that the number of tiles stored in the layer for the BPA, matches the data in the BPA!
        """
        ...

    @abstractmethod
    def set_chunk(
        self, layer: int, index: int, new_tilemappings: Sequence[TilemapEntryProtocol]
    ) -> None:
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
    def process_bpa_change(self, bpa_index: int, tiles_bpa_new: u16) -> None:
        """
        Update the layer entries for BPA tile number change and also re-map all tilemappings,
        so that they still match their original tile, even though some tiles in-between may now
        be new or removed.
        """
        ...
