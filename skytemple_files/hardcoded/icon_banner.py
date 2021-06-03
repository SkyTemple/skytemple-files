"""NDS rom icon banner, contains the localized rom name and icon"""
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

from ndspy.rom import NintendoDSRom
from skytemple_files.common.util import read_uintle, read_bytes, write_uintle
from skytemple_files.common.nds_hashing import nds_crc16


def _utf16_encode_fixed(title: str) -> bytes:
    encoded = title.encode("UTF-16LE")
    assert len(encoded) < 0x100, "Title length must be less than 256 characters"
    return encoded.ljust(0x100, b'\0')


ICON_BANNER_SIZE = 0x840


# http://problemkaputt.de/gbatek.htm#dscartridgeicontitle
class IconBanner:
    def __init__(self, rom: NintendoDSRom):
        self.rom = rom
        data = rom.iconBanner

        self.version = read_uintle(data, 0x0, 0x2)
        assert len(data) == ICON_BANNER_SIZE
        assert self.version == 1  # EoS should always use version 1

        self.checksum = read_uintle(data, 0x2, 0x2)

        self.icon_bitmap = read_bytes(data, 0x20, 0x200)
        self.icon_palette = read_bytes(data, 0x220, 0x20)

        self.title_japanese = read_bytes(data, 0x240, 0x100).decode('UTF-16LE').rstrip('\x00')
        self.title_english = read_bytes(data, 0x340, 0x100).decode('UTF-16LE').rstrip('\x00')
        self.title_french = read_bytes(data, 0x440, 0x100).decode('UTF-16LE').rstrip('\x00')
        self.title_german = read_bytes(data, 0x540, 0x100).decode('UTF-16LE').rstrip('\x00')
        self.title_italian = read_bytes(data, 0x640, 0x100).decode('UTF-16LE').rstrip('\x00')
        self.title_spanish = read_bytes(data, 0x740, 0x100).decode('UTF-16LE').rstrip('\x00')

    def save_to_rom(self):
        data = bytearray(ICON_BANNER_SIZE)

        write_uintle(data, self.version, 0x0, 0x2)

        data[0x20:0x20 + 0x200] = self.icon_bitmap
        data[0x220:0x220 + 0x20] = self.icon_palette

        data[0x240:0x240 + 0x100] = _utf16_encode_fixed(self.title_japanese)
        data[0x340:0x340 + 0x100] = _utf16_encode_fixed(self.title_english)
        data[0x440:0x440 + 0x100] = _utf16_encode_fixed(self.title_french)
        data[0x540:0x540 + 0x100] = _utf16_encode_fixed(self.title_german)
        data[0x640:0x640 + 0x100] = _utf16_encode_fixed(self.title_italian)
        data[0x740:0x740 + 0x100] = _utf16_encode_fixed(self.title_spanish)

        calculated_checksum = nds_crc16(data, 0x20, 0x820)
        write_uintle(data, calculated_checksum, 0x2, 0x2)

        self.rom.iconBanner = data
