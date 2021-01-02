"""Exports all DPCIs from the dungeon.bin"""
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
import itertools
import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import get_ppmdu_config_for_rom
from skytemple_files.container.dungeon_bin.handler import DungeonBinHandler
from skytemple_files.graphics.dpc.model import Dpc
from skytemple_files.graphics.dpci.model import Dpci
from skytemple_files.graphics.dpl.model import Dpl
from skytemple_files.graphics.dpla.model import Dpla

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(os.path.join(output_dir, 'ani'), exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))

dungeon_bin_bin = rom.getFileByName('DUNGEON/dungeon.bin')
static_data = get_ppmdu_config_for_rom(rom)
dungeon_bin = DungeonBinHandler.deserialize(dungeon_bin_bin, static_data)

for i, file in enumerate(dungeon_bin):
    fn = dungeon_bin.get_filename(i)
    if fn.endswith('.dpc'):
        file: Dpc
        pal_file: Dpl = dungeon_bin.get(fn.replace('.dpc', '.dpl'))
        ani_pal_file: Dpla = dungeon_bin.get(fn.replace('.dpc', '.dpla'))
        dpci: Dpci = dungeon_bin.get(fn.replace('.dpc', '.dpci'))
        fn = fn.replace('dungeon', 'tileset')
        print(fn)

        images = []
        base_img = file.chunks_to_pil(dpci, pal_file.palettes)
        images.append(base_img)

        base_img.save(os.path.join(output_dir, fn + '.png'))

        # Pal ani
        number_frames = int(len(ani_pal_file.colors[0]) / 3)
        has_a_second_palette = len(ani_pal_file.colors) > 16 and len(ani_pal_file.colors[16]) > 0

        for fidx in range(0, number_frames):
            pal_copy = pal_file.palettes.copy()
            img_copy = base_img.copy()
            # Put palette 11
            pal_copy[10] = ani_pal_file.get_palette_for_frame(0, fidx)
            if has_a_second_palette:
                # Put palette 12
                pal_copy[11] = ani_pal_file.get_palette_for_frame(1, fidx)
            img_copy.putpalette(itertools.chain.from_iterable(pal_copy))
            images.append(img_copy)

        images[0].save(
            os.path.join(output_dir, 'ani', fn + '.gif'),
            save_all=True,
            append_images=images[1:],
            duration=40,
            loop=0,
            optimize=False
        )