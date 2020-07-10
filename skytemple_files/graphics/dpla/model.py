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
from typing import Optional

from skytemple_files.common.util import *


class Dpla:
    """
    This palette file contains sets of 16 colors and "frames" of animations for them. Each Sir0 poiinter
    points to one color entry and each of these color entries has 0-X frames of animation.
    """
    def __init__(self, data: bytes, pointer_to_pointers: int):
        toc_pointers = []
        for i in range(pointer_to_pointers, len(data), 4):
            toc_pointers.append(read_uintle(data, i, 4))

        # A list of colors stored in this file. The colors are lists of RGB value tuples: [(R, G, B), (R, G, B)...]
        self.colors = []
        for pnt in toc_pointers:
            # 0x0         2           uint16      (NbColors) The amount of colors in this entry.
            number_colors = read_uintle(data, pnt, 2)
            # 0x2         2           uint16      unknown
            unk = read_uintle(data, pnt + 2, 2)
            # 0x4         (NbColors * 4)          A list of colors. Always at least 4 bytes even when empty! Is completely 0 if nb of color == 0 !
            # [
            #     0x0     4           RGBX32      A color.
            #     ...
            # ]
            frames = []
            for r, g, b, x in iter_bytes(data, 4, pnt + 4, pnt + 4 + (number_colors * 4)):
                frames.append((r, g, b))
                assert x == 128  # just in case it isn't... then we'd have a real alpha channel
            self.colors.append(frames)

    def get_palette_for_frame(self, pal_idx: int, frame_id: int):
        """
        Returns the color palette at the given frame id. Returned is a stream of RGB colors: [R, G, B, R, G, B...].
        Returned are always 16 colors. If the palette file has more than 16 colors, the pal_idx specifies what set
        of 16 colors to return.
        """
        colors = self.colors[pal_idx * 16:(pal_idx + 1) * 16]
        frame_pal = []
        for color in colors:
            if len(color) < 1:
                color = [(0, 0, 0)]
            r, g, b = color[frame_id % len(color)]
            frame_pal.append(r)
            frame_pal.append(g)
            frame_pal.append(b)

        return frame_pal

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        # TODO - A pointer for each palette must be created. Data Pointer must point to list of pointers at end.
        raise NotImplementedError()

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int) -> 'Dpla':
        return cls(content_data, data_pointer)
