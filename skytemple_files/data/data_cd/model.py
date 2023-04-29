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

from typing import List

from range_typed_integers import u16

from skytemple_files.common.i18n_util import _
from skytemple_files.common.util import (
    AutoString,
    read_u16,
    read_u32,
)
from skytemple_files.data.data_cd.armips_importer import ArmipsImporter
from skytemple_files.user_error import UserValueError


class DataCD(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        limit = read_u32(data, 0)
        self.items_effects = []
        self.effects_code: List[bytes] = []
        for x in range(4, limit, 2):
            self.items_effects.append(read_u16(data, x))

        last_ptr = read_u32(data, limit)
        for x in range(limit, last_ptr, 8):
            start = read_u32(data, x)
            length = read_u32(data, x + 4)
            self.effects_code.append(data[start : start + length])

    def nb_items(self) -> int:
        return len(self.items_effects)

    def get_item_effect_id(self, item_id: int) -> int:
        return self.items_effects[item_id]

    def set_item_effect_id(self, item_id: int, effect_id: u16) -> None:
        self.items_effects[item_id] = effect_id

    def add_item_effect_id(self, effect_id: u16) -> None:
        self.items_effects.append(effect_id)

    def get_all_of(self, effect_id: int) -> List[int]:
        item_ids = []
        for i, x in enumerate(self.items_effects):
            if x == effect_id:
                item_ids.append(i)
        return item_ids

    def nb_effects(self) -> int:
        return len(self.effects_code)

    def get_effect_code(self, effect_id: int) -> bytes:
        return self.effects_code[effect_id]

    def del_effect_code(self, effect_id: int) -> None:
        if len(self.get_all_of(effect_id)) != 0:
            raise UserValueError(_("To delete this effect, no items must use it."))
        for i in range(len(self.items_effects)):
            if self.items_effects[i] > effect_id:
                self.items_effects[i] -= 1  # type: ignore

        del self.effects_code[effect_id]

    def add_effect_code(self, data: bytes) -> None:
        self.effects_code.append(data)

    def import_armips_effect_code(self, effect_id: int, armips_asm: str) -> None:
        self.set_effect_code(effect_id, ArmipsImporter().assemble(armips_asm))

    def set_effect_code(self, effect_id: int, data: bytes) -> None:
        self.effects_code[effect_id] = data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataCD):
            return False
        return (
            self.items_effects == other.items_effects
            and self.effects_code == other.effects_code
        )
