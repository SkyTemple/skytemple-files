#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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

from skytemple_files.common.types.file_types import FileType
from skytemple_files.graphics.kao.handler import KaoHandler

os.makedirs(os.path.join(os.path.dirname(__file__), 'dbg_output'), exist_ok=True)

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bin = rom.getFileByName('FONT/kaomado.kao')

kao = KaoHandler.deserialize(bin)

data_length_before = 0
data_length_after = 0
for idx, subidx, kao_image in kao:
    if kao_image:
        print(f"== {idx} - {subidx} ==")
        im = kao_image.get()
        at_before = FileType.COMMON_AT.deserialize(kao_image.compressed_img_data)
        print(f"Size before: {at_before.length_compressed}")
        data_length_before += at_before.length_compressed
        # Test replacing the image (with the old one, so should be the same result)
        kao_image.set(im)
        at_after = FileType.COMMON_AT.deserialize(kao_image.compressed_img_data)
        im_after = kao_image.get()
        im_after.save(f'/tmp/{idx}_{subidx}.png')
        im.save(os.path.join(os.path.dirname(__file__), 'dbg_output', f'{idx}_{subidx}.png'))
        data_length_after += at_after.length_compressed
        print(f"Size after : {at_after.length_compressed}")
print(f"== WHOLE KAO ==")
print(f"Size before: {data_length_before}")
print(f"Size after : {data_length_after}")
