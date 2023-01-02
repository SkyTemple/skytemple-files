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

import os
from xml.etree.ElementTree import ElementTree

from ndspy.rom import NintendoDSRom
from PIL import Image

from skytemple_files.graphics.fonts.banner_font.handler import BannerFontHandler

# base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
out_dir = os.path.join(os.path.dirname(__file__), "dbg_output")
os.makedirs(out_dir, exist_ok=True)

# rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))
rom = NintendoDSRom.fromFile(
    "/media/disk/Documents/Common/Games/Nintendo DS/Hack/Pokemon Mystery Dungeon - Explorers of Sky (4273) (US).nds"
)

for fn in ["FONT/banner.bin", "FONT/banner_c.bin", "FONT/banner_s.bin"]:
    font_ref = rom.getFileByName(fn)
    font = BannerFontHandler.deserialize(font_ref)
    tree = ElementTree()
    xml = tree.parse(os.path.join(out_dir, fn.replace("/", "_") + f".xml"))
    tables = dict()
    for i in range(256):
        path = os.path.join(out_dir, fn.replace("/", "_") + f".{i}.png")
        if os.path.exists(path):
            tables[i] = Image.open(path, "r")

    font.import_from_xml(xml, tables)
    assert BannerFontHandler.deserialize(
        BannerFontHandler.serialize(font)
    ) == BannerFontHandler.deserialize(font_ref)
