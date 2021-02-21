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
from enum import Enum, auto
from typing import Optional

try:
    from PIL import Image
except ImportError:
    from pil import Image

from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.common.i18n_util import f, _
MAGIC_NUMBER = b'WTE\0'
logger = logging.getLogger(__name__)


class WteImageType(Enum):
    NONE       = 0x00, _('Palette Only'), 0, False
    COLOR_2BPP = 0x02, _('2 bits per pixel (4 colors)'), 2, True
    COLOR_4BPP = 0x03, _('4 bits per pixel (16 colors)'), 4, True
    COLOR_8BPP = 0x04, _('8 bits per pixel (256 colors)'), 8, True
    
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: int, explanation: str, bpp: int, has_image: bool
    ):
        self.explanation = explanation
        self.bpp = bpp
        self.has_image = has_image

class Wte(Sir0Serializable, AutoString):
    def __init__(self, data: Optional[bytes], header_pnt: int):
        """Constructs a Wte model. Setting data to None will initialize an empty model."""
        if data is None:
            self.image_type = WteImageType.NONE
            self.actual_dim = 0
            self.unk10 = 0
            self.width = 0
            self.height = 0
            self.image_data = bytes()
            self.palette = []
            return

        if not isinstance(data, memoryview):
            data = memoryview(data)

        assert self.matches(data, header_pnt), "The Wte file must begin with the WTE magic number"
        pointer_image = read_uintle(data, header_pnt + 0x4, 4)
        image_length = read_uintle(data, header_pnt + 0x8, 4)

        # actual_dim and image_type both forms the image mode
        self.actual_dim = read_uintle(data, header_pnt + 0xC, 1)
        self.image_type = WteImageType(read_uintle(data, header_pnt + 0xD, 1))
        
        self.unk10 = read_uintle(data, header_pnt + 0x10, 4)
        self.width = read_uintle(data, header_pnt + 0x14, 2)
        self.height = read_uintle(data, header_pnt + 0x16, 2)
        pointer_pal = read_uintle(data, header_pnt + 0x18, 4)
        number_pal_colors = read_uintle(data, header_pnt + 0x1C, 4)
        assert read_uintle(data, header_pnt + 0x20, 4) == 0

        self.image_data = self._read_image(data, pointer_image, image_length)
        self.palette = self._read_palette(data, pointer_pal, number_pal_colors)

    @staticmethod
    def matches(data, header_pnt):
        return data[header_pnt:header_pnt+len(MAGIC_NUMBER)] == MAGIC_NUMBER

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int,
                    static_data: Optional[Pmd2Data] = None) -> 'Sir0Serializable':
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.graphics.wte.writer import WteWriter
        return WteWriter(self).write()

    def actual_dimensions(self) -> Tuple[int, int]:
        return (8*(2**(self.actual_dim & 0x07)), 8*(2**((self.actual_dim>>3) & 0x07)))

    def _adjust_actual_dimensions(self, canvas_width: int, canvas_height: int):
        """ Adjusts the actual dimensions specified by the image mode so the image can fit into those dimensions. """
        width = 0
        while 8*(2**width)<canvas_width:
            width+=1
        height = 0
        while 8*(2**height)<canvas_height:
            height+=1
        if width>=8 or height>=8: # Max theoretical size: (2**(7+3), 2**(7+3)) = (1024, 1024)
            raise ValueError('Canvas size too large.')
        self.actual_dim = width + (height<<3)
    
    def get_mode(self) -> int:
        """ Returns the mode used by this file. This is to update the corresponding WTU file. """
        return self.actual_dim+(self.image_type.value<<8)
    
    def has_image(self) -> bool:
        """ Returns if this WTE file has actual image data. """
        return self.image_type.has_image
    def has_palette(self) -> bool:
        """ Returns if this WTE file has actual palette data. """
        return len(self.palette)>0
    
    def nb_palette_variants(self) -> int:
        """ Returns how many palette variants this image has. """
        if self.image_type.has_image:
            nb_total_colors = len(self.palette)//3
            nb_colors_per_variant = 2**self.image_type.bpp
            if nb_total_colors%nb_colors_per_variant==0:
                return nb_total_colors//nb_colors_per_variant
            else:
                return (nb_total_colors//nb_colors_per_variant)+1
        else:
            return 1
    
    def get_palette(self) -> List[int]:
        """ Returns the palette that will be used to display the image. """
        colors_per_line : int = 2**self.image_type.bpp
        if not self.has_palette():
            # Generates a default grayscale palette if the file doesn't have one
            return [min((i//3)*(256//colors_per_line), 255) for i in range(colors_per_line*3)]
        else:
            return self.palette
        
    def to_pil_palette(self) -> Image.Image:
        """ Returns the palette as an image where each pixel represents each color of the palette. """
        colors_per_line = 16
        palette : List[int] = [i for i in range(len(self.get_palette())//3)]
        if len(palette)%colors_per_line!=0:
            palette += [0] * (colors_per_line - len(palette)%colors_per_line)
        img = Image.frombytes(mode="P", data=bytes(palette), size=(colors_per_line, len(palette)//colors_per_line))
        img.putpalette(self.get_palette())
        return img
    
    def to_pil_canvas(self, variation: int = 0) -> Image.Image:
        """ Returns the image with its data part size (the width and height specified in the WTE header).
            If this file has no image, returns an image representation of the palette instead. """
        im : Image.Image = self.to_pil(variation)
        if not self.has_image():
            return im
        else:
            return im.crop(box=[0,0,self.width,self.height])
        
    def to_pil(self, variation: int = 0) -> Image.Image:
        """ Returns the image with its actual size (the one specified by the image mode).
            If this file has no image, returns an image representation of the palette instead. """
        
        dimensions = self.actual_dimensions()
        pil_img_data = bytearray(dimensions[0] * dimensions[1])
        if not self.has_image():
            assert len(self.image_data) == 0
            im = self.to_pil_palette()
            return im.resize((im.width*16, im.height*16), resample=Image.NEAREST)

        pixels_per_byte = 8 // self.image_type.bpp
        nb_colors = 2**self.image_type.bpp
        for i, px in enumerate(self.image_data):
            for j in range(pixels_per_byte):
                pil_img_data[i*pixels_per_byte+j] = (px>>(self.image_type.bpp*j))%nb_colors
        im = Image.frombuffer('P', dimensions, pil_img_data, 'raw', 'P', 0, 1)
        im.putpalette(self.get_palette()[3*(2**self.image_type.bpp)*variation:])
        return im

    def from_pil(self, img: Image.Image, img_type: WteImageType, discard_palette: bool) -> 'Wte':
        """ Replace the image data by the new one passed in argument. """
        if img.mode != 'P':
            raise AttributeError(_('Can not convert PIL image to WTE: Must be indexed image (=using a palette)'))
        
        if img_type.has_image:
            try:
                self._adjust_actual_dimensions(img.width, img.height)
            except ValueError:
                raise ValueError(_('This image is too big to fit into a WTE file.'))
            
            self.width = img.width
            self.height = img.height
            dimensions = self.actual_dimensions()
        else:
            self.width = 0
            self.height = 0
            self.actual_dim = 0

        self.image_type = img_type
        if self.image_type.has_image:
            raw_image = img.tobytes("raw", "P")
            self.image_data = bytearray(dimensions[0] // 8 * self.height * img_type.bpp)
            i = 0
            pixels_per_byte = 8 // img_type.bpp
            for pix in raw_image:
                b = (i % pixels_per_byte)*img_type.bpp
                x = i // pixels_per_byte
                self.image_data[x] += pix<<b
                i+=1
                if i%dimensions[0]==self.width:
                    i += dimensions[0] - self.width
        else:
            self.image_data = bytearray(0)
        if discard_palette:
            self.palette = []
        else:
            self.palette = [x for x in memoryview(img.palette.palette)]
        return self

    def _read_image(self, data: memoryview, pointer_image, image_length) -> memoryview:
        return data[pointer_image:pointer_image+image_length]

    def _read_palette(self, data: memoryview, pointer_pal, number_pal_colors) -> List[int]:
        pal = []
        data = data[pointer_pal:pointer_pal+(number_pal_colors*4)]
        for i, (r, g, b, x) in enumerate(iter_bytes(data, 4)):
            pal.append(r)
            pal.append(g)
            pal.append(b)
            assert x == 0x80
        return pal

    def __eq__(self, other):
        if not isinstance(other, Wte):
            return False
        return self.actual_dim == other.actual_dim and \
            self.image_type == other.image_type and \
            self.unk10 == other.unk10 and \
            self.width == other.width and \
            self.height == other.height and \
            self.image_data == other.image_data and \
            self.palette == other.palette
