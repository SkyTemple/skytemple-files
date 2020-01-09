import os
import traceback

from bitstring import BitStream
from ndspy.rom import NintendoDSRom

from skytemple_files.unique.bg_list_dat.handler import BgListDatHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(os.path.join(os.path.dirname(__file__), 'dbg_output'), exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bin = BitStream(rom.getFileByName('MAP_BG/bg_list.dat'))
bg_list = BgListDatHandler.deserialize(bin)

possible_values_for_unk6 = {}
possible_values_for_unk7 = {}

for i, l in enumerate(bg_list.level):
    maps = [
        'P01P01A',  # OK: Map with collision
        'T00P03',   # OK: Map with an odd amount of chunks in width
        'D01P11B',  # OK: Map with an odd amount of chunks in width and collision
        'G01P03A',  #     Map with unk6 != 0
        'D01P41A',  #     Map with weird collision for no reason?
        'D06P11A',  #     Map weirdly broken (layer 2 and onwards maybe? - Alignment?)
        'D08P11A',  #     Broken map with odd amount of chunks and width AND height
        'D17P31A',  #     Completly destroyed (with odd amount of chunks and width AND height)
        'D22P11A',  #     Broken collision (with odd amount of chunks and width AND height)
        'P19P02A',  # OK: Map with odd amount of chunks in height and collision
        'H01P99A',  #     Map with an odd amount of chunks in width and collision, completely broken
    ]
    #if l.bma_name not in maps:
    #    continue
    if l.bma_name != 'H01P99A':
        continue
    try:
        filename_h = os.path.join(os.path.dirname(__file__), 'dbg_output', l.bma_name.replace('/', '_'))
        # S05P01A : Logos
        bma = l.get_bma(rom)
        print(f"{i} - {l.bma_name}: {bma}")
        try:
            assert bma.map_width_camera == bma.map_width_meta * bma.tiling_width
            assert bma.map_height_camera == bma.map_height_meta * bma.tiling_height
        except AssertionError:
            print("DIMENSION ASSERTION FAILED")
        if bma.unk6 not in possible_values_for_unk6:
            possible_values_for_unk6[bma.unk6] = []
        possible_values_for_unk6[bma.unk6].append(bma)
        if bma.unk7 not in possible_values_for_unk7:
            possible_values_for_unk7[bma.unk7] = []
        possible_values_for_unk7[bma.unk7].append(bma)
        setattr(bma, 'dbg_name', l.bma_name)

        # Saving animated map!
        bpas = l.get_bpas(rom)
        bpc = l.get_bpc(rom)
        bpl = l.get_bpl(rom)
        # Default for only one frame, doesn't really matter
        duration = 1000
        if len(bpas) > 0:
            # Assuming the game runs 60 FPS.
            duration = round(1000 / 60 * bpas[0].frame_info[0].unk1)
        frames = bma.to_pil(bpc, bpl.palettes, bpas)
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
    except (ValueError, AssertionError, NotImplementedError, SystemError) as ex:
        print(f"error for {l.bma_name}:")
        print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))

print("=====")
print(f"Possible values for unk6: {possible_values_for_unk6.keys()}")
print(f"Possible values for unk6: {possible_values_for_unk7.keys()}")

print("-----")
print("Levels with unk6=0")
for l in possible_values_for_unk6[0]:
    # P01P01A
    print(l.dbg_name)

print("-----")
print("Levels with unk6=1")
for l in possible_values_for_unk6[1]:
    # G01P03A
    print(l.dbg_name)
