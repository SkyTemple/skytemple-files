#  Copyright 2020 Parakoopa
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
from skytemple_files.graphics.wte.handler import WteHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
out_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
os.makedirs(out_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))

original = WteHandler.deserialize(rom.getFileByName('FONT/frame.wte'))
fake = WteHandler.new(original.to_pil(), original.identifier)

original.to_pil().save(os.path.join(out_dir, 'original.png'))
fake.to_pil().save(os.path.join(out_dir, 'fake.png'))

assert original.identifier == fake.identifier
assert original.image_data == fake.image_data
assert original.palette == fake.palette

for fn in ['FONT/frame.wte', 'FONT/frame0.wte', 'FONT/frame1.wte',
           'FONT/frame2.wte', 'FONT/frame3.wte', 'FONT/frame4.wte']:
    fake = WteHandler.new(original.to_pil(), original.identifier)
    original = WteHandler.deserialize(rom.getFileByName(fn))
    new = WteHandler.new(Image.open(os.path.join(out_dir, 'frame_import.png')), original.identifier)
    pal = new.palette
    new.palette = original.palette
    new.palette[0*16*3:1*16*3] = pal[0*16*3:1*16*3]
    new.palette[1*16*3:2*16*3] = pal[0*16*3:1*16*3]
    new.palette[2*16*3:3*16*3] = pal[0*16*3:1*16*3]
    new.palette[3*16*3:4*16*3] = pal[0*16*3:1*16*3]
    new.to_pil().save(os.path.join(out_dir, fn.replace('/', '_') + '.mod.png'))

    rom.setFileByName(fn, WteHandler.serialize(new))

rom.saveToFile(os.path.join(out_dir, 'wte_test.nds'))
