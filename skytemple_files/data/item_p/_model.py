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

from typing import Optional, List, Tuple, Sequence

from range_typed_integers import u16, u8, u32

from skytemple_files.common.util import (
    AutoString,
    read_u8,
    read_u16,
    write_u16,
    write_u8,
)
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.container.sir0.sir0_util import decode_sir0_pointer_offsets
from skytemple_files.data.item_p import ITEM_P_ENTRY_SIZE
from skytemple_files.data.item_p.protocol import ItemPProtocol, ItemPEntryProtocol


class ItemPEntry(ItemPEntryProtocol, AutoString):
    buy_price: u16
    sell_price: u16
    category: u8
    sprite: u8
    item_id: u16
    move_id: u16
    range_min: u8
    range_max: u8
    palette: u8
    action_name: u8
    is_valid: bool
    is_in_td: bool
    ai_flag_1: bool
    ai_flag_2: bool
    ai_flag_3: bool

    def __init__(self, data: bytes):
        self.buy_price = read_u16(data, 0)  # Buy Price in Kecleon Shops
        self.sell_price = read_u16(data, 2)  # Sell Price in Kecleon Shops
        self.category = read_u8(data, 4)  # Category
        self.sprite = read_u8(data, 5)  # Sprite ID associated to that item
        self.item_id = read_u16(data, 6)  # Item ID
        self.move_id = read_u16(data, 8)  # Move ID associated to that item
        self.range_min = read_u8(
            data, 10
        )  # For stackable, indicates the minimum amount you can get for 1 instance of that item
        self.range_max = read_u8(
            data, 11
        )  # For stackable, indicates the maximum amount you can get for 1 instance of that item
        self.palette = read_u8(data, 12)  # Palette ID associated to that item
        self.action_name = read_u8(
            data, 13
        )  # Action name displayed in dungeon menus (Use, Eat, Ingest, Equip...)
        bitfield = read_u8(data, 14)
        self.is_valid = (bitfield & 0x1) != 0  # Is Valid
        self.is_in_td = (bitfield & 0x2) != 0  # Is in Time/Darkness
        self.ai_flag_1 = (bitfield & 0x20) != 0  # AI flag: Throw at enemies
        self.ai_flag_2 = (bitfield & 0x40) != 0  # AI flag: Throw at allies
        self.ai_flag_3 = (bitfield & 0x80) != 0  # AI flag: Use on self

    def to_bytes(self) -> bytes:
        data = bytearray(ITEM_P_ENTRY_SIZE)
        write_u16(data, self.buy_price, 0)
        write_u16(data, self.sell_price, 2)
        write_u8(data, self.category, 4)
        write_u8(data, self.sprite, 5)
        write_u16(data, self.item_id, 6)
        write_u16(data, self.move_id, 8)
        write_u8(data, self.range_min, 10)
        write_u8(data, self.range_max, 11)
        write_u8(data, self.palette, 12)
        write_u8(data, self.action_name, 13)
        bitfield = 0
        if self.is_valid:
            bitfield |= 0x1
        if self.is_in_td:
            bitfield |= 0x2
        if self.ai_flag_1:
            bitfield |= 0x20
        if self.ai_flag_2:
            bitfield |= 0x40
        if self.ai_flag_3:
            bitfield |= 0x80
        write_u8(data, u8(bitfield), 14)
        return bytes(data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ItemPEntry):
            return False
        return (
            self.buy_price == other.buy_price
            and self.sell_price == other.sell_price
            and self.category == other.category
            and self.sprite == other.sprite
            and self.item_id == other.item_id
            and self.move_id == other.move_id
            and self.range_min == other.range_min
            and self.range_max == other.range_max
            and self.palette == other.palette
            and self.action_name == other.action_name
            and self.is_valid == other.is_valid
            and self.is_in_td == other.is_in_td
            and self.ai_flag_1 == other.ai_flag_1
            and self.ai_flag_2 == other.ai_flag_2
            and self.ai_flag_3 == other.ai_flag_3
        )


class ItemP(ItemPProtocol[ItemPEntry], Sir0Serializable, AutoString):
    def __init__(self, data: bytes, pointer_to_pointers: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.item_list: List[ItemPEntry] = []
        for x in range(0, len(data), ITEM_P_ENTRY_SIZE):
            self.item_list.append(ItemPEntry(data[x : x + ITEM_P_ENTRY_SIZE]))

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: u32,
    ) -> "Sir0Serializable":
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[u32], Optional[u32]]:
        pointer_offsets: List[u32] = []
        header_offset = u32(0)
        data = bytearray(0)
        for i in self.item_list:
            data += i.to_bytes()
        return bytes(data), pointer_offsets, header_offset

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ItemP):
            return False
        return self.item_list == other.item_list

    @staticmethod
    def _decode_ints(data: bytes, pnt_start: u32) -> Sequence[u32]:
        return decode_sir0_pointer_offsets(data, pnt_start, False)
