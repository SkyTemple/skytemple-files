"""Common module for reading and writing tiled indexed rgb 4bpp images"""
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
import logging
import math
import warnings
from itertools import chain
from typing import List, Tuple, Union
from skytemple_files.common.i18n_util import f, _

try:
    from PIL import Image
except ImportError:
    from pil import Image

from skytemple_files.common.util import iter_bytes_4bit_le, iter_bytes

logger = logging.getLogger(__name__)


class TilemapEntry:
    def __init__(self, idx, flip_x, flip_y, pal_idx, ignore_too_large=False):
        self.idx = idx
        if idx > 0x3FF and not ignore_too_large:
            raise ValueError(f(_("Tile Mapping can not be processed. The tile number referenced ({idx}) is bigger "
                                 "than the maximum ({0x3FF}). If you are importing an image, please try to have "
                                 "less unique tiles.")))
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.pal_idx = pal_idx

    def __str__(self):
        return f"{self.idx} - {self.pal_idx} - {self.to_int():>016b} - " \
               f"{'x' if self.flip_x else ''}{'y' if self.flip_y else ''}"

    def __eq__(self, other):
        if isinstance(other, TilemapEntry):
            return self.to_int() == other.to_int()
        return False

    def to_int(self):
        """Converts tile map entry back into the byte format used by game"""
        xf = 1 if self.flip_x else 0
        yf = 1 if self.flip_y else 0
        # '0010000000100101'
        return (self.idx & 0x3FF) + (xf << 10) + (yf << 11) + ((self.pal_idx & 0x3F) << 12)

    @classmethod
    def from_int(cls, entry):
        """Create a tile map entry from the common two byte format used by the game"""
        return cls(
            # 0000 0011 1111 1111, tile index
            idx=entry & 0x3FF,
            # 1111 0000 0000 0000, pal index
            pal_idx=(entry & 0xF000) >> 12,
            # 0000 0100 0000 0000, hflip
            flip_x=(entry & 0x400) > 0,
            # 0000 1000 0000 0000, vflip
            flip_y=(entry & 0x800) > 0
        )


def to_pil(
        tilemap: List[TilemapEntry], tiles: List[bytes], palettes: List[List[int]],
        tile_dim: int,
        img_width: int, img_height: int,
        tiling_width=1, tiling_height=1,
        ignore_flip_bits=False, bpp=4
) -> Image.Image:
    """
    Convert all tiles referenced in tile_mapping to one big PIL image.

    The resulting image has one large palette with all palettes merged together.
    If ignore_flip_bits is set, tiles are not flipped.

    tiling_width/height control how many tiles form a chunk.
    """
    if bpp == 8:
        iter_fn = iter
    elif bpp == 4:
        iter_fn = iter_bytes_4bit_le
    else:
        raise ValueError(_("Only 4bpp and 8bpp images are supported."))
    pil_img_data = bytearray(img_width * img_height)
    img_width_in_tiles = int(img_width / tile_dim)
    number_tiles = len(tilemap)
    number_of_cols_per_pal = int(len(palettes[0]) / 3)

    for i in range(0, number_tiles):
        tiles_in_chunks = tiling_width * tiling_height
        chunk_x = math.floor(math.floor((i / tiles_in_chunks)) % (img_width_in_tiles / tiling_width))
        chunk_y = math.floor(math.floor((i / tiles_in_chunks)) / (img_width_in_tiles / tiling_width))

        tile_x = (chunk_x * tiling_width) + (i % tiling_width)
        tile_y = (chunk_y * tiling_height) + (math.floor(i / tiling_width) % tiling_height)
        tile_mapping = tilemap[i]
        try:
            tile_data = tiles[tile_mapping.idx]
        except IndexError:
            # This happens when exporting a BPCs chunk without "loading" the BPAs, because the BPA tiles
            # take up slots after the BPC slots.
            logger.warning(f'TiledImage: TileMappingEntry {tile_mapping} contains invalid tile reference. '
                           f'Replaced with 0.')
            tile_data = tiles[0]
        # Since our PIL image has one big flat palette, we need to calculate the offset to that
        pal_start_offset = number_of_cols_per_pal * tile_mapping.pal_idx
        for idx, pal in enumerate(iter_fn(tile_data)):
            real_pal = pal_start_offset + pal
            x_in_tile, y_in_tile = _px_pos_flipped(
                idx % tile_dim, math.floor(idx / tile_dim), tile_dim, tile_dim,
                tile_mapping.flip_x and not ignore_flip_bits, tile_mapping.flip_y and not ignore_flip_bits
            )
            real_x = tile_x * tile_dim + x_in_tile
            real_y = tile_y * tile_dim + y_in_tile
            nidx = real_y * img_width + real_x
            #print(f"{i} : {tile_x}x{tile_y} -- {x_in_tile}x{y_in_tile} -> {real_x}x{real_y}={nidx}")
            pil_img_data[nidx] = real_pal
    #assert len(pil_img_data) == dim_w * dim_h * 8

    im = Image.frombuffer('P', (img_width, img_height), pil_img_data, 'raw', 'P', 0, 1)

    im.putpalette(chain.from_iterable(palettes))
    return im


def to_pil_tiled(
        tilemap: List[TilemapEntry], in_tiles: List[bytes], palettes: List[List[int]],
        tile_dim: int,
        ignore_flip_bits=False
) -> List[Image.Image]:
    """
    Convert all tiles of the image into separate PIL images.
    Each image has one palette with 16 colors.
    If ignore_flip_bits is set, tiles are not flipped.
    """
    tiles = []
    number_tiles = len(tilemap)

    for i in range(0, number_tiles):
        pil_img_data = bytearray(tile_dim * tile_dim)
        tile_mapping = tilemap[i]
        tile_data = in_tiles[tile_mapping.idx]
        for idx, pal in enumerate(iter_bytes_4bit_le(tile_data)):
            real_x, real_y = _px_pos_flipped(
                idx % tile_dim, math.floor(idx / tile_dim), tile_dim, tile_dim,
                tile_mapping.flip_x and not ignore_flip_bits, tile_mapping.flip_y and not ignore_flip_bits
            )
            nidx = real_y * tile_dim + real_x
            pil_img_data[nidx] = pal

        im = Image.frombuffer('P', (tile_dim, tile_dim), pil_img_data, 'raw', 'P', 0, 1)
        im.putpalette(palettes[tile_mapping.pal_idx])
        tiles.append(im)

    return tiles


def from_pil(
        pil: Image.Image, single_palette_size: int, max_nb_palettes: int, tile_dim: int,
        img_width: int,  img_height: int,
        tiling_width=1, tiling_height=1, force_import=False, optimize=True, palette_offset=0
) -> Tuple[List[bytearray], List[TilemapEntry], List[List[int]]]:
    """
    Modify the image data in the tiled image by importing the passed PIL.

    The passed tiled image will be split into separate tiles and the tile's palette index
    is determined by the first pixel value of each tile in the PIL. The PIL
    must have a palette containing the 16 sub-palettes with 16 colors each (256 colors).
    The index of the tile stored is determined by the image dimensions and the tiling width and height.

    If a pixel in a tile uses a color outside of it's 16 color range, an error is thrown or
    the color is replaced with 0 of the palette (transparent). This is controlled by
    the force_import flag.

    If optimize is True, we check each read tile, if this tile or a flipped version already exists in the data set,
    if so we re-use the tile.

    palette_offset can be used to offset all color values in the original PIL image by the number of x palettes,
    in the case where palettes were merged.

    Returns (tiles, tile mappings, palettes)
    """
    # All of this has to refactored, like wtf.

    max_len_pal = single_palette_size * max_nb_palettes
    if pil.mode != 'P':
        raise ValueError(_('Can not convert PIL image to PMD tiled image: Must be indexed image (=using a palette)'))
    if pil.palette.mode != 'RGB' \
            or len(pil.palette.palette) > max_len_pal * 3 \
            or len(pil.palette.palette) % single_palette_size * 3 != 0:
        raise ValueError(f(_('Can not convert PIL image to PMD tiled image: '
                             'Palette must contain max {max_len_pal} RGB colors '
                             'and be divisible by {single_palette_size}.')))
    if pil.width != img_width or pil.height != img_height:
        raise ValueError(f(_('Can not convert PIL image to PMD tiled image: '
                             'Image dimensions must be {img_width}x{img_height}px.')))

    # Build new palette
    new_palette = memoryview(pil.palette.palette)
    palettes: List[List[int]] = []
    for i, col in enumerate(new_palette):
        if i % (single_palette_size * 3) == 0:
            cur_palette = []
            palettes.append(cur_palette)
        cur_palette.append(col)

    raw_pil_image = pil.tobytes('raw', 'P')
    number_of_tiles = int(len(raw_pil_image) / tile_dim / tile_dim)

    tiles_with_sum: List[Tuple[int, bytearray]] = [None for __ in range(0, number_of_tiles)]
    tilemap: List[TilemapEntry] = [None for __ in range(0, number_of_tiles)]
    the_two_px_to_write = [0, 0]

    # Set inside the loop:
    tile_palette_indices = [None for __ in range(0, number_of_tiles)]

    already_initialised_tiles = []

    for idx, pix in enumerate(raw_pil_image):
        pix = pix + palette_offset * single_palette_size
        # Only calculate position for first pixel in two pixel pair (it's always the even one)
        if idx % 2 == 0:
            x = idx % img_width
            y = int(idx / img_width)

            # I'm so sorry for this, if someone wants to rewrite this, please go ahead!
            chunk_x = math.floor(x / (tile_dim * tiling_width))
            chunk_y = math.floor(y / (tile_dim * tiling_height))
            tiles_up_to_current_chunk_y = int(img_width / tile_dim * chunk_y * tiling_height)

            tile_x = (chunk_x * tiling_width * tiling_height) + (math.floor(x / tile_dim) - (chunk_x * tiling_width))
            tile_y = (chunk_y * tiling_height) + (math.floor(y / tile_dim) - (chunk_y * tiling_height))
            tile_id = tiles_up_to_current_chunk_y + ((tile_y - tiling_height * chunk_y) * tiling_width) + tile_x

            in_tile_x = x - tile_dim * math.floor(x / tile_dim)
            in_tile_y = y - tile_dim * math.floor(y / tile_dim)
            idx_in_tile = in_tile_y * tile_dim + in_tile_x

            nidx = int(idx_in_tile / 2)
            #print(f"{idx}@{x}x{y}: {tile_id} : [chunk {chunk_x}x{chunk_y}] "
            #      f"{tile_x}x{tile_y} -- {idx_in_tile} : {in_tile_x}x{in_tile_y} = {nidx}")

            if tile_id not in already_initialised_tiles:
                already_initialised_tiles.append(tile_id)
                # Begin a new tile
                tiles_with_sum[tile_id] = [0, bytearray(int(tile_dim * tile_dim / 2))]
                # Get the palette index from the first pixel
                tile_palette_indices[tile_id] = math.floor(pix / single_palette_size)

        # The "real" value is the value of the color in the currently used palette of the tile
        real_pix = pix - (tile_palette_indices[tile_id] * single_palette_size)
        if real_pix > (single_palette_size - 1) or real_pix < 0:
            # The color is out of range!
            if not force_import:
                raise ValueError(f(_("Can not convert PIL image to PMD tiled image: "
                                     "The color {pix} (from palette {math.floor(pix / single_palette_size)}) used by "
                                     "pixel {x+(idx % 2)}x{y} in tile {tile_id} ({tile_x}x{tile_y} is out of range. "
                                     "Expected are colors from palette {tile_palette_indices[tile_id]} ("
                                     "{tile_palette_indices[tile_id] * single_palette_size} - "
                                     "{(tile_palette_indices[tile_id]+1) * single_palette_size - 1}).")))
            # Just set the color to 0 instead if invalid...
            else:
                logger.warning(f(_("Can not convert PIL image to PMD tiled image: "
                                   "The color {pix} (from palette {math.floor(pix / single_palette_size)}) used by "
                                   "pixel {x+(idx % 2)}x{y} in tile {tile_id} ({tile_x}x{tile_y} is out of range. "
                                   "Expected are colors from palette {tile_palette_indices[tile_id]} ("
                                   "{tile_palette_indices[tile_id] * single_palette_size} - "
                                   "{(tile_palette_indices[tile_id]+1) * single_palette_size - 1}).")))
            real_pix = 0

        # We store 2 bytes as one... in LE
        the_two_px_to_write[idx % 2] = real_pix

        # Only store when we are on the second pixel
        if idx % 2 == 1:
            # Little endian:
            tiles_with_sum[tile_id][0] += (the_two_px_to_write[0] + the_two_px_to_write[1])
            tiles_with_sum[tile_id][1][nidx] = the_two_px_to_write[0] + (the_two_px_to_write[1] << 4)

    final_tiles_with_sum: List[Tuple[int, bytearray]] = []
    len_final_tiles = 0
    # Create tilemap and optimize tiles list
    for tile_id, tile_with_sum in enumerate(tiles_with_sum):
        reusable_tile_idx = None
        flip_x = False
        flip_y = False
        if optimize:
            reusable_tile_idx, flip_x, flip_y = search_for_tile_with_sum(final_tiles_with_sum, tile_with_sum, tile_dim)
        if reusable_tile_idx is not None:
            tile_id_to_use = reusable_tile_idx
        else:
            final_tiles_with_sum.append(tile_with_sum)
            tile_id_to_use = len_final_tiles
            len_final_tiles += 1
        tilemap[tile_id] = TilemapEntry(
            idx=tile_id_to_use,
            pal_idx=tile_palette_indices[tile_id],
            flip_x=flip_x,
            flip_y=flip_y,
            ignore_too_large=True
        )
    if len_final_tiles > 1024:
        raise ValueError(f(_("An image selected to import is too complex. It has too many unique tiles "
                             "({len_final_tiles}, max allowed are 1024).\nTry to have less unique tiles. Unique tiles "
                             "are 8x8 sections of the images that can't be found anywhere else in the image (including "
                             "flipped or with a different sub-palette).")))
    final_tiles: List[bytearray] = []
    for s, tile in final_tiles_with_sum:
        final_tiles.append(tile)
    return final_tiles, tilemap, palettes


def search_for_chunk(chunk, tile_mappings):
    """
    In the provided list of tile mappings, find an existing chunk.
    Returns the position of the first tile of the chunk or None if not found.
    The chunk dimensions are derived from the passed chunk.
    """
    tiles_in_chunk = len(chunk)
    for chk_fst_tile_idx in range(0, len(tile_mappings), tiles_in_chunk):
        if chunk == tile_mappings[chk_fst_tile_idx:chk_fst_tile_idx+tiles_in_chunk]:
            return chk_fst_tile_idx
    return None


def search_for_tile_with_sum(tiles_with_sum: List[Tuple[int, bytearray]], tile_with_sum: Tuple[int, bytearray], tile_dim) -> Tuple[Union[int, None], bool, bool]:
    """
    Search for the tile, or a flipped version of it, in tiles and return the index and flipped state
    Increases performance by comparing the bytes sum of each tile before actually compare them
    """
    s = tile_with_sum[0]
    tile = tile_with_sum[1]
    for i, tile_tuple in enumerate(tiles_with_sum):
        sum_tile = tile_tuple[0]
        if sum_tile==s:
            tile_in_tiles = tile_tuple[1]
            if tile_in_tiles == tile:
                return i, False, False
            x_flipped = _flip_tile_x(tile_in_tiles, tile_dim)
            if x_flipped == tile:
                return i, True, False
            if _flip_tile_y(tile_in_tiles, tile_dim) == tile:
                return i, False, True
            if _flip_tile_y(x_flipped, tile_dim) == tile:
                return i, True, True
    return None, False, False

def search_for_tile(tiles, tile, tile_dim) -> Tuple[Union[int, None], bool, bool]:
    """
    Search for the tile, or a flipped version of it, in tiles and return the index and flipped state
    """
    for i, tile_in_tiles in enumerate(tiles):
        if tile_in_tiles == tile:
            return i, False, False
        x_flipped = _flip_tile_x(tile_in_tiles, tile_dim)
        if x_flipped == tile:
            return i, True, False
        if _flip_tile_y(tile_in_tiles, tile_dim) == tile:
            return i, False, True
        if _flip_tile_y(x_flipped, tile_dim) == tile:
            return i, True, True
    return None, False, False


def _flip_tile_x(tile: bytes, tile_dim):
    """Flip all pixels in tile on the x-axis"""
    tile_flipped = bytearray(len(tile))
    for i, b in enumerate(tile):
        row_idx = (i * 2) % tile_dim
        col_idx = math.floor((i * 2) / tile_dim)
        tile_flipped[int((col_idx * tile_dim + (tile_dim - 1 - row_idx)) / 2)] = ((b & 0x0F) << 4 | (b & 0xF0) >> 4)
    return tile_flipped


def _flip_tile_y(tile: bytes, tile_dim):
    """Flip all pixels in tile on the y-axis"""
    tile_flipped = bytearray(len(tile))
    for i, b in enumerate(tile):
        row_idx = (i * 2) % tile_dim
        col_idx = math.floor((i * 2) / tile_dim)
        tile_flipped[int(((tile_dim - 1 - col_idx) * tile_dim + row_idx) / 2)] = b
    return tile_flipped


def _px_pos_flipped(x, y, w, h, flip_x, flip_y) -> Tuple[int, int]:
    """
    Returns the flipped x and y position for a pixel in a fixed size image.
    If x and/or y actually get flipped is controled by the flip_ params.
    """
    new_x = w - x - 1 if flip_x else x
    new_y = h - y - 1 if flip_y else y
    return new_x, new_y

