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

import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_files_from_rom_with_extension, get_ppmdu_config_for_rom
from skytemple_files.graphics.chr.handler import ChrHandler
from skytemple_files.graphics.pal.handler import PalHandler

try:
    from PIL import Image
except ImportError:
    from pil import Image

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
out_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
os.makedirs(out_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))
config = get_ppmdu_config_for_rom(rom)

for fn in get_files_from_rom_with_extension(rom, 'chr'):
    font = ChrHandler.deserialize(rom.getFileByName(fn))
    pal = PalHandler.deserialize(rom.getFileByName(fn[:-4]+".pal"))
    font_ref = rom.getFileByName(fn)
    pal_ref = rom.getFileByName(fn[:-4]+".pal")
    font.set_palette(pal)
    path = os.path.join(out_dir, fn.replace('/', '_') + f'.png')
    font.from_pil(Image.open(path, 'r'))
    with open("test.dat", "wb") as f:
        f.write(ChrHandler.serialize(font))
    assert PalHandler.serialize(pal)==pal_ref
    assert ChrHandler.serialize(font)==font_ref
