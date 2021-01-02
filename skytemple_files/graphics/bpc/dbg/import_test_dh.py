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

from skytemple_files.common.util import get_files_from_rom_with_extension
from skytemple_files.graphics.bpc.handler import BpcHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bin_before = rom.getFileByName('MAP_BG/p01p01a.bpc')
bpc_before = BpcHandler.deserialize(bin_before)

with open(os.path.join(base_dir, 'dh', 'P01P01A.1.tiles.png'), 'rb') as f:
    bpc_before.pil_to_tiles(1, Image.open(f))

bin_after = BpcHandler.serialize(bpc_before)
bpc_after = BpcHandler.deserialize(bin_after)

rom.setFileByName('MAP_BG/p01p01a.bpc', bin_after)


rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
