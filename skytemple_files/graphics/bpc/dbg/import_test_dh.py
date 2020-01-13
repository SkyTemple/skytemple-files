import os

from PIL import Image
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
