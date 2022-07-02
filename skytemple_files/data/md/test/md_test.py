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
from typing import Sequence, Tuple, Optional

from skytemple_files.data.md.handler import MdHandler
from skytemple_files.data.md.protocol import MdProtocol, MdEntryProtocol
from skytemple_files.data.md.test.fixture import (
    eq_md_protocol,
    EXPECTED_MD_ENTRIES,
    EXPECTED_BASE_INDICES,
    FIX_NUM_ENTITIES,
    FIX_MAX_POSSIBLE,
    EXPECTED_NEW_ENTRY,
    EXPECTED_NEW_ENTRY_BASE_ID,
)
from skytemple_files.test.case import SkyTempleFilesTestCase, fixpath, romtest


class MdTestCase(SkyTempleFilesTestCase[MdHandler, MdProtocol[MdEntryProtocol]]):
    handler = MdHandler

    def setUp(self) -> None:
        self.fixture = self._load_main_fixture(self._fix_path())

    def test_entries_read(self) -> None:
        self.assertEqual(len(self.fixture.entries), len(EXPECTED_MD_ENTRIES))

        for entry_fixture, entry_expected in zip(
            self.fixture.entries, EXPECTED_MD_ENTRIES
        ):
            self.assertMdEntriesEqual(entry_expected, entry_fixture)

    def test_entries_write(self) -> None:
        md_after = self._save_and_reload_main_fixture(self.fixture)

        self.assertEqual(len(self.fixture.entries), len(md_after.entries))

        for entry_before, entry_after in zip(self.fixture.entries, md_after.entries):
            self.assertMdEntriesEqual(entry_before, entry_after)

    def test_md_entry_md_index_base_and_properties(self) -> None:
        self.assertEqual(len(self.fixture.entries), len(EXPECTED_BASE_INDICES))
        self.handler.properties().num_entities = 123456
        self.handler.properties().max_possible = 123456
        self.handler.properties().num_entities = FIX_NUM_ENTITIES
        self.handler.properties().max_possible = FIX_MAX_POSSIBLE

        for i, (entry_fixture, expected_md_index_base) in enumerate(
            zip(self.fixture.entries, EXPECTED_BASE_INDICES)
        ):
            self.assertEqual(
                entry_fixture.md_index_base,
                expected_md_index_base,
                f"Expected the md_index_base to match in iteration {i}",
            )

    def test_md_entry_new_empty(self) -> None:
        self.assertMdEntriesEqual(
            self.handler.get_entry_model_cls().new_empty(EXPECTED_NEW_ENTRY_BASE_ID),
            EXPECTED_NEW_ENTRY,
        )

    def test_md_get_by_id(self) -> None:
        self.assertMdEntriesEqual(
            EXPECTED_MD_ENTRIES[0],
            self.fixture.get_by_index(0),
        )
        self.assertMdEntriesEqual(
            EXPECTED_MD_ENTRIES[1],
            self.fixture.get_by_index(1),
        )
        self.assertMdEntriesEqual(
            EXPECTED_MD_ENTRIES[4],
            self.fixture.get_by_index(4),
        )

    def test_md_get_by_entity_id(self) -> None:
        self.assertMdIndexTuplesEqual(
            [(0, EXPECTED_MD_ENTRIES[0]), (6, EXPECTED_MD_ENTRIES[6])],
            self.fixture.get_by_entity_id(0),
        )
        self.assertMdIndexTuplesEqual(
            [(1, EXPECTED_MD_ENTRIES[1]), (7, EXPECTED_MD_ENTRIES[7])],
            self.fixture.get_by_entity_id(1),
        )
        self.assertMdIndexTuplesEqual(
            [(4, EXPECTED_MD_ENTRIES[4])],
            self.fixture.get_by_entity_id(4),
        )

    def test_md___len__(self) -> None:
        self.assertEqual(len(EXPECTED_MD_ENTRIES), len(self.fixture))

    def test_md___getitem__(self) -> None:
        self.assertMdEntriesEqual(
            self.fixture[0],
            EXPECTED_MD_ENTRIES[0],
        )
        self.assertMdEntriesEqual(
            self.fixture[1],
            EXPECTED_MD_ENTRIES[1],
        )
        self.assertMdEntriesEqual(
            self.fixture[4],
            EXPECTED_MD_ENTRIES[4],
        )

    def test_md___setitem__(self) -> None:
        self.fixture[0] = self.fixture.entries[5]
        self.fixture[1] = self.fixture.entries[6]
        self.fixture[4] = self.fixture.entries[7]
        self.assertMdEntriesEqual(
            EXPECTED_MD_ENTRIES[5],
            self.fixture[0],
        )
        self.assertMdEntriesEqual(
            EXPECTED_MD_ENTRIES[6],
            self.fixture[1],
        )
        self.assertMdEntriesEqual(
            EXPECTED_MD_ENTRIES[7],
            self.fixture[4],
        )

    def test_md___delitem__(self) -> None:
        del self.fixture[2]
        cpy_expected = list(EXPECTED_MD_ENTRIES)
        del cpy_expected[2]

        self.assertEqual(len(self.fixture), len(cpy_expected))

        for entry_fixture, entry_expected in zip(self.fixture.entries, cpy_expected):
            self.assertMdEntriesEqual(entry_expected, entry_fixture)

    def test_md___iter__(self) -> None:
        self.assertEqual(len(self.fixture), len(EXPECTED_MD_ENTRIES))

        for entry_fixture, entry_expected in zip(self.fixture, EXPECTED_MD_ENTRIES):
            self.assertMdEntriesEqual(entry_expected, entry_fixture)

    @romtest(file_ext="md", path="BALANCE/")
    def test_using_rom(self, _, file):
        md_before = self.handler.deserialize(file)
        md_after = self._save_and_reload_main_fixture(md_before)

        self.assertEqual(len(md_before.entries), len(md_after.entries))

        for entry_before, entry_after in zip(md_before.entries, md_after.entries):
            self.assertMdEntriesEqual(entry_before, entry_after)

    def assertMdIndexTuplesEqual(
        self,
        a: Sequence[Tuple[int, MdEntryProtocol]],
        b: Sequence[Tuple[int, MdEntryProtocol]],
    ):
        self.assertEqual(len(a), len(b))
        for i, (aa, bb) in enumerate(zip(a, b)):
            self.assertEqual(aa[0], bb[0], f"The md_index must match in iteration {i}")
            self.assertMdEntriesEqual(
                aa[1], bb[1], "The md entry must match in iteration {i}"
            )

    def assertMdEntriesEqual(
        self,
        entry_before: MdEntryProtocol,
        entry_after: MdEntryProtocol,
        msg: Optional[str] = None,
    ):
        if msg is None:
            msg = ""
        else:
            msg += "\n"
        self.assertTrue(
            eq_md_protocol(entry_before, entry_after),
            f"{msg}Entries must be equal.\n1st: \n{entry_before}\n2nd:{entry_after}",
        )

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path(cls):
        return "fixtures", "fixture.md"
