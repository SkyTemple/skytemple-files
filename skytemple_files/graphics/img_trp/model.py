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

from typing import Optional

from skytemple_files.common.tiled_image import to_pil, TilemapEntry, from_pil
from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.graphics.img_trp import TILE_DIM, CHUNK_DIM, PAL_ENTRY_LEN, PAL_LEN

try:
    from PIL import Image
except ImportError:
    from pil import Image


class ImgTrp(Sir0Serializable):
    def __init__(self, data: Optional[bytes], header_pnt: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.sprites: List[List[bytes]] = self._read_sprites(
            data,
            read_uintle(data, header_pnt + 0x04, 4),
            read_uintle(data, header_pnt + 0x00, 4)
        )
        self.palettes: List[List[int]] = self._read_palettes(
            data,
            read_uintle(data, header_pnt + 0x0C, 4) // PAL_LEN,
            read_uintle(data, header_pnt + 0x08, 4)
        )

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int,
                    static_data: Optional[Pmd2Data] = None) -> 'Sir0Serializable':
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.graphics.img_trp.writer import ImgTrpWriter
        return ImgTrpWriter(self).write()

    def to_pil(self, index, palette_index=0) -> Image.Image:
        dummy_tilemap = []
        for i in range(CHUNK_DIM * CHUNK_DIM):
            dummy_tilemap.append(TilemapEntry(i, False, False, palette_index))

        return to_pil(
            dummy_tilemap,
            self.sprites[index],
            self.palettes,
            TILE_DIM,
            TILE_DIM * CHUNK_DIM, TILE_DIM * CHUNK_DIM,
            CHUNK_DIM, CHUNK_DIM
        )
    
    def from_pil(self, index, img: Image.Image, import_palettes=True):
        tiles, tilemaps, palettes = from_pil(
            img, PAL_LEN, len(self.palettes), TILE_DIM, TILE_DIM * CHUNK_DIM, TILE_DIM * CHUNK_DIM
        )
        self.sprites[index] = tiles
        if import_palettes:
            self.palettes = palettes

    def _read_sprites(self, data, count, data_pointer):
        tiles = []
        T = TILE_DIM * TILE_DIM * CHUNK_DIM * CHUNK_DIM // 2
        for x in range(count):
            xdata = data[data_pointer+(x*T):data_pointer+((x+1)*T)]
            tiles.append(list(iter_bytes(xdata, int(TILE_DIM * TILE_DIM / 2))))  # / 2 because 4bpp
        return tiles

    def _read_palettes(self, data, count, data_pointer):
        palettes = []
        data = data[data_pointer:data_pointer+PAL_ENTRY_LEN*PAL_LEN*count]
        pal = []
        for i, (r, g, b, x) in enumerate(iter_bytes(data, PAL_ENTRY_LEN)):
            pal.append(r)
            pal.append(g)
            pal.append(b)
            if i % PAL_LEN == PAL_LEN - 1:
                palettes.append(pal)
                pal = []
        if len(pal) > 0:
            palettes.append(pal)
        return palettes

    def __eq__(self, other):
        if not isinstance(other, ImgTrp):
            return False
        return self.sprites == other.sprites and self.palettes == other.palettes
