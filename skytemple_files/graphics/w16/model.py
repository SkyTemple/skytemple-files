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
import itertools
from abc import ABC, abstractmethod
from itertools import zip_longest

try:
    from PIL import Image
except ImportError:
    from pil import Image

from skytemple_files.common.tiled_image import to_pil, TilemapEntry, from_pil
from skytemple_files.common.util import *
TOC_ENTRY_LEN = 4 + 4
NUM_CHANNELS = 3
NUM_COLORS_IN_PAL = 16
# Tiling settings:
TILE_DIM = 8


class W16Image(ABC):
    def __init__(self, entry_data: 'W16TocEntry', compressed_img_data: bytes, pal: List[int]):
        self.entry_data = entry_data
        self.compressed_img_data = compressed_img_data
        self.pal = pal

    @classmethod
    @abstractmethod
    def compress(cls, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decompress(self) -> bytes:
        pass

    def get(self) -> Image.Image:
        decompressed_data = self.decompress()
        w = TILE_DIM * self.entry_data.width
        h = TILE_DIM * self.entry_data.height

        # Create a virtual tilemap
        tilemap = []
        for i in range(int((w * h) / (TILE_DIM * TILE_DIM))):
            tilemap.append(TilemapEntry(
                idx=i,
                pal_idx=0,
                flip_x=False,
                flip_y=False
            ))

        return to_pil(
            tilemap, list(grouper(int(TILE_DIM * TILE_DIM / 2), decompressed_data)),
            [self.pal], TILE_DIM, w, h
        )

    def set(self, pil: Image.Image) -> 'W16Image':
        """Sets the w16 image using a PIL image with 16-bit color palette as input"""
        self.entry_data.width = int(pil.width / TILE_DIM)
        self.entry_data.height = int(pil.height / TILE_DIM)
        new_pal, new_img = self._read_in(pil, self.entry_data.width, self.entry_data.height)
        self.pal = new_pal
        self.compressed_img_data = self.compress(new_img)
        return self

    @classmethod
    def new(cls, entry_data: 'W16TocEntry', pil: Image) -> 'W16Image':
        """Creates a new W16Image from a PIL image with 16-bit color palette as input"""
        entry_data.width = int(pil.width / TILE_DIM)
        entry_data.height = int(pil.height / TILE_DIM)
        new_pal, new_img = cls._read_in(pil, entry_data.width, entry_data.height)
        return cls(entry_data, cls.compress(new_img), new_pal)

    @classmethod
    def _read_in(cls, pil: Image, w_in_tiles, h_in_tiles) -> Tuple[List[int], bytes]:
        w = TILE_DIM * w_in_tiles
        h = TILE_DIM * h_in_tiles
        tiles, tile_mappings, pal = from_pil(
            pil, 16, 1, TILE_DIM,
            w, h, 1, 1,
            force_import=True, optimize=False
        )
        # todo: in theory the tiles could be out of order and we would need to check using the mappings,
        #       in practice they aren't.
        tiles_concat = bytes(itertools.chain.from_iterable(tiles))
        return pal[0], tiles_concat

class W16AtImage(W16Image):
    @classmethod
    def compress(cls, data: bytes) -> bytes:
        from skytemple_files.common.types.file_types import FileType
        return FileType.COMMON_AT.serialize(FileType.COMMON_AT.compress(data))

    def decompress(self) -> bytes:
        from skytemple_files.common.types.file_types import FileType
        return FileType.COMMON_AT.deserialize(self.compressed_img_data).decompress()

class W16RawImage(W16Image):
    @classmethod
    def compress(cls, data: bytes) -> bytes:
        return data

    def decompress(self) -> bytes:
        return self.compressed_img_data


class W16TocEntry:
    def __init__(self, width, height, index, null):
        self.width = width
        self.height = height
        self.index = index
        self.null = null


class W16:
    def __init__(self, data: bytes):
        from skytemple_files.common.types.file_types import FileType
        if not isinstance(data, memoryview):
            data = memoryview(data)

        self._files = []
        len_pal_bytes = int(NUM_CHANNELS * NUM_COLORS_IN_PAL)
        i = 0
        while True:
            # Read TOC entry
            pointer = read_uintle(data, i * 8, 4)
            if pointer == len(data):
                break
            unk1 = read_uintle(data, i * 8 + 4)
            unk2 = read_uintle(data, i * 8 + 5)
            index = read_uintle(data, i * 8 + 6)
            null = read_uintle(data, i * 8 + 7)
            assert null == 0
            entry_data = W16TocEntry(unk1, unk2, index, null)
            # Read palette
            pal = self._read_pal(data[pointer:pointer + len_pal_bytes])
            # Read image
            next_pointer = read_uintle(data, (i+1) * 8, 4)
            img_data = data[pointer + len_pal_bytes:next_pointer]
            if FileType.COMMON_AT.matches(img_data):
                self._files.append(W16AtImage(entry_data, img_data, pal))
            else:
                self._files.append(W16RawImage(entry_data, img_data, pal))

            i += 1

    def __len__(self):
        return len(self._files)

    def __getitem__(self, key: int) -> W16Image:
        return self._files[key]

    def __setitem__(self, key: int, value: W16Image):
        self._files[key] = value

    def __delitem__(self, key: int):
        del self._files[key]

    def __iter__(self):
        return iter(self._files)

    def append(self, img: W16Image):
        self._files.append(img)

    def _read_pal(self, pal_bytes: bytes) -> List[int]:
        palette = []
        for pal_entry in iter_bytes(pal_bytes, NUM_CHANNELS):
            r, g, b = pal_entry
            palette.append(r)
            palette.append(g)
            palette.append(b)
        return palette


def grouper(n, iterable, fillvalue=None):
    """grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"""
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)
