"""Common module for reading and writing tiled indexed rgb 4bpp images"""
import math
import warnings
from itertools import chain
from typing import List, Tuple

from PIL import Image

from skytemple_files.common.util import iter_bytes_4bit_le


class TilemapEntry:
    def __init__(self, idx, flip_x, flip_y, pal_idx):
        self.idx = idx
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.pal_idx = pal_idx

    def __str__(self):
        return f"{self.idx} - {self.pal_idx} - {self.to_int():>016b} - " \
               f"{'x' if self.flip_x else ''}{'y' if self.flip_y else ''}"

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
        ignore_flip_bits=False
) -> Image.Image:
    """
    Convert all tiles referenced in tile_mapping to one big PIL image.

    The resulting image has one large palette with all palettes merged together.
    If ignore_flip_bits is set, tiles are not flipped.

    tiling_width/height control how many tiles form a chunk.
    """
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
            warnings.warn(f'TiledImage: TileMappingEntry {tile_mapping} contains invalid tile reference. '
                          f'Replaced with 0.')
            tile_data = tiles[0]
        # Since our PIL image has one big flat palette, we need to calculate the offset to that
        pal_start_offset = number_of_cols_per_pal * tile_mapping.pal_idx
        for idx, pal in enumerate(iter_bytes_4bit_le(tile_data)):
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
        tiling_width=1, tiling_height=1, force_import=False
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

    Currently all tiles are imported as-is, without checking if the same or a flipped
    version of a tile already exists. So basically no "compression" in image size is done
    by re-using tiles.

    Returns (tiles, tile mappings, palettes)
    """
    # All of this has to refactored, like wtf.

    max_len_pal = single_palette_size * max_nb_palettes
    if pil.mode != 'P':
        raise ValueError('Can not convert PIL image to PMD tiled image: Must be indexed image (=using a palette)')
    if pil.palette.mode != 'RGB' \
            or len(pil.palette.palette) > max_len_pal * 3 \
            or len(pil.palette.palette) % single_palette_size * 3 != 0:
        raise ValueError(f'Can not convert PIL image to PMD tiled image: '
                         f'Palette must contain max {max_len_pal} RGB colors '
                         f'and be divisible by {single_palette_size}.')
    if pil.width != img_width or pil.height != img_height:
        raise ValueError(f'Can not convert PIL image to PMD tiled image: '
                         f'Image dimensions must be {img_width}x{img_height}px.')

    # Build new palette
    new_palette = memoryview(pil.palette.palette)
    palettes: List[List[int]] = []
    for i, col in enumerate(new_palette):
        if i % (single_palette_size * 3) == 0:
            cur_palette = []
            palettes.append(cur_palette)
        cur_palette.append(col)

    raw_pil_image = pil.tobytes('raw', 'P')
    single_tile_pixel_size = tile_dim * tile_dim
    number_of_tiles = int(len(raw_pil_image) / tile_dim / tile_dim)

    tiles: List[bytearray] = [None for _ in range(0, number_of_tiles)]
    tilemap: List[TilemapEntry] = [None for _ in range(0, number_of_tiles)]
    the_two_px_to_write = [0, 0]

    # Set inside the loop:
    tile_palette_indices = [None for _ in range(0, number_of_tiles)]

    already_initialised_tiles = []

    # TODO: Doesn't actually take tiling_width and tiling_height into account right now, I already
    #       have enough headaches for now
    for idx, pix in enumerate(raw_pil_image):
        # Only calculate position for first pixel in two pixel pair (it's always the even one)
        if idx % 2 == 0:
            x =idx % img_width
            y = int(idx / img_width)

            tile_x = math.floor(x / tile_dim)
            tile_y = math.floor(y / tile_dim)
            tile_id = tile_y * int(img_width / tile_dim) + tile_x

            in_tile_x = x - tile_dim * tile_x
            in_tile_y = y - tile_dim * tile_y
            idx_in_tile = in_tile_y * tile_dim + in_tile_x

            nidx = int(idx_in_tile/ 2)
            #print(f"{idx}@{x}x{y}: {tile_id} : {tile_x}x{tile_y} -- {idx_in_tile} : {in_tile_x}x{in_tile_y} = {nidx}")

            if tile_id not in already_initialised_tiles:
                already_initialised_tiles.append(tile_id)
                # Begin a new tile and tile mapping
                # Get the palette index from the first pixel
                current_tile_palette_index = math.floor(pix / single_palette_size)
                tiles[tile_id] = bytearray(int(tile_dim * tile_dim / 2))
                tile_palette_indices[tile_id] = current_tile_palette_index
                tilemap[tile_id] = TilemapEntry(
                    idx=tile_id,
                    pal_idx=current_tile_palette_index,
                    flip_x=False,
                    flip_y=False
                )

        # The "real" value is the value of the color in the currently used palette of the tile
        real_pix = pix - (tile_palette_indices[tile_id] * single_palette_size)
        if real_pix > single_palette_size or real_pix < 0:
            # The color is out of range!
            if not force_import:
                raise ValueError(f"an not convert PIL image to PMD tiled image: "
                                 f"The color ({pix}, from palette {math.floor(pix / single_palette_size)}) used by "
                                 f"pixel {x+idx % 2}x{y} in tile {tile_id} ({tile_x}x{tile_y} is out of range. "
                                 f"Expected are colors from palette {tile_palette_indices[tile_id]} ("
                                 f"{tile_palette_indices[tile_id] * single_palette_size} - "
                                 f"{(tile_palette_indices[tile_id]+1) * single_palette_size - 1}).")
            # Just set the color to 0 instead if invalid...
            real_pix = 0

        # We store 2 bytes as one... in LE
        the_two_px_to_write[idx % 2] = real_pix

        # Only store when we are on the second pixel
        if idx % 2 == 1:
            # Little endian:
            tiles[tile_id][nidx] = the_two_px_to_write[0] + (the_two_px_to_write[1] << 4)

    return tiles, tilemap, palettes


def _px_pos_flipped(x, y, w, h, flip_x, flip_y) -> Tuple[int, int]:
    """
    Returns the flipped x and y position for a pixel in a fixed size image.
    If x and/or y actually get flipped is controled by the flip_ params.
    """
    new_x = w - x - 1 if flip_x else x
    new_y = h - y - 1 if flip_y else y
    return new_x, new_y

