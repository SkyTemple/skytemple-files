"""Debugging import problems"""
import os

from ndspy.rom import NintendoDSRom

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom_vanilla = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
rom_modified = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))

bin_vanilla = rom_vanilla.getFileByName('MAP_BG/s05p01a.bma')

with open('/tmp/before.bin', 'wb') as f:
    f.write(bin_vanilla)

bin_modified = rom_modified.getFileByName('MAP_BG/s05p01a.bma')

with open('/tmp/after.bin', 'wb') as f:
    f.write(bin_modified)
