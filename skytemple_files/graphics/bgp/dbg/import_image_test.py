import math
import os
from time import time

from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_files_from_rom_with_extension
from skytemple_files.compression_container.at4px.handler import At4pxHandler
from skytemple_files.graphics.bgp.handler import BgpHandler
from skytemple_files.graphics.bgp.model import BGP_RES_WIDTH_IN_TILES

os.makedirs(os.path.join(os.path.dirname(__file__), 'dbg_output'), exist_ok=True)

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

for filename in get_files_from_rom_with_extension(rom, 'bgp'):
    print("Processing " + filename)

    bin_before = rom.getFileByName(filename)
    bgp = BgpHandler.deserialize(bin_before)

    img_before = bgp.to_pil()
    bgp.from_pil(img_before)
    img_after = bgp.to_pil()

    #img_before.show()
    #img_after.show()

    bin_after = BgpHandler.serialize(bgp)

    print(f"Size before: {len(bin_before)}")
    print(f"Size after: {len(bin_after)}")

    rom.setFileByName(filename, bin_after)


rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))