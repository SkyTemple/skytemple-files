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

try:
    from PIL import Image
except ImportError:
    from pil import Image

from skytemple_files.common.tiled_image import to_pil, TilemapEntry, to_pil_tiled, from_pil
from skytemple_files.common.util import *

BGP_RES_WIDTH = 256
BGP_RES_HEIGHT = 192
BGP_HEADER_LENGTH = 32
BGP_PAL_ENTRY_LEN = 4
BGP_PAL_UNKNOWN4_COLOR_VAL = 0x80
# The palette is actually a list of smaller palettes. Each palette has this many colors:
BGP_PAL_NUMBER_COLORS = 16
# The maximum number of palettes supported
BGP_MAX_PAL = 16
BGP_TILEMAP_ENTRY_BYTELEN = 2
BGP_PIXEL_BITLEN = 4
BGP_TILE_DIM = 8
BGP_RES_WIDTH_IN_TILES = int(BGP_RES_WIDTH / BGP_TILE_DIM)
BGP_RES_HEIGHT_IN_TILES = int(BGP_RES_HEIGHT / BGP_TILE_DIM)
BGP_TOTAL_NUMBER_TILES = BGP_RES_WIDTH_IN_TILES * BGP_RES_HEIGHT_IN_TILES
# All BPGs have this many tiles and tilemapping entries for some reason
BGP_TOTAL_NUMBER_TILES_ACTUALLY = 1024
# NOTE: Tile 0 is always 0x0.


class BgpHeader:
    """Header for a Bgp Image"""
    def __init__(self, data: bytes, offset=0):
        # WARNING: The pointers and lengths are not updated after creation. The writer re-generates them.
        self.palette_begin = read_uintle(data, offset, 4)
        if self.palette_begin != BGP_HEADER_LENGTH:
            raise ValueError("Invalid BGP image: Palette pointer too low.")
        self.palette_length = read_uintle(data, offset + 4, 4)
        self.tiles_begin = read_uintle(data, offset + 8, 4)
        self.tiles_length = read_uintle(data, offset + 12, 4)
        self.tilemap_data_begin = read_uintle(data, offset + 16, 4)
        self.tilemap_data_length = read_uintle(data, offset + 20, 4)
        self.unknown3 = read_uintle(data, offset + 24, 4)
        self.unknown4 = read_uintle(data, offset + 28, 4)


class Bgp:
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            self.data = memoryview(data)
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
        for pal_entry in iter_bytes(self.data, BGP_PAL_ENTRY_LEN, self.header.palette_begin, pal_end):
            r, g, b, unk = pal_entry
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
        for i, entry in enumerate(iter_bytes(self.data, BGP_TILEMAP_ENTRY_BYTELEN, self.header.tilemap_data_begin, tilemap_end)):
            # NOTE: There will likely be more than 768 (BGP_TOTAL_NUMBER_TILES) tiles. Why is unknown, but the
            #       rest is just zero padding.
            self.tilemap.append(TilemapEntry.from_int(int.from_bytes(entry, 'little')))
        if len(self.tilemap) < BGP_TOTAL_NUMBER_TILES:
            raise ValueError(f"Invalid BGP image: Too few tiles ({len(self.tilemap)}) in tile mapping."
                             f"Must be at least {BGP_TOTAL_NUMBER_TILES}.")

    def _extract_tiles(self):
        self.tiles = []
        tiles_end = self.header.tiles_begin + self.header.tiles_length
        # (8 / BGP_PIXEL_BITLEN) = 8 / 4 = 2
        for tile in iter_bytes(self.data, int(BGP_TILE_DIM * BGP_TILE_DIM / 2), self.header.tiles_begin, tiles_end):
            # NOTE: Again, the number of tiles is probably bigger than BGP_TOTAL_NUMBER_TILES... (zero padding)
            self.tiles.append(bytearray(tile))
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
            self.tilemap[:BGP_TOTAL_NUMBER_TILES], self.tiles, self.palettes, BGP_TILE_DIM, BGP_RES_WIDTH, BGP_RES_HEIGHT, 1, 1, ignore_flip_bits
        )

    def to_pil_tiled(self, ignore_flip_bits=False) -> List[Image.Image]:
        """
        Convert all tiles of the BGP into separate PIL images.
        Each image has one palette with 16 colors.
        If ignore_flip_bits is set, tiles are not flipped.

        768 tiles are returned, for dimension calculating, see the constants of this module.
        """
        return to_pil_tiled(
            self.tilemap[:BGP_TOTAL_NUMBER_TILES], self.tiles, self.palettes, BGP_TILE_DIM, ignore_flip_bits
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
        """
        self.tiles, self.tilemap, self.palettes = from_pil(
            pil, BGP_PAL_NUMBER_COLORS, BGP_MAX_PAL, BGP_TILE_DIM, BGP_RES_WIDTH,
            BGP_RES_HEIGHT, 1, 1, force_import
        )
        # Fill up the tiles and tilemaps to 1024, which seems to be the required default
        for _ in range(len(self.tiles), BGP_TOTAL_NUMBER_TILES_ACTUALLY):
            self.tiles.append(bytearray(int(BGP_TILE_DIM * BGP_TILE_DIM / 2)))
        for _ in range(len(self.tilemap), BGP_TOTAL_NUMBER_TILES_ACTUALLY):
            self.tilemap.append(TilemapEntry.from_int(0))

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
