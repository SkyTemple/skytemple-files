#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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

from dataclasses import dataclass
from typing import List

from range_typed_integers import u16, u8

from skytemple_files.common.util import AutoString
from skytemple_files.data.item_p.protocol import ItemPEntryProtocol


# Compares ANY implementation of two ItemPEntryProtocol.
def eq_item_p_protocol(one: ItemPEntryProtocol, two: ItemPEntryProtocol) -> bool:
    return (
        one.buy_price == two.buy_price
        and one.sell_price == two.sell_price
        and one.category == two.category
        and one.sprite == two.sprite
        and one.item_id == two.item_id
        and one.move_id == two.move_id
        and one.range_min == two.range_min
        and one.range_max == two.range_max
        and one.palette == two.palette
        and one.action_name == two.action_name
        and one.is_valid == two.is_valid
        and one.is_in_td == two.is_in_td
        and one.ai_flag_1 == two.ai_flag_1
        and one.ai_flag_2 == two.ai_flag_2
        and one.ai_flag_3 == two.ai_flag_3
    )


# Similar to the "actual" ItemPEntryProtocol Python implementation
# but used for storing expected Fixture values.
@dataclass(eq=False)
class ExpectedItemPEntry(ItemPEntryProtocol, AutoString):
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

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()


EXPECTED_ITEM_P_ENTRIES: List[ExpectedItemPEntry] = [
    ExpectedItemPEntry(
        u16(41038),
        u16(23076),
        u8(243),
        u8(20),
        u16(58032),
        u16(57469),
        u8(179),
        u8(239),
        u8(114),
        u8(5),
        True,
        False,
        True,
        False,
        False,
    ),
    ExpectedItemPEntry(
        u16(24658),
        u16(54010),
        u8(125),
        u8(177),
        u16(59465),
        u16(24462),
        u8(254),
        u8(110),
        u8(108),
        u8(0),
        True,
        True,
        True,
        True,
        False,
    ),
    ExpectedItemPEntry(
        u16(9850),
        u16(63153),
        u8(85),
        u8(5),
        u16(60035),
        u16(63780),
        u8(195),
        u8(165),
        u8(25),
        u8(15),
        False,
        False,
        False,
        False,
        True,
    ),
    ExpectedItemPEntry(
        u16(33115),
        u16(39123),
        u8(64),
        u8(132),
        u16(52965),
        u16(22435),
        u8(226),
        u8(221),
        u8(60),
        u8(2),
        False,
        True,
        True,
        True,
        True,
    ),
    ExpectedItemPEntry(
        u16(64636),
        u16(34448),
        u8(164),
        u8(164),
        u16(2219),
        u16(44636),
        u8(91),
        u8(74),
        u8(229),
        u8(22),
        False,
        False,
        True,
        False,
        True,
    ),
    ExpectedItemPEntry(
        u16(37377),
        u16(30597),
        u8(43),
        u8(42),
        u16(219),
        u16(27750),
        u8(55),
        u8(150),
        u8(215),
        u8(29),
        True,
        True,
        True,
        True,
        False,
    ),
]
