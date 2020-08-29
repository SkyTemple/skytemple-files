#  Copyright 2020 Parakoopa
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
from typing import Optional

try:
    from PIL import Image
except ImportError:
    from pil import Image

from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
MAGIC_NUMBER = b'WTE\0'
logger = logging.getLogger(__name__)


class Wte(Sir0Serializable, AutoString):
    def __init__(self, data: Optional[bytes], header_pnt: int):
        """Construts a Wte model. Setting data to None will initialize an empty model."""
        if data is None:
            self.identifier = -1
            self.unk10 = 0
            self.width = 0
            self.height = 0
            self.image_data = bytes()
            self.palette = []
            self.is_weird: Optional[bool] = None
            return

        if not isinstance(data, memoryview):
            data = memoryview(data)

        assert self.matches(data, header_pnt), "The Wte file must begin with the WTE magic number"
        pointer_image = read_uintle(data, header_pnt + 0x4, 4)
        image_length = read_uintle(data, header_pnt + 0x8, 4)
        self.identifier = read_uintle(data, header_pnt + 0xC, 4)
        self.unk10 = read_uintle(data, header_pnt + 0x10, 4)
        self.width = read_uintle(data, header_pnt + 0x14, 2)
        self.height = read_uintle(data, header_pnt + 0x16, 2)
        pointer_pal = read_uintle(data, header_pnt + 0x18, 4)
        number_pal_colors = read_uintle(data, header_pnt + 0x1C, 4)
        assert read_uintle(data, header_pnt + 0x20, 4) == 0

        self.image_data = self._read_image(data, pointer_image, image_length)
        self.palette = self._read_palette(data, pointer_pal, number_pal_colors)

        # This flag indicates whether or not the image data in this Wte file is weird (0x0 size,
        # image data outside dimensions, empty palette).
        # It is set after calling to_pil!
        # If it's weird, a warning in the UI about changing it should be displayed.
        self.is_weird: Optional[bool] = None

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

    def to_pil(self) -> Image.Image:
        self.is_weird = False
        pil_img_data = bytearray(self.width * self.height)
        if len(pil_img_data) <= 0:
            assert len(self.image_data) == 0
            logger.warning('Wte was empty, returned 1x1px image.')
            self.is_weird = True
            im = Image.new('P', (1, 1), 0)
            im.putpalette(self.palette)
            return im
        for i, px in enumerate(iter_bytes_4bit_le(self.image_data)):
            if i >= len(pil_img_data):
                logger.warning('Wte had more image data than width and height defined, it was discarded!')
                self.is_weird = True
                break  # ???
            pil_img_data[i] = px
        im = Image.frombuffer('P', (self.width, self.height), pil_img_data, 'raw', 'P', 0, 1)
        if len(self.palette) <= 0:
            self.is_weird = True
        im.putpalette(self.palette)
        return im

    def from_pil(self, img: Image.Image) -> 'Wte':
        if img.mode != 'P':
            raise ValueError('Can not convert PIL image to WTE: Must be indexed image (=using a palette)')

        self.width = img.width
        self.height = img.height

        raw_pil_image = img.tobytes('raw', 'P')
        self.image_data = bytearray(int(self.width * self.height / 2))
        for i, (pix0, pix1) in enumerate(chunks(raw_pil_image, 2)):
            self.image_data[i] = pix0 + (pix1 << 4)

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
        return self.identifier == other.identifier and \
            self.unk10 == other.unk10 and \
            self.width == other.width and \
            self.height == other.height and \
            self.image_data == other.image_data and \
            self.palette == other.palette
