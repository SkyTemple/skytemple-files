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

from skytemple_files.graphics.w16.handler import W16Handler
from skytemple_files.graphics.w16.model import W16Image

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

filenames = ['rankmark', 'clrmark1', 'clrmark2']

for fn in filenames:
    bin = rom.getFileByName(f'FONT/{fn}.w16')
    w16 = W16Handler.deserialize(bin)
    for i, img in enumerate(w16):
        img: W16Image
        im = img.get()
        print(fn, i, img.entry_data.width, img.entry_data.height)
        im.save(f'/tmp/{fn}_{i:03}.png')
