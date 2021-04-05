"""Converts Md models back into the binary format used by the game"""
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
from skytemple_files.data.md.model import Md, MD_ENTRY_LEN


class MdWriter:
    def __init__(self, model: Md):
        self.model = model
        self.data = None
        self.bytes_written = 0

    def write(self) -> bytes:
        # At max we will need 8 byte header + (number entries * 68):
        self.data = bytearray(8 + len(self.model.entries) * MD_ENTRY_LEN)
        self.bytes_written = 4
        self.data[0:4] = b'MD\0\0'
        self._write_data(len(self.model.entries), 4)

        for entry in self.model.entries:
            self._write_data(entry.entid)
            self._write_data(entry.unk31)
            self._write_data(entry.national_pokedex_number)
            self._write_data(entry.base_movement_speed)
            self._write_data(entry.pre_evo_index)
            self._write_data(entry.evo_method.value)
            self._write_data(entry.evo_param1)
            self._write_data(entry.evo_param2.value)
            self._write_data(entry.sprite_index, signed=True)
            self._write_data(entry.gender.value, 1)
            self._write_data(entry.body_size, 1)
            self._write_data(entry.type_primary.value, 1)
            self._write_data(entry.type_secondary.value, 1)
            self._write_data(entry.movement_type.value, 1)
            self._write_data(entry.iq_group.value, 1)
            self._write_data(entry.ability_primary.value, 1)
            self._write_data(entry.ability_secondary.value, 1)
            self._write_data(generate_bitfield((
                entry.item_required_for_spawning, entry.can_evolve, entry.bitfield1_5, entry.can_move,
                entry.bitfield1_3, entry.bitfield1_2, entry.bitfield1_1, entry.bitfield1_0)))
            self._write_data(entry.exp_yield)
            self._write_data(entry.recruit_rate1, signed=True)
            self._write_data(entry.base_hp)
            self._write_data(entry.recruit_rate2, signed=True)
            self._write_data(entry.base_atk, 1)
            self._write_data(entry.base_sp_atk, 1)
            self._write_data(entry.base_def, 1)
            self._write_data(entry.base_sp_def, 1)
            self._write_data(entry.weight, signed=True)
            self._write_data(entry.size, signed=True)
            self._write_data(entry.unk17, 1, signed=True)
            self._write_data(entry.unk18, 1, signed=True)
            self._write_data(entry.shadow_size.value, 1, signed=True)
            self._write_data(entry.chance_spawn_asleep, 1, signed=True)
            self._write_data(entry.hp_regeneration, 1)
            self._write_data(entry.unk21_h, 1, signed=True)
            self._write_data(entry.base_form_index, signed=True)
            self._write_data(entry.exclusive_item1, signed=True)
            self._write_data(entry.exclusive_item2, signed=True)
            self._write_data(entry.exclusive_item3, signed=True)
            self._write_data(entry.exclusive_item4, signed=True)
            self._write_data(entry.unk27, signed=True)
            self._write_data(entry.unk28, signed=True)
            self._write_data(entry.unk29, signed=True)
            self._write_data(entry.unk30, signed=True)

        assert self.bytes_written == len(self.data)
        return self.data

    def _write_data(self, val, length=2, signed=False):
        if signed:
            write_sintle(self.data, val, self.bytes_written, length)
        else:
            write_uintle(self.data, val, self.bytes_written, length)
        self.bytes_written += length
