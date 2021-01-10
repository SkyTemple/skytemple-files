"""NOTE: THIS IS CURRENTLY OUTDATAED FROM EARLY EXPERIMENTATION!"""
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
import os

from PIL import Image
from ndspy.rom import NintendoDSRom

from skytemple_files.common.tiled_image import to_pil, TilemapEntry
from skytemple_files.common.util import get_ppmdu_config_for_rom, iter_bytes
from skytemple_files.container.dungeon_bin.handler import DungeonBinHandler
from skytemple_files.compression_container.common_at.model import CommonAt

from itertools import islice

from skytemple_files.container.sir0.handler import Sir0Handler
from skytemple_files.graphics.dpl.model import Dpl
from skytemple_files.graphics.dpla.model import Dpla

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(os.path.join(output_dir, 'raw'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'test'), exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))

dungeon_bin_bin = rom.getFileByName('DUNGEON/dungeon.bin')
static_data = get_ppmdu_config_for_rom(rom)
dungeon_bin = DungeonBinHandler.deserialize(dungeon_bin_bin, static_data)


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def output_dpla(fn: str, file: Dpla):
    print("Outputting weird palette as image.")
    max_pal_len = max(max(int(len(p) / 3) for p in file.colors), 1)
    # each entry on the y access is a color, x axis shows animation
    out_img = Image.new('RGBA', (max_pal_len, max(len(file.colors), 1)), (0, 0, 0, 0))
    pix = out_img.load()
    for palidx, pal in enumerate(file.colors):
        for i, (r, g, b) in enumerate(chunk(pal, 3)):
            pix[(i, palidx)] = (r, g, b, 255)

    out_img.save(os.path.join(output_dir, fn + '.png'))


def output_raw_palette(fn: str, file: Dpl):
    print("Outputting raw palette as image.")
    max_pal_len = max(max(int(len(p) / 3) for p in file.palettes), 1)
    # each entry on the y access is a palette, x axis shows palette colors
    out_img = Image.new('RGBA', (max_pal_len, max(len(file.palettes), 1)), (0, 0, 0, 0))
    pix = out_img.load()
    for palidx, pal in enumerate(file.palettes):
        for i, (r, g, b) in enumerate(chunk(pal, 3)):
            pix[(i, palidx)] = (r, g, b, 255)

    out_img.save(os.path.join(output_dir, fn + '.png'))


def output_at_water_tiles(fn: str, common_at: CommonAt, pal: Dpla):
    print("Outputting water AT as image.")
    img_bin = common_at.decompress()
    tiles = list(iter_bytes(img_bin, int(8 * 8 / 2)))
    # create a dummy tile map containing all the tiles
    tilemap = []
    for i in range(0, len(tiles)):
        tilemap.append(TilemapEntry(
            i, False, False, 0, True
        ))
    out_img = to_pil(
        tilemap, tiles, [pal.get_palette_for_frame(0, 0)], 8,
        int(len(tiles) * 8 / 3), 4 * 8,
        tiling_width=1, tiling_height=1
    )
    os.makedirs(os.path.join(output_dir, 'raw_img'), exist_ok=True)
    with open(os.path.join(output_dir, 'raw_img', fn), 'wb') as f:
        f.write(img_bin)

    out_img.save(os.path.join(output_dir, fn + '.png'))


def output_at_dungeon_tiles(fn: str, common_at: CommonAt, pal: Dpla):
    print("Outputting dungeon AT as image.")
    img_bin = common_at.decompress()
    tiles = list(iter_bytes(img_bin, int(8 * 8)))
    # create a dummy tile map containing all the tiles
    tilemap = []
    for i in range(0, len(tiles)):
        tilemap.append(TilemapEntry(
            i, False, False, 0, True
        ))
    out_img = to_pil(
        tilemap, tiles, [pal.get_palette_for_frame(0, 0)], 8,
        int(len(tiles) * 8 / 3), 4 * 8,
        tiling_width=1, tiling_height=1, bpp=8
    )
    # Alternate stategy:
    img_8bpp = img_bin  #bytes(x for x in iter_bytes_4bit_le(img_bin))
    mod = 16 * 4
    channels = 1
    mode = 'RGB' if channels == 3 else 'P'
    out_img = Image.frombuffer(mode, (int(len(img_8bpp) / mod / channels), mod), bytes(img_8bpp), 'raw', mode, 0, 1)
    if mode == 'P':
        out_img.putpalette(pal.get_palette_for_frame(0, 0))
    os.makedirs(os.path.join(output_dir, 'raw_img'), exist_ok=True)
    with open(os.path.join(output_dir, 'raw_img', fn), 'wb') as f:
        f.write(img_bin)

    out_img.save(os.path.join(output_dir, fn + '.png'))


# Output high level representations for all models, if possible.
for i, file in enumerate(dungeon_bin):
    fn = dungeon_bin.get_filename(i)
    fdef = static_data.dungeon_data.dungeon_bin_files.get(i)
    print(i, type(file), fn)
    if isinstance(file, Dpla):
        output_dpla(fn, file)
    elif isinstance(file, CommonAt):
        # As the palette, we use one of the first 170 files, matching the modulo index.
        # TODO: This is currently using the animated palette actually...
        pal = dungeon_bin[i % 170]
        assert isinstance(pal, Dpla)
        if fdef.name == "dungeon%i.bpci":
            output_at_water_tiles(fn, file, pal)
        else:
            output_at_dungeon_tiles(fn, file, pal)
    elif isinstance(file, Dpl):
        output_raw_palette(fn, file)
    elif isinstance(file, bytes):
        print("No model, skipped.")
    else:
        print("Unknown type, skipped.")

# Also output the raw files
for i, file in enumerate(dungeon_bin.get_files_bytes()):
    fn = dungeon_bin.get_filename(i)
    if i == 1028:
        sir0 = Sir0Handler.deserialize(file)
        file = sir0.content
    with open(os.path.join(output_dir, 'raw', fn), 'wb') as f:
        f.write(file)

for i, file in enumerate(dungeon_bin):
    fn = dungeon_bin.get_filename(i)
    if fn.endswith('.at.sir0'):
        with open(os.path.join(output_dir, 'test', fn), 'wb') as f:
            f.write(file.decompress())
