"""Testing script to corrupt some dungon.bin files, to find out what they do."""
#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
import itertools
import os

from PIL import Image
from ndspy.rom import NintendoDSRom

from skytemple_files.common.tiled_image import to_pil, TilemapEntry
from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_ppmdu_config_for_rom, iter_bytes, iter_bytes_4bit_le, write_uintle, \
    read_uintle
from skytemple_files.container.dungeon_bin.handler import DungeonBinHandler
from skytemple_files.container.dungeon_bin.sub.sir0_at4px import DbinSir0At4pxHandler
from skytemple_files.compression_container.common_at.model import CommonAt

from itertools import islice

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(os.path.join(output_dir, 'raw'), exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))

dungeon_bin_bin = rom.getFileByName('DUNGEON/dungeon.bin')
static_data = get_ppmdu_config_for_rom(rom)
dungeon_bin = DungeonBinHandler.deserialize(dungeon_bin_bin, static_data)

# CHECK 1: We can serialize bin packs correctly
dungeon_bin_bin_after = DungeonBinHandler.serialize(dungeon_bin)
assert dungeon_bin_bin == dungeon_bin_bin_after


# -- CORUPTION TASKS
def corrupt171():
    """Corrupt 171: Dungeon tiles Beach cave 1? -- No actually not.
    Seems to be some kind of map assembling information."""
    img171 = dungeon_bin[171].decompress()
    # Make the first entry tile 2
    img171 = b'\x02' * len(img171)
    dungeon_bin[171] = FileType.COMMON_AT.compress(img171)


def corrupt341():
    """Corrupt 341: Dungeon tiles Beach cave 2? -- No? Tiles -> Chunk mappings or similar?"""
    img341 = dungeon_bin[341].decompress()
    img341new = bytearray(img341)

    # Decode XOR
    #XOR_ROW_LEN = 7200#18 * 7
    #rows_decoded = []
    #row_before = bytes(XOR_ROW_LEN)
    #for chunk in iter_bytes(img341, XOR_ROW_LEN):
    #    xored = bytearray(a ^ b for (a, b) in zip(chunk, row_before))
    #    row_before = xored
    #    rows_decoded.append(xored)

    dummy_map = [
        TilemapEntry(10, False, False, 0),
        TilemapEntry(10, True, False, 0),
        TilemapEntry(10, False, True, 0),
        TilemapEntry(5, False, False, 0),
        TilemapEntry(5, True, False, 0),
        TilemapEntry(5, False, True, 0),
        TilemapEntry(10, False, False, 6),
        TilemapEntry(10, True, False, 6),
        TilemapEntry(10, False, True, 6)
    ]

    for j in range(1, 300):
        for i, m in enumerate(dummy_map):
            write_uintle(img341new, m.to_int(), (j * 18) + 2 * i, 2)

    all_tilemaps = []
    for bytes2 in iter_bytes(img341new, 2):
        all_tilemaps.append(TilemapEntry.from_int(read_uintle(bytes2, 0, 2)))

    # Encode XOR
    #rows_encoded = []
    #row_before = bytes(XOR_ROW_LEN)
    #for row in rows_decoded:
    #    xored = bytes(a ^ b for (a, b) in zip(row, row_before))
    #    row_before = row
    #    rows_encoded.append(xored)
    #img341new = bytes(itertools.chain.from_iterable(rows_encoded))
    #assert img341 == img341new

    with open('/tmp/corrupt.bin', 'wb') as f:
        f.write(img341new)
    dungeon_bin[341] = FileType.COMMON_AT.compress(img341new)


def corrupt511():
    """Corrupt 511: Dungeon tiles Beach cave 3?"""
    img511 = dungeon_bin[511].decompress()
    # Make every second byte 2
    img511new = bytearray(len(img511))
    for i, b in enumerate(img511):
        if i % 2 != 0:
            img511new[i] = img511[i]
        else:
            img511new[i] = 2
    dungeon_bin[511] = FileType.COMMON_AT.compress(img511new)

# -- /

# Run corruption tasks
corrupt171()
#corrupt341()
#corrupt511()

dungeon_bin_bin_after_changes = DungeonBinHandler.serialize(dungeon_bin)
rom.setFileByName('DUNGEON/dungeon.bin', dungeon_bin_bin_after_changes)
assert dungeon_bin_bin != dungeon_bin_bin_after_changes
rom.saveToFile(os.path.join(output_dir, 'corrupt.nds'))
