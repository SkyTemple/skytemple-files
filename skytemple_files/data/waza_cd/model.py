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

class WazaCD(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        limit = read_uintle(data, 0, 4)
        self.moves_effects = []
        self.effects_code = []
        for x in range(4, limit, 2):
            self.moves_effects.append(read_uintle(data, x, 2))

        last_ptr = read_uintle(data, limit, 4)
        for x in range(limit, last_ptr, 8):
            start = read_uintle(data, x, 4)
            length = read_uintle(data, x+4, 4)
            self.effects_code.append(data[start:start+length])

    def nb_moves(self) -> bytes:
        return len(self.moves_effects)
    def get_move_effect_id(self, move_id: int) -> int:
        return self.moves_effects[move_id]
    def set_move_effect_id(self, move_id: int, effect_id: int):
        self.moves_effects[move_id] = effect_id
        
    def get_all_of(self, effect_id: int) -> int:
        move_ids = []
        for i, x in enumerate(self.moves_effects):
            if x==effect_id:
                move_ids.append(i)
        return move_ids
    
    def nb_effects(self) -> bytes:
        return len(self.effects_code)
    def get_effect_code(self, effect_id: int) -> bytes:
        return self.effects_code[effect_id]
    
    def del_effect_code(self, effect_id: int):
        if len(self.get_all_of(effect_id))!=0:
            raise ValueError("To delete this effect, no moves must use it.")
        for i in range(len(self.moves_effects)):
            if self.moves_effects[i]>effect_id:
                self.moves_effects[i] -= 1
        
        del self.effects_code[effect_id]
    
    def add_effect_code(self, data: bytes):
        self.effects_code.append(data)
        
    def set_effect_code(self, effect_id: int, data: bytes):
        self.effects_code[effect_id] = data
    
    def __eq__(self, other):
        if not isinstance(other, WazaCD):
            return False
        return self.moves_effects == other.moves_effects and \
               self.effects_code == other.effects_code
