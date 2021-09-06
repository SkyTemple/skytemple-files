#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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

try:
    from PIL import Image
except ImportError:
    from pil import Image
from ndspy.rom import NintendoDSRom

from skytemple_files.graphics.bgp.handler import BgpHandler

os.makedirs(os.path.join(os.path.dirname(__file__), 'dbg_output'), exist_ok=True)

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

file_list = [
    'BACK/s09p01a.bgp',
    'BACK/s09p02a.bgp',
    'BACK/s09p03a.bgp',
    'BACK/s09p04a.bgp',
    'BACK/s09p05a.bgp',
    'BACK/s09p06a.bgp',
    'BACK/s09p07a.bgp',
    'BACK/s09p08a.bgp',
    'BACK/s09p09a.bgp',
    'BACK/s09p10a.bgp'
]

with open(os.path.join(base_dir, 'dh', 'ph.png'), 'rb') as f:
    img = Image.open(f)

    for filename in file_list:
        filename_h = os.path.join(os.path.dirname(__file__), 'dbg_output', filename.replace('/', '_'))
        print("Processing " + filename)

        bin_before = rom.getFileByName(filename)
        bgp = BgpHandler.deserialize(bin_before)

        bgp.from_pil(img)
        img_after = bgp.to_pil()
        bin_after = BgpHandler.serialize(bgp)
        bgp.to_pil().save(filename_h + '.png')

        rom.setFileByName(filename, bin_after)


rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))