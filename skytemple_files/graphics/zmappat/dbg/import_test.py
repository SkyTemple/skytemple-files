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
# mypy: ignore-errors

from __future__ import annotations

import os

from ndspy.rom import NintendoDSRom
from PIL import Image

from skytemple_files.graphics.zmappat.handler import ZMappaTHandler

base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")
out_dir = os.path.join(os.path.dirname(__file__), "dbg_output")
os.makedirs(out_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, "skyworkcopy_us.nds"))

tiles = []
masks = []
for i in range(3):
    fn = f"dungeon.bin__minimap.zmappat.img-{i}.png"
    tiles.append(Image.open(os.path.join(out_dir, fn), "r"))
    fn = f"dungeon.bin__minimap.zmappat.mask-{i}.png"
    masks.append(Image.open(os.path.join(out_dir, fn), "r"))
zmappat = ZMappaTHandler.new(tiles, masks, False)
tiles = []
masks = []
for i in range(3):
    fn = f"dungeon.bin__minimap.zmappat.img-min-{i}.png"
    tiles.append(Image.open(os.path.join(out_dir, fn), "r"))
    fn = f"dungeon.bin__minimap.zmappat.mask-min-{i}.png"
    masks.append(Image.open(os.path.join(out_dir, fn), "r"))
zmappat_min = ZMappaTHandler.new(tiles, masks, True)
assert zmappat == zmappat_min
with open(os.path.join(out_dir, "dungeon.bin__minimap.zmappat"), "rb") as f:
    zmappat_ref = ZMappaTHandler.deserialize(f.read())
    f.close()
assert zmappat_min == zmappat_ref
