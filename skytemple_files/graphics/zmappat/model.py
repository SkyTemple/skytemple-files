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
from enum import Enum
from typing import Optional

try:
    from PIL import Image
except ImportError:
    from pil import Image

from skytemple_files.common.util import *
from skytemple_files.graphics.zmappat import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.common.i18n_util import f, _

logger = logging.getLogger(__name__)


class ZMappaTVariation(Enum):
    SEMI_OPAQUE = 0x00, _('Semi-Opaque'), "sopaque"
    TRANSPARENT = 0x01, _('Transparent'), "trans"
    OPAQUE = 0x02, _('Opaque'), "opaque"

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: int, description: str, filename: str
    ):
        self.description = description
        self.filename = filename


class ZMappaT(Sir0Serializable, AutoString):
    def __init__(self, data: Optional[bytes], header_pnt: int):
        """Constructs a ZMappaT model. Setting data to None will initialize an empty model."""
        if data is None:
            self.tiles = []
            self.masks = []
            self.palette = []
            return

        if not isinstance(data, memoryview):
            data = memoryview(data)

        pointer_tiles = read_uintle(data, header_pnt, 4)
        pointer_pal = read_uintle(data, header_pnt + 0x4, 4)

        self.tiles, self.masks = self._read_tiles(data, pointer_tiles, (pointer_pal - pointer_tiles) // 4)
        self.palette = self._read_palette(data, pointer_pal)

        assert len(self.tiles) == ZMAPPAT_NB_TILES_PER_VARIATION * ZMAPPAT_NB_VARIATIONS
        assert len(self.masks) == ZMAPPAT_NB_TILES_PER_VARIATION * ZMAPPAT_NB_VARIATIONS

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int,
                    static_data: Optional[Pmd2Data] = None) -> 'Sir0Serializable':
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.graphics.zmappat.writer import ZMappaTWriter
        return ZMappaTWriter(self).write()

    def _read_tiles(self, data: memoryview, pointer_tiles, nb_tiles) -> Tuple[List[bytearray], List[bytearray]]:
        tiles = []
        masks = []
        for i in range(nb_tiles):
            offset = read_uintle(data, pointer_tiles + i * 0x4, 4)
            data_tile = data[offset:offset + ZMAPPAT_TILE_SIZE]
            current_mask = bytearray(ZMAPPAT_TILE_SIZE // 2)
            current_tile = bytearray(ZMAPPAT_TILE_SIZE // 2)
            for chunks in range(ZMAPPAT_TILE_SIZE // 8):
                current_mask[chunks * 4:(chunks + 1) * 4] = data_tile[chunks * 8:chunks * 8 + 4]
                current_tile[chunks * 4:(chunks + 1) * 4] = data_tile[chunks * 8 + 4:chunks * 8 + 8]
            masks.append(current_mask)
            tiles.append(current_tile)
        return tiles, masks

    def _read_palette(self, data: memoryview, pointer_pal) -> List[int]:
        pal = []
        data = data[pointer_pal:pointer_pal + (16 * 4)]
        for i, (r, g, b, x) in enumerate(iter_bytes(data, 4)):
            pal.append(r)
            pal.append(g)
            pal.append(b)
        return pal

    def _to_pil_chunk(self, chunks, variation: ZMappaTVariation) -> Image.Image:
        """ Returns an image using the chunks given."""
        dimensions = (8 * ZMAPPAT_NB_TILES_PER_LINE, 8 * ZMAPPAT_NB_TILES_PER_VARIATION // ZMAPPAT_NB_TILES_PER_LINE)
        pil_img_data = bytearray(ZMAPPAT_NB_TILES_PER_VARIATION * 64)

        for i, t in enumerate(chunks[ZMAPPAT_NB_TILES_PER_VARIATION * variation.value:ZMAPPAT_NB_TILES_PER_VARIATION * (
                variation.value + 1)]):
            x_tile = i % ZMAPPAT_NB_TILES_PER_LINE
            y_tile = i // ZMAPPAT_NB_TILES_PER_LINE
            for y in range(8):
                start = (y_tile * 64 + y * 8) * ZMAPPAT_NB_TILES_PER_LINE + x_tile * 8
                pil_img_data[start:start + 8] = t[y * 8:y * 8 + 8]
        im = Image.frombuffer('P', dimensions, pil_img_data, 'raw', 'P', 0, 1)
        return im

    def _to_pil_chunk_minimized(self, chunks, variation: ZMappaTVariation) -> Image.Image:
        """ Returns an image using the chunks given.
        This is the minimized version. """
        dimensions = (
        4 * (ZMAPPAT_NB_TILES_PER_LINE // 2), 4 * (ZMAPPAT_NB_TILES_PER_VARIATION // ZMAPPAT_NB_TILES_PER_LINE) // 2)
        pil_img_data = bytearray(ZMAPPAT_NB_TILES_PER_VARIATION * 4)

        for i, t in enumerate(chunks[ZMAPPAT_NB_TILES_PER_VARIATION * variation.value:ZMAPPAT_NB_TILES_PER_VARIATION * (
                variation.value + 1)]):
            if i % 4 == 0:
                x_tile = (i // 4) % (ZMAPPAT_NB_TILES_PER_LINE // 2)
                y_tile = (i // 4) // (ZMAPPAT_NB_TILES_PER_LINE // 2)
                for y in range(4):
                    start = (y_tile * 16 + y * 4) * ZMAPPAT_NB_TILES_PER_LINE // 2 + x_tile * 4
                    pil_img_data[start:start + 4] = t[y * 8:y * 8 + 4]
        im = Image.frombuffer('P', dimensions, pil_img_data, 'raw', 'P', 0, 1)
        return im

    def to_pil_tiles(self, variation: ZMappaTVariation) -> Image.Image:
        """ Returns an image representing all the tiles of this zmappat file."""
        im = self._to_pil_chunk(self.tiles, variation)
        im.putpalette(self.palette)
        return im

    def to_pil_masks(self, variation: ZMappaTVariation) -> Image.Image:
        """ Returns an image representing all the masks of this zmappat file."""
        im = self._to_pil_chunk(self.masks, variation)
        im.putpalette([i // 3 for i in range(256 * 3)])
        return im

    def to_pil_tiles_minimized(self, variation: ZMappaTVariation) -> Image.Image:
        """ Returns an image representing all the tiles of this zmappat file.
        This is the minimized version."""
        im = self._to_pil_chunk_minimized(self.tiles, variation)
        im.putpalette(self.palette)
        return im

    def to_pil_masks_minimized(self, variation: ZMappaTVariation) -> Image.Image:
        """ Returns an image representing all the masks of this zmappat file.
        This is the minimized version."""
        im = self._to_pil_chunk_minimized(self.masks, variation)
        im.putpalette([i // 3 for i in range(256 * 3)])
        return im

    def from_pil(self, imgs: List[Image.Image], masks: List[Image.Image]) -> 'ZMappaT':
        """ Replace the tile/mask data by the new ones passed in argument. """
        if len(imgs) != ZMAPPAT_NB_VARIATIONS or len(masks) != ZMAPPAT_NB_VARIATIONS:
            raise ValueError(_("Tile and masks list must have exactly 3 items"))
        new_tiles = []
        new_masks = []
        for v in range(ZMAPPAT_NB_VARIATIONS):
            if imgs[v].mode != 'P' or masks[v].mode != 'P':
                raise AttributeError(_('Can not convert PIL image to ZMAPPAT: Must be indexed images (=using a palette)'))
            for i in range(ZMAPPAT_NB_TILES_PER_VARIATION):
                x_tile = i % ZMAPPAT_NB_TILES_PER_LINE
                y_tile = i // ZMAPPAT_NB_TILES_PER_LINE
                tile_img = imgs[v].crop(box=[x_tile * 8, y_tile * 8, (x_tile + 1) * 8, (y_tile + 1) * 8])
                mask_img = masks[v].crop(box=[x_tile * 8, y_tile * 8, (x_tile + 1) * 8, (y_tile + 1) * 8])
                new_tiles.append(bytearray(tile_img.tobytes("raw", "P")))
                new_masks.append(bytearray(mask_img.tobytes("raw", "P")))
        self.tiles = new_tiles
        self.masks = new_masks
        self.palette = [x for x in memoryview(imgs[0].palette.palette)]

    def from_pil_minimized(self, imgs: List[Image.Image], masks: List[Image.Image]) -> 'ZMappaT':
        """ Replace the tile/mask data by the new ones passed in argument.
        This is for the minimized version. """
        if len(imgs) != ZMAPPAT_NB_VARIATIONS or len(masks) != ZMAPPAT_NB_VARIATIONS:
            raise ValueError(_("Tile and masks list must have exactly 3 items"))
        new_tiles = []
        new_masks = []
        for v in range(ZMAPPAT_NB_VARIATIONS):
            if imgs[v].mode != 'P' or masks[v].mode != 'P':
                raise AttributeError(_('Can not convert PIL image to ZMAPPAT: Must be indexed images (=using a palette)'))
            for i in range(ZMAPPAT_NB_TILES_PER_VARIATION // 4):
                x_tile = i % (ZMAPPAT_NB_TILES_PER_LINE // 2)
                y_tile = i // (ZMAPPAT_NB_TILES_PER_LINE // 2)
                mini_tile_img = imgs[v].crop(box=[x_tile * 4, y_tile * 4, (x_tile + 1) * 4, (y_tile + 1) * 4])
                mini_mask_img = masks[v].crop(box=[x_tile * 4, y_tile * 4, (x_tile + 1) * 4, (y_tile + 1) * 4])
                for y in range(2):
                    for x in range(2):
                        tile_img = Image.new(mode='P', size=(8, 8), color=0)
                        tile_img.paste(mini_tile_img, (x * 4, y * 4))
                        mask_img = Image.new(mode='P', size=(8, 8), color=255)
                        mask_img.paste(mini_mask_img, (x * 4, y * 4))
                        new_tiles.append(bytearray(tile_img.tobytes("raw", "P")))
                        new_masks.append(bytearray(mask_img.tobytes("raw", "P")))
        self.tiles = new_tiles
        self.masks = new_masks
        self.palette = [x for x in memoryview(imgs[0].palette.palette)]

    def __eq__(self, other):
        if not isinstance(other, ZMappaT):
            return False
        return self.tiles == other.tiles and \
               self.masks == other.masks and \
               self.palette == other.palette
