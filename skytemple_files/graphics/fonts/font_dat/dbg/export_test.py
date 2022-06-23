#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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
# mypy: ignore-errors

from __future__ import annotations

import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import get_ppmdu_config_for_rom
from skytemple_files.common.xml_util import prettify
from skytemple_files.graphics.fonts.font_dat.handler import FontDatHandler

base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")
out_dir = os.path.join(os.path.dirname(__file__), "dbg_output")
os.makedirs(out_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, "skyworkcopy_us.nds"))
config = get_ppmdu_config_for_rom(rom)

for fn in ["FONT/kanji_rd.dat", "FONT/unkno_rd.dat"]:
    font = FontDatHandler.deserialize(rom.getFileByName(fn))
    xml, tables = font.export_to_xml()
    with open(os.path.join(out_dir, fn.replace("/", "_") + f".xml"), "w") as f:
        f.write(prettify(xml))
    for i, table in tables.items():
        table.save(os.path.join(out_dir, fn.replace("/", "_") + f".{i}.png"))
    assert font == FontDatHandler.deserialize(FontDatHandler.serialize(font))
