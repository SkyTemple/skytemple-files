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
import math
from typing import List

from skytemple_files.common.util import read_uintle
from skytemple_files.graphics.dpc.model import Dpc
from skytemple_files.graphics.dpci.model import Dpci

try:
    from PIL import Image
except ImportError:
    from pil import Image

DBG_TILING_DIM = 3
DBG_CHUNK_WIDTH = 24
DBG_WIDTH_AND_HEIGHT = 32


class Dbg:
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.mappings = []
        for pos in range(0, len(data), 2):
            self.mappings.append(read_uintle(data, pos, 2))

    def to_pil(
            self, dpc: Dpc, dpci: Dpci, palettes: List[List[int]]
    ) -> Image.Image:
        width_and_height_map = DBG_WIDTH_AND_HEIGHT * DBG_CHUNK_WIDTH

        chunks = dpc.chunks_to_pil(dpci, palettes, 1)
        fimg = Image.new('P', (width_and_height_map, width_and_height_map))
        fimg.putpalette(chunks.getpalette())

        for i, mt_idx in enumerate(self.mappings):
            x = i % DBG_WIDTH_AND_HEIGHT
            y = math.floor(i / DBG_WIDTH_AND_HEIGHT)
            fimg.paste(
                chunks.crop((0, mt_idx * DBG_CHUNK_WIDTH, DBG_CHUNK_WIDTH, mt_idx * DBG_CHUNK_WIDTH + DBG_CHUNK_WIDTH)),
                (x * DBG_CHUNK_WIDTH, y * DBG_CHUNK_WIDTH)
            )

        return fimg

    def to_bytes(self):
        raise NotImplementedError()  # todo
