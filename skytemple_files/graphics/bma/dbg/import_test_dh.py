import os

from PIL import Image
from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from skytemple_files.graphics.bg_list_dat.handler import BgListDatHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bg_list = BgListDatHandler.deserialize(rom.getFileByName('MAP_BG/bg_list.dat'))

for i, l in enumerate(bg_list.level):
    if l.bma_name != 'P01P01A':
        continue

    bma = l.get_bma(rom)
    bpc = l.get_bpc(rom)
    bpl = l.get_bpl(rom)
    bpas = l.get_bpas(rom)

    with open(os.path.join(base_dir, 'dh', 'P01P01A_LOWER.png'), 'rb') as lf:
        with open(os.path.join(base_dir, 'dh', 'P01P01A_HIGHER.png'), 'rb') as hf:
            bma.from_pil(bpc, bpl, Image.open(lf), Image.open(hf))

    rom.setFileByName('MAP_BG/p01p01a.bma', FileType.BMA.serialize(bma))
    rom.setFileByName('MAP_BG/p01p01a.bpl', FileType.BPL.serialize(bpl))
    rom.setFileByName('MAP_BG/p01p01a.bpc', FileType.BPC.serialize(bpc))

    bma = l.get_bma(rom)
    bpc = l.get_bpc(rom)
    bpl = l.get_bpl(rom)
    bma.to_pil_single_layer(bpc, bpl.palettes, bpas, 0).show()
    bma.to_pil_single_layer(bpc, bpl.palettes, bpas, 1).show()

rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
