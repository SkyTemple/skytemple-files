import os

from ndspy.rom import NintendoDSRom

from skytemple_files.graphics.bpl.handler import BplHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bin_before = rom.getFileByName('MAP_BG/p01p01a.bpl')
bpl_before = BplHandler.deserialize(bin_before)

for palette in bpl_before.palettes:
    palette[14] = 0xff

bin_after = BplHandler.serialize(bpl_before)

rom.setFileByName('MAP_BG/p01p01a.bpl', bin_after)


rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
