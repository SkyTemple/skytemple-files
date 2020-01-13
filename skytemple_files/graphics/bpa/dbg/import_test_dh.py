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
