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

from PIL import Image
from ndspy.rom import NintendoDSRom

from skytemple_files.graphics.w16.handler import W16Handler
from skytemple_files.graphics.w16.model import W16Image

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))


origs = []

filenames = ['FONT/rankmark.w16', 'FONT/clrmark1.w16', 'FONT/clrmark2.w16']

for fn in filenames:
    bin_before = rom.getFileByName(fn)
    w16 = W16Handler.deserialize(bin_before)
    for i, img in enumerate(w16):
        orig = img.get()
        origs.append(orig)
        im = img.set(orig)

    rom.setFileByName(fn, W16Handler.serialize(w16))

    # test & verify
    bin_after = rom.getFileByName(fn)
    w16 = W16Handler.deserialize(bin_after)

    with open(f'/tmp/before.bin', 'wb') as f:
        f.write(bin_before)

    with open(f'/tmp/after.bin', 'wb') as f:
        f.write(bin_after)

    for i, img in enumerate(w16):
        im = img.get()
        #assert im == origs[i]
    #assert bin_before == bin_after

rom.saveToFile('/tmp/w16test.nds')
