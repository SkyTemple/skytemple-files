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

from enum import Enum
from typing import List

from range_typed_integers import u16, u8, u32, i32

from skytemple_files.common.i18n_util import _
from skytemple_files.common.util import (
    AutoString,
    write_u32,
    read_i32,
    read_u8,
    write_i32,
    read_u16,
    write_u16,
    read_u32,
    write_u8,
)
from skytemple_files.data.anim import (
    GENERAL_DATA_SIZE,
    MOVE_DATA_SIZE,
    TRAP_DATA_SIZE,
    ITEM_DATA_SIZE,
    SPECIAL_MOVE_DATA_SIZE,
)


class AnimPointType(Enum):
    HEAD = 0x00, _("Head")
    LEFT_HAND = 0x01, _("Left Hand")
    RIGHT_HAND = 0x02, _("Right Hand")
    CENTER = 0x03, _("Center")
    NONE = 0xFF, _("None")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, description: str):
        self.description = description


class AnimType(Enum):
    INVALID = 0x00, _("Invalid")
    WAN_FILE0 = 0x01, _("WAN File 0")
    WAN_FILE1 = 0x02, _("WAN File 1")
    WAN_OTHER = 0x03, _("WAN")
    WAT = 0x04, _("WAT")
    SCREEN = 0x05, _("Screen")
    WBA = 0x06, _("WBA")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, description: str):
        self.description = description


class TrapAnim(AutoString):
    anim: u16

    def __init__(self, data: bytes):
        self.anim = read_u16(data, 0)

    def to_bytes(self):
        data = bytearray(TRAP_DATA_SIZE)
        write_u16(data, self.anim, 0)
        return data


class ItemAnim(AutoString):
    anim1: u16
    anim2: u16

    def __init__(self, data: bytes):
        self.anim1 = read_u16(data, 0)
        self.anim2 = read_u16(data, 2)

    def to_bytes(self):
        data = bytearray(ITEM_DATA_SIZE)
        write_u16(data, self.anim1, 0)
        write_u16(data, self.anim2, 2)
        return data


class MoveAnim(AutoString):
    anim1: u16
    anim2: u16
    anim3: u16
    anim4: u16
    dir: int
    flag1: bool
    flag2: bool
    flag3: bool
    flag4: bool
    speed: u32
    animation: u8
    point: AnimPointType
    sfx: u16
    spec_entries: u16
    spec_start: u16

    def __init__(self, data: bytes):
        self.anim1 = read_u16(data, 0)
        self.anim2 = read_u16(data, 2)
        self.anim3 = read_u16(data, 4)
        self.anim4 = read_u16(data, 6)
        flags = read_u32(data, 8)
        self.dir = flags & 0x7
        self.flag1 = bool(flags & 0x8)
        self.flag2 = bool(flags & 0x10)
        self.flag3 = bool(flags & 0x20)
        self.flag4 = bool(flags & 0x40)
        self.speed = read_u32(data, 12)
        self.animation = read_u8(data, 16)
        self.point = AnimPointType(read_u8(data, 17))  # type: ignore
        self.sfx = read_u16(data, 18)
        self.spec_entries = read_u16(data, 20)
        self.spec_start = read_u16(data, 22)

    def to_bytes(self):
        data = bytearray(MOVE_DATA_SIZE)
        write_u16(data, self.anim1, 0)
        write_u16(data, self.anim2, 2)
        write_u16(data, self.anim3, 4)
        write_u16(data, self.anim4, 6)
        flags = (
            self.dir
            | (int(self.flag1) << 3)
            | (int(self.flag2) << 4)
            | (int(self.flag3) << 5)
            | (int(self.flag4) << 6)
        )
        write_u32(data, u32(flags), 8)
        write_u32(data, self.speed, 12)
        write_u8(data, self.animation, 16)
        write_u8(data, self.point.value, 17)
        write_u16(data, self.sfx, 18)
        write_u16(data, self.spec_entries, 20)
        write_u16(data, self.spec_start, 22)
        return data


class GeneralAnim(AutoString):
    anim_type: AnimType
    anim_file: u32
    unk1: u32
    unk2: u32
    sfx: i32
    unk3: u32
    u8: bool
    point: AnimPointType
    unk5: bool
    loop: bool

    def __init__(self, data: bytes):
        self.anim_type = AnimType(read_u32(data, 0))  # type: ignore
        self.anim_file = read_u32(data, 4)
        self.unk1 = read_u32(data, 8)
        self.unk2 = read_u32(data, 12)
        self.sfx = read_i32(data, 16)
        self.unk3 = read_u32(data, 20)
        self.unk4 = bool(read_u8(data, 24))
        self.point = AnimPointType(read_u8(data, 25))  # type: ignore
        self.unk5 = bool(read_u8(data, 26))
        self.loop = bool(read_u8(data, 27))

    def to_bytes(self):
        data = bytearray(GENERAL_DATA_SIZE)
        write_u32(data, self.anim_type.value, 0)
        write_u32(data, self.anim_file, 4)
        write_u32(data, self.unk1, 8)
        write_u32(data, self.unk2, 12)
        write_i32(data, self.sfx, 16)
        write_u32(data, self.unk3, 20)
        write_u8(data, u8(int(self.unk4)), 24)
        write_u8(data, self.point.value, 25)
        write_u8(data, u8(int(self.unk5)), 26)
        write_u8(data, u8(int(self.loop)), 27)
        return data


class SpecMoveAnim(AutoString):
    pkmn_id: u16
    animation: u8
    point: AnimPointType
    sfx: u16

    def __init__(self, data: bytes):
        self.pkmn_id = read_u16(data, 0)
        self.animation = read_u8(data, 2)
        self.point = AnimPointType(read_u8(data, 3))  # type: ignore
        self.sfx = read_u16(data, 4)

    def to_bytes(self):
        data = bytearray(SPECIAL_MOVE_DATA_SIZE)
        write_u16(data, self.pkmn_id, 0)
        write_u8(data, self.animation, 2)
        write_u8(data, self.point.value, 3)
        write_u16(data, self.sfx, 4)
        return data


class Anim(AutoString):
    trap_table: List[TrapAnim]
    item_table: List[ItemAnim]
    move_table: List[MoveAnim]
    general_table: List[GeneralAnim]
    special_move_table: List[SpecMoveAnim]

    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        trap_table_ptr = read_u32(data, 0)
        item_table_ptr = read_u32(data, 4)
        move_table_ptr = read_u32(data, 8)
        general_table_ptr = read_u32(data, 12)
        special_move_table_ptr = read_u32(data, 16)

        self.trap_table = []
        for x in range(trap_table_ptr, item_table_ptr, TRAP_DATA_SIZE):
            self.trap_table.append(TrapAnim(data[x : x + TRAP_DATA_SIZE]))
        self.item_table = []
        for x in range(item_table_ptr, move_table_ptr, ITEM_DATA_SIZE):
            self.item_table.append(ItemAnim(data[x : x + ITEM_DATA_SIZE]))
        self.move_table = []
        for x in range(move_table_ptr, general_table_ptr, MOVE_DATA_SIZE):
            self.move_table.append(MoveAnim(data[x : x + MOVE_DATA_SIZE]))
        self.general_table = []
        for x in range(general_table_ptr, special_move_table_ptr, GENERAL_DATA_SIZE):
            self.general_table.append(GeneralAnim(data[x : x + GENERAL_DATA_SIZE]))
        self.special_move_table = []
        for x in range(special_move_table_ptr, len(data), SPECIAL_MOVE_DATA_SIZE):
            self.special_move_table.append(
                SpecMoveAnim(data[x : x + SPECIAL_MOVE_DATA_SIZE])
            )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Anim):
            return False
        return (
            self.trap_table == other.trap_table
            and self.item_table == other.item_table
            and self.move_table == other.move_table
            and self.general_table == other.general_table
            and self.special_move_table == other.special_move_table
        )
