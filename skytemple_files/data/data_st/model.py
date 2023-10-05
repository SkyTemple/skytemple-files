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


from range_typed_integers import i16

from skytemple_files.common.util import AutoString, read_i16, read_u32


class DataST(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        limit = read_u32(data, 0)
        self.struct_ids = []
        for x in range(4, limit, 2):
            self.struct_ids.append(read_i16(data, x))
        self.struct_data = bytes(data[limit:])

    def nb_struct_ids(self) -> int:
        return len(self.struct_ids)

    def get_item_struct_id(self, item_id: int) -> int:
        return self.struct_ids[item_id]

    def set_item_struct_id(self, item_id: int, struct_id: i16):
        self.struct_ids[item_id] = struct_id

    def add_item_struct_id(self, struct_id: i16):
        self.struct_ids.append(struct_id)

    def get_all_of(self, struct_id: int) -> list[int]:
        ids = []
        for i, x in enumerate(self.struct_ids):
            if x == struct_id:
                ids.append(i)
        return ids

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataST):
            return False
        return (
            self.struct_ids == other.struct_ids
            and self.struct_data == other.struct_data
        )
