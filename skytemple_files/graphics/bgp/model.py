import math
from itertools import chain
from typing import Tuple, List

from PIL import Image
from bitstring import BitStream

from skytemple_files.common.tiled_image import to_pil, TilemapEntry, to_pil_tiled
from skytemple_files.common.util import read_bytes

BGP_RES_WIDTH = 256
BGP_RES_HEIGHT = 192
BGP_HEADER_LENGTH = 32
BGP_PAL_ENTRY_LEN = 4
BGP_PAL_UNKNOWN4_COLOR_VAL = 0x80
# The palette is actually a list of smaller palettes. Each palette has this many colors:
BGP_PAL_NUMBER_COLORS = 16
BGP_TILEMAP_ENTRY_BITLEN = 16
BGP_PIXEL_BITLEN = 4
BGP_TILE_DIM = 8
BGP_RES_WIDTH_IN_TILES = int(BGP_RES_WIDTH / BGP_TILE_DIM)
BGP_RES_HEIGHT_IN_TILES = int(BGP_RES_HEIGHT / BGP_TILE_DIM)
BGP_TOTAL_NUMBER_TILES = BGP_RES_WIDTH_IN_TILES * BGP_RES_HEIGHT_IN_TILES
# NOTE: Tile 0 is always 0x0.


class BgpHeader:
    """Header for a Bgp Image"""
    def __init__(self, data: BitStream, offset=0):
        self.palette_begin = read_bytes(data, offset, 4).uintle
        if self.palette_begin != BGP_HEADER_LENGTH:
            raise ValueError("Invalid BGP image: Palette pointer too low.")
        self.palette_length = read_bytes(data, offset + 4, 4).uintle
        self.tiles_begin = read_bytes(data, offset + 8, 4).uintle
        self.tiles_length = read_bytes(data, offset + 12, 4).uintle
        self.tilemap_data_begin = read_bytes(data, offset + 16, 4).uintle
        self.tilemap_data_length = read_bytes(data, offset + 20, 4).uintle
        self.unknown3 = read_bytes(data, offset + 24, 4).uintle
        self.unknown4 = read_bytes(data, offset + 28, 4).uintle


class Bgp:
    def __init__(self, data: BitStream):
        self.data = data
        self.header = BgpHeader(self.data)
        self._extract_palette()
        self._extract_tilemap()
        self._extract_tiles()

    def _extract_palette(self):
        if self.header.palette_length % 16 != 0:
            raise ValueError("Invalid BGP image: Palette must be dividable by 16")
        pal_end = self.header.palette_begin + self.header.palette_length
        self.palettes = []
        self.current_palette = []
        colors_read_for_current_palette = 0
        for pal_entry in self.data.cut(8 * BGP_PAL_ENTRY_LEN, self.header.palette_begin * 8, pal_end * 8):
            r, g, b, unk = pal_entry.bytes
            self.current_palette.append(r)
            self.current_palette.append(g)
            self.current_palette.append(b)
            colors_read_for_current_palette += 1
            if colors_read_for_current_palette >= 16:
                self.palettes.append(self.current_palette)
                self.current_palette = []
                colors_read_for_current_palette = 0

    def _extract_tilemap(self):
        tilemap_end = self.header.tilemap_data_begin + self.header.tilemap_data_length
        self.tilemap = []
        for i, entry in enumerate(self.data.cut(BGP_TILEMAP_ENTRY_BITLEN, self.header.tilemap_data_begin * 8, tilemap_end * 8)):
            # NOTE: There will likely be more than 768 (BGP_TOTAL_NUMBER_TILES) tiles. Why is unknown, but the
            #       rest is just zero padding.
            self.tilemap.append(TilemapEntry.from_bytes(entry.uintle))
        if len(self.tilemap) < BGP_TOTAL_NUMBER_TILES:
            raise ValueError(f"Invalid BGP image: Too few tiles ({len(self.tilemap)}) in tile mapping."
                             f"Must be at least {BGP_TOTAL_NUMBER_TILES}.")

    def _extract_tiles(self):
        self.tiles = []
        tiles_end = self.header.tiles_begin + self.header.tiles_length
        for tile in self.data.cut(BGP_PIXEL_BITLEN * BGP_TILE_DIM * BGP_TILE_DIM, self.header.tiles_begin * 8,
                                  tiles_end * 8):
            # NOTE: Again, the number of tiles is probably bigger than BGP_TOTAL_NUMBER_TILES... (zero padding)
            self.tiles.append(tile)
        if len(self.tiles) < BGP_TOTAL_NUMBER_TILES:
            raise ValueError(f"Invalid BGP image: Too few tiles ({len(self.tiles)}) in tile data."
                             f"Must be at least {BGP_TOTAL_NUMBER_TILES}.")

    def to_pil(self, ignore_flip_bits=False) -> Image.Image:
        """
        Convert all tiles of the BGP to one big PIL image.
        The resulting image has one large palette with 256 colors.
        If ignore_flip_bits is set, tiles are not flipped.

        The image returned will have the size 256x192.
        For dimension calculating, see the constants of this module.
        """
        return to_pil(
            self.tilemap, self.tiles, self.palettes, BGP_TILE_DIM, BGP_RES_WIDTH, BGP_RES_HEIGHT, 1, 1, ignore_flip_bits
        )

    def to_pil_tiled(self, ignore_flip_bits=False) -> List[Image.Image]:
        """
        Convert all tiles of the BGP into separate PIL images.
        Each image has one palette with 16 colors.
        If ignore_flip_bits is set, tiles are not flipped.

        768 tiles are returned, for dimension calculating, see the constants of this module.
        """
        return to_pil_tiled(
            self.tilemap, self.tiles, self.palettes, BGP_TILE_DIM, ignore_flip_bits
        )

    def from_pil(self, pil: Image.Image, force_import=False) -> None:
        """
        Modify the image data in the BGP by importing the passed PIL.
        The passed PIL will be split into separate tiles and the tile's palette index
        is determined by the first pixel value of each tile in the PIL. The PIL
        must have a palette containing the 16 sub-palettes with 16 colors each (256 colors).

        If a pixel in a tile uses a color outside of it's 16 color range, an error is thrown or
        the color is replaced with 0 of the palette (transparent). This is controlled by
        the force_import flag.

        The image must have the size 256x192. For dimension calculating, see the constants of this module.

        Currently all tiles are imported as-is, without checking if the same or a flipped
        version of a tile already exists. So basically no "compression" in image size is done
        by re-using tiles.
        """
        pass  # todo [in tiled_image.py]

    def from_pil_tiled(self, pils: List[Image.Image]) -> None:
        """
        Modify the image data in the BGP by importing the passed PILs.
        Each of the PILs is one tile (in order). The palette of the PIL (16 colors) is imported
        into the 16 palette list of the BGP, if the palette is not already in it.

        The list of PILs must contain 768 tiles. For dimension calculating, see the constants of this module.

        If a palette is not already in the palette list but the list is already full,
        an error is thrown. This means the PILs must all share the same common 16 color palettes.

        Currently all tiles are imported as-is, without checking if the same or a flipped
        version of a tile already exists. So basically no "compression" in image size is done
        by re-using tiles.
        """
        pass  # todo [in tiled_image.py]
