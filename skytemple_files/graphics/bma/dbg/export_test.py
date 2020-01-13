import os
import traceback

from ndspy.rom import NintendoDSRom

from skytemple_files.graphics.bg_list_dat.handler import BgListDatHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(os.path.join(os.path.dirname(__file__), 'dbg_output'), exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bin = rom.getFileByName('MAP_BG/bg_list.dat')
bg_list = BgListDatHandler.deserialize(bin)

possible_values_for_unk6 = {}
possible_values_for_unk7 = {}

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
        if bma.unk6 not in possible_values_for_unk6:
            possible_values_for_unk6[bma.unk6] = []
        possible_values_for_unk6[bma.unk6].append(bma)
        if bma.number_of_collision_layers not in possible_values_for_unk7:
            possible_values_for_unk7[bma.number_of_collision_layers] = []
        possible_values_for_unk7[bma.number_of_collision_layers].append(bma)
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
    except (NotImplementedError, SystemError) as ex:
        print(f"error for {l.bma_name}: {repr(ex)}")
        print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))

print("=====")
print(f"Possible values for unk6: {possible_values_for_unk6.keys()}")
print(f"Possible values for unk7: {possible_values_for_unk7.keys()}")

print("-----")
print("Levels with unk7=0")
for l in possible_values_for_unk7[0]:
    print(l.dbg_name)

print("-----")
print("Levels with unk7=1")
for l in possible_values_for_unk7[1]:
    print(l.dbg_name)

print("-----")
print("Levels with unk7=2")
for l in possible_values_for_unk7[2]:
    print(l.dbg_name)
