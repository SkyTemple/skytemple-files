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

from skytemple_files.graphics.bpa.handler import BpaHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bin_before = rom.getFileByName('MAP_BG/p01p01a1.bpa')
bpa_before = BpaHandler.deserialize(bin_before)

with open(os.path.join(base_dir, 'dh', 'P01P01A1.png'), 'rb') as f:
    bpa_before.pil_to_tiles(Image.open(f))

bin_after = BpaHandler.serialize(bpa_before)

rom.setFileByName('MAP_BG/p01p01a1.bpa', bin_after)


rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
