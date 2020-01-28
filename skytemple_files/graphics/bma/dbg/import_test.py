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

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import get_files_from_rom_with_extension
from skytemple_files.graphics.bma.handler import BmaHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

for filename in get_files_from_rom_with_extension(rom, 'bma'):
    bin_before = rom.getFileByName(filename)
    bma_before = BmaHandler.deserialize(bin_before)
    print(f"Processing {filename} ({bma_before.number_of_layers})")

    #if bma_before.number_of_collision_layers > 0:
    #    bma_before.collision = [0 for _ in range(0, len(bma_before.collision))]

    bin_after = BmaHandler.serialize(bma_before)
    bma_after = BmaHandler.deserialize(bin_after)

    #with open('/tmp/before.bin', 'wb') as f:
    #    f.write(bin_before)
    #with open('/tmp/after.bin', 'wb') as f:
    #    f.write(bin_after)

    assert bma_before.map_width_camera == bma_after.map_width_camera
    assert bma_before.map_height_camera == bma_after.map_height_camera
    assert bma_before.tiling_width == bma_after.tiling_width
    assert bma_before.tiling_height == bma_after.tiling_height
    assert bma_before.map_width_chunks == bma_after.map_width_chunks
    assert bma_before.map_height_chunks == bma_after.map_height_chunks
    assert bma_before.number_of_layers == bma_after.number_of_layers
    assert bma_before.unk6 == bma_after.unk6
    assert bma_before.number_of_collision_layers == bma_after.number_of_collision_layers
    assert bma_before.layer0 == bma_after.layer0
    assert bma_before.layer1 == bma_after.layer1
    assert bma_before.unknown_data_block == bma_after.unknown_data_block
    assert bma_before.collision == bma_after.collision
    assert bma_before.collision2 == bma_after.collision2

    print(f"Size change: {len(bin_after)-len(bin_before)}")

    rom.setFileByName(filename, bin_after)


rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
