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
from skytemple_files.graphics.bpl.handler import BplHandler

os.makedirs(os.path.join(os.path.dirname(__file__), 'dbg_output'), exist_ok=True)

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

for filename in get_files_from_rom_with_extension(rom, 'bpl'):
    filename_h = os.path.join(os.path.dirname(__file__), 'dbg_output', filename.replace('/', '_'))

    bin = rom.getFileByName(filename)
    bpl = BplHandler.deserialize(bin)

    # Print debug information about palette
    print(f"{filename}: "
          f"NoPal: {bpl.number_palettes} - "
          f"2ndCT?: {bpl.has_palette_animation} - "
          f"2ndCT: {bpl.animation_specs}")

    # Experiment: Assume the extra colors are actually an image
    #             and the entry in the index table the dimensions...
    # RESULT: From looking at this, I think this is actually part of a palette animation!
    #if bpl.has_palette_animation:
    #    rgb = bytes(bytearray(chain.from_iterable(bpl.extra_colors)))
    #    for e in bpl.extra_color_index_table:
    #        if e.color_index != 0:
    #            im = Image.frombuffer('RGB', (e.duration_per_frame, e.color_index), rgb, 'raw', 'RGB', 0, 1)
    #            im.resize((im.size[0]*16, im.size[1]*16)).show()

    # Convert BPL to image
    # TODO (Palettes and extra palette)
