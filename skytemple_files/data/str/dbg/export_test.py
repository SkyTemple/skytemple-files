import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import get_files_from_rom_with_extension
from skytemple_files.data.str.handler import StrHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

for filename in get_files_from_rom_with_extension(rom, 'str'):
    print("Processing " + filename)

    bin = rom.getFileByName(filename)
    str = StrHandler.deserialize(bin)

    #cc = ['↑', '↓']
    cc = ['ª', 'º']
    from skytemple_files.data.str.codec import _special_characters
    for i, string in enumerate(str.strings):
        if 16792 < i >= 16322:
            print(f"{i} {string}")
