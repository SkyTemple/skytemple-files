"""NDS rom icon banner, contains the localized rom name and icon"""
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

import itertools

from ndspy.rom import NintendoDSRom
from PIL import Image
from range_typed_integers import u16

from skytemple_files.common.nds_hashing import nds_crc16
from skytemple_files.common.tiled_image import TilemapEntry, from_pil, to_pil
from skytemple_files.common.util import chunks, read_bytes, read_u16, write_u16


def _utf16_encode_fixed(title: str) -> bytes:
    encoded = title.encode("UTF-16LE")
    assert len(encoded) < 0x100, "Title length must be less than 256 characters"
    return encoded.ljust(0x100, b"\0")


ICON_BANNER_SIZE = 0x840
ICON_DIM_TILE = 8
ICON_DIM_IMG_TILES = 4
ICON_DIM_IMG_PX = ICON_DIM_IMG_TILES * ICON_DIM_TILE
ICON_PAL_CNT = 4


class Icon:
    def __init__(self, bitmap: bytes, palette: bytes):
        self.bitmap = bitmap
        self._palette = []
        for i in range(0, len(palette) // 2):
            bgr = read_u16(palette, i * 2)
            self._palette.append((bgr & 0x001F) * 0x08)
            self._palette.append(((bgr & 0x03E0) >> 5) * 0x08)
            self._palette.append(((bgr & 0x7C00) >> 10) * 0x08)

    @property
    def palette(self) -> bytes:
        data = bytearray(len(self._palette) // 3 * ICON_PAL_CNT // 2)
        cursor = 0
        for r, g, b in chunks(self._palette, 3):
            r //= 8
            g = (g // 8) << 5
            b = (b // 8) << 10
            write_u16(data, u16(r + g + b), cursor)
            cursor += 2
        return data

    def to_pil(self) -> Image.Image:
        tilemap = []
        for i in range(ICON_DIM_IMG_TILES * ICON_DIM_IMG_TILES):
            tilemap.append(TilemapEntry(idx=i, pal_idx=0, flip_x=False, flip_y=False))

        return to_pil(
            tilemap,
            list(chunks(self.bitmap, ICON_DIM_TILE * ICON_DIM_TILE // 2)),
            [self._palette],
            ICON_DIM_TILE,
            ICON_DIM_IMG_PX,
            ICON_DIM_IMG_PX,
            bpp=4,
        )

    def from_pil(self, img: Image.Image) -> None:
        tiles, _, pals = from_pil(
            img, 16, 1, ICON_DIM_TILE, ICON_DIM_IMG_PX, ICON_DIM_IMG_PX, optimize=False
        )
        self.bitmap = bytes(itertools.chain.from_iterable(tiles))
        self._palette = pals[0]


# http://problemkaputt.de/gbatek.htm#dscartridgeicontitle
class IconBanner:
    def __init__(self, rom: NintendoDSRom):
        self.rom = rom
        data = rom.iconBanner

        self.version = read_u16(data, 0x0)
        assert len(data) == ICON_BANNER_SIZE
        assert self.version == 1  # EoS should always use version 1

        self.checksum = read_u16(data, 0x2)

        self.icon = Icon(read_bytes(data, 0x20, 0x200), read_bytes(data, 0x220, 0x20))

        self.title_japanese = (
            read_bytes(data, 0x240, 0x100).decode("UTF-16LE").rstrip("\x00")
        )
        self.title_english = (
            read_bytes(data, 0x340, 0x100).decode("UTF-16LE").rstrip("\x00")
        )
        self.title_french = (
            read_bytes(data, 0x440, 0x100).decode("UTF-16LE").rstrip("\x00")
        )
        self.title_german = (
            read_bytes(data, 0x540, 0x100).decode("UTF-16LE").rstrip("\x00")
        )
        self.title_italian = (
            read_bytes(data, 0x640, 0x100).decode("UTF-16LE").rstrip("\x00")
        )
        self.title_spanish = (
            read_bytes(data, 0x740, 0x100).decode("UTF-16LE").rstrip("\x00")
        )

    def save_to_rom(self) -> None:
        data = bytearray(ICON_BANNER_SIZE)

        write_u16(data, self.version, 0x0)

        data[0x20 : 0x20 + 0x200] = self.icon.bitmap
        data[0x220 : 0x220 + 0x20] = self.icon.palette

        data[0x240 : 0x240 + 0x100] = _utf16_encode_fixed(self.title_japanese)
        data[0x340 : 0x340 + 0x100] = _utf16_encode_fixed(self.title_english)
        data[0x440 : 0x440 + 0x100] = _utf16_encode_fixed(self.title_french)
        data[0x540 : 0x540 + 0x100] = _utf16_encode_fixed(self.title_german)
        data[0x640 : 0x640 + 0x100] = _utf16_encode_fixed(self.title_italian)
        data[0x740 : 0x740 + 0x100] = _utf16_encode_fixed(self.title_spanish)

        calculated_checksum = nds_crc16(data, 0x20, 0x820)
        write_u16(data, calculated_checksum, 0x2)

        self.rom.iconBanner = data
