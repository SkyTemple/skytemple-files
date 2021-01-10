"""Testing script, that exports all of the maps as images."""
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
import sys
import warnings
from typing import Optional

from skytemple_files.container.bin_pack.model import BinPack
from skytemple_files.data.md.model import Md
from skytemple_files.script.ssa_sse_sss.actor import SsaActor
from skytemple_files.script.ssa_sse_sss.object import SsaObject

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    from pil import Image, ImageDraw, ImageFont
from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.common.script_util import load_script_files, SCRIPT_DIR
from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_rom_folder
from skytemple_files.script.ssa_sse_sss.handler import SsaHandler
from skytemple_files.script.ssa_sse_sss.position import SsaPosition

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

TILE_SIZE = 8
TILE_SIZE_H = 4
ALPHA_T = 255
COLOR_ACTOR = (255, 0, 255, ALPHA_T)
COLOR_OBJECTS = (255, 160, 0, ALPHA_T)
COLOR_PERFORMER = (0, 255, 255, ALPHA_T)
COLOR_EVENTS = (0, 0, 255, 100)
COLOR_BLACK = (0, 0, 0, ALPHA_T)
COLOR_POS_MARKERS = (0, 255, 0)
TXT_AREA_SIZE = 200
MAP_WIDTH = 900

loaded_map_bg_images = {}
monster_bin_pack_file: Optional[BinPack] = None
monster_md: Optional[Md] = None

def draw_maps_main():
    global monster_bin_pack_file, monster_md
    os.makedirs(output_dir, exist_ok=True)

    rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))
    monster_bin_pack_file = FileType.BIN_PACK.deserialize(rom.getFileByName('MONSTER/monster.bin'))
    monster_md = FileType.MD.deserialize(rom.getFileByName('BALANCE/monster.md'))

    script_info = load_script_files(get_rom_folder(rom, SCRIPT_DIR))

    map_bg_entry_level_list = FileType.BG_LIST_DAT.deserialize(rom.getFileByName('MAP_BG/bg_list.dat')).level

    for script_map in script_info['maps'].values():
        # Map BGs are NOT *actually* mapped 1:1 to scripts. They are loaded via Opcode. However it turns out, using the BPL name
        # is an easy way to map them.
        map_bg_entry = next(x for x in map_bg_entry_level_list if x.bpl_name == script_map['name'])
        if script_map['enter_sse'] is not None:
            process(rom, map_bg_entry, script_map['name'], SCRIPT_DIR + '/' + script_map['name'] + '/' + script_map['enter_sse'])
        for ssa, _ in script_map['ssas']:
            process(rom, map_bg_entry, script_map['name'], SCRIPT_DIR + '/' + script_map['name'] + '/' + ssa)
        for sss in script_map['subscripts'].keys():
            process(rom, map_bg_entry, script_map['name'], SCRIPT_DIR + '/' + script_map['name'] + '/' + sss)


def load_map_bg(rom, map_bg_entry, map_name):
    global loaded_map_bg_images
    if map_name not in loaded_map_bg_images:
        loaded_map_bg_images[map_name] = map_bg_entry.get_bma(rom).to_pil(
            map_bg_entry.get_bpc(rom), map_bg_entry.get_bpl(rom), map_bg_entry.get_bpas(rom), False, False
        )[0]

    return loaded_map_bg_images[map_name]


def draw_grid(draw, image):
    for x in range(0, image.width, TILE_SIZE):
        line = ((x, 0), (x, image.height - TXT_AREA_SIZE))
        draw.line(line, fill=(0, 0, 0, 40))

    for y in range(0, image.height - TXT_AREA_SIZE, TILE_SIZE):
        line = ((0, y), (image.width, y))
        draw.line(line, fill=(0, 0, 0, 40))


def draw_actor(img: Image.Image, draw, actor: SsaActor):
    """Draws the sprite for an actor"""

    if actor.actor.entid == 0:
        return triangle(draw, actor.pos.x_absolute, actor.pos.y_absolute, COLOR_ACTOR, actor.pos.direction.id)

    actor_sprite_id = monster_md[actor.actor.entid].sprite_index

    sprite = FileType.WAN.deserialize(
        FileType.COMMON_AT.deserialize(monster_bin_pack_file[actor_sprite_id]).decompress()
    )
    ani_group = sprite.get_animations_for_group(sprite.anim_groups[11])
    frame_id = actor.pos.direction.id - 1 if actor.pos.direction.id > 0 else 0
    mfg_id = ani_group[frame_id].frames[0].frame_id

    sprite_img, (cx, cy) = sprite.render_frame_group(sprite.frame_groups[mfg_id])
    render_x = actor.pos.x_absolute - cx
    render_y = actor.pos.y_absolute - cy
    img.paste(sprite_img, (render_x, render_y), sprite_img)

def draw_object(img: Image.Image, draw, obj: SsaObject, rom: NintendoDSRom):
    """Draws the sprite for an object"""

    if obj.object.name == 'NULL':
        return triangle(draw, obj.pos.x_absolute, obj.pos.y_absolute, COLOR_ACTOR, obj.pos.direction.id)

    try:
        sprite = FileType.WAN.deserialize(
            rom.getFileByName(f'GROUND/{obj.object.name}.wan')
        )
    except ValueError as e:
        warnings.warn(f"Failed to render a sprite, replaced with placeholder ({obj}): {e}")
        return triangle(draw, obj.pos.x_absolute, obj.pos.y_absolute, COLOR_ACTOR, obj.pos.direction.id)

    ani_group = sprite.get_animations_for_group(sprite.anim_groups[0])
    frame_id = obj.pos.direction.id - 1 if obj.pos.direction.id > 0 else 0
    if frame_id > len(ani_group) - 1:
        frame_id = 0
    mfg_id = ani_group[frame_id].frames[0].frame_id

    sprite_img, (cx, cy) = sprite.render_frame_group(sprite.frame_groups[mfg_id])
    render_x = obj.pos.x_absolute - cx
    render_y = obj.pos.y_absolute - cy
    img.paste(sprite_img, (render_x, render_y), sprite_img)


def process(rom, map_bg_entry, map_name, file_name):
    print(f"Processing {file_name}...")

    map_bg = load_map_bg(rom, map_bg_entry, map_name)

    ssa = SsaHandler.deserialize(rom.getFileByName(file_name))
    for layer_id, layer in enumerate(ssa.layer_list):
        if len(layer.actors) <= 0 and len(layer.objects) <= 0 and len(layer.performers) <= 0 and len(layer.events) <= 0 and len(layer.unk10s) <= 0:
            continue

        w = map_bg.width if map_bg.width > MAP_WIDTH else MAP_WIDTH

        img = Image.new('RGB', (w, map_bg.height + TXT_AREA_SIZE), (255, 255, 255))
        img.paste(map_bg, (0, 0))
        draw = ImageDraw.Draw(img, 'RGBA')

        draw_grid(draw, img)

        text_y = map_bg.height + 10
        # Actors
        text_x = 20
        draw.text((text_x, text_y), "Actors:", COLOR_ACTOR)
        for i, actor in enumerate(layer.actors):
            draw_actor(img, draw, actor)
            draw.text((actor.pos.x_absolute, actor.pos.y_absolute + TILE_SIZE), str(i), (0, 0, 0))
            actor_text = f"{i}: {actor.actor.name} - S:{actor.script_id}"
            draw.text((text_x, text_y + 10 + (i * 10)), actor_text, (0, 0, 0))

        # Objects
        text_x = 200
        draw.text((text_x, text_y), "Objects:", COLOR_OBJECTS)
        for i, object in enumerate(layer.objects):
            draw_object(img, draw, object, rom)
            draw.text((object.pos.x_absolute, object.pos.y_absolute + TILE_SIZE), str(i), (0, 0, 0))
            object_text = f"{i}: {object.object.name} - S:{object.script_id} - Unks: ({object.hitbox_w},{object.unk12})"
            draw.text((text_x, text_y + 10 + (i * 10)), object_text, (0, 0, 0))

        # Performers
        text_x = 420
        draw.text((text_x, text_y), "Performers:", COLOR_PERFORMER)
        for i, performer in enumerate(layer.performers):
            triangle(draw, performer.pos.x_absolute, performer.pos.y_absolute, COLOR_PERFORMER, performer.pos.direction.id)
            draw.text((performer.pos.x_absolute, performer.pos.y_absolute + TILE_SIZE), str(i), (0, 0, 0))
            object_text = f"{i}: T:{performer.type} - Unks: ({performer.hitbox_w},{performer.hitbox_h},{performer.unk10},{performer.unk12})"
            draw.text((text_x, text_y + 10 + (i * 10)), object_text, (0, 0, 0))

        # Events
        text_x = 620
        draw.text((text_x, text_y), "Events:", COLOR_EVENTS)
        for i, event in enumerate(layer.events):
            draw.rectangle((
                event.pos.x_absolute, event.pos.y_absolute,
                event.pos.x_absolute + (event.trigger_width * TILE_SIZE), event.pos.y_absolute + (event.trigger_height * TILE_SIZE),
            ), COLOR_EVENTS, (0, 0, 0))
            draw.text((event.pos.x_absolute, event.pos.y_absolute), str(i), (255, 255, 255))
            object_text = f"{i}: Trigger: {event.trigger_id}"
            draw.text((text_x, text_y + 10 + (i * 10)), object_text, (0, 0, 0))

        # Position Markers
        text_x = 720
        draw.text((text_x, text_y), "Position Markers:", COLOR_POS_MARKERS)
        for i, pos_marker in enumerate(ssa.position_markers):
            draw.rectangle((
                pos_marker.pos.x_absolute, pos_marker.pos.y_absolute,
                pos_marker.pos.x_absolute + TILE_SIZE, pos_marker.pos.y_absolute + TILE_SIZE,
            ), COLOR_POS_MARKERS, (0, 0, 0))
            draw.text((pos_marker.pos.x_absolute, pos_marker.pos.y_absolute + TILE_SIZE), str(i), (0, 0, 0))
            object_text = f"{i}: " \
                          f"@({pos_marker.pos.x_relative}[{pos_marker.pos.x_offset}], " \
                          f"{pos_marker.pos.y_relative}[{pos_marker.pos.y_offset}) " \
                          f"{pos_marker.unkA}-{pos_marker.unkC}-{pos_marker.unkE}"
            draw.text((text_x, text_y + 10 + (i * 10)), object_text, (0, 0, 0))

        # Trigger
        text_y = map_bg.height + 10 + 130
        text_x = 20
        draw.text((text_x, text_y), "Trigger:", COLOR_BLACK)
        for i, trigger in enumerate(ssa.triggers):
            object_text = f"{i}: CoRo: {trigger.coroutine.name} - S:{trigger.script_id}"
            draw.text((text_x, text_y + 10 + (i * 10)), object_text, (0, 0, 0))

        # Unk10
        text_y = map_bg.height + 10 + 130
        text_x = 240
        draw.text((text_x, text_y), "Unk10:", COLOR_BLACK)
        for i, unk10 in enumerate(layer.unk10s):
            object_text = f"{i}: {unk10}"
            draw.text((text_x, text_y + 10 + (i * 10)), object_text, (0, 0, 0))

        out_file_name = os.path.join(output_dir, file_name.replace('/', '_') + '_layer' + str(layer_id) + '.png')
        img.save(out_file_name)


def triangle(draw, x, y, fill, direction):
    if direction == 1 or direction == 0:
        # Down
        draw.polygon([(x, y), (x + TILE_SIZE, y), (x + TILE_SIZE_H, y + TILE_SIZE)], fill=fill, outline=(0, 0, 0))
    elif direction == 2:
        # DownRight
        draw.polygon([(x + TILE_SIZE, y), (x + TILE_SIZE, y + TILE_SIZE), (x, y + TILE_SIZE)], fill=fill, outline=(0, 0, 0))
    elif direction == 3:
        # Right
        draw.polygon([(x, y), (x + TILE_SIZE, y + TILE_SIZE_H), (x, y + TILE_SIZE)], fill=fill, outline=(0, 0, 0))
    elif direction == 4:
        # UpRight
        draw.polygon([(x, y), (x + TILE_SIZE, y), (x + TILE_SIZE, y + TILE_SIZE)], fill=fill, outline=(0, 0, 0))
    elif direction == 5:
        # Up
        draw.polygon([(x, y + TILE_SIZE), (x + TILE_SIZE, y + TILE_SIZE), (x + TILE_SIZE_H, y)], fill=fill, outline=(0, 0, 0))
    elif direction == 6:
        # UpLeft
        draw.polygon([(x, y + TILE_SIZE), (x, y), (x + TILE_SIZE, y)], fill=fill, outline=(0, 0, 0))
    elif direction == 7:
        # Left
        draw.polygon([(x + TILE_SIZE, y), (x, y + TILE_SIZE_H), (x + TILE_SIZE, y + TILE_SIZE)], fill=fill, outline=(0, 0, 0))
    elif direction == 8:
        # DownLeft
        draw.polygon([(x, y), (x, y + TILE_SIZE), (x + TILE_SIZE, y + TILE_SIZE)], fill=fill, outline=(0, 0, 0))


if __name__ == '__main__':
    draw_maps_main()
