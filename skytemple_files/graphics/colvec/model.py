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
from skytemple_files.graphics.colvec import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
try:
    from PIL import Image
except ImportError:
    from pil import Image


class Colvec(Sir0Serializable, AutoString):
    def __init__(self, data: Optional[bytes], header_pnt: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.colormaps = []
        for i in range(len(data)//COLVEC_DATA_LEN):
            self.colormaps.append([])
            colormap = data[i*COLVEC_DATA_LEN:(i+1)*COLVEC_DATA_LEN]
            for i, (r, g, b, x) in enumerate(iter_bytes(colormap, 4)):
                self.colormaps[-1].append(r)
                self.colormaps[-1].append(g)
                self.colormaps[-1].append(b)
                assert x == 0xff
    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int,
                    static_data: Optional[Pmd2Data] = None) -> 'Sir0Serializable':
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.graphics.colvec.writer import ColvecWriter
        return ColvecWriter(self).write()
    
    def nb_colormaps(self):
        return len(self.colormaps)
    
    def apply_colormap(self, index, palette: List[int]) -> List[int]:
        """ Transforms the palette using the colormap in index """
        new_palette = []
        for i, v in enumerate(palette):
            comp = i%3
            new_palette.append(self.colormaps[index][v*3+comp])
        return new_palette
    
    def to_pil(self, index) -> Image.Image:
        """ Returns the palette as an image where each pixel represents each color of the colormap. """
        img = Image.frombytes(mode="RGB", data=bytes(self.colormaps[index]), size=(16,16))
        return img
    
    def from_pil(self, index, img: Image.Image):
        img = img.convert("RGB")
        self.colormaps[index] = [x for x in memoryview(img.tobytes()[:768])]
        self.colormaps[index] += [0]*(768-len(self.colormaps[index]))

    def __eq__(self, other):
        if not isinstance(other, Colvec):
            return False
        return self.colormaps == other.colormaps
