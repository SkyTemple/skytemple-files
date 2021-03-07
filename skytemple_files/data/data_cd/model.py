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


class DataCD(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        limit = read_uintle(data, 0, 4)
        self.items_effects = []
        self.effects_code = []
        for x in range(4, limit, 2):
            self.items_effects.append(read_uintle(data, x, 2))

        last_ptr = read_uintle(data, limit, 4)
        for x in range(limit, last_ptr, 8):
            start = read_uintle(data, x, 4)
            length = read_uintle(data, x+4, 4)
            self.effects_code.append(data[start:start+length])

    def nb_items(self) -> int:
        return len(self.items_effects)

    def get_item_effect_id(self, item_id: int) -> int:
        return self.items_effects[item_id]

    def set_item_effect_id(self, item_id: int, effect_id: int):
        self.items_effects[item_id] = effect_id
        
    def add_item_effect_id(self, effect_id: int):
        self.items_effects.append(effect_id)
        
    def get_all_of(self, effect_id: int) -> List[int]:
        item_ids = []
        for i, x in enumerate(self.items_effects):
            if x==effect_id:
                item_ids.append(i)
        return item_ids
    
    def nb_effects(self) -> int:
        return len(self.effects_code)

    def get_effect_code(self, effect_id: int) -> bytes:
        return self.effects_code[effect_id]
    
    def del_effect_code(self, effect_id: int):
        if len(self.get_all_of(effect_id))!=0:
            raise ValueError(_("To delete this effect, no items must use it."))
        for i in range(len(self.items_effects)):
            if self.items_effects[i]>effect_id:
                self.items_effects[i] -= 1
        
        del self.effects_code[effect_id]
    
    def add_effect_code(self, data: bytes):
        self.effects_code.append(data)

    def import_armips_effect_code(self, effect_id: int, armips_asm: str):
        self.set_effect_code(effect_id, ArmipsImporter().assemble(armips_asm))
        
    def set_effect_code(self, effect_id: int, data: bytes):
        self.effects_code[effect_id] = data
    
    def __eq__(self, other):
        if not isinstance(other, DataCD):
            return False
        return self.items_effects == other.items_effects and \
               self.effects_code == other.effects_code
