import os
import traceback

from bitstring import BitStream
from ndspy.rom import NintendoDSRom

from skytemple_files.unique.bg_list_dat.handler import BgListDatHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
dbg_output = os.path.join(os.path.dirname(__file__), 'dbg_output')
os.makedirs(dbg_output, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bin = BitStream(rom.getFileByName('MAP_BG/bg_list.dat'))
bg_list = BgListDatHandler.deserialize(bin)

for i, l in enumerate(bg_list.level):
    if len(l.bpa_names) < 1:
        continue
    try:
        bpl = l.get_bpl(rom)

        for j, bpa in enumerate(l.get_bpas(rom)):
            print(f"{i},{j} (bma: {l.bma_name}) - {l.bpa_names[j]}: {bpa}")  # - BPC LayerSpec: {bpc.layers}

            bpa.tiles_to_pil(bpl.palettes[0]).save(os.path.join(dbg_output, f'{l.bpa_names[j]}.png'))

    except (ValueError, AssertionError, SystemError) as ex:
        print(f"error for {l.bma_name}:")
        print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))
