"""Common module for reading and writing tiled indexed rgb 4bpp images"""
import math
import warnings
from itertools import chain
from typing import List, Tuple

from PIL import Image
from bitstring import BitStream


class TilemapEntry:
    def __init__(self, idx, flip_x, flip_y, pal_idx, dbg=0):
        self.idx = idx
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.pal_idx = pal_idx
        self.dbg = dbg

    def __str__(self):
        return f"{self.idx} - {self.pal_idx} - {self.dbg:>016b} - " \
               f"{'x' if self.flip_x else ''}{'y' if self.flip_y else ''}"

    @classmethod
    def from_bytes(cls, entry):
        """Create a tile map entry from the common two byte format used by the game"""
        return cls(
            # 0000 0011 1111 1111, tile index
            idx=entry & 0x3FF,
            # 1111 0000 0000 0000, pal index
            pal_idx=(entry & 0xF000) >> 12,
            # 0000 0100 0000 0000, hflip
            flip_x=(entry & 0x400) > 0,
            # 0000 1000 0000 0000, vflip
            flip_y=(entry & 0x800) > 0,
            dbg=entry
        )


def to_pil(
        tilemap: List[TilemapEntry], tiles: List[BitStream], palettes: List[List[int]],
        tile_dim: int,
        img_width: int, img_height: int,
        tiling_width=1, tiling_height=1,
        ignore_flip_bits=False
) -> Image.Image:
    """
    Convert all tiles referenced in tile_mapping to one big PIL image.

    The resulting image has one large palette with all palettes merged together.
    If ignore_flip_bits is set, tiles are not flipped.

    tiling_width/height control how many tiles form a meta-tile.
    """
    pil_img_data = BitStream(img_width * img_height * 8)
    img_width_in_tiles = int(img_width / tile_dim)
    number_tiles = len(tilemap)
    number_of_cols_per_pal = int(len(palettes[0]) / 3)

    for i in range(0, number_tiles):
        tiles_in_meta = tiling_width * tiling_height
        meta_x = math.floor(math.floor((i / tiles_in_meta)) % (img_width_in_tiles / tiling_width))
        meta_y = math.floor(math.floor((i / tiles_in_meta)) / (img_width_in_tiles / tiling_width))

        tile_x = (meta_x * tiling_width) + (i % tiling_width)
        tile_y = (meta_y * tiling_height) + (math.floor(i / tiling_width) % tiling_height)
        tile_mapping = tilemap[i]
        try:
            tile_data = tiles[tile_mapping.idx]
        except IndexError:
            # This happens when exporting a BPCs meta tiles without "loading" the BPAs, because the BPA tiles
            # take up slots after the BPC slots.
            warnings.warn(f'TiledImage: TileMappingEntry {tile_mapping} contains invalid tile reference. '
                          f'Replaced with 0.')
            tile_data = tiles[0]
        # Since our PIL image has one big flat palette, we need to calculate the offset to that
        pal_start_offset = number_of_cols_per_pal * tile_mapping.pal_idx
        for idx, pal in enumerate(tile_data.cut(4)):
            # Little Endian
            if idx % 2 == 0:
                idx += 1
            else:
                idx -= 1
            real_pal = pal_start_offset + pal.uint
            x_in_tile, y_in_tile = _px_pos_flipped(
                idx % tile_dim, math.floor(idx / tile_dim), tile_dim, tile_dim,
                tile_mapping.flip_x and not ignore_flip_bits, tile_mapping.flip_y and not ignore_flip_bits
            )
            real_x = tile_x * tile_dim + x_in_tile
            real_y = tile_y * tile_dim + y_in_tile
            nidx = real_y * img_width + real_x
            #print(f"{i} : {tile_x}x{tile_y} -- {x_in_tile}x{y_in_tile} -> {real_x}x{real_y}={nidx}")
            pil_img_data[nidx*8:nidx*8+8] = real_pal
    #assert len(pil_img_data) == dim_w * dim_h * 8

    im = Image.frombuffer('P', (img_width, img_height), pil_img_data.bytes, 'raw', 'P', 0, 1)

    im.putpalette(chain.from_iterable(palettes))
    return im


def to_pil_tiled(
        tilemap: List[TilemapEntry], in_tiles: List[BitStream], palettes: List[List[int]],
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
        pil_img_data = BitStream(tile_dim * tile_dim * 8)
        tile_mapping = tilemap[i]
        tile_data = in_tiles[tile_mapping.idx]
        for idx, pal in enumerate(tile_data.cut(4)):
            # Little Endian
            if idx % 2 == 0:
                idx += 1
            else:
                idx -= 1
            real_x, real_y = _px_pos_flipped(
                idx % tile_dim, math.floor(idx / tile_dim), tile_dim, tile_dim,
                tile_mapping.flip_x and not ignore_flip_bits, tile_mapping.flip_y and not ignore_flip_bits
            )
            nidx = real_y * tile_dim + real_x
            pil_img_data[nidx*8:nidx*8+8] = pal.uint

        im = Image.frombuffer('P', (tile_dim, tile_dim), pil_img_data.bytes, 'raw', 'P', 0, 1)
        im.putpalette(palettes[tile_mapping.pal_idx])
        tiles.append(im)

    return tiles


def _px_pos_flipped(x, y, w, h, flip_x, flip_y) -> Tuple[int, int]:
    """
    Returns the flipped x and y position for a pixel in a fixed size image.
    If x and/or y actually get flipped is controled by the flip_ params.
    """
    new_x = w - x - 1 if flip_x else x
    new_y = h - y - 1 if flip_y else y
    return new_x, new_y

