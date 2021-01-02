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
from typing import List

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import read_uintle
from skytemple_files.container.sir0.handler import Sir0Handler
from skytemple_files.dungeon_data.mappa_bin.handler import MappaBinHandler

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(output_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))


def validate_mappa_sir0(data: bytes, header_start: int, content_pointer_offsets: List[int]):
    """
    Reads through the mappa file, collects all known possible pointers and checks if all of them are in the
    pointer list, and no more.
    """
    # The 5 header pointer
    count_pointers = 5
    dungeon_list_index_start = read_uintle(data, header_start + 0x00, 4)
    assert header_start + 0x00 in content_pointer_offsets
    floor_layout_data_start = read_uintle(data, header_start + 0x04, 4)
    assert header_start + 0x04 in content_pointer_offsets
    item_spawn_list_index_start = read_uintle(data, header_start + 0x08, 4)
    assert header_start + 0x08 in content_pointer_offsets
    monster_spawn_list_index_start = read_uintle(data, header_start + 0x0C, 4)
    assert header_start + 0x0C in content_pointer_offsets
    trap_spawn_list_index_start = read_uintle(data, header_start + 0x10, 4)
    assert header_start + 0x10 in content_pointer_offsets
    # Read floor list list
    start = dungeon_list_index_start
    end = floor_layout_data_start
    dungeons = []
    for i in range(start, end, 4):
        pnt_floor_index_entry = read_uintle(data, i, 4)
        assert i in content_pointer_offsets
        count_pointers += 1
        # Read floor list
        assert not any(x in content_pointer_offsets for x in range(pnt_floor_index_entry, pnt_floor_index_entry + 18))
        floor_data_pos = floor_layout_data_start + 32 * read_uintle(data, pnt_floor_index_entry + 0x00, 2)
        assert floor_data_pos not in content_pointer_offsets
        pokemon_spawn_pnt = monster_spawn_list_index_start + 4 * read_uintle(data, pnt_floor_index_entry + 0x02, 2)
        assert pokemon_spawn_pnt in content_pointer_offsets
        trap_spawn_pnt = trap_spawn_list_index_start + 4 * read_uintle(data, pnt_floor_index_entry + 0x04, 2)
        assert trap_spawn_pnt in content_pointer_offsets
        item_spawn_pnt = item_spawn_list_index_start + 4 * read_uintle(data, pnt_floor_index_entry + 0x06, 2)
        assert item_spawn_pnt in content_pointer_offsets
        item_shop_spawn_pnt = item_spawn_list_index_start + 4 * read_uintle(data, pnt_floor_index_entry + 0x08, 2)
        assert item_shop_spawn_pnt in content_pointer_offsets
        item_mhouse_spawn_pnt = item_spawn_list_index_start + 4 * read_uintle(data, pnt_floor_index_entry + 0x0A, 2)
        assert item_mhouse_spawn_pnt in content_pointer_offsets
        item_buried_spawn_pnt = item_spawn_list_index_start + 4 * read_uintle(data, pnt_floor_index_entry + 0x0C, 2)
        assert item_buried_spawn_pnt in content_pointer_offsets
        item_unk1_spawn_pnt = item_spawn_list_index_start + 4 * read_uintle(data, pnt_floor_index_entry + 0x0E, 2)
        assert item_unk1_spawn_pnt in content_pointer_offsets
        item_unk2_spawn_pnt = item_spawn_list_index_start + 4 * read_uintle(data, pnt_floor_index_entry + 0x10, 2)
        assert item_unk2_spawn_pnt in content_pointer_offsets
    return dungeons


mappa_bin = rom.getFileByName('BALANCE/mappa_s.bin')
mappa_sir0 = Sir0Handler.deserialize(mappa_bin)
mappa = MappaBinHandler.deserialize(mappa_bin)

validate_mappa_sir0(mappa_sir0.content, mappa_sir0.data_pointer, mappa_sir0.content_pointer_offsets)
rewrapped = Sir0Handler.wrap_obj(mappa)
validate_mappa_sir0(rewrapped.content, rewrapped.data_pointer, rewrapped.content_pointer_offsets)

#assert len(mappa_sir0.content_pointer_offsets) == len(rewrapped.content_pointer_offsets)

