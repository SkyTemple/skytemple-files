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

try:
    from PIL import Image
except ImportError:
    from pil import Image
from ndspy.rom import NintendoDSRom

from skytemple_files.graphics.kao.handler import KaoHandler

dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(dir, 'skyworkcopy_edit.nds'))

kao_data = rom.getFileByName('FONT/kaomado.kao')
kao = KaoHandler.deserialize(kao_data)
#kao.get(427, 0).get().show()
with open(os.path.join(dir, 'kaomado.kao'), 'wb') as f:
    f.write(kao_data)

with open(os.path.join(dir, 'dh', 'new427.png'), 'rb') as f:
    i = Image.open(f)
    kao.get(427, 0).set(i)
    kao.get(427, 2).set(i)

with open(os.path.join(dir, 'dh', 'new051.png'), 'rb') as f:
    i = Image.open(f)
    kao.get(51, 0).set(i)
    kao.get(51, 2).set(i)

with open(os.path.join(dir, 'dh', 'new468.png'), 'rb') as f:
    i = Image.open(f)
    kao.get(468, 0).set(i)

with open(os.path.join(dir, 'dh', 'new265.png'), 'rb') as f:
    i = Image.open(f)
    kao.get(265, 0).set(i)

with open(os.path.join(dir, 'dh', 'new040.png'), 'rb') as f:
    i = Image.open(f)
    kao.get(40, 0).set(i)

with open(os.path.join(dir, 'dh', 'new049.png'), 'rb') as f:
    i = Image.open(f)
    kao.get(49, 0).set(i)

with open(os.path.join(dir, 'dh', 'new533.png'), 'rb') as f:
    i = Image.open(f)
    kao.get(533, 0).set(i)

with open(os.path.join(dir, 'dh', 'new039.png'), 'rb') as f:
    i = Image.open(f)
    kao.get(39, 0).set(i)

kao_data_new = KaoHandler.serialize(kao)
#kao.get(427, 0).get().show()
rom.setFileByName('FONT/kaomado.kao', kao_data_new)
with open(os.path.join(dir, 'kaomado_edit.kao'), 'wb') as f:
    f.write(kao_data_new)

with open(os.path.join(dir, 'dh', 'text_e.str'), 'rb') as f:
    rom.setFileByName('MESSAGE/text_e.str', f.read())

rom.saveToFile(os.path.join(dir, 'skyworkcopy_edit.nds'))

# Test
kao_data = rom.getFileByName('FONT/kaomado.kao')
kao = KaoHandler.deserialize(kao_data)
kao.get(427, 0).get().show()
kao.get(51, 0).get().show()
kao.get(468, 0).get().show()
kao.get(265, 0).get().show()
kao.get(40, 0).get().show()
kao.get(49, 0).get().show()
kao.get(533, 0).get().show()
kao.get(39, 0).get().show()
