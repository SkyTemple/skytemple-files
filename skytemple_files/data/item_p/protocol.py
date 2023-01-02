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

from abc import abstractmethod
from typing import Protocol, TypeVar, MutableSequence

from range_typed_integers import u16, u8

from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable


class ItemPEntryProtocol(Protocol):
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

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...


E = TypeVar("E", bound=ItemPEntryProtocol)


class ItemPProtocol(Sir0Serializable, Protocol[E]):
    item_list: MutableSequence[E]

    def __init__(self, data: bytes, pointer_to_pointers: int):
        ...
