#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
from enum import Enum, auto

from skytemple_files.common.util import *
from skytemple_files.common.i18n_util import f, _

from skytemple_files.data.anim import *

class AnimPointType(Enum):
    HEAD       = 0x00, _('Head')
    LEFT_HAND  = 0x01, _('Left Hand')
    RIGHT_HAND = 0x02, _('Right Hand')
    CENTER     = 0x03, _('Center')
    NONE       = 0xFF, _('None')
    
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: int, description: str
    ):
        self.description = description

class AnimType(Enum):
    INVALID   = 0x00, _('Invalid')
    WAN_FILE0 = 0x01, _('WAN File 0')
    WAN_FILE1 = 0x02, _('WAN File 1')
    WAN_OTHER = 0x03, _('WAN')
    WAT       = 0x04, _('WAT')
    SCREEN    = 0x05, _('Screen')
    WBA       = 0x06, _('WBA')
    
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: int, description: str
    ):
        self.description = description
        
class TrapAnim(AutoString):
    def __init__(self, data: bytes):
        self.anim = read_uintle(data, 0, 2)
    def to_bytes(self):
        data = bytearray(TRAP_DATA_SIZE)
        write_uintle(data, self.anim, 0, 2)
        return data

class ItemAnim(AutoString):
    def __init__(self, data: bytes):
        self.anim1 = read_uintle(data, 0, 2)
        self.anim2 = read_uintle(data, 2, 2)
    def to_bytes(self):
        data = bytearray(ITEM_DATA_SIZE)
        write_uintle(data, self.anim1, 0, 2)
        write_uintle(data, self.anim2, 2, 2)
        return data

class MoveAnim(AutoString):
    def __init__(self, data: bytes):
        self.anim1 = read_uintle(data, 0, 2)
        self.anim2 = read_uintle(data, 2, 2)
        self.anim3 = read_uintle(data, 4, 2)
        self.anim4 = read_uintle(data, 6, 2)
        flags = read_uintle(data, 8, 4)
        self.dir = flags&0x7
        self.flag1 = bool(flags&0x8)
        self.flag2 = bool(flags&0x10)
        self.flag3 = bool(flags&0x20)
        self.flag4 = bool(flags&0x40)
        self.speed = read_uintle(data, 12, 4)
        self.animation = read_uintle(data, 16, 1)
        self.point = AnimPointType(read_uintle(data, 17, 1))
        self.sfx = read_uintle(data, 18, 2)
        self.spec_entries = read_uintle(data, 20, 2)
        self.spec_start = read_uintle(data, 22, 2)
    def to_bytes(self):
        data = bytearray(MOVE_DATA_SIZE)
        write_uintle(data, self.anim1, 0, 2)
        write_uintle(data, self.anim2, 2, 2)
        write_uintle(data, self.anim3, 4, 2)
        write_uintle(data, self.anim4, 6, 2)
        flags = self.dir | (int(self.flag1)<<3) | (int(self.flag2)<<4)  | (int(self.flag3)<<5) | (int(self.flag4)<<6)
        write_uintle(data, flags, 8, 4)
        write_uintle(data, self.speed, 12, 4)
        write_uintle(data, self.animation, 16, 1)
        write_uintle(data, self.point.value, 17, 1)
        write_uintle(data, self.sfx, 18, 2)
        write_uintle(data, self.spec_entries, 20, 2)
        write_uintle(data, self.spec_start, 22, 2)
        return data

class GeneralAnim(AutoString):
    def __init__(self, data: bytes):
        self.anim_type = AnimType(read_uintle(data, 0, 4))
        self.anim_file = read_uintle(data, 4, 4)
        self.unk1 = read_uintle(data, 8, 4)
        self.unk2 = read_uintle(data, 12, 4)
        self.sfx = read_sintle(data, 16, 4)
        self.unk3 = read_uintle(data, 20, 4)
        self.unk4 = bool(read_uintle(data, 24, 1))
        self.point = AnimPointType(read_uintle(data, 25, 1))
        self.unk5 = bool(read_uintle(data, 26, 1))
        self.loop = bool(read_uintle(data, 27, 1))
    def to_bytes(self):
        data = bytearray(GENERAL_DATA_SIZE)
        write_uintle(data, self.anim_type.value, 0, 4)
        write_uintle(data, self.anim_file, 4, 4)
        write_uintle(data, self.unk1, 8, 4)
        write_uintle(data, self.unk2, 12, 4)
        write_sintle(data, self.sfx, 16, 4)
        write_uintle(data, self.unk3, 20, 4)
        write_uintle(data, int(self.unk4), 24, 1)
        write_uintle(data, self.point.value, 25, 1)
        write_uintle(data, int(self.unk5), 26, 1)
        write_uintle(data, int(self.loop), 27, 1)
        return data

class SpecMoveAnim(AutoString):
    def __init__(self, data: bytes):
        self.pkmn_id = read_uintle(data, 0, 2)
        self.animation = read_uintle(data, 2, 1)
        self.point = AnimPointType(read_uintle(data, 3, 1))
        self.sfx = read_uintle(data, 4, 2)
    def to_bytes(self):
        data = bytearray(SPECIAL_MOVE_DATA_SIZE)
        write_uintle(data, self.pkmn_id, 0, 2)
        write_uintle(data, self.animation, 2, 1)
        write_uintle(data, self.point.value, 3, 1)
        write_uintle(data, self.sfx, 4, 2)
        return data

class Anim(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        trap_table_ptr = read_uintle(data, 0, 4)
        item_table_ptr = read_uintle(data, 4, 4)
        move_table_ptr = read_uintle(data, 8, 4)
        general_table_ptr = read_uintle(data, 12, 4)
        special_move_table_ptr = read_uintle(data, 16, 4)

        self.trap_table = []
        for x in range(trap_table_ptr,item_table_ptr,TRAP_DATA_SIZE):
            self.trap_table.append(TrapAnim(data[x:x+TRAP_DATA_SIZE]))
        self.item_table = []
        for x in range(item_table_ptr,move_table_ptr,ITEM_DATA_SIZE):
            self.item_table.append(ItemAnim(data[x:x+ITEM_DATA_SIZE]))
        self.move_table = []
        for x in range(move_table_ptr,general_table_ptr,MOVE_DATA_SIZE):
            self.move_table.append(MoveAnim(data[x:x+MOVE_DATA_SIZE]))
        self.general_table = []
        for x in range(general_table_ptr,special_move_table_ptr,GENERAL_DATA_SIZE):
            self.general_table.append(GeneralAnim(data[x:x+GENERAL_DATA_SIZE]))
        self.special_move_table = []
        for x in range(special_move_table_ptr,len(data),SPECIAL_MOVE_DATA_SIZE):
            self.special_move_table.append(SpecMoveAnim(data[x:x+SPECIAL_MOVE_DATA_SIZE]))

    def __eq__(self, other):
        if not isinstance(other, Anim):
            return False
        return self.trap_table == other.trap_table and \
               self.item_table == other.item_table and \
               self.move_table == other.move_table and \
               self.general_table == other.general_table and \
               self.special_move_table == other.special_move_table
