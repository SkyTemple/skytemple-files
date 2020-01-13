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
    bpc_after = BpcHandler.deserialize(bin_after)

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

    rom.setFileByName(filename, bin_after)


rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
