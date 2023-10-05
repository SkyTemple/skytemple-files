#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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

from __future__ import annotations


from PIL import Image
from range_typed_integers import u32

from skytemple_files.common.util import AutoString, iter_bytes
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.graphics.colvec import COLVEC_DATA_LEN


class Colvec(Sir0Serializable, AutoString):
    def __init__(self, data: bytes, header_pnt: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.colormaps: list[list[int]] = []
        for i in range(len(data) // COLVEC_DATA_LEN):
            self.colormaps.append([])
            colormap = data[i * COLVEC_DATA_LEN : (i + 1) * COLVEC_DATA_LEN]
            for i, (r, g, b, x) in enumerate(iter_bytes(colormap, 4)):
                self.colormaps[-1].append(r)
                self.colormaps[-1].append(g)
                self.colormaps[-1].append(b)
                assert x == 0xFF

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: u32,
    ) -> Sir0Serializable:
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> tuple[bytes, list[u32], u32 | None]:
        from skytemple_files.graphics.colvec.writer import ColvecWriter

        return ColvecWriter(self).write()  # type: ignore

    def nb_colormaps(self):
        return len(self.colormaps)

    def apply_colormap(self, index, palette: list[int]) -> list[int]:
        """Transforms the palette using the colormap in index"""
        new_palette = []
        for i, v in enumerate(palette):
            comp = i % 3
            new_palette.append(self.colormaps[index][v * 3 + comp])
        return new_palette

    def to_pil(self, index) -> Image.Image:
        """Returns the palette as an image where each pixel represents each color of the colormap."""
        img = Image.frombytes(
            mode="RGB", data=bytes(self.colormaps[index]), size=(16, 16)
        )
        return img

    def from_pil(self, index, img: Image.Image):
        img = img.convert("RGB")
        self.colormaps[index] = [x for x in memoryview(img.tobytes()[:768])]
        self.colormaps[index] += [0] * (768 - len(self.colormaps[index]))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Colvec):
            return False
        return self.colormaps == other.colormaps
