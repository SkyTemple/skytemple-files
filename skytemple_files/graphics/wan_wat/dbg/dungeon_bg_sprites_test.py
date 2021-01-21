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
import colorsys
import json
import os
from math import floor

from PIL import ImageFilter, Image
from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from colorthief import ColorThief

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
os.makedirs(output_dir, exist_ok=True)
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

GROUP_WALK = 0
GROUP_IDLE = 11
WIDTH = 96 * 2 * 16
HEIGHT = 96 * 2 * 16
DIM_CHUNK = 8 * 3


class ColorThiefExistingImage(ColorThief):
    def __init__(self, img):
        self.image = img


def get_dominant_color(img):
    return ColorThiefExistingImage(img).get_color(quality=1)


def outline_sprite(img, color):
    alpha_flat = img.getchannel('A')
    im_outline = img.filter(ImageFilter.FIND_EDGES)
    alpha_outline = im_outline.getchannel('A')
    im_outline = Image.new('RGBA', im_outline.size, color=color)
    im_flat = Image.new('RGBA', im_outline.size, color=(253, 247, 238, 255))
    im_flat.putalpha(alpha_flat)
    im_flat.paste(im_outline, (0, 0), alpha_outline)
    return im_flat


def process_color(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

    l = max(0.5, l)
    s = 0.3

    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return floor(r * 255), floor(g * 255), floor(b * 255)


def render_group(wan_model, group_id, base_pil, x_offset, color=None):
    g = wan_model.anim_groups[group_id]

    group_meta_entry = []
    # First find the max size needed
    max_size = 0
    for ani_i, ani in enumerate(wan_model.get_animations_for_group(g)):
        for frame_i, frame in enumerate(ani.frames):
            mfg_id = wan_model.frame_groups[frame.frame_id]
            img, (cx, cy) = wan_model.render_frame_group(mfg_id)
            max_size = max(max_size, max((cx, cy)) + max((img.width, img.height)))

    group_meta_entry.append(max_size)
    group_entry = []
    group_meta_entry.append(group_entry)
    for ani_i, ani in enumerate(wan_model.get_animations_for_group(g)):
        ani_entry = []
        group_entry.append(ani_entry)
        for frame_i, frame in enumerate(ani.frames):
            ani_entry.append(frame.duration)
            # A single image
            mfg_id = wan_model.frame_groups[frame.frame_id]
            img, (cx, cy) = wan_model.render_frame_group(mfg_id)
            if color is None:
                color = process_color(*get_dominant_color(img))
            oimg = outline_sprite(img, color)
            base_pil.paste(oimg, (
                x_offset + ani_i * max_size - cx + int(max_size / 2),
                frame_i * max_size - cy + int(max_size / 2)
            ))
    return group_meta_entry, color


# Actor Sprites
pack_file = rom.getFileByName('MONSTER/monster.bin')
sprites = FileType.BIN_PACK.deserialize(pack_file)
monster_md = FileType.MD.deserialize(rom.getFileByName('BALANCE/monster.md'))
sprite_data = []

for i, monster in enumerate(monster_md.entries):
    if i < 1 or i > 536:
        continue
    print(f"Monster {i} - Sprite {monster.sprite_index}")
    sprite = sprites[monster.sprite_index]
    sprite_bin_decompressed = FileType.COMMON_AT.deserialize(sprite).decompress()
    wan_model = FileType.WAN.deserialize(sprite_bin_decompressed)

    img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))

    sprite_data_entry = []
    sprite_data.append(sprite_data_entry)

    sprite_data_entry.append(monster.shadow_size.value)
    sprite_data_entry.append(monster.movement_type.value)
    entry, color = render_group(wan_model, GROUP_IDLE, img, 0)
    dim_idle_x = entry[0] * 8
    dim_idle_y = entry[0] * max(len(dir) for dir in entry[1])
    sprite_data_entry.append(entry)
    entry, _ = render_group(wan_model, GROUP_WALK, img, dim_idle_x, color)
    dim_walk_x = entry[0] * 8
    dim_walk_y = entry[0] * max(len(dir) for dir in entry[1])
    sprite_data_entry.append(entry)

    img.crop((0, 0, dim_idle_x + dim_walk_x, max(dim_idle_y, dim_walk_y))).save(os.path.join(output_dir, f'{i}.png'))

with open(os.path.join(output_dir, 'sprites.json'), 'w') as f:
    json.dump(sprite_data, f, separators=(',', ':'))
