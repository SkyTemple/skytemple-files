#!/usr/bin/env python3
"""
This is a sample Python CLI script that uses SkyTemple Files to export all maps of the game,
including sprites of objects and actors on them.

This is also an example on how to use the following file handlers:
- BMA, BPL, PPC, BPA
- BG_LIST_DAT
- DUNGEON_BIN
- DMA, DPC, DPCI, DPL, DPLA
- MAPPA
- MD
- SSA
- LSD
- WAN, WAT
- (BIN_PACK)
- (COMMON_AT)
- (Compressions)
- (Hardcoded Lists)
"""
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
import argparse
import json
import os
import sys
import traceback
import warnings
from typing import Optional, List, Dict

from PIL import Image, ImageDraw
from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptData
from skytemple_files.common.script_util import load_script_files, SCRIPT_DIR
from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_ppmdu_config_for_rom, get_rom_folder, get_binary_from_rom_ppmdu
from skytemple_files.container.bin_pack.model import BinPack
from skytemple_files.data.md.model import Md
from skytemple_files.graphics.bma.model import Bma
from skytemple_files.graphics.bpc.model import BPC_TILE_DIM
from skytemple_files.graphics.dma.dma_drawer import DmaDrawer
from skytemple_files.graphics.dma.model import Dma
from skytemple_files.graphics.dpc.model import Dpc
from skytemple_files.graphics.dpci.model import Dpci
from skytemple_files.graphics.dpl.model import Dpl
from skytemple_files.graphics.dpla.model import Dpla
from skytemple_files.hardcoded.dungeons import HardcodedDungeons
from skytemple_files.hardcoded.ground_dungeon_tilesets import HardcodedGroundDungeonTilesets, GroundTilesetMapping
from skytemple_files.script.ssa_sse_sss.actor import SsaActor
from skytemple_files.script.ssa_sse_sss.layer import SsaLayer
from skytemple_files.script.ssa_sse_sss.object import SsaObject

ALPHA_T = 177
COLOR_ACTORS = (255, 0, 255, ALPHA_T)
COLOR_OBJECTS = (255, 160, 0, ALPHA_T)
COLOR_PERFORMER = (0, 255, 255, ALPHA_T)
COLOR_EVENTS = (0, 0, 255, 100)
BPC_TILE_DIM_H = int(BPC_TILE_DIM / 2)

monster_bin_pack_file: Optional[BinPack] = None
monster_md: Optional[Md] = None
map_bgs: Dict[str, List[Image.Image]] = {}
map_bg_durations: Dict[str, int] = {}
draw_invisible_actors_objects = False


def draw_map_bgs(rom: NintendoDSRom, map_bg_dir):
    global map_bgs, map_bg_durations
    os.makedirs(map_bg_dir, exist_ok=True)

    bin = rom.getFileByName('MAP_BG/bg_list.dat')
    bg_list = FileType.BG_LIST_DAT.deserialize(bin)

    count = len(bg_list.level)
    for i, l in enumerate(bg_list.level):
        try:
            bma = l.get_bma(rom)
            print(f"{i + 1}/{count} - {l.bpl_name}")

            bpas = l.get_bpas(rom)
            non_none_bpas = [b for b in bpas if b is not None]
            bpc = l.get_bpc(rom)
            bpl = l.get_bpl(rom)

            # Saving animated map!
            bpa_duration = -1
            pal_ani_duration = -1
            if len(non_none_bpas) > 0:
                bpa_duration = round(1000 / 60 * non_none_bpas[0].frame_info[0].duration_per_frame)
            if bpl.has_palette_animation:
                pal_ani_duration = round(1000 / 60 * max(spec.duration_per_frame for spec in bpl.animation_specs))
            duration = max(bpa_duration, pal_ani_duration)
            if duration == -1:
                # Default for only one frame, doesn't really matter
                duration = 1000
            frames = bma.to_pil(bpc, bpl, bpas, include_collision=False, include_unknown_data_block=False)
            frames[0].save(
                os.path.join(map_bg_dir, l.bpl_name + '.gif'),
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=0,
                optimize=False
            )
            frames[0].save(
                os.path.join(map_bg_dir, l.bpl_name + '.png')
            )
            map_bgs[l.bpl_name] = frames
            map_bg_durations[l.bpl_name] = duration
        except (NotImplementedError, SystemError) as ex:
            print(f"error for {l.bma_name}: {repr(ex)}", file=sys.stderr)
            print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)), file=sys.stderr)


def draw_dungeon_map_bgs(rom, dungeon_map_bg_dir, config):
    os.makedirs(dungeon_map_bg_dir, exist_ok=True)
    dungeon_bin = FileType.DUNGEON_BIN.deserialize(rom.getFileByName('DUNGEON/dungeon.bin'), config)

    ground_dungeon_tilesets = HardcodedGroundDungeonTilesets.get_ground_dungeon_tilesets(
        get_binary_from_rom_ppmdu(rom, config.binaries['overlay/overlay_0011.bin']),
        config
    )
    dungeons = HardcodedDungeons.get_dungeon_list(
        get_binary_from_rom_ppmdu(rom, config.binaries['arm9.bin']),
        config
    )
    mappa = FileType.MAPPA_BIN.deserialize(rom.getFileByName('BALANCE/mappa_s.bin'))
    
    levels_by_id = config.script_data.level_list__by_id

    bg_list_bin = rom.getFileByName('MAP_BG/bg_list.dat')
    bg_list = FileType.BG_LIST_DAT.deserialize(bg_list_bin)

    for i, entry in enumerate(ground_dungeon_tilesets):
        if entry.ground_level >= 0xFFFF:
            continue
        level = levels_by_id[entry.ground_level]
        print(f"{i + 1}/{len(ground_dungeon_tilesets)-1} - {level.name}")
        print(entry)

        mappa_idx = dungeons[entry.dungeon_id].mappa_index
        start_offset = dungeons[entry.dungeon_id].start_after
        length = dungeons[entry.dungeon_id].number_floors
        if entry.dungeon_id == 71:
            print("DEEP CONCEALED RUINS SKIPPED")
            continue
        if entry.unk2 == 1:
            tileset_id = mappa.floor_lists[mappa_idx][start_offset].layout.tileset_id
        elif entry.unk2 == 100:
            tileset_id = mappa.floor_lists[mappa_idx][start_offset + length - 1].layout.tileset_id
        else:
            raise ValueError("Unknown unk2")
        if tileset_id == 170:
            tileset_id = 1
        dma: Dma = dungeon_bin.get(f'dungeon{tileset_id}.dma')
        dpl: Dpl = dungeon_bin.get(f'dungeon{tileset_id}.dpl')
        dpla: Dpla = dungeon_bin.get(f'dungeon{tileset_id}.dpla')
        dpci: Dpci = dungeon_bin.get(f'dungeon{tileset_id}.dpci')
        dpc: Dpc = dungeon_bin.get(f'dungeon{tileset_id}.dpc')

        bma: Bma = bg_list.level[level.mapid].get_bma(rom)

        duration = round(1000 / 60 * max(16, min(dpla.durations_per_frame_for_colors)))

        drawer = DmaDrawer(dma)
        rules = drawer.rules_from_bma(bma)
        mappings = drawer.get_mappings_for_rules(rules, treat_outside_as_wall=True, variation_index=0)
        frames = drawer.draw(mappings, dpci, dpc, dpl, dpla)
        frames[0].save(
            os.path.join(dungeon_map_bg_dir, level.name + '.gif'),
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            optimize=False
        )
        frames[0].save(
            os.path.join(dungeon_map_bg_dir, level.name + '.png')
        )


def draw_maps(rom: NintendoDSRom, map_dir, scriptdata: Pmd2ScriptData):
    script_info = load_script_files(get_rom_folder(rom, SCRIPT_DIR))
    count = len(script_info['maps'])
    for i, script_map in enumerate(script_info['maps'].values()):
        if script_map['enter_sse'] is not None:
            draw_scenes_for(rom, i, count,
                            os.path.join(map_dir, script_map['name'], script_map['enter_sse']),
                            script_map['name'], script_map['enter_sse'],
                            SCRIPT_DIR + '/' + script_map['name'] + '/' + script_map['enter_sse'],
                            scriptdata)
        for ssa, _ in script_map['ssas']:
            draw_scenes_for(rom, i, count,
                            os.path.join(map_dir, script_map['name'], ssa),
                            script_map['name'], ssa,
                            SCRIPT_DIR + '/' + script_map['name'] + '/' + ssa,
                            scriptdata)
        for sss in script_map['subscripts'].keys():
            draw_scenes_for(rom, i, count,
                            os.path.join(map_dir, script_map['name'], sss),
                            script_map['name'], sss,
                            SCRIPT_DIR + '/' + script_map['name'] + '/' + sss,
                            scriptdata)


def draw_scene_for__objects(rom: NintendoDSRom, file_name, dim_w, dim_h,  layer: SsaLayer) -> Image.Image:
    img = Image.new('RGBA', (dim_w, dim_h), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img, 'RGBA')
    has_written_something = False
    # Objects
    for i, object in enumerate(layer.objects):
        has_written_something = True
        draw_object(img, draw, object, rom)

    if has_written_something:
        img.save(file_name)

    return img


def draw_scene_for__actors(rom: NintendoDSRom, file_name, dim_w, dim_h,  layer: SsaLayer) -> Image.Image:
    img = Image.new('RGBA', (dim_w, dim_h), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img, 'RGBA')
    has_written_something = False
    # Actors
    for i, actor in enumerate(layer.actors):
        has_written_something = True
        draw_actor(img, draw, actor)

    if has_written_something:
        img.save(file_name)

    return img

def draw_scene_for__rest(rom: NintendoDSRom, file_name, dim_w, dim_h, layer: SsaLayer) -> Image.Image:
    img = Image.new('RGBA', (dim_w, dim_h), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img, 'RGBA')
    has_written_something = False
    # Performers
    for i, performer in enumerate(layer.performers):
        has_written_something = True
        triangle(draw, performer.pos.x_absolute, performer.pos.y_absolute, COLOR_PERFORMER, performer.pos.direction.id)

    # Events
    for i, event in enumerate(layer.events):
        has_written_something = True
        draw.rectangle((
            event.pos.x_absolute, event.pos.y_absolute,
            event.pos.x_absolute + (event.trigger_width * BPC_TILE_DIM),
            event.pos.y_absolute + (event.trigger_height * BPC_TILE_DIM),
        ), COLOR_EVENTS, (0, 0, 0))

    if has_written_something:
        img.save(file_name)

    return img


def draw_actor(img: Image.Image, draw, actor: SsaActor):
    """Draws the sprite for an actor"""
    if actor.actor.entid == 0:
        if draw_invisible_actors_objects:
            return triangle(draw, actor.pos.x_absolute, actor.pos.y_absolute, COLOR_ACTORS, actor.pos.direction.id)
        return

    actor_sprite_id = monster_md[actor.actor.entid].sprite_index

    try:
        sprite = FileType.WAN.deserialize(
            FileType.COMMON_AT.deserialize(monster_bin_pack_file[actor_sprite_id]).decompress()
        )
        ani_group = sprite.get_animations_for_group(sprite.anim_groups[0])
    except (ValueError, TypeError) as e:
        warnings.warn(f"Failed to render a sprite, replaced with placeholder ({actor}, {actor_sprite_id}): {e}")
        if not draw_invisible_actors_objects:
            return
        return triangle(draw, actor.pos.x_absolute, actor.pos.y_absolute, COLOR_ACTORS, actor.pos.direction.id)

    frame_id = actor.pos.direction.id - 1 if actor.pos.direction.id > 0 else 0
    mfg_id = ani_group[frame_id].frames[0].frame_id

    sprite_img, (cx, cy) = sprite.render_frame_group(sprite.frame_groups[mfg_id])
    render_x = actor.pos.x_absolute - cx
    render_y = actor.pos.y_absolute - cy
    img.paste(sprite_img, (render_x, render_y), sprite_img)


def draw_object(img: Image.Image, draw, obj: SsaObject, rom: NintendoDSRom):
    """Draws the sprite for an object"""
    if obj.object.name == 'NULL':
        if draw_invisible_actors_objects:
            # Draw invisible object hitboxes
            w = obj.hitbox_w * BPC_TILE_DIM
            h = obj.hitbox_h * BPC_TILE_DIM
            tlx = obj.pos.x_absolute - int(w / 2)
            tly = obj.pos.y_absolute - int(h / 2)
            draw.rectangle((
                tlx, tly, tlx + w, tly + h,
            ), COLOR_OBJECTS, (0, 0, 0))
        return

    try:
        sprite = FileType.WAN.deserialize(
            rom.getFileByName(f'GROUND/{obj.object.name}.wan')
        )
        ani_group = sprite.get_animations_for_group(sprite.anim_groups[0])
    except (ValueError, TypeError) as e:
        warnings.warn(f"Failed to render a sprite, replaced with placeholder ({obj}): {e}")
        if not draw_invisible_actors_objects:
            return
        return triangle(draw, obj.pos.x_absolute, obj.pos.y_absolute, COLOR_OBJECTS, obj.pos.direction.id)

    frame_id = obj.pos.direction.id - 1 if obj.pos.direction.id > 0 else 0
    if frame_id > len(ani_group) - 1:
        frame_id = 0
    mfg_id = ani_group[frame_id].frames[0].frame_id

    sprite_img, (cx, cy) = sprite.render_frame_group(sprite.frame_groups[mfg_id])
    render_x = obj.pos.x_absolute - cx
    render_y = obj.pos.y_absolute - cy
    img.paste(sprite_img, (render_x, render_y), sprite_img)


def draw_scene__merged(map_bg: List[Image.Image], duration, overlays: List[Image.Image], file_name, dim_w, dim_h):
    new_map_bg = []
    for frame in map_bg:
        frame = frame.convert('RGBA')
        for overlay in overlays:
            frame.paste(overlay, (0, 0, dim_w, dim_h), overlay)
        new_map_bg.append(frame)

    new_map_bg[0].save(
        os.path.join(file_name),
        save_all=True,
        append_images=new_map_bg[1:],
        duration=duration,
        loop=0,
        optimize=False
    )


def draw_scenes_for(rom, i, count, dir_name, map_name, scene_name, file_name, scriptdata: Pmd2ScriptData):
    os.makedirs(os.path.join(dir_name, 'ACTORS'), exist_ok=True)
    os.makedirs(os.path.join(dir_name, 'OBJECTS'), exist_ok=True)
    os.makedirs(os.path.join(dir_name, 'PERF_TRIGGER'), exist_ok=True)
    print(f"{i + 1}/{count} - {map_name} - {scene_name}")
    ssa = FileType.SSA.deserialize(rom.getFileByName(file_name), scriptdata=scriptdata)

    map_bg = map_bgs[map_name]
    dim_w, dim_h = map_bg[0].width, map_bg[0].height

    imgs = []
    for layer_id, layer in enumerate(ssa.layer_list):
        # OBJECTS
        # -> .png
        png_name_actobjs = os.path.join(dir_name, 'OBJECTS', f'layer_{layer_id}.png')
        imgs.append(draw_scene_for__objects(rom, png_name_actobjs, dim_w, dim_h, layer))
        # ACTORS_
        # -> .png
        png_name_actobjs = os.path.join(dir_name, 'ACTORS', f'layer_{layer_id}.png')
        imgs.append(draw_scene_for__actors(rom, png_name_actobjs, dim_w, dim_h, layer))
        # PERF_TRIGGER
        # -> .png
        png_name_perftrgs = os.path.join(dir_name, 'PERF_TRIGGER', f'layer_{layer_id}.png')
        imgs.append(draw_scene_for__rest(rom, png_name_perftrgs, dim_w, dim_h, layer))
        pass

    # {map_name}_{scene_name}_all_merged.webp
    draw_scene__merged(map_bg, map_bg_durations[map_name], 
                       imgs, os.path.join(dir_name, f'{map_name}_{scene_name}_all_merged.webp'), dim_w, dim_h)


def triangle(draw, x, y, fill, direction):
    if direction == 1 or direction == 0:
        # Down
        draw.polygon([(x, y), (x + BPC_TILE_DIM, y), (x + BPC_TILE_DIM_H, y + BPC_TILE_DIM)], fill=fill, outline=(0, 0, 0))
    elif direction == 2:
        # DownRight
        draw.polygon([(x + BPC_TILE_DIM, y), (x + BPC_TILE_DIM, y + BPC_TILE_DIM), (x, y + BPC_TILE_DIM)], fill=fill, outline=(0, 0, 0))
    elif direction == 3:
        # Right
        draw.polygon([(x, y), (x + BPC_TILE_DIM, y + BPC_TILE_DIM_H), (x, y + BPC_TILE_DIM)], fill=fill, outline=(0, 0, 0))
    elif direction == 4:
        # UpRight
        draw.polygon([(x, y), (x + BPC_TILE_DIM, y), (x + BPC_TILE_DIM, y + BPC_TILE_DIM)], fill=fill, outline=(0, 0, 0))
    elif direction == 5:
        # Up
        draw.polygon([(x, y + BPC_TILE_DIM), (x + BPC_TILE_DIM, y + BPC_TILE_DIM), (x + BPC_TILE_DIM_H, y)], fill=fill, outline=(0, 0, 0))
    elif direction == 6:
        # UpLeft
        draw.polygon([(x, y + BPC_TILE_DIM), (x, y), (x + BPC_TILE_DIM, y)], fill=fill, outline=(0, 0, 0))
    elif direction == 7:
        # Left
        draw.polygon([(x + BPC_TILE_DIM, y), (x, y + BPC_TILE_DIM_H), (x + BPC_TILE_DIM, y + BPC_TILE_DIM)], fill=fill, outline=(0, 0, 0))
    elif direction == 8:
        # DownLeft
        draw.polygon([(x, y), (x, y + BPC_TILE_DIM), (x + BPC_TILE_DIM, y + BPC_TILE_DIM)], fill=fill, outline=(0, 0, 0))


def run_main(rom_path, export_dir, actor_mapping_path=None, opt_draw_invisible_actors_objects=True):
    global monster_bin_pack_file, monster_md, draw_invisible_actors_objects, ground_dungeon_tilesets
    draw_invisible_actors_objects = opt_draw_invisible_actors_objects

    print("Loading ROM and core files...")
    os.makedirs(export_dir, exist_ok=True)
    rom = NintendoDSRom.fromFile(rom_path)
    config = get_ppmdu_config_for_rom(rom)

    scriptdata = config.script_data
    if actor_mapping_path:
        with open(actor_mapping_path, 'r') as f:
            actor_mapping = json.load(f)
            for name, entid in actor_mapping.items():
                scriptdata.level_entities__by_name[name].entid = entid

    monster_bin_pack_file = FileType.BIN_PACK.deserialize(rom.getFileByName('MONSTER/monster.bin'))
    monster_md = FileType.MD.deserialize(rom.getFileByName('BALANCE/monster.md'))

    map_bg_dir = os.path.join(export_dir, 'MAP_BG')
    dungeon_map_bg_dir = os.path.join(export_dir, 'MAP_BG_DUNGEON_TILESET')
    print("-- DRAWING BACKGROUNDS --")
    draw_map_bgs(rom, map_bg_dir)
    print("-- DRAWING REST ROOM AND BOSS ROOM BACKGROUNDS --")
    draw_dungeon_map_bgs(rom, dungeon_map_bg_dir, config)
    print("-- DRAWING MAP ENTITIES --")
    draw_maps(rom, os.path.join(export_dir, 'MAP'), scriptdata)


def main():
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(description="""Export the maps from PMD EoS (EU/US).

    The maps are exported into the directory EXPORT_DIR. If the directory doesn't exist, it's created.

    Please note, that the script keeps the map bgs in memory to draw the merged maps, this requires up
    to 2GB of RAM.

    The export directory will contain the following subdirs:
    - MAP_BG                 - Map backgrounds of all maps in the game, as static PNG files and animated GIF files.
    - MAP_BG_DUNGEON_TILESET - Map backgrounds of all maps in the game that use dungeon tilesets for rendering in game,
                               rendered as GIFs.
    - MAP                    - All script maps in the game:
       - {map_name} - A directory for a map. The dimensions of all images in this directory are taken 
                      from the MapBG with the same name.
          - {scene_name} - A directory for a scene (SSA/SSE/SSS)
              - {map_name}_{scene_name}_all_merged.webp - All assets of the scene as one animated WebP
                                                          image. The Map BG of the same name (BPL name)
                                                          is used as a background.
              - OBJECTS - A directory containing PNG files for each layer with all objects on them.
              - ACTORS  - A directory containing PNG files for each layer with all actors on them.
              - PERF_TRIGGER - A directory with PNG files for each layer, with markers for 
                                         all performers, triggers and position marks.

        """, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('rom_path', metavar='ROM_PATH',
                        help='Path to the ROM file.')
    parser.add_argument('export_dir', metavar='EXPORT_DIR',
                        help='Directory to export into.')
    parser.add_argument('-a', '--actors', dest='actor_maping', metavar='PATH', required=False,
                        help='A JSON file with one object, where each key is an name from the actor table, '
                             'and the value is an entity ID from the MONSTER.md. This replaces the entity ID in the '
                             'actor table that will be used to render the actor sprite. Use this to set standin '
                             'sprites for things like the PLAYER or ATTENDANT1 actors.')
    parser.add_argument('-i', '--hide-invisible', dest='hide_invisble', action="store_true",
                        required=False, default=False,
                        help='If set, hide invisible actors and objects.')

    args = parser.parse_args()

    run_main(args.rom_path, args.export_dir, args.actor_maping, not args.hide_invisble)


if __name__ == '__main__':
    main()
