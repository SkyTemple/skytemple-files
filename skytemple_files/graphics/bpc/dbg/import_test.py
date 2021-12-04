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
# mypy: ignore-errors

import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import get_files_from_rom_with_extension
from skytemple_files.graphics.bpc.handler import BpcHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

for filename in get_files_from_rom_with_extension(rom, 'bpc'):
    bin_before = rom.getFileByName(filename)
    bpc_before = BpcHandler.deserialize(bin_before)
    print(f"Processing {filename} ({bpc_before.number_of_layers})")

    bin_after = BpcHandler.serialize(bpc_before)

    rom.setFileByName(filename, bin_after)
    #rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
    #rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))

    bpc_after = BpcHandler.deserialize(rom.getFileByName(filename))

    assert bpc_before.number_of_layers == bpc_after.number_of_layers
    for layer in range(0, bpc_before.number_of_layers):
        assert len(bpc_before.layers[layer].tiles) == len(bpc_after.layers[layer].tiles)
        for i in range(0, len(bpc_before.layers[layer].tiles)):
            assert bpc_before.layers[layer].tiles[i] == bpc_after.layers[layer].tiles[i]
        assert len(bpc_before.layers[layer].tilemap) == len(bpc_after.layers[layer].tilemap)
        for i in range(0, len(bpc_before.layers[layer].tilemap)):
            assert bpc_before.layers[layer].tilemap[i].to_int() == bpc_after.layers[layer].tilemap[i].to_int()
        assert bpc_before.layers[layer].number_tiles == bpc_after.layers[layer].number_tiles
        assert bpc_before.layers[layer].bpas == bpc_after.layers[layer].bpas
        assert bpc_before.layers[layer].chunk_tilemap_len == bpc_after.layers[layer].chunk_tilemap_len
    assert len(bin_before) % 2 == 0
    assert bpc_before._lower_layer_pointer % 2 == 0
    assert bpc_before._upper_layer_pointer % 2 == 0
    assert len(bin_after) % 2 == 0
    assert bpc_after._lower_layer_pointer % 2 == 0
    assert bpc_after._upper_layer_pointer % 2 == 0

    bin_after2 = BpcHandler.serialize(bpc_before)
    assert bin_after == bin_after2

    rom.setFileByName(filename, bin_after)


rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
