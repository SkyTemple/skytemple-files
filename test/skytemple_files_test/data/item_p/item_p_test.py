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

import typing
from typing import Optional

from range_typed_integers import u8, u16

from skytemple_files.data.item_p.handler import ItemPHandler
from skytemple_files.data.item_p.protocol import ItemPProtocol, ItemPEntryProtocol
from skytemple_files_test.data.item_p.fixture import (
    EXPECTED_ITEM_P_ENTRIES,
    eq_item_p_protocol,
)
from skytemple_files_test.case import SkyTempleFilesTestCase, romtest, fixpath


class ItemPTestCase(
    SkyTempleFilesTestCase[ItemPHandler, ItemPProtocol[ItemPEntryProtocol]]
):
    handler = ItemPHandler

    def setUp(self) -> None:
        self.fixture = self._load_main_fixture(self._fix_path())

    def test_entries_read(self) -> None:
        self.assertEqual(len(self.fixture.item_list), len(EXPECTED_ITEM_P_ENTRIES))

        for entry_fixture, entry_expected in zip(
            self.fixture.item_list, EXPECTED_ITEM_P_ENTRIES
        ):
            self.assertItemPEntriesEqual(entry_expected, entry_fixture)

    def test_entries_write(self) -> None:
        item_p_after = self._save_and_reload_main_fixture(self.fixture)

        self.assertEqual(len(self.fixture.item_list), len(item_p_after.item_list))

        for entry_before, entry_after in zip(
            self.fixture.item_list, item_p_after.item_list
        ):
            self.assertItemPEntriesEqual(entry_before, entry_after)

    def test_entries_attrs(self):
        e = self.fixture.item_list[0]

        e.buy_price = u16(0xFFF)
        e.sell_price = u16(0xFFF)
        e.category = u8(123)
        e.sprite = u8(123)
        e.item_id = u16(0xFFF)
        e.move_id = u16(0xFFF)
        e.range_min = u8(123)
        e.range_max = u8(123)
        e.palette = u8(123)
        e.action_name = u8(123)
        e.is_valid = True
        e.is_in_td = False
        e.ai_flag_1 = True
        e.ai_flag_2 = False
        e.ai_flag_3 = True

        self.assertEqual(e.buy_price, u16(0xFFF))
        self.assertEqual(e.sell_price, u16(0xFFF))
        self.assertEqual(e.category, u8(123))
        self.assertEqual(e.sprite, u8(123))
        self.assertEqual(e.item_id, u16(0xFFF))
        self.assertEqual(e.move_id, u16(0xFFF))
        self.assertEqual(e.range_min, u8(123))
        self.assertEqual(e.range_max, u8(123))
        self.assertEqual(e.palette, u8(123))
        self.assertEqual(e.action_name, u8(123))
        self.assertEqual(e.is_valid, True)
        self.assertEqual(e.is_in_td, False)
        self.assertEqual(e.ai_flag_1, True)
        self.assertEqual(e.ai_flag_2, False)
        self.assertEqual(e.ai_flag_3, True)


    def test_write_bin(self) -> None:
        item_p_after = self._save_and_reload_main_fixture(self.fixture)
        with open(self._fix_path(), "rb") as f:
            self.assertEqual(f.read(), self.handler.serialize(item_p_after))

    def test_entries_eq(self) -> None:
        for entry_fixture, entry_fixture_plus_1 in zip(
            self.fixture.item_list, self.fixture.item_list[1:]
        ):
            self.assertEqual(entry_fixture, entry_fixture)
            self.assertNotEqual(entry_fixture, entry_fixture_plus_1)

    @romtest(file_names=["item_p.bin"], path="BALANCE/")
    def test_using_rom(self, _, file):
        item_p_before = self.handler.deserialize(file)
        item_p_after = self._save_and_reload_main_fixture(item_p_before)

        self.assertEqual(len(item_p_before.item_list), len(item_p_after.item_list))

        for entry_before, entry_after in zip(
            item_p_before.item_list, item_p_after.item_list
        ):
            self.assertItemPEntriesEqual(entry_before, entry_after)

    def assertItemPEntriesEqual(
        self,
        entry_before: ItemPEntryProtocol,
        entry_after: ItemPEntryProtocol,
        msg: Optional[str] = None,
    ):
        if msg is None:
            msg = ""
        else:
            msg += "\n"
        self.assertTrue(
            eq_item_p_protocol(entry_before, entry_after),
            f"{msg}Entries must be equal.\n1st: \n{entry_before}\n2nd:{entry_after}",
        )

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path(cls):
        return "fixtures", "fixture.bin"
