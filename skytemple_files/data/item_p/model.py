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
from typing import Optional, Dict

from skytemple_files.common.ppmdu_config.dungeon_data import Pmd2DungeonItemCategory
from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.container.sir0.sir0_util import decode_sir0_pointer_offsets
from skytemple_files.data.item_p import *


class ItemPEntry(AutoString):
    def __init__(self, data: bytes):
        self.buy_price = read_uintle(data, 0, 2) # Buy Price in Kecleon Shops
        self.sell_price = read_uintle(data, 2, 2) # Sell Price in Kecleon Shops
        self.category = read_uintle(data, 4, 1) # Category
        self.sprite = read_uintle(data, 5, 1) # Sprite ID associated to that item
        self.item_id = read_uintle(data, 6, 2) # Item ID
        self.move_id = read_uintle(data, 8, 2) # Move ID associated to that item
        self.range_min = read_uintle(data, 10, 1) # For stackable, indicates the minimum amount you can get for 1 instance of that item
        self.range_max = read_uintle(data, 11, 1) # For stackable, indicates the maximum amount you can get for 1 instance of that item
        self.palette = read_uintle(data, 12, 1) # Palette ID associated to that item
        self.action_name = read_uintle(data, 13, 1) # Action name displayed in dungeon menus (Use, Eat, Ingest, Equip...)
        bitfield = read_uintle(data, 14, 1)
        self.is_valid = (bitfield&0x1)!=0 # Is Valid
        self.is_in_td = (bitfield&0x2)!=0 # Is in Time/Darkness
        self.ai_flag_1 = (bitfield&0x20)!=0 # Flag 1 for the AI?
        self.ai_flag_2 = (bitfield&0x40)!=0 # Flag 2 for the AI?
        self.ai_flag_3 = (bitfield&0x80)!=0 # Flag 3 for the AI?

    def category_enum(self) -> 'MappaItemCategory':
        """:deprecated: Use category_pmd2obj"""
        from skytemple_files.dungeon_data.mappa_bin.item_list import MappaItemCategory
        return MappaItemCategory(self.category)

    def category_pmd2obj(self, item_categories: Dict[int, Pmd2DungeonItemCategory]) -> Pmd2DungeonItemCategory:
        return item_categories[self.category]

    def to_bytes(self) -> bytes:
        data = bytearray(ITEM_P_ENTRY_SIZE)
        write_uintle(data, self.buy_price, 0, 2)
        write_uintle(data, self.sell_price, 2, 2)
        write_uintle(data, self.category, 4, 1)
        write_uintle(data, self.sprite, 5, 1)
        write_uintle(data, self.item_id, 6, 2)
        write_uintle(data, self.move_id, 8, 2)
        write_uintle(data, self.range_min, 10, 1)
        write_uintle(data, self.range_max, 11, 1)
        write_uintle(data, self.palette, 12, 1)
        write_uintle(data, self.action_name, 13, 1)
        bitfield = 0
        if self.is_valid:
            bitfield|=0x1
        if self.is_in_td:
            bitfield|=0x2
        if self.ai_flag_1:
            bitfield|=0x20
        if self.ai_flag_2:
            bitfield|=0x40
        if self.ai_flag_3:
            bitfield|=0x80
        write_uintle(data, bitfield, 14, 1)
        return bytes(data)
    
    def __eq__(self, other):
        if not isinstance(other, ItemPEntry):
            return False
        return self.buy_price == other.buy_price and \
               self.sell_price == other.sell_price and \
               self.category == other.category and \
               self.sprite == other.sprite and \
               self.item_id == other.item_id and \
               self.move_id == other.move_id and \
               self.range_min == other.range_min and \
               self.range_max == other.range_max and \
               self.palette == other.palette and \
               self.action_name == other.action_name and \
               self.is_valid == other.is_valid and \
               self.is_in_td == other.is_in_td and \
               self.ai_flag_1 == other.ai_flag_1 and \
               self.ai_flag_2 == other.ai_flag_2 and \
               self.ai_flag_3 == other.ai_flag_3
               
        
class ItemP(Sir0Serializable, AutoString):
    def __init__(self, data: bytes, header_pointer: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.item_list = []
        for x in range(0, len(data), ITEM_P_ENTRY_SIZE):
            self.item_list.append(ItemPEntry(data[x:x+ITEM_P_ENTRY_SIZE]))

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int,
                    static_data: Optional[Pmd2Data] = None) -> 'Sir0Serializable':
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.data.item_p.writer import ItemPWriter
        return ItemPWriter(self).write()

    def __eq__(self, other):
        if not isinstance(other, ItemP):
            return False
        return self.item_list == other.item_list

    @staticmethod
    def _decode_ints(data: bytes, pnt_start: int) -> List[int]:
        return decode_sir0_pointer_offsets(data, pnt_start, False)
