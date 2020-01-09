import os

from bitstring import BitStream
from ndspy.rom import NintendoDSRom

from skytemple_files.unique.bg_list_dat.handler import BgListDatHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

with open(os.path.join(base_dir, 's05p01a.bma'), 'rb') as f:
    rom.setFileByName('MAP_BG/s05p01a.bma', f.read())

with open(os.path.join(base_dir, 'p01p01a.bma'), 'rb') as f:
    rom.setFileByName('MAP_BG/p01p01a.bma', f.read())

with open(os.path.join(base_dir, 'g01p03a.bma'), 'rb') as f:
    rom.setFileByName('MAP_BG/g01p03a.bma', f.read())

rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
