import os

from PIL import Image
from ndspy.rom import NintendoDSRom

from skytemple_files.graphics.bgp.handler import BgpHandler

os.makedirs(os.path.join(os.path.dirname(__file__), 'dbg_output'), exist_ok=True)

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

file_list = [
    'BACK/s09p01a.bgp',
    'BACK/s09p02a.bgp',
    'BACK/s09p03a.bgp',
    'BACK/s09p04a.bgp',
    'BACK/s09p05a.bgp',
    'BACK/s09p06a.bgp',
    'BACK/s09p07a.bgp',
    'BACK/s09p08a.bgp',
    'BACK/s09p09a.bgp',
    'BACK/s09p10a.bgp'
]

with open(os.path.join(base_dir, 'dh', 'ph.png'), 'rb') as f:
    img = Image.open(f)

    for filename in file_list:
        print("Processing " + filename)

        bin_before = rom.getFileByName(filename)
        bgp = BgpHandler.deserialize(bin_before)

        bgp.from_pil(img)
        img_after = bgp.to_pil()
        bin_after = BgpHandler.serialize(bgp)

        rom.setFileByName(filename, bin_after)


rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))