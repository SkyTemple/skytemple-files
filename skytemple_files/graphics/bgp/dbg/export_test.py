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

import math
import os
from time import time

from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_files_from_rom_with_extension
from skytemple_files.graphics.bgp.handler import BgpHandler
from skytemple_files.graphics.bgp.model import BGP_RES_WIDTH_IN_TILES

os.makedirs(os.path.join(os.path.dirname(__file__), 'dbg_output'), exist_ok=True)

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

for filename in get_files_from_rom_with_extension(rom, 'bgp'):
    print("Processing " + filename)
    filename_h = os.path.join(os.path.dirname(__file__), 'dbg_output', filename.replace('/', '_'))

    bin = rom.getFileByName(filename)
    with open(filename_h, 'wb') as f:
        tb = time()
        d = FileType.COMMON_AT.deserialize(bin).decompress()
        print(f"Decrompressing this takes {time() - tb}s.")
        f.write(d)

    bgp = BgpHandler.deserialize(bin)

    # Save as one big image
    bgp.to_pil().save(filename_h + '.png')

    # Save as tiles
    tile_dir = filename_h + '.tiles'
    os.makedirs(tile_dir, exist_ok=True)
    for i, img in enumerate(bgp.to_pil_tiled()):
        tile_x = i % BGP_RES_WIDTH_IN_TILES
        tile_y = math.floor(i / BGP_RES_WIDTH_IN_TILES)
        img.save(os.path.join(tile_dir, f'{tile_x}_{tile_y}.png'))

