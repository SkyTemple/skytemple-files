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

from skytemple_files.common.util import AutoString, read_u16, read_u8
from skytemple_files.graphics.fonts.graphic_font import GRAPHIC_FONT_ENTRY_LEN
from skytemple_files.graphics.pal.model import Pal


class GraphicFont(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        number_entries = read_u16(data, 0x02) // GRAPHIC_FONT_ENTRY_LEN

        self.palette: Pal | None = None
        self.entries: list[Image.Image | None] = []
        for i in range(
            0, number_entries * GRAPHIC_FONT_ENTRY_LEN, GRAPHIC_FONT_ENTRY_LEN
        ):
            width = read_u8(data, i + 0x00)
            height = read_u8(data, i + 0x01)
            offset = read_u16(data, i + 0x02)
            if width > 0 or height > 0:
                data_raw = data[offset : offset + width * height]
                self.entries.append(
                    Image.frombytes(
                        mode="P", size=(width, height), data=bytes(data_raw)
                    )
                )
            else:
                self.entries.append(None)

    def set_palette(self, palette: Pal):
        self.palette = palette

    def get_palette_raw(self) -> list[int]:
        if self.palette:
            return [0, 0, 255] * 0x80 + self.palette.get_palette_4bpc()[: 0x80 * 3]
        else:
            return [0, 0, 255] * 0x80 + [
                (i // 3) % 16 * 16 + (i // 3) // 16 for i in range(0x80 * 3)
            ]

    def set_palette_raw(self, data: list[int]):
        if self.palette:
            self.palette.set_palette_4bpc(data[0x80 * 3 :])

    def get_nb_entries(self) -> int:
        return len(self.entries)

    def get_entry(self, index) -> Image.Image:
        entry = self.entries[index]
        if entry:
            entry = entry.convert(mode="P")
            entry.putpalette(self.get_palette_raw())
        return entry

    def set_entries(self, entries: list[Image.Image | None]):
        self.entries = entries
        for e in entries:
            if e:
                self.set_palette_raw(list(e.palette.palette))
                break

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GraphicFont):
            return False
        return self.entries == other.entries and self.palette == other.palette
