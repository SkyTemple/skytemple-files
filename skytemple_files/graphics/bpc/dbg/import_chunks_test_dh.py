import os

from PIL import Image
from ndspy.rom import NintendoDSRom

from skytemple_files.graphics.bpc.handler import BpcHandler
from skytemple_files.graphics.bpl.handler import BplHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bpl = BplHandler.deserialize(rom.getFileByName('MAP_BG/p01p01a.bpl'))

bin_before = rom.getFileByName('MAP_BG/p01p01a.bpc')
bpc_before = BpcHandler.deserialize(bin_before)
bpc_before.chunks_to_pil(1, bpl.palettes).show()

with open(os.path.join(base_dir, 'dh', 'P01P01A.1.png'), 'rb') as f:
    bpc_before.pil_to_chunks(1, Image.open(f))

bin_after = BpcHandler.serialize(bpc_before)
bpc_after = BpcHandler.deserialize(bin_after)
bpc_after.chunks_to_pil(1, bpl.palettes).show()

rom.setFileByName('MAP_BG/p01p01a.bpc', bin_after)


rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
