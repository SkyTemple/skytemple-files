import math
from typing import Tuple, List

from PIL import Image

from skytemple_files.common.tiled_image import TilemapEntry, to_pil
from skytemple_files.common.util import *
from skytemple_files.graphics.bpa.model import Bpa

BPC_PIXEL_BITLEN = 4
BPC_TILE_DIM = 8
BPC_TILEMAP_BYTELEN = 2


class BpcLayer:
    def __init__(self, number_tiles, bpas, tilemap_len, tiles=None, tilemap=None):
        # The actual number of tiles is one lower
        # TODO: Remember to add 1 during seri.
        self.number_tiles = number_tiles - 1
        # There must be 4 BPAs. (0 for not used)
        assert len(bpas) == 4
        self.bpas = bpas
        self.chunk_tilemap_len = tilemap_len
        # May also be set from outside after creation:
        self.tiles = tiles
        self.tilemap = tilemap

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
        # start_tile_map_1 is 2 bytes-aligned TODO: Don't forget for serialization!
        if start_tile_map_1 % 2 != 0:
            start_tile_map_1 += 1

        # Read the first layer tilemap
        self.layers[0].tilemap = self._read_tilemap_data(FileType.BPC_TILEMAP.decompress(
            data[start_tile_map_1:end_of_layer_data],
            # TODO: It's not documented yet that the 9 used here in the docs by psy_commando is actually the
            #       size of the chunks.
            stop_when_size=(self.layers[0].chunk_tilemap_len - 1) * (self.tiling_width * self.tiling_height) * 2
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
                stop_when_size=(self.layers[1].chunk_tilemap_len - 1) * (self.tiling_width * self.tiling_height) * 2
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
            tilemap.append(TilemapEntry.from_bytes(0))
        for i, entry in enumerate(iter_bytes(data, BPC_TILEMAP_BYTELEN)):
            tilemap.append(TilemapEntry.from_bytes(int.from_bytes(entry, 'little')))
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
        for i in range(0, self.layers[layer].number_tiles):
            dummy_tile_map.append(TilemapEntry(
                idx=i,
                pal_idx=single_palette if single_palette is not None else self._get_palette_for_tile(layer, i),
                flip_x=False,
                flip_y=False
            ))
        width = width_in_tiles * BPC_TILE_DIM
        height = math.ceil(self.layers[layer].number_tiles / width_in_tiles) * BPC_TILE_DIM

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

        TODO: The speed can be increased SIGNIFICANTLY if we only re-render the changed
              animated tiles instead!

        TODO: Move to a method to export single chunks and then merge them instead?
        """
        ldata = self.layers[layer]
        # First check if we even have BPAs to use
        is_using_bpa = len(bpas) > 0 and any(x > 0 for x in ldata.bpas)
        if not is_using_bpa:
            # Simply build the single chunks frame
            return [self.chunks_to_pil(layer, palettes, width_in_mtiles)]

        bpa_animation_indices = [0, 0, 0, 0]
        frames = []

        is_first_run_add_extra_tile = True

        while True:  # Ended by check at end (do while)
            previous_end_of_tiles = ldata.number_tiles
            # For each frame: Insert all BPA current frame tiles into their slots
            for bpaidx, bpa in enumerate(self.get_bpas_for_layer(layer, bpas)):
                # There is one extra null tile between the BPC and each of the BPA data:
                previous_end_of_tiles += 1
                if is_first_run_add_extra_tile:
                    ldata.tiles.append(bytearray(int(BPC_TILE_DIM * BPC_TILE_DIM / 2)))

                # Add the BPA tiles for this frame to the set of BPC tiles:
                new_end_of_tiles = previous_end_of_tiles + bpa.number_of_images
                ldata.tiles[previous_end_of_tiles:new_end_of_tiles] = bpa.tiles_for_frame(bpa_animation_indices[bpaidx])

                previous_end_of_tiles = new_end_of_tiles
                bpa_animation_indices[bpaidx] += 1
                bpa_animation_indices[bpaidx] %= bpa.number_of_frames

            frames.append(self.chunks_to_pil(layer, palettes, width_in_mtiles))

            is_first_run_add_extra_tile = False
            # All animations have been played, we are done!
            if bpa_animation_indices == [0, 0, 0, 0]:
                break

        # RESET the layer's tiles to NOT include the BPA tiles!
        ldata.tiles = ldata.tiles[:ldata.number_tiles]
        return frames

    def pil_to_tiles(self, layer: int, image: Image.Image):
        pass  # todo - replaces the tile data but doesn't change any tile mappings and so also no chunks

    def pil_to_chunks(self, layer: int, image: Image.Image):
        pass  # todo - replaces the tile data AND all tile mappings - Used to create new chunks.
              #        Works like BGP import. - "Unsets" BPA mappings however, because chunks_to_pil contains
              #        no BPA.

    def get_tile(self, layer: int, index: int) -> TilemapEntry:
        return self.layers[layer].tilemap[index]

    def set_tile(self, layer: int, index: int, tile_mapping: TilemapEntry):
        self.layers[layer].tilemap[index] = tile_mapping

    def get_chunk(self, layer: int, index: int) -> List[TilemapEntry]:
        mtidx = index * self.tiling_width * self.tiling_height
        return self.layers[layer].tilemap[mtidx:mtidx+9]

    def get_bpas_for_layer(self, layer: int, possible_bpas_ordered: List[Bpa]) -> List[Bpa]:
        """
        This method returns a list of BPAs assigned to the BPC layer from an ordered list of possible candidates.
        What is returned depends on the BPA mapping of the layer.

        The way the game maps BPAs to BPC layers is really weird...
        If a map has two BPAs assigned, you would assume, that each occupies a unique slot
        in the BPA list for a layer. But they don't. Instead the four slot list is simply filled left to right.
        Example: BPC has two BPAs with the following tile numbers: [64, 128].
        Now the layers may have specs like this:  Layer1: [64, 0, 0, 0] - Layer2: [128, 0, 0, 0]
        As you can see, BPAs are entirely just mapped by their number of tiles.
        Now what happens when two BPAs of a BPC have the same index number? I don't know! But in this case
        the method will return the first matching BPA passed in. Should a BPC layer contain multiple BPA
        index counts of the same length, the next BPA with that number of tiles is added.
        """
        possible_bpas_ordered = possible_bpas_ordered.copy()
        bpas = []
        for bpa_tile_num in self.layers[layer].bpas:
            if bpa_tile_num == 0:
                continue
            try:
                match_idx = next((i for i, e in enumerate(possible_bpas_ordered) if e.number_of_images == bpa_tile_num))
            except StopIteration as err:
                raise ValueError(f"The list of possible BPAs doesn't contain a BPA with the number "
                                 f"of tiles {bpa_tile_num}, as it's defined in the BPC's layer.") from err
            bpas.append(possible_bpas_ordered.pop(match_idx))
        return bpas

    def set_chunk(self, layer: int, index: int, new_tilemappings: List[TilemapEntry]):
        if len(new_tilemappings) < self.tiling_width * self.tiling_height:
            raise ValueError(f"The new tilemapping for this chunk must contain"
                             f"{self.tiling_width}x{self.tiling_height} tiles.")
        mtidx = index * self.tiling_width * self.tiling_height
        self.layers[layer].tilemap[mtidx:mtidx+9] = new_tilemappings

    def _get_palette_for_tile(self, layer, i):
        """Returns the first found palette of the tile with idx i. Or 0"""
        for t in self.layers[layer].tilemap:
            if t.idx == i:
                return t.pal_idx
        return 0
