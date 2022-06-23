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

from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import (
    get_files_from_rom_with_extension,
    get_ppmdu_config_for_rom,
)
from skytemple_files.graphics.wte.handler import WteHandler

base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")
out_dir = os.path.join(os.path.dirname(__file__), "dbg_output")
os.makedirs(out_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, "skyworkcopy_us.nds"))
config = get_ppmdu_config_for_rom(rom)
dungeon_bin = FileType.DUNGEON_BIN.deserialize(
    rom.getFileByName("DUNGEON/dungeon.bin"), config
)

for fn in get_files_from_rom_with_extension(rom, "wte"):
    print(fn)
    wte = WteHandler.deserialize(rom.getFileByName(fn))
    wte.to_pil().save(os.path.join(out_dir, fn.replace("/", "_") + ".png"))
    print(wte)
    assert wte == WteHandler.deserialize(WteHandler.serialize(wte))

for i, file in enumerate(dungeon_bin):
    fn = dungeon_bin.get_filename(i)
    if fn.endswith(".wte"):
        print(f"dungeon.bin:{fn}")
        file.to_pil().save(
            os.path.join(out_dir, "dungeon.bin__" + fn.replace("/", "_") + ".png")
        )
        print(file)
        assert file == WteHandler.deserialize(WteHandler.serialize(file))
