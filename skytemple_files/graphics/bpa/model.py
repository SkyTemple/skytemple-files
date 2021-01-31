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
from typing import Optional

try:
    from PIL import Image
except ImportError:
    from pil import Image

from skytemple_files.common.tiled_image import to_pil, TilemapEntry, from_pil
from skytemple_files.common.util import *
from skytemple_files.graphics.bpl.model import BPL_IMG_PAL_LEN, BPL_MAX_PAL
from skytemple_files.common.i18n_util import f, _

BPA_PIXEL_BITLEN = 4
BPA_TILE_DIM = 8


class BpaFrameInfo:
    def __init__(self, duration_per_frame, unk2):
        # speed?
        self.duration_per_frame = duration_per_frame
        # always 0?
        self.unk2 = unk2
        assert self.unk2 == 0

    def __str__(self):
        return f"BpaFrameInfo({self.duration_per_frame}, {self.unk2})"


class Bpa:
    def __init__(self, data: Optional[bytes]):
        self.number_of_tiles = 0
        self.number_of_frames = 0
        self.tiles = []
        self.frame_info = []
        if data is None:
            return

        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.number_of_tiles = read_uintle(data, 0, 2)
        self.number_of_frames = read_uintle(data, 2, 2)

        # Read image header
        for i in range(0, self.number_of_frames):
            self.frame_info.append(BpaFrameInfo(
                read_uintle(data, 4 + i*4, 2),
                read_uintle(data, 4 + i*4 + 2, 2),
            ))
        end_header = 4 + self.number_of_frames * 4

        self.tiles = []
        slice_size = int(BPA_TILE_DIM * BPA_TILE_DIM / 2)
        for i, tile in enumerate(iter_bytes(data, slice_size, end_header, end_header + (slice_size * self.number_of_frames * self.number_of_tiles))):
            self.tiles.append(bytearray(tile))

    def __str__(self):
        return f"Idx: {self.number_of_tiles}, " \
               f"#c: {self.number_of_frames}"

    def get_tile(self, tile_idx, frame_idx) -> bytes:
        """Returns the tile data of tile no. tile_idx for frame frame_idx."""
        return self.tiles[frame_idx * self.number_of_tiles + tile_idx]

    def tiles_to_pil(self, palette: List[int]) -> Image.Image:
        """
        Exports the BPA as an image, where each row of 8x8 tiles is the
        animation set for a single tile. The 16 color palette passed is used to color the image.
        """
        dummy_tile_map = []
        width_in_tiles = self.number_of_frames
        etr = self.number_of_frames * self.number_of_tiles

        # create a dummy tile map containing all the tiles
        # The tiles in the BPA are stored so, that each tile of the each frame is next
        # to each other. So the second frame of the first tile is at self.number_of_images + 1.
        for tile_idx in range(0, self.number_of_tiles):
            for frame_idx in range(0, self.number_of_frames):
                dummy_tile_map.append(TilemapEntry(
                    idx=frame_idx * self.number_of_tiles + tile_idx,
                    pal_idx=0,
                    flip_x=False,
                    flip_y=False,
                    ignore_too_large=True
                ))
        width = width_in_tiles * BPA_TILE_DIM
        height = math.ceil(etr / width_in_tiles) * BPA_TILE_DIM

        return to_pil(
            dummy_tile_map, self.tiles, [palette], BPA_TILE_DIM, width, height
        )

    def tiles_to_pil_separate(self, palette, width_in_tiles=20) -> List[Image.Image]:
        """
        Exports the BPA as an image, where each row of 8x8 tiles is the
        animation set for a single tile. The 16 color palette passed is used to color the image.
        """
        dummy_tile_map = []

        # create a dummy tile map containing all the tiles
        for tile_idx in range(0, self.number_of_tiles * self.number_of_frames):
            dummy_tile_map.append(TilemapEntry(
                idx=tile_idx,
                pal_idx=0,
                flip_x=False,
                flip_y=False,
                ignore_too_large=True
            ))
        width = width_in_tiles * BPA_TILE_DIM
        height = math.ceil(self.number_of_tiles / width_in_tiles) * BPA_TILE_DIM

        images = []
        for frame_start in range(0, self.number_of_tiles * self.number_of_frames, self.number_of_tiles):
            images.append(to_pil(
                dummy_tile_map[frame_start:frame_start+self.number_of_tiles], self.tiles, [palette], BPA_TILE_DIM, width, height
            ))
        return images

    def pil_to_tiles(self, image: Image.Image):
        """
        Converts a PIL image back to the BPA.
        The format is expected to be the same as tiles_to_pil. This means, that
        each rows of tiles is one image set and each column is one frame.
        """
        tiles, _, __ = from_pil(
            image, BPL_IMG_PAL_LEN, BPL_MAX_PAL, BPA_TILE_DIM,
            image.width, image.height, optimize=False
        )
        self.tiles = []
        self.number_of_frames = int(image.width / BPA_TILE_DIM)
        self.number_of_tiles = int(image.height / BPA_TILE_DIM)

        # We need to re-order the tiles to actually save them
        for frame_idx in range(0, self.number_of_frames):
            for tile_idx in range(0, self.number_of_tiles):
                self.tiles.append(tiles[tile_idx * self.number_of_frames + frame_idx])

        self._correct_frame_info()

    def pil_to_tiles_separate(self, images: List[Image.Image]):
        frames = []
        first_image_dims = None
        for image in images:
            frames.append(from_pil(
                image, BPL_IMG_PAL_LEN, BPL_MAX_PAL, BPA_TILE_DIM,
                image.width, image.height, optimize=False
            )[0])
            if first_image_dims is None:
                first_image_dims = (image.width, image.height)
            if (image.width, image.height) != first_image_dims:
                raise ValueError(_("The dimensions of all images must be the same."))
        self.tiles = []
        self.number_of_frames = len(frames)
        self.number_of_tiles = int((images[0].height * images[0].width) / (BPA_TILE_DIM * BPA_TILE_DIM))

        for tile in frames:
            self.tiles += tile

        self._correct_frame_info()

    def _correct_frame_info(self):
        # Correct frame info size
        len_finfo = len(self.frame_info)
        if len_finfo > self.number_of_frames:
            self.frame_info = self.frame_info[:self.number_of_frames]
        elif len_finfo < self.number_of_frames:
            for i in range(len_finfo, self.number_of_frames):
                # If the length is shorter, we just copy the last entry
                if len(self.frame_info) > 0:
                    self.frame_info.append(self.frame_info[len_finfo-1])
                else:
                    # ... or we default to 10.
                    self.frame_info.append(BpaFrameInfo(10, 0))

    def tiles_for_frame(self, frame):
        """Returns the tiles for the specified frame. Strips the empty dummy tile image at the beginning."""
        return self.tiles[frame * self.number_of_tiles:]
