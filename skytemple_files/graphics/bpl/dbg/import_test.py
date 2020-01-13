import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import get_files_from_rom_with_extension
from skytemple_files.graphics.bpl.handler import BplHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

for filename in get_files_from_rom_with_extension(rom, 'bpl'):
    bin_before = rom.getFileByName(filename)
    bpa_before = BplHandler.deserialize(bin_before)
    print(f"Processing {filename} ")

    bin_after = BplHandler.serialize(bpa_before)

    with open('/tmp/before.bin', 'wb') as f:
        f.write(bin_before)

    with open('/tmp/after.bin', 'wb') as f:
        f.write(bin_after)

    assert bin_before == bin_after

    rom.setFileByName(filename, bin_after)


rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
