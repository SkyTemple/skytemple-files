#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
# mypy: ignore-errors

import os
import traceback

from ndspy.rom import NintendoDSRom

from skytemple_files.graphics.bg_list_dat.handler import BgListDatHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
dbg_output = os.path.join(os.path.dirname(__file__), 'dbg_output')
os.makedirs(dbg_output, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))

bin = rom.getFileByName('MAP_BG/bg_list.dat')
bg_list = BgListDatHandler.deserialize(bin)

for i, l in enumerate(bg_list.level):
    if len(l.bpa_names) < 1:
        continue
    try:
        bpl = l.get_bpl(rom)

        for j, bpa in enumerate(l.get_bpas(rom)):
            if bpa is not None:
                print(f"{i},{j} (bma: {l.bma_name}) - {l.bpa_names[j]}: {bpa}")  # - BPC LayerSpec: {bpc.layers}

                bpa.tiles_to_pil(bpl.palettes[0]).save(os.path.join(dbg_output, f'{l.bpa_names[j]}.png'))

                frames = bpa.tiles_to_pil_separate(bpl.palettes[0])
                frames[0].save(
                    os.path.join(dbg_output, f'{l.bpa_names[j]}.gif'),
                    save_all=True,
                    append_images=frames[1:],
                    duration=(1000 / 60) * bpa.frame_info[0].duration_per_frame,
                    loop=0,
                    optimize=False
                )

    except (ValueError, AssertionError, SystemError) as ex:
        print(f"error for {l.bma_name}:")
        print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))
