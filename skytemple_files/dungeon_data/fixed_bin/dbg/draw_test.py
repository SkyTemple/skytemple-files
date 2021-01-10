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
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptDirection
from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_ppmdu_config_for_rom, get_binary_from_rom_ppmdu
from skytemple_files.dungeon_data.fixed_bin.model import TileRule, FloorType, TileRuleType
from skytemple_files.graphics.dma.dma_drawer import DmaDrawer
from skytemple_files.graphics.dma.model import Dma, DmaType
from skytemple_files.graphics.dpc.model import Dpc
from skytemple_files.graphics.dpci.model import Dpci
from skytemple_files.graphics.dpl.model import Dpl
from skytemple_files.graphics.dpla.model import Dpla
from skytemple_files.hardcoded.fixed_floor import HardcodedFixedFloorTables

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(output_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(output_dir, 'test_fixed_floor.nds'))
static_data = get_ppmdu_config_for_rom(rom)

ov29 = get_binary_from_rom_ppmdu(rom, static_data.binaries['overlay/overlay_0029.bin'])

fixed = FileType.FIXED_BIN.deserialize(rom.getFileByName('BALANCE/fixed.bin'), static_data)
dungeon_bin = FileType.DUNGEON_BIN.deserialize(rom.getFileByName('DUNGEON/dungeon.bin'), static_data)
mappa = FileType.MAPPA_BIN.deserialize(rom.getFileByName('BALANCE/mappa_s.bin'))
monster_bin = FileType.BIN_PACK.deserialize(rom.getFileByName('MONSTER/monster.bin'))
monster_md = FileType.MD.deserialize(rom.getFileByName('BALANCE/monster.md'))
entity_table = HardcodedFixedFloorTables.get_entity_spawn_table(ov29, static_data)
item_table = HardcodedFixedFloorTables.get_item_spawn_list(ov29, static_data)
monster_table = HardcodedFixedFloorTables.get_monster_spawn_list(ov29, static_data)


def draw_monster_sprite(img: Image.Image, x: int, y: int, monster_id: int, direction: Pmd2ScriptDirection):
    sprite_index = monster_md.entries[monster_id].sprite_index
    if sprite_index >= len(monster_bin):
        return False

    sprite = FileType.WAN.deserialize(
        FileType.COMMON_AT.deserialize(monster_bin[sprite_index]).decompress()
    )
    ani_group = sprite.get_animations_for_group(sprite.anim_groups[0])

    frame_id = direction.ssb_id if direction is not None else 0
    mfg_id = ani_group[frame_id].frames[0].frame_id

    sprite_img, (cx, cy) = sprite.render_frame_group(sprite.frame_groups[mfg_id])
    render_x = x * 24 - cx + 12
    render_y = y * 24 - cy + 18
    img.paste(sprite_img, (render_x, render_y), sprite_img)
    return True


def draw_text(img: Image.Image, x: int, y: int, color: Tuple[int, int, int], text: str):
    fnt = ImageFont.load_default()
    draw = ImageDraw.Draw(img, 'RGBA')
    draw.text(
        (x * 24, y * 24),
        text,
        font=fnt,
        fill=color
    )


# Tileset IDs to use - if we can't render one for a fixed floor or don't have one use 0.
fixed_floor_tileset_ids = {floor_id: 0 for floor_id in range(0, len(fixed.fixed_floors))}
for floor_list in mappa.floor_lists:
    for floor in floor_list:
        if floor.layout.fixed_floor_id > 0 and floor.layout.tileset_id < 170:
            fixed_floor_tileset_ids[floor.layout.fixed_floor_id] = floor.layout.tileset_id

for i, ffloor in enumerate(fixed.fixed_floors):
    fname = os.path.join(output_dir, f'{i}.png')
    tileset_id = fixed_floor_tileset_ids[i]
    print(f'{i} using tileset {tileset_id}')
    if len(ffloor.actions) < 1:
        print('Skipped empty.')

    dma: Dma = dungeon_bin.get(f'dungeon{tileset_id}.dma')
    dpl: Dpl = dungeon_bin.get(f'dungeon{tileset_id}.dpl')
    dpla: Dpla = dungeon_bin.get(f'dungeon{tileset_id}.dpla')
    dpci: Dpci = dungeon_bin.get(f'dungeon{tileset_id}.dpci')
    dpc: Dpc = dungeon_bin.get(f'dungeon{tileset_id}.dpc')

    draw_outside_as_second_terrain = any(action.tr_type == TileRuleType.SECONDARY_HALLWAY_VOID_ALL
                                         for action in ffloor.actions if isinstance(action, TileRule))
    outside = DmaType.WATER if draw_outside_as_second_terrain else DmaType.WALL

    rules = []
    rules.append([outside] * (ffloor.width + 8))
    rules.append([outside] * (ffloor.width + 8))
    rules.append([outside] * (ffloor.width + 8))
    rules.append([outside] * (ffloor.width + 8))
    ridx = 0
    for y in range(0, ffloor.height):
        row = [outside, outside, outside, outside]
        rules.append(row)
        for x in range(0, ffloor.width):
            action = ffloor.actions[ridx]
            if isinstance(action, TileRule):
                if action.tr_type.floor_type == FloorType.FLOOR:
                    row.append(DmaType.FLOOR)
                elif action.tr_type.floor_type == FloorType.WALL:
                    row.append(DmaType.WALL)
                elif action.tr_type.floor_type == FloorType.SECONDARY:
                    row.append(DmaType.WATER)
                elif action.tr_type.floor_type == FloorType.FLOOR_OR_WALL:
                    row.append(DmaType.WALL)
            else:
                # TODO? Could be something else
                row.append(DmaType.FLOOR)
            ridx += 1
        row += [outside, outside, outside, outside]
    rules.append([outside] * (ffloor.width + 8))
    rules.append([outside] * (ffloor.width + 8))
    rules.append([outside] * (ffloor.width + 8))
    rules.append([outside] * (ffloor.width + 8))

    drawer = DmaDrawer(dma)
    mappings = drawer.get_mappings_for_rules(rules, None, True)
    dungeon_floor = drawer.draw(mappings, dpci, dpc, dpl, dpla)[0].convert('RGBA')

    ridx = 0
    # Draw items and Pokémon
    for y in range(4, ffloor.height + 4):
        for x in range(4, ffloor.width + 4):
            action = ffloor.actions[ridx]
            if isinstance(action, TileRule):
                # Leader spawn tile
                if action.tr_type == TileRuleType.LEADER_SPAWN:
                    draw_monster_sprite(dungeon_floor, x, y, 1, action.direction)
                # Key walls
                if action.tr_type == TileRuleType.FL_WA_ROOM_FLAG_0C or action.tr_type == TileRuleType.FL_WA_ROOM_FLAG_0D:
                    draw_text(dungeon_floor, x, y, (0, 255, 0), f'KEY\nDOOR')
                # Warp zone
                if action.tr_type == TileRuleType.WARP_ZONE or action.tr_type == TileRuleType.WARP_ZONE_2:
                    draw_text(dungeon_floor, x, y, (255, 255, 0),  f'WARP\nZONE')
            else:
                entity_spawn_entry = entity_table[action.entity_rule_id]
                # Monster spawn
                monster_spawn_entry = monster_table[entity_spawn_entry.monster_id]
                if 0 < monster_spawn_entry.md_idx <= 1154:
                    if not draw_monster_sprite(dungeon_floor, x, y, monster_spawn_entry.md_idx, action.direction):
                        direction = action.direction.name if action.direction is not None else 'Down'
                        draw_text(dungeon_floor, x, y, (255, 0, 0), f'P{monster_spawn_entry.md_idx}\n{direction}')
                elif monster_spawn_entry.md_idx > 0:
                    direction = action.direction.name if action.direction is not None else 'Down'
                    draw_text(dungeon_floor, x, y, (255, 0, 0), f'P{monster_spawn_entry.md_idx}\n{direction}')
                # Item spawn
                item_spawn_entry = item_table[entity_spawn_entry.item_id]
                if item_spawn_entry.item_id > 0:
                    draw_text(dungeon_floor, x, y, (0, 0, 255), f'I{item_spawn_entry.item_id}')
            ridx += 1

    dungeon_floor.save(fname)
