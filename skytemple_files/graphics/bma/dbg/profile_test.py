"""Tests the speed of BMA export for performance increasing attempts"""

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

import os
import time

from ndspy.rom import NintendoDSRom

from skytemple_files.graphics.bg_list_dat.handler import BgListDatHandler


def main():

    base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
    os.makedirs(os.path.join(os.path.dirname(__file__), 'dbg_output'), exist_ok=True)

    rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

    bin = rom.getFileByName('MAP_BG/bg_list.dat')
    bg_list = BgListDatHandler.deserialize(bin)

    with open(os.path.join(os.path.dirname(__file__), 'dbg_output', 'profile_result.csv'), 'w+') as csv:
        csv.write('name,run,bma_load,bpa_load,bpc_load,bpl_load,bpc_tile_export,'
                  'bpc_chunk_export,bpc_animated_export,bma_export,bma_save\n')
        for i, l in enumerate(bg_list.level):
            maps = [
                'P01P01A', 'T00P03', 'D01P11B', 'G01P03A',
                'D01P41A', 'D06P11A', 'D08P11A', 'D17P31A',
                'D22P11A', 'P19P02A', 'H01P99A', 'G01P08A',
                'V10P03C', 'D28P32A', 'P17P02A', 'D47P11A',
                'D31P11A', 'D79P11A'
            ]
            if l.bma_name not in maps:
                continue
            # We profile each map 10 times
            for run in range(0, 10):
                filename_h = os.path.join(os.path.dirname(__file__), 'dbg_output', l.bma_name.replace('/', '_'))

                time_1_before_bma_load = time.time()
                bma = l.get_bma(rom)
                print(f"{i} - {l.bma_name}: {bma} - BG List: {l}")

                time_3_before_bpa_load = time.time()
                bpas = l.get_bpas(rom)
                time_4_before_bpc_load = time.time()
                bpc = l.get_bpc(rom)
                time_5_before_bpl_load = time.time()
                bpl = l.get_bpl(rom)

                # Profile BPC tile and chunk export
                time_6_before_bpc_tile_export = time.time()
                bpc.tiles_to_pil(0, bpl.palettes)
                if bpc.number_of_layers > 1:
                    bpc.tiles_to_pil(1, bpl.palettes)

                time_7_before_bpc_chunk_export = time.time()
                bpc.chunks_to_pil(0, bpl.palettes)
                if bpc.number_of_layers > 1:
                    bpc.chunks_to_pil(1, bpl.palettes)

                time_8_before_bpc_animated_chunk_export = time.time()
                bpc.chunks_animated_to_pil(0, bpl.palettes, bpas)
                if bpc.number_of_layers > 1:
                    bpc.chunks_animated_to_pil(1, bpl.palettes, bpas)

                # Saving animated map!
                # Default for only one frame, doesn't really matter
                duration = 1000
                if len(bpas) > 0:
                    # Assuming the game runs 60 FPS.
                    duration = round(1000 / 60 * bpas[0].frame_info[0].duration_per_frame)
                time_9_before_bma_export = time.time()
                frames = bma.to_pil(bpc, bpl, bpas)

                time_10_before_bma_save = time.time()
                frames[0].save(
                    filename_h + '.webp',
                    save_all=True,
                    append_images=frames[1:],
                    duration=duration,
                    loop=0,
                    optimize=False
                )
                for i, f in enumerate(frames):
                    f.save(filename_h + '.' + str(i) + '.png')
                time_11_after = time.time()
                # Write result
                csv.write(f'{l.bma_name},{run},'
                          f'{time_3_before_bpa_load-time_1_before_bma_load},'
                          f'{time_4_before_bpc_load-time_3_before_bpa_load},'
                          f'{time_5_before_bpl_load-time_4_before_bpc_load},'
                          f'{time_6_before_bpc_tile_export-time_5_before_bpl_load},'
                          f'{time_7_before_bpc_chunk_export-time_6_before_bpc_tile_export},'
                          f'{time_8_before_bpc_animated_chunk_export-time_7_before_bpc_chunk_export},'
                          f'{time_9_before_bma_export-time_8_before_bpc_animated_chunk_export},'
                          f'{time_10_before_bma_save-time_9_before_bma_export},'
                          f'{time_11_after-time_10_before_bma_save}\n')
                print(f"> run took {time_11_after-time_1_before_bma_load} seconds.")


if __name__ == '__main__':
    main()
