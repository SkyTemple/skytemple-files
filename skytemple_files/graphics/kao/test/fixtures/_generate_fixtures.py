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
from __future__ import annotations

import os
from random import randrange

from ndspy.rom import NintendoDSRom
from PIL import Image, ImageDraw

from skytemple_files.graphics.kao.handler import KaoHandler

rom: NintendoDSRom = NintendoDSRom.fromFile(os.path.join('..', '..', '..', '..', '..', '..', 'CLEAN_ROM', 'pmdsky.nds'))

kao = KaoHandler.deserialize(rom.getFileByName('FONT/kaomado.kao'))

for idx, sidx, img in kao:
    print(idx, sidx, img)
    pil = Image.new('P', (40, 40))
    pal = bytearray()
    pil.putpalette([randrange(0, 256) for _ in range(0, 256 * 3)])
    for i in range(0, 15):
        pil.putpixel((i, 0), i)
    d = ImageDraw.Draw(pil)
    d.text((5, 5), str(idx), fill=1)
    d.text((5, 20), str(sidx), fill=2)
    if img is not None:
        img.set(pil)
    if idx in (0, 552, 1153):
        os.makedirs(f'rgb/{idx:04}', exist_ok=True)
        os.makedirs(f'{idx:04}', exist_ok=True)
        pil.save(f'{idx:04}/{sidx:02}.png')
        pil.convert('RGB').save(f'rgb/{idx:04}/{sidx:02}.png')

with open('kaomado.kao', 'wb') as f:
    f.write(KaoHandler.serialize(kao))
