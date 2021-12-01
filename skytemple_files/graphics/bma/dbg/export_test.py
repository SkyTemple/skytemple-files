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
os.makedirs(os.path.join(os.path.dirname(__file__), 'dbg_output'), exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))

bin = rom.getFileByName('MAP_BG/bg_list.dat')
bg_list = BgListDatHandler.deserialize(bin)

for i, l in enumerate(bg_list.level):
    maps = [
        #'P01P01A',  # OK: Map with collision
        #'T00P03',   # OK: Map with an odd amount of chunks in width
        #'D01P11B',  # OK: Map with an odd amount of chunks in width and collision
        #'G01P03A',  # OK: Map with unk6 != 0
        #'D01P41A',  # OK: Map with weird collision for no reason?
        #'D06P11A',  # OK: Map weirdly broken (layer 2 and onwards maybe? - Alignment?)
        #'D08P11A',  # OK: Broken map with odd amount of chunks and width AND height
        #'D17P31A',  # OK: Weird lower layer. 2nd BPA seems to be the issue
        #'D22P11A',  # OK: Broken collision (with odd amount of chunks and width AND height)
        #'P19P02A',  # OK: Map with odd amount of chunks in height and collision
        #'H01P99A',  # OK: Weird lower layer. 2nd BPA seems to be the issue
        #'G01P08A',  # OK: Wrong collision length. Why? [reason was failed dimension assertion, see model]
        #'V10P03C',  #     broken tiles?
        #'D28P32A',  #     broken tiles?
        #'P17P02A',  # OK: For below: Collision is 0x0002
        #'D47P11A',
        #'D31P11A',
        #'D79P11A'
    ]
    #if l.bma_name not in maps:
    #    continue
    try:
        filename_h = os.path.join(os.path.dirname(__file__), 'dbg_output', l.bma_name.replace('/', '_'))
        # S05P01A : Logos
        bma = l.get_bma(rom)
        print(f"{i} - {l.bma_name}: {bma} - BG List: {l}")
        try:
            assert bma.map_width_camera == bma.map_width_chunks * bma.tiling_width
            assert bma.map_height_camera == bma.map_height_chunks * bma.tiling_height
        except AssertionError:
            print("DIMENSION ASSERTION FAILED")
        setattr(bma, 'dbg_name', l.bma_name)

        bpas = l.get_bpas(rom)
        non_none_bpas = [b for b in bpas if b is not None]
        bpc = l.get_bpc(rom)
        bpl = l.get_bpl(rom)

        # Saving single frames
        bma.to_pil_single_layer(bpc, bpl.palettes, bpas, 0).save(filename_h + '_LOWER.png')
        if bma.number_of_layers > 1:
            bma.to_pil_single_layer(bpc, bpl.palettes, bpas, 1).save(filename_h + '_HIGHER.png')

        # Saving animated map!
        bpa_duration = -1
        pal_ani_duration = -1
        if len(non_none_bpas) > 0:
            # Assuming the game runs 60 FPS.
            bpa_duration = round(1000 / 60 * non_none_bpas[0].frame_info[0].duration_per_frame)
        if bpl.has_palette_animation:
            pal_ani_duration = round(1000 / 60 * max(spec.duration_per_frame for spec in bpl.animation_specs))
        duration = max(bpa_duration, pal_ani_duration)
        if duration == -1:
            # Default for only one frame, doesn't really matter
            duration = 1000
        frames = bma.to_pil(bpc, bpl, bpas, include_collision=False, include_unknown_data_block=False)
        frames[0].save(
            filename_h + '.gif',
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            optimize=False
        )
        #for i, f in enumerate(frames):
        #    f.save(filename_h + '.' + str(i) + '.png')
    except (NotImplementedError, SystemError) as ex:
        print(f"error for {l.bma_name}: {repr(ex)}")
        print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))
