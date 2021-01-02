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
from skytemple_files.graphics.fonts.graphic_font.handler import GraphicFontHandler
from skytemple_files.graphics.pal.handler import PalHandler

try:
    from PIL import Image
except ImportError:
    from pil import Image

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
out_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
os.makedirs(out_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))

for fn in ["FONT/staffont", "FONT/markfont"]:
    font_ref = rom.getFileByName(fn+".dat")
    font = GraphicFontHandler.deserialize(font_ref)
    pal_ref = rom.getFileByName(fn+".pal")
    pal = PalHandler.deserialize(pal_ref)
    font.set_palette(pal)
    lst_entries = []
    for i in range(font.get_nb_entries()):
        path = os.path.join(out_dir, fn.replace('/', '_') + f'_{i:0>4}.png')
        if os.path.exists(path):
            lst_entries.append(Image.open(path, 'r'))
        else:
            lst_entries.append(None)
    font.set_entries(lst_entries)
    assert GraphicFontHandler.serialize(font)==font_ref
