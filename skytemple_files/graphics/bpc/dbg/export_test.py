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
import traceback
import time

from ndspy.rom import NintendoDSRom

from skytemple_files.graphics.bg_list_dat.handler import BgListDatHandler

def main():
    os.makedirs(os.path.join(os.path.dirname(__file__), 'dbg_output'), exist_ok=True)

    base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

    rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
    prf('opening rom')

    bin = rom.getFileByName('MAP_BG/bg_list.dat')
    prf('loading level list')
    bg_list = BgListDatHandler.deserialize(bin)
    prf('deserializing level list')

    for l in bg_list.level:
        filename = l.bpc_name
        prf(f'loading {filename}')
        #if filename != 'D15P21A' and filename != 'D17P34A' and
        #if filename != 'D01P41A':  # beach cave boss area
        #    continue
        # debug map: T00P01
        # crossroads: P01P01A
        if filename != 'P01P01A':
            continue
        try:
            filename_h = os.path.join(os.path.dirname(__file__), 'dbg_output', filename.replace('/', '_'))

            bma = l.get_bma(rom)
            prf(f'loading {filename} BMA')
            bpc = l.get_bpc(rom, bma.tiling_width, bma.tiling_height)
            prf(f'loading {filename} BPC')
            bpl = l.get_bpl(rom)
            prf(f'loading {filename} BPL')

            # Print debug information
            print(f"{l}")
            print(f"{filename} ({bpc.number_of_layers}): "
                  f"UP: {bpc._upper_layer_pointer} - "
                  f"LW: {bpc._lower_layer_pointer} - "
                  f"LayerSpec: {bpc.layers}")

            # Palettes!
            palettes = bpl.palettes

            prf(f'setting up for {filename} image export, including BPA load')
            bpas = l.get_bpas(rom)
            non_none_bpas = [b for b in bpas if b is not None]
            for n in range(0, bpc.number_of_layers):
                # Save tiles!
                bpc.tiles_to_pil(n, palettes).save(filename_h + '.' + str(n) + '.tiles.png')
                prf(f'saving tiles for {filename}')
                # Save chunks!
                bpc.chunks_to_pil(n, palettes).save(filename_h + '.' + str(n) + '.png')
                prf(f'saving chunks for {filename}')
                # Saving animated chunks!
                # Default for only one frame, doesn't really matter
                duration = 1000
                if len(non_none_bpas) > 0:
                    # Assuming the game runs 60 FPS.
                    duration = round(1000 / 60 * non_none_bpas[0].frame_info[0].duration_per_frame)
                frames = bpc.chunks_animated_to_pil(n, palettes, bpas)
                frames[0].save(
                    filename_h + '.' + str(n) + '.gif',
                    save_all=True,
                    append_images=frames[1:],
                    duration=duration,
                    loop=0,
                    optimize=False
                )
                prf(f'saving animated chunks for {filename}')

        except (ValueError, AssertionError, NotImplementedError, SystemError) as ex:
            prf(f'error for {filename}')
            print(f"error for {filename}:")
            print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))


last_time = time.time()


def prf(name):
    global last_time
    new_time = time.time()
    print(f">>>>>> {name} took {int(round((new_time - last_time) * 1000))}ms")
    last_time = new_time


if __name__ == '__main__':
    main()
