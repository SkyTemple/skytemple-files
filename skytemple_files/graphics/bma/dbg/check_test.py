import os

from ndspy.rom import NintendoDSRom

from skytemple_files.graphics.bg_list_dat.handler import BgListDatHandler

os.makedirs(os.path.join(os.path.dirname(__file__), 'dbg_output'), exist_ok=True)

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bin = rom.getFileByName('MAP_BG/bg_list.dat')
bg_list = BgListDatHandler.deserialize(bin)

for l in bg_list.level:
    filename = l.bpc_name

    bma = l.get_bma(rom)
    bpc = l.get_bpc(rom, bma.tiling_width, bma.tiling_height)

    print(f"{filename}: {bma.number_of_layers == bpc.number_of_layers} | {bma.number_of_layers} | {bpc.number_of_layers}")
