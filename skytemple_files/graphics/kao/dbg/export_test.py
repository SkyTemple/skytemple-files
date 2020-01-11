import os

from PIL import Image
from bitstring import BitStream
from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from skytemple_files.graphics.kao.handler import KaoHandler

os.makedirs(os.path.join(os.path.dirname(__file__), 'dbg_output'), exist_ok=True)

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bin = rom.getFileByName('FONT/kaomado.kao')

kao = KaoHandler.deserialize(BitStream(bin))

for idx, subidx, kao_image in kao:
    if kao_image:
        im = kao_image.get()
        at4px_before = FileType.AT4PX.deserialize(kao_image.compressed_img_data)
        # Test replacing the image (with the old one, so should be the same result)
        kao_image.set(im)
        at4px_after = FileType.AT4PX.deserialize(kao_image.compressed_img_data)
        im_after = kao_image.get()
        im_after.save(f'/tmp/{idx}_{subidx}.png')
        im.save(os.path.join(os.path.dirname(__file__), 'dbg_output', f'{idx}_{subidx}.png'))
        print(f"== {idx} - {subidx} ==")
        print(f"Size before: {at4px_before.length_compressed}")
        print(f"Size after : {at4px_after.length_compressed}")
