"""Converts Md models back into the binary format used by the game"""
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

from range_typed_integers import u32, u8, i8, u16, i16, i32

from skytemple_files.common.util import (
    write_u32,
    write_i8,
    write_i32,
    generate_bitfield,
    write_u16,
    write_i16,
    write_u8,
)
from skytemple_files.data.md._model import MD_ENTRY_LEN, Md


class MdWriter:
    def __init__(self):
        self.data: bytearray = bytearray()
        self.bytes_written = 0

    def write(self, model: Md) -> bytes:
        # At max we will need 8 byte header + (number entries * 68):
        self.data = bytearray(8 + len(model.entries) * MD_ENTRY_LEN)
        self.bytes_written = 4
        self.data[0:4] = b"MD\0\0"
        self._write_u32(u32(len(model.entries)))

        for entry in model.entries:
            self._write_u16(entry.entid)
            self._write_u16(entry.unk31)
            self._write_u16(entry.national_pokedex_number)
            self._write_u16(entry.base_movement_speed)
            self._write_u16(entry.pre_evo_index)
            self._write_u16(entry.evo_method)
            self._write_u16(entry.evo_param1)
            self._write_u16(entry.evo_param2)
            self._write_i16(entry.sprite_index)
            self._write_u8(entry.gender)
            self._write_u8(entry.body_size)
            self._write_u8(entry.type_primary)
            self._write_u8(entry.type_secondary)
            self._write_u8(entry.movement_type)
            self._write_u8(entry.iq_group)
            self._write_u8(entry.ability_primary)
            self._write_u8(entry.ability_secondary)
            self._write_u16(
                u16(
                    generate_bitfield(
                        (
                            entry.item_required_for_spawning,
                            entry.can_evolve,
                            entry.bitfield1_5,
                            entry.can_move,
                            entry.bitfield1_3,
                            entry.bitfield1_2,
                            entry.bitfield1_1,
                            entry.bitfield1_0,
                        )
                    )
                )
            )
            self._write_u16(entry.exp_yield)
            self._write_i16(entry.recruit_rate1)
            self._write_u16(entry.base_hp)
            self._write_i16(entry.recruit_rate2)
            self._write_u8(entry.base_atk)
            self._write_u8(entry.base_sp_atk)
            self._write_u8(entry.base_def)
            self._write_u8(entry.base_sp_def)
            self._write_i16(entry.weight)
            self._write_i16(entry.size)
            self._write_u8(entry.unk17)
            self._write_u8(entry.unk18)
            self._write_i8(entry.shadow_size)
            self._write_i8(
                entry.chance_spawn_asleep,
            )
            self._write_u8(entry.hp_regeneration)
            self._write_i8(entry.unk21_h)
            self._write_i16(entry.base_form_index)
            self._write_i16(entry.exclusive_item1)
            self._write_i16(entry.exclusive_item2)
            self._write_i16(entry.exclusive_item3)
            self._write_i16(entry.exclusive_item4)
            self._write_i16(entry.unk27)
            self._write_i16(entry.unk28)
            self._write_i16(entry.unk29)
            self._write_i16(entry.unk30)

        assert self.bytes_written == len(self.data)
        return self.data

    def _write_u8(self, val: u8):
        write_u8(self.data, val, self.bytes_written)
        self.bytes_written += 1

    def _write_i8(self, val: i8):
        write_i8(self.data, val, self.bytes_written)
        self.bytes_written += 1

    def _write_u16(self, val: u16):
        write_u16(self.data, val, self.bytes_written)
        self.bytes_written += 2

    def _write_i16(self, val: i16):
        write_i16(self.data, val, self.bytes_written)
        self.bytes_written += 2

    def _write_u32(self, val: u32):
        write_u32(self.data, val, self.bytes_written)
        self.bytes_written += 4

    def _write_i32(self, val: i32):
        write_i32(self.data, val, self.bytes_written)
        self.bytes_written += 4
