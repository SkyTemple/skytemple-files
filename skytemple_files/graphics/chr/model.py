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

from skytemple_files.common.util import *
from skytemple_files.graphics.chr import *
from skytemple_files.graphics.pal.model import Pal
from skytemple_files.common.i18n_util import f, _

try:
    from PIL import Image
except ImportError:
    from pil import Image

class Chr(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        number_entries = len(data)//(CHR_TILE_WIDTH**2)

        self.palette = None
        self.tiles: List[Image.Image] = []
        for i in range(number_entries):
            data_raw = data[(CHR_TILE_WIDTH**2)*i:(CHR_TILE_WIDTH**2)*(i+1)]
            self.tiles.append(Image.frombytes(mode='P', size=(CHR_TILE_WIDTH,CHR_TILE_WIDTH), data=bytes(data_raw)))
        
    def set_palette(self, palette: Pal):
        self.palette = palette
        
    def get_palette_raw(self) -> List[int]:
        if self.palette:
            return self.palette.get_palette_2bpc()
        else:
            return [(i//3)%16*16+(i//3)//16 for i in range(0x100*3)]
    
    def set_palette_raw(self, data: List[int]):
        if self.palette:
            self.palette.set_palette_2bpc(data)
    
    def get_nb_tiles(self) -> int:
        return len(self.tiles)
    
    def get_nb_palettes(self) -> int:
        return (len(self.get_palette_raw())//3)//16
    
    def to_pil(self, color_variation = 0) -> Image.Image:
        img = Image.new(mode="P", size=(CHR_TILE_WIDTH*len(self.tiles), CHR_TILE_WIDTH), color=0)
        for i, t in enumerate(self.tiles):
            img.paste(t, box=(i*CHR_TILE_WIDTH, 0))
        img.putpalette(self.get_palette_raw()[color_variation*16*3:])
        return img
    
    def from_pil(self, img: Image.Image):
        if img.mode != 'P':
            raise AttributeError(_('Cannot convert PIL image to CHR: Must be indexed image (=using a palette)'))
        if img.width%CHR_TILE_WIDTH!=0 or img.height%CHR_TILE_WIDTH!=0:
            raise AttributeError(f(_('Cannot convert PIL image to CHR: width and height must be a multiple of {CHR_TILE_WIDTH}')))
        self.tiles = []
        for y in range(img.height//CHR_TILE_WIDTH):
            for x in range(img.width//CHR_TILE_WIDTH):
                self.tiles.append(img.crop([x*CHR_TILE_WIDTH, y*CHR_TILE_WIDTH, (x+1)*CHR_TILE_WIDTH, (y+1)*CHR_TILE_WIDTH]))
        self.set_palette_raw(list(img.palette.palette))
    
    def __eq__(self, other):
        if not isinstance(other, GraphicFont):
            return False
        return self.tiles == other.tiles and \
               self.palette == other.palette
