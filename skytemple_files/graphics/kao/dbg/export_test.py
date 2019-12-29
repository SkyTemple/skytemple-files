from PIL import Image
from bitstring import BitStream

from skytemple_files.common.types.file_types import FileType
from skytemple_files.graphics.kao.handler import KaoHandler

with open('/tmp/sky/data/FONT/kaomado.kao', 'rb') as f:
    bin = f.read()

kao = KaoHandler.unserialize(BitStream(bin))

for idx, subidx, kao_image in kao:
    if kao_image:
        im = kao_image.get()
        at4px_before = FileType.AT4PX.unserialize(kao_image.compressed_img_data)
        # Test replacing the image (with the old one, so should be the same result)
        #kao_image.set(im)
        #at4px_after = FileType.AT4PX.unserialize(kao_image.compressed_img_data)
        #im_after = kao_image.get()
        #im_after.save(f'/tmp/{idx}_{subidx}.png')
        im.save(f'/tmp/{idx}_{subidx}.png')
        print(f"== {idx} - {subidx} ==")
        print(f"Size before: {at4px_before.length_compressed}")
        #print(f"Size after : {at4px_after.length_compressed}")
exit()

kao_image = kao.get(0, 0)
if kao_image:
    at4px_before = FileType.AT4PX.unserialize(kao_image.compressed_img_data)
    im_before = kao_image.get()
    #im_before.show('before')
    im_before.save('/tmp/out.png')
    # Test replacing the image (with the old one, so should be the same result)
    with open('/tmp/out.png', 'rb') as f:
        im_before_reopened = Image.open(f)
        kao_image.set(im_before_reopened)
    at4px_after = FileType.AT4PX.unserialize(kao_image.compressed_img_data)
    im_after = kao_image.get()
    im_after.show('after')
    print(f"Size before: {at4px_before.length_compressed}")
    print(f"Size after : {at4px_after.length_compressed}")
