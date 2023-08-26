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

from typing import List

from PIL import Image
from range_typed_integers import u32, u16

from skytemple_files.common.protocol import TilemapEntryProtocol
from skytemple_files.common.tiled_image import (
    TilemapEntry,
    from_pil,
    to_pil,
    to_pil_tiled,
)
from skytemple_files.common.util import iter_bytes, read_u32
from skytemple_files.graphics.bgp import (
    BGP_RES_WIDTH,
    BGP_RES_HEIGHT,
    BGP_HEADER_LENGTH,
    BGP_PAL_ENTRY_LEN,
    BGP_PAL_NUMBER_COLORS,
    BGP_MAX_PAL,
    BGP_TILEMAP_ENTRY_BYTELEN,
    BGP_TILE_DIM,
    BGP_TOTAL_NUMBER_TILES,
    BGP_TOTAL_NUMBER_TILES_ACTUALLY,
)


from skytemple_files.graphics.bgp.protocol import BgpProtocol


class BgpHeader:
    """Header for a Bgp Image"""

    palette_begin: u32
    palette_length: u32
    tiles_begin: u32
    tiles_length: u32
    tilemap_data_begin: u32
    tilemap_data_length: u32
    unknown3: u32
    unknown4: u32

    def __init__(self, data: bytes, offset=0):
        # WARNING: The pointers and lengths are not updated after creation. The writer re-generates them.
        self.palette_begin = read_u32(data, offset)
        if self.palette_begin != BGP_HEADER_LENGTH:
            raise ValueError("Invalid BGP image: Palette pointer too low.")
        self.palette_length = read_u32(data, offset + 4)
        self.tiles_begin = read_u32(data, offset + 8)
        self.tiles_length = read_u32(data, offset + 12)
        self.tilemap_data_begin = read_u32(data, offset + 16)
        self.tilemap_data_length = read_u32(data, offset + 20)
        self.unknown3 = read_u32(data, offset + 24)
        self.unknown4 = read_u32(data, offset + 28)


class Bgp(BgpProtocol):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            self.data = memoryview(data)
        else:
            self.data = data
        self.header = BgpHeader(self.data)

        self.palettes: List[List[int]] = []
        self.tiles: List[bytearray] = []
        self.tilemap: List[TilemapEntryProtocol] = []

        self._extract_palette()
        self._extract_tilemap()
        self._extract_tiles()

    def _extract_palette(self):
        if self.header.palette_length % 16 != 0:
            raise ValueError("Invalid BGP image: Palette must be dividable by 16")
        pal_end = self.header.palette_begin + self.header.palette_length
        self.palettes = []
        current_palette = []
        colors_read_for_current_palette = 0
        for pal_entry in iter_bytes(
            self.data, BGP_PAL_ENTRY_LEN, self.header.palette_begin, pal_end
        ):
            r, g, b, unk = pal_entry
            current_palette.append(r)
            current_palette.append(g)
            current_palette.append(b)
            colors_read_for_current_palette += 1
            if colors_read_for_current_palette >= 16:
                self.palettes.append(current_palette)
                current_palette = []
                colors_read_for_current_palette = 0

    def _extract_tilemap(self):
        tilemap_end = self.header.tilemap_data_begin + self.header.tilemap_data_length
        self.tilemap = []
        for i, entry in enumerate(
            iter_bytes(
                self.data,
                BGP_TILEMAP_ENTRY_BYTELEN,
                self.header.tilemap_data_begin,
                tilemap_end,
            )
        ):
            # NOTE: There will likely be more than 768 (BGP_TOTAL_NUMBER_TILES) tiles. Why is unknown, but the
            #       rest is just zero padding.
            self.tilemap.append(
                TilemapEntry.from_int(u16(int.from_bytes(entry, "little")))
            )
        if len(self.tilemap) < BGP_TOTAL_NUMBER_TILES:
            raise ValueError(
                f"Invalid BGP image: Too few tiles ({len(self.tilemap)}) in tile mapping."
                f"Must be at least {BGP_TOTAL_NUMBER_TILES}."
            )

    def _extract_tiles(self):
        self.tiles = []
        tiles_end = self.header.tiles_begin + self.header.tiles_length
        # (8 / BGP_PIXEL_BITLEN) = 8 / 4 = 2
        for tile in iter_bytes(
            self.data,
            int(BGP_TILE_DIM * BGP_TILE_DIM / 2),
            self.header.tiles_begin,
            tiles_end,
        ):
            # NOTE: Again, the number of tiles is probably bigger than BGP_TOTAL_NUMBER_TILES... (zero padding)
            self.tiles.append(bytearray(tile))
        if len(self.tiles) < BGP_TOTAL_NUMBER_TILES:
            raise ValueError(
                f"Invalid BGP image: Too few tiles ({len(self.tiles)}) in tile data."
                f"Must be at least {BGP_TOTAL_NUMBER_TILES}."
            )

    def to_pil(self, ignore_flip_bits=False) -> Image.Image:
        """
        Convert all tiles of the BGP to one big PIL image.
        The resulting image has one large palette with 256 colors.
        If ignore_flip_bits is set, tiles are not flipped.

        The image returned will have the size 256x192.
        For dimension calculating, see the constants of this module.
        """
        return to_pil(
            self.tilemap[:BGP_TOTAL_NUMBER_TILES],
            self.tiles,
            self.palettes,
            BGP_TILE_DIM,
            BGP_RES_WIDTH,
            BGP_RES_HEIGHT,
            1,
            1,
            ignore_flip_bits,
        )

    def to_pil_tiled(self, ignore_flip_bits=False) -> List[Image.Image]:
        """
        Convert all tiles of the BGP into separate PIL images.
        Each image has one palette with 16 colors.
        If ignore_flip_bits is set, tiles are not flipped.

        768 tiles are returned, for dimension calculating, see the constants of this module.
        """
        return to_pil_tiled(
            self.tilemap[:BGP_TOTAL_NUMBER_TILES],
            self.tiles,
            self.palettes,
            BGP_TILE_DIM,
            ignore_flip_bits,
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
            pil,
            BGP_PAL_NUMBER_COLORS,
            BGP_MAX_PAL,
            BGP_TILE_DIM,
            BGP_RES_WIDTH,
            BGP_RES_HEIGHT,
            1,
            1,
            force_import,
        )

        if len(self.tiles) == 0x3FF:
            raise AttributeError(f"Error when importing: max tile count reached.")

        # Add the 0 tile (used to clear bgs)
        self.tiles.insert(0, bytearray(int(BGP_TILE_DIM * BGP_TILE_DIM / 2)))
        # Shift tile indices by 1
        for x in self.tilemap:
            x.idx += 1

        # Fill up the tiles and tilemaps to 1024, which seems to be the required default
        for _ in range(len(self.tiles), BGP_TOTAL_NUMBER_TILES_ACTUALLY):
            self.tiles.append(bytearray(int(BGP_TILE_DIM * BGP_TILE_DIM / 2)))
        for _ in range(len(self.tilemap), BGP_TOTAL_NUMBER_TILES_ACTUALLY):
            self.tilemap.append(TilemapEntry.from_int(u16(0)))
