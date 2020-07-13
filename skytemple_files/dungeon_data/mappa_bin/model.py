#  Copyright 2020 Parakoopa
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
from typing import Optional

from skytemple_files.common.util import *
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.dungeon_data.mappa_bin.floor import MappaFloor
FLOOR_IDX_ENTRY_LEN = 18


class MappaBinReadContainer:
    def __init__(self, data: memoryview, header_start: int):
        self.data = data
        self.dungeon_list_index_start = read_uintle(data, header_start + 0x00, 4)
        self.floor_layout_data_start = read_uintle(data, header_start + 0x04, 4)
        self.item_spawn_list_index_start = read_uintle(data, header_start + 0x08, 4)
        self.monster_spawn_list_index_start = read_uintle(data, header_start + 0x0C, 4)
        self.trap_spawn_list_index_start = read_uintle(data, header_start + 0x10, 4)


class MappaBin(Sir0Serializable):
    def __init__(self, data: bytes, header_start: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        self.dungeons = self._read_dungeon_list(MappaBinReadContainer(data, header_start))
        print("ok.")

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.dungeon_data.mappa_bin.writer import MappaBinWriter
        return MappaBinWriter(self).write()

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int) -> 'MappaBin':
        return cls(content_data, data_pointer)

    def _read_dungeon_list(self, read: MappaBinReadContainer):
        start = read.dungeon_list_index_start
        end = read.floor_layout_data_start
        dungeons = []
        for i in range(start, end, 4):
            dungeons.append(self._read_floors(read, read_uintle(read.data, i, 4)))
        return dungeons

    def _read_floors(self, read: MappaBinReadContainer, pointer):
        # The first floor is just nulls, we omit it.
        empty = bytes(FLOOR_IDX_ENTRY_LEN)
        assert read.data[pointer:pointer + FLOOR_IDX_ENTRY_LEN] == empty, \
            "The first floor of a dungeon must be a null floor."
        floors = []
        pointer += FLOOR_IDX_ENTRY_LEN
        floor_data = read.data[pointer:pointer + FLOOR_IDX_ENTRY_LEN]
        while floor_data != empty:
            floors.append(MappaFloor.from_mappa(read, floor_data))
            pointer += FLOOR_IDX_ENTRY_LEN
            floor_data = read.data[pointer:pointer + FLOOR_IDX_ENTRY_LEN]
            if pointer >= read.dungeon_list_index_start:
                break
        return floors

