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
from typing import Optional

from skytemple_files.common.util import *
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
G_FLOOR_IDX_ENTRY_LEN = 4


class MappaGBinReadContainer:
    def __init__(self, data: bytes, header_start: int):
        self.data = data
        self.dungeon_list_index_start = read_uintle(data, header_start + 0x00, 4)
        self.floor_layout_data_start = read_uintle(data, header_start + 0x04, 4)


class StubMappaGFloor:
    """A mappa_g floor that only references an index for all of it's data."""
    def __init__(self, layout_idx: int):
        self.layout_idx: int = layout_idx

    def to_mappa(self) -> bytes:
        data = bytearray(4)
        write_uintle(data, self.layout_idx, 0x00, 2)
        return data


class MappaGFloor(AutoString):
    def __init__(self, layout: 'MappaGFloorLayout'):
        self.layout: MappaGFloorLayout = layout

    @classmethod
    def from_mappa(cls, read: 'MappaGBinReadContainer', floor_data: bytes) -> 'MappaGFloor':
        return cls(MappaGFloorLayout.from_mappa(
            read, read.floor_layout_data_start + 4 * read_uintle(floor_data, 0x00, 2)
        ))

    @staticmethod
    def _read_pointer(data: bytes, start, index):
        return read_uintle(data, start + (4 * index), 4)

    def __eq__(self, other):
        if not isinstance(other, MappaGFloor):
            return False
        return self.layout == other.layout


class MappaGFloorLayout(AutoString):
    def __init__(self, tileset_id: int, fixed_floor_id: int):
        self.tileset_id = tileset_id
        self.fixed_floor_id = fixed_floor_id

    @classmethod
    def from_mappa(cls, read: 'MappaGBinReadContainer', pointer: int):
        return cls(
            tileset_id=read_uintle(read.data, pointer + 0x00),
            fixed_floor_id=read_uintle(read.data, pointer + 0x01),
        )

    def to_mappa(self) -> bytes:
        data = bytearray(4)
        write_uintle(data, self.tileset_id, 0x00, 1)
        write_uintle(data, self.fixed_floor_id, 0x01, 1)
        return data

    def __eq__(self, other):
        if not isinstance(other, MappaGFloorLayout):
            return False
        return self.tileset_id == other.tileset_id and self.fixed_floor_id == other.fixed_floor_id


class MappaGBin(Sir0Serializable):
    def __init__(self, floor_lists: List[List[MappaGFloor]]):
        self.floor_lists = floor_lists

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.dungeon_data.mappa_g_bin.writer import MappaGBinWriter
        return MappaGBinWriter(self).write()

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int, static_data=None) -> 'MappaGBin':
        return cls(cls._read_floor_list(MappaGBinReadContainer(
            content_data, data_pointer
        )))

    @classmethod
    def _read_floor_list(cls, read: MappaGBinReadContainer):
        start = read.dungeon_list_index_start
        end = read.floor_layout_data_start
        dungeons = []
        for i in range(start, end, 4):
            if i + 4 == end:
                end_pnt = start
            else:
                end_pnt = read_uintle(read.data, i + 4, 4)
            dungeons.append(cls._read_floors(
                read, read_uintle(read.data, i, 4), end_pnt
            ))
        return dungeons

    @classmethod
    def _read_floors(cls, read: MappaGBinReadContainer, pointer_beg, pointer_end):
        assert pointer_end > pointer_beg
        # The zeroth floor is just nulls, we omit it.
        empty = bytes(G_FLOOR_IDX_ENTRY_LEN)
        assert read.data[pointer_beg:pointer_beg + G_FLOOR_IDX_ENTRY_LEN] == empty, \
            "The first floor of a dungeon must be a null floor."
        floors = []
        pointer_beg += 4
        for i in range(pointer_beg, pointer_end, 4):
            floor_data = read.data[i:i + G_FLOOR_IDX_ENTRY_LEN]
            floors.append(MappaGFloor.from_mappa(read, floor_data))
            if i >= read.dungeon_list_index_start:
                break
        return floors

    def minimize(self) -> Tuple[
        List[List[StubMappaGFloor]], List[MappaGFloorLayout]
    ]:
        """
        Collects a list of floors, that references indices in other lists, like stored in the mappa_g files.
        If two floors use the same exact data for something, they will be pointing to the same index in the lists,
        there are no duplicates.
        Returned are all lists.
        """
        floor_lists = []
        floor_layouts = [MappaGFloorLayout(0, 0)]
        for floor_list in self.floor_lists:
            stub_floor_list = []
            for floor in floor_list:
                # Layout
                layout_idx = self._find_if_not_exists_insert(floor_layouts, floor.layout)

                stub_floor_list.append(StubMappaGFloor(layout_idx))

            floor_lists.append(stub_floor_list)

        return floor_lists, floor_layouts

    @staticmethod
    def _find_if_not_exists_insert(lst, elem):
        try:
            index = lst.index(elem)
        except ValueError:
            index = len(lst)
            lst.append(elem)
        return index

    def __eq__(self, other):
        if not isinstance(other, MappaGBin):
            return False
        return self.floor_lists == other.floor_lists
