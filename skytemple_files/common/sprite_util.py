"""Utility functions for dealing with sprites"""
#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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
from __future__ import annotations

import math
from typing import Optional, List

from skytemple_files.common.types.file_types import FileType
from skytemple_files.container.bin_pack.model import BinPack
from skytemple_files.data.md.protocol import MdEntryProtocol
from skytemple_files.hardcoded.monster_sprite_data_table import (
    MonsterSpriteDataTableEntry,
)


def check_and_correct_monster_sprite_size(
    md_target: MdEntryProtocol,
    *,
    md_gender1: MdEntryProtocol,
    md_gender2: Optional[MdEntryProtocol],
    monster_bin: BinPack,
    sprite_size_table: List[MonsterSpriteDataTableEntry],
    is_expand_poke_list_patch_applied: bool = False,
) -> bool:
    """
    Check that the data in the Pokémon sprite-size metadata
    table matches the currently selected sprite of the Pokémon.
    If not, change the value and save it.

    Arguments:
        - md_target: The MD entry to modify. This should be one of `md_gender1` or `md_gender2`.
        - md_gender1: The primary gender entry.
        - md_gender2: The secondary gender entry or None.
        - monster_bin: monster.bin sprite file
        - sprite_size_table: Sprite size metadata table
        - is_expand_poke_list_patch_applied: Whether ExpandPokeList is applied.

    Returns True if a change was performed.
    If changes were performed the data in the following input parameters may be modified and should
    be written back to ROM:

    - md_target
    - sprite_size_table
    """
    changed = False
    effective_base_attr = "md_index_base"

    # If ExpandPokeList is applied, unk17 and unk18 are the values used instead
    if is_expand_poke_list_patch_applied:
        effective_base_attr = "entid"
        check_value = md_target.unk17
        check_value_file = md_target.unk18
        max_tile_slots_needed, max_file_size_needed = _get_sprite_properties(
            monster_bin, md_target
        )
    else:
        check_value = sprite_size_table[md_gender1.md_index_base].sprite_tile_slots
        check_value_file = sprite_size_table[md_gender1.md_index_base].unk1
        max_tile_slots_needed, max_file_size_needed = _get_sprite_properties(
            monster_bin, md_gender1
        )
        if md_gender2 is not None:
            max_tile_slots_needed2, max_file_size_needed2 = _get_sprite_properties(
                monster_bin, md_gender2
            )
            max_tile_slots_needed = max(max_tile_slots_needed, max_tile_slots_needed2)
            max_file_size_needed = max(max_file_size_needed, max_file_size_needed2)

    if check_value != max_tile_slots_needed:
        if is_expand_poke_list_patch_applied:
            md_target.unk17 = max_tile_slots_needed
        else:
            sprite_size_table[
                getattr(md_gender1, effective_base_attr)
            ].sprite_tile_slots = max_tile_slots_needed

        changed = True

    if check_value_file != max_file_size_needed:
        if is_expand_poke_list_patch_applied:
            md_target.unk18 = max_file_size_needed
        else:
            sprite_size_table[
                getattr(md_gender1, effective_base_attr)
            ].unk1 = max_file_size_needed

        changed = True
    return changed


def _get_sprite_properties(monster_bin: BinPack, entry: MdEntryProtocol):
    if entry.sprite_index < 0:
        return 0, 0
    sprite_bin = monster_bin[entry.sprite_index]
    sprite_bytes = FileType.COMMON_AT.deserialize(sprite_bin).decompress()
    sprite = FileType.WAN.deserialize(sprite_bytes)
    max_tile_slots_needed = max((6, sprite.model.frame_store.max_fragment_alloc_count))
    max_file_size_needed = math.ceil(len(sprite_bytes) / 512)
    return max_tile_slots_needed, max_file_size_needed
