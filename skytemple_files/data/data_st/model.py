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

from skytemple_files.common.util import *
from skytemple_files.common.i18n_util import _
from skytemple_files.data.data_cd.armips_importer import ArmipsImporter


class DataST(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        limit = read_uintle(data, 0, 4)
        self.struct_ids = []
        for x in range(4, limit, 2):
            self.struct_ids.append(read_sintle(data, x, 2))
        self.struct_data = bytes(data[limit:])

    def nb_struct_ids(self) -> int:
        return len(self.struct_ids)

    def get_item_struct_id(self, item_id: int) -> int:
        return self.struct_ids[item_id]

    def set_item_struct_id(self, item_id: int, struct_id: int):
        self.struct_ids[item_id] = struct_id
        
    def add_item_struct_id(self, struct_id: int):
        self.struct_ids.append(struct_id)
        
    def get_all_of(self, struct_id: int) -> List[int]:
        ids = []
        for i, x in enumerate(self.struct_ids):
            if x==struct_id:
                ids.append(i)
        return ids
    
    
    def __eq__(self, other):
        if not isinstance(other, DataST):
            return False
        return self.struct_ids == other.struct_ids and \
               self.struct_data == other.struct_data
