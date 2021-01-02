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
from typing import Tuple

try:
    from PIL import Image
except ImportError:
    from pil import Image

from skytemple_files.common.tiled_image import TilemapEntry, to_pil, from_pil
from skytemple_files.common.util import *
from skytemple_files.graphics.bpa.model import Bpa
from skytemple_files.graphics.bpl.model import BPL_IMG_PAL_LEN, BPL_MAX_PAL

BPC_PIXEL_BITLEN = 4
BPC_TILE_DIM = 8
BPC_TILEMAP_BYTELEN = 2


class BpcLayer:
    def __init__(self, number_tiles, bpas, tilemap_len, tiles=None, tilemap=None):
        # The actual number of tiles is one lower
        self.number_tiles = number_tiles - 1
        # There must be 4 BPAs. (0 for not used)
        assert len(bpas) == 4
        self.bpas = bpas
        # TODO: Incosistent with number_tiles. If we want to be consistent we also have to subtract
        #       1 here or remove the -1 above.
        self.chunk_tilemap_len = tilemap_len
        # May also be set from outside after creation:
        self.tiles = tiles
        self.tilemap: List[TilemapEntry] = tilemap

    def __repr__(self):
        return f"<#T{self.number_tiles} #TM{self.chunk_tilemap_len} - BPA: [{self.bpas}]>"


class Bpc:
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
        from skytemple_files.common.types.file_types import FileType
        if not isinstance(data, memoryview):
            data = memoryview(data)

        self.tiling_width = tiling_width
        self.tiling_height = tiling_height

        # Only stored for debug. They are not updated, only regenerated when serialized:
        self._upper_layer_pointer = read_uintle(data, 0, 2)
        self._lower_layer_pointer = read_uintle(data, 2, 2)

        self.number_of_layers = 2 if self._lower_layer_pointer > 0 else 1

        # Depending on the number of layers there are now one or two metadata sections
        # for these layers. The layers are completed by a BMA file that comes with this BPC file!
        # The BMA contains tiling w/h and w/h of the map. See bg_list.dat for mapping.
        self.layers = []
        for layer_spec in iter_bytes(data, 12, 4, 4 + (12 * self.number_of_layers)):
            bpas = [
                read_uintle(layer_spec, 2, 2),
                read_uintle(layer_spec, 4, 2),
                read_uintle(layer_spec, 6, 2),
                read_uintle(layer_spec, 8, 2)
            ]
            self.layers.append(BpcLayer(
                number_tiles=read_uintle(layer_spec, 0, 2),
                tilemap_len=read_uintle(layer_spec, 10, 2),
                bpas=bpas
            ))

        # Read the first layer image data
        end_of_layer_data = self._lower_layer_pointer if self._lower_layer_pointer > 0 else None
        self.layers[0].tiles, compressed_tile_size_1 = self._read_tile_data(FileType.BPC_IMAGE.decompress(
            # We don't know when the compressed data ends, but at least it can't go into the next layer
            data[self._upper_layer_pointer:end_of_layer_data],
            stop_when_size=self.layers[0].number_tiles * 32
        ))
        assert len(self.layers[0].tiles) - 1 == self.layers[0].number_tiles
        start_tile_map_1 = self._upper_layer_pointer + compressed_tile_size_1
        # start_tile_map_1 is 2 bytes-aligned
        if start_tile_map_1 % 2 != 0:
            start_tile_map_1 += 1

        # Read the first layer tilemap
        self.layers[0].tilemap = self._read_tilemap_data(FileType.BPC_TILEMAP.decompress(
            data[start_tile_map_1:end_of_layer_data],
            # TODO: It's not documented yet that the 9 used here in the docs by psy_commando is actually the
            #       size of the chunks.
            stop_when_size=(self.layers[0].chunk_tilemap_len - 1) * (self.tiling_width * self.tiling_height) * BPC_TILEMAP_BYTELEN
        ))

        if self.number_of_layers > 1:
            # Read the second layer image data
            self.layers[1].tiles, compressed_tile_size_2 = self._read_tile_data(FileType.BPC_IMAGE.decompress(
                data[self._lower_layer_pointer:],
                stop_when_size=self.layers[1].number_tiles * 32
            ))
            start_tile_map_2 = self._lower_layer_pointer + compressed_tile_size_2
            # start_tile_map_2 is 2 bytes-aligned
            if start_tile_map_2 % 2 != 0:
                start_tile_map_2 += 1
            # Read the second layer tilemap
            self.layers[1].tilemap = self._read_tilemap_data(FileType.BPC_TILEMAP.decompress(
                data[start_tile_map_2:],
                stop_when_size=(self.layers[1].chunk_tilemap_len - 1) * (self.tiling_width * self.tiling_height) * BPC_TILEMAP_BYTELEN
            ))

    def _read_tile_data(self, data: Tuple[bytes, int]):
        """Handles the decompressed tile data returned by the BPC_IMAGE decompressor."""
        n_bytes = int(BPC_TILE_DIM * BPC_TILE_DIM / 2)
        # The first tile is not stored, but is always empty
        tiles = [bytearray(n_bytes)]
        for tile in iter_bytes(data[0], n_bytes):
            tiles.append(bytearray(tile))
        return tiles, data[1]

    def _read_tilemap_data(self, data: bytes):
        """Handles the decompressed tile data returned by the BPC_TILEMAP decompressor."""
        tilemap = []
        # The first chunk is not stored, but is always empty
        for i in range(0, self.tiling_width*self.tiling_height):
            tilemap.append(TilemapEntry.from_int(0))
        for i, entry in enumerate(iter_bytes(data, BPC_TILEMAP_BYTELEN)):
            tilemap.append(TilemapEntry.from_int(int.from_bytes(entry, 'little')))
        return tilemap

    def chunks_to_pil(self, layer: int, palettes: List[List[int]], width_in_mtiles=20) -> Image.Image:
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
        width = width_in_mtiles * self.tiling_width * BPC_TILE_DIM
        height = math.ceil(self.layers[layer].chunk_tilemap_len / width_in_mtiles) * self.tiling_height * BPC_TILE_DIM
        return to_pil(
            self.layers[layer].tilemap, self.layers[layer].tiles, palettes, BPC_TILE_DIM,
            width, height, self.tiling_width, self.tiling_height
        )

    def single_chunk_to_pil(self, layer: int, chunk_idx: int, palettes: List[List[int]]) -> Image.Image:
        """
        Convert a single chunk of the BPC to one big PIL image. For general notes, see chunks_to_pil.

        Does NOT export BPA tiles. Chunks that reference BPA tiles are replaced with empty tiles.
        """
        mtidx = chunk_idx * self.tiling_width * self.tiling_height
        return to_pil(
            self.layers[layer].tilemap[mtidx:mtidx + 9], self.layers[layer].tiles, palettes, BPC_TILE_DIM,
            BPC_TILE_DIM * self.tiling_width, BPC_TILE_DIM * self.tiling_height,
            self.tiling_width, self.tiling_height
        )

    def tiles_to_pil(self, layer: int, palettes: List[List[int]], width_in_tiles=20, single_palette=None) -> Image.Image:
        """
        Convert all individual tiles of the BPC into one PIL image.
        The image contains all tiles next to each other, the image width is tile_width tiles.
        The resulting image has one large palette with all palettes merged together.

        The tiles are exported with the palette of the first placed tile or 0 if tile is not in tilemap,
        for easier editing. The result image contains a palette that consists of all palettes merged together.

        If single_palette is not None, all palettes are exported using the palette no. stored in single_palette.

        The first tile is a NULL tile. It is always empty, even when re-imported.
        """

        # create a dummy tile map containing all the tiles
        dummy_tile_map = []
        for i in range(0, self.layers[layer].number_tiles+1):
            dummy_tile_map.append(TilemapEntry(
                idx=i,
                pal_idx=single_palette if single_palette is not None else self._get_palette_for_tile(layer, i),
                flip_x=False,
                flip_y=False
            ))
        width = width_in_tiles * BPC_TILE_DIM
        height = math.ceil((self.layers[layer].number_tiles+1) / width_in_tiles) * BPC_TILE_DIM

        return to_pil(
            dummy_tile_map, self.layers[layer].tiles, palettes, BPC_TILE_DIM, width, height
        )

    def chunks_animated_to_pil(
            self, layer: int, palettes: List[List[int]], bpas: List[Bpa], width_in_mtiles=20
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

        TODO: The speed can be increased if we only re-render the changed animated tiles instead!
        """
        ldata = self.layers[layer]
        # First check if we even have BPAs to use
        is_using_bpa = len(bpas) > 0 and any(x > 0 for x in ldata.bpas)
        if not is_using_bpa:
            # Simply build the single chunks frame
            return [self.chunks_to_pil(layer, palettes, width_in_mtiles)]

        bpa_animation_indices = [0, 0, 0, 0]
        frames = []

        orig_len = len(ldata.tiles)
        while True:  # Ended by check at end (do while)
            previous_end_of_tiles = orig_len
            # For each frame: Insert all BPA current frame tiles into their slots
            for bpaidx, bpa in enumerate(self.get_bpas_for_layer(layer, bpas)):

                # Add the BPA tiles for this frame to the set of BPC tiles:
                new_end_of_tiles = previous_end_of_tiles + bpa.number_of_tiles
                ldata.tiles[previous_end_of_tiles:new_end_of_tiles] = bpa.tiles_for_frame(bpa_animation_indices[bpaidx])

                previous_end_of_tiles = new_end_of_tiles
                bpa_animation_indices[bpaidx] += 1
                bpa_animation_indices[bpaidx] %= bpa.number_of_frames

            frames.append(self.chunks_to_pil(layer, palettes, width_in_mtiles))
            # All animations have been played, we are done!
            if bpa_animation_indices == [0, 0, 0, 0]:
                break

        # RESET the layer's tiles to NOT include the BPA tiles!
        ldata.tiles = ldata.tiles[:orig_len]
        return frames

    def single_chunk_animated_to_pil(
            self, layer: int, chunk_idx: int, palettes: List[List[int]], bpas: List[Bpa]
    ) -> List[Image.Image]:
        """
        Exports a single chunk. For general notes see chunks_to_pil. For notes regarding the animation see
        chunks_animated_to_pil.

        TODO: Code duplication with chunks_animated_to_pil. Could probably be refactored.
        """
        ldata = self.layers[layer]
        # First check if we even have BPAs to use
        is_using_bpa = len(bpas) > 0 and any(x > 0 for x in ldata.bpas)
        if is_using_bpa:
            # Also check if any of the tiles in the chunk even uses BPA tiles
            is_using_bpa = False
            for tilem in self.get_chunk(layer, chunk_idx):
                if tilem.idx > ldata.number_tiles:
                    is_using_bpa = True
                    break
        if not is_using_bpa:
            # Simply build the single chunks frame
            return [self.single_chunk_to_pil(layer, chunk_idx, palettes)]

        bpa_animation_indices = [0, 0, 0, 0]
        frames = []

        orig_len = len(ldata.tiles)
        while True:  # Ended by check at end (do while)
            previous_end_of_tiles = orig_len
            # For each frame: Insert all BPA current frame tiles into their slots
            for bpaidx, bpa in enumerate(self.get_bpas_for_layer(layer, bpas)):

                # Add the BPA tiles for this frame to the set of BPC tiles:
                new_end_of_tiles = previous_end_of_tiles + bpa.number_of_tiles
                ldata.tiles[previous_end_of_tiles:new_end_of_tiles] = bpa.tiles_for_frame(bpa_animation_indices[bpaidx])

                previous_end_of_tiles = new_end_of_tiles
                if bpa.number_of_frames > 0:
                    bpa_animation_indices[bpaidx] += 1
                    bpa_animation_indices[bpaidx] %= bpa.number_of_frames

            frames.append(self.single_chunk_to_pil(layer, chunk_idx, palettes))
            # All animations have been played, we are done!
            if bpa_animation_indices == [0, 0, 0, 0]:
                break

        # RESET the layer's tiles to NOT include the BPA tiles!
        ldata.tiles = ldata.tiles[:orig_len]
        return frames

    def pil_to_tiles(self, layer: int, image: Image.Image):
        """
        Imports tiles that are in a format as described in the documentation for tiles_to_pil.
        Tile mappings, chunks and palettes are not updated.
        """
        self.layers[layer].tiles, _, __ = from_pil(
            image, BPL_IMG_PAL_LEN, BPL_MAX_PAL, BPC_TILE_DIM,
            image.width, image.height, optimize=False
        )
        self.layers[layer].number_tiles = len(self.layers[layer].tiles) - 1

    def pil_to_chunks(self, layer: int, image: Image.Image, force_import=True) -> List[List[int]]:
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
        self.layers[layer].tiles, self.layers[layer].tilemap, palettes = from_pil(
            image, BPL_IMG_PAL_LEN, BPL_MAX_PAL, BPC_TILE_DIM,
            image.width, image.height, 3, 3, force_import
        )
        self.layers[layer].number_tiles = len(self.layers[layer].tiles) - 1
        self.layers[layer].chunk_tilemap_len = int(len(self.layers[layer].tilemap) / self.tiling_width / self.tiling_height)
        return palettes

    def get_tile(self, layer: int, index: int) -> TilemapEntry:
        return self.layers[layer].tilemap[index]

    def set_tile(self, layer: int, index: int, tile_mapping: TilemapEntry):
        self.layers[layer].tilemap[index] = tile_mapping

    def get_chunk(self, layer: int, index: int) -> List[TilemapEntry]:
        mtidx = index * self.tiling_width * self.tiling_height
        return self.layers[layer].tilemap[mtidx:mtidx+9]

    def import_tiles(self, layer: int, tiles: List[bytearray], contains_null_tile=False):
        """
        Replace the tiles of the specified layer.
        If contains_null_tile is False, the null tile is added to the list, at the beginning.
        """
        if not contains_null_tile:
            tiles = [bytearray(int(BPC_TILE_DIM * BPC_TILE_DIM / 2))] + tiles
        self.layers[layer].tiles = tiles
        self.layers[layer].number_tiles = len(tiles) - 1

    def import_tile_mappings(
            self, layer: int, tile_mappings: List[TilemapEntry],
            contains_null_chunk=False, correct_tile_ids=True
    ):
        """
        Replace the tile mappings of the specified layer.
        If contains_null_tile is False, the null chunk is added to the list, at the beginning.

        If correct_tile_ids is True, then the tile id of tile_mappings is also increased by one. Use this,
        if you previously used import_tiles with contains_null_tile=False
        """
        nb_tiles_in_chunk = self.tiling_width * self.tiling_height
        if correct_tile_ids:
            for entry in tile_mappings:
                if not contains_null_chunk:
                    entry.idx += 1
        if not contains_null_chunk:
            tile_mappings = [TilemapEntry.from_int(0) for _ in range(0, nb_tiles_in_chunk)] + tile_mappings
        self.layers[layer].tilemap = tile_mappings
        self.layers[layer].chunk_tilemap_len = int(len(tile_mappings) / self.tiling_width / self.tiling_height)

    def get_bpas_for_layer(self, layer: int, bpas_from_bg_list: List[Bpa]) -> List[Bpa]:
        """
        This method returns a list of not None BPAs assigned to the BPC layer from an ordered list of possible candidates.
        What is returned depends on the BPA mapping of the layer.

        The bg_list.dat contains a list of 8 BPAs. The first four are for layer 0, the next four for layer 1.

        This method asserts, that the number of tiles stored in the layer for the BPA, matches the data in the BPA!
        """
        bpas = bpas_from_bg_list[layer*4:(layer*4)+4]
        not_none_bpas = []
        for i, bpa in enumerate(bpas):
            if bpa is not None:
                assert self.layers[layer].bpas[i] == bpa.number_of_tiles
                not_none_bpas.append(bpa)
            else:
                assert self.layers[layer].bpas[i] == 0
        return not_none_bpas

    def set_chunk(self, layer: int, index: int, new_tilemappings: List[TilemapEntry]):
        if len(new_tilemappings) < self.tiling_width * self.tiling_height:
            raise ValueError(f"The new tilemapping for this chunk must contain"
                             f"{self.tiling_width}x{self.tiling_height} tiles.")
        mtidx = index * self.tiling_width * self.tiling_height
        self.layers[layer].tilemap[mtidx:mtidx+9] = new_tilemappings

    def remove_upper_layer(self):
        """Remove the upper layer. Silently does nothing when it doesn't exist."""
        if self.number_of_layers == 1:
            return
        self.number_of_layers = 1
        self.layers[0] = self.layers[1]
        del self.layers[1]

    def add_upper_layer(self):
        """Add an upper layer. Silently does nothing when it already exists."""
        if self.number_of_layers == 2:
            return
        self.number_of_layers = 2
        if len(self.layers) < 2:
            self.layers.append(self.layers[0])
        else:
            self.layers[1] = self.layers[0]

        tilemap = []
        # The first chunk is not stored, but is always empty
        for i in range(0, self.tiling_width * self.tiling_height):
            tilemap.append(TilemapEntry.from_int(0))
        self.layers[0] = BpcLayer(
            number_tiles=1,
            tilemap_len=1,
            bpas=[0, 0, 0, 0],
            # The first tile is not stored, but is always empty
            tiles=[bytearray(int(BPC_TILE_DIM * BPC_TILE_DIM / 2))],
            tilemap=tilemap
        )

    def process_bpa_change(self, bpa_index, tiles_bpa_new):
        """
        Update the layer entries for BPA tile number change and also re-map all tilemappings,
        so that they still match their original tile, even though some tiles in-between may now
        be new or removed.
        """
        layer_idx = int(bpa_index / 4)
        bpa_layer_idx = bpa_index % 4
        # Re-map all affected tile mappings.
        tile_idx_start = len(self.layers[layer_idx].tiles)
        for bpaidx, n_bpas in enumerate(self.layers[layer_idx].bpas):
            if bpaidx >= bpa_layer_idx:
                break
            tile_idx_start = tile_idx_start + n_bpas

        old_tile_idx_end = tile_idx_start + self.layers[layer_idx].bpas[bpa_layer_idx]
        number_tiles_added = tiles_bpa_new - self.layers[layer_idx].bpas[bpa_layer_idx] # may be negative, of course.
        for mapping in self.layers[layer_idx].tilemap:
            if mapping.idx > old_tile_idx_end:
                # We need to move this back by the full amount
                mapping.idx += number_tiles_added
            elif mapping.idx >= tile_idx_start:
                # We may need to set to 0, if we removed
                relative_old_mapping = mapping.idx - tile_idx_start
                if relative_old_mapping >= tiles_bpa_new:
                    mapping.idx = 0

        # Finally: Update layer entry.
        self.layers[layer_idx].bpas[bpa_layer_idx] = tiles_bpa_new

    def _get_palette_for_tile(self, layer, i):
        """Returns the first found palette of the tile with idx i. Or 0"""
        for t in self.layers[layer].tilemap:
            if t.idx == i:
                return t.pal_idx
        return 0
