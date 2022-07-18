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

from parameterized import parameterized

from skytemple_files.common.util import read_bytes, read_u32
from skytemple_files.container.sir0 import HEADER_LEN
from skytemple_files.container.sir0.handler import Sir0Handler
from skytemple_files.container.sir0.protocol import Sir0Protocol
from skytemple_files_test.container.sir0.fixture import (
    DUMMY_FIXTURES,
    DummySir0Serializable,
)
from skytemple_files_test.case import SkyTempleFilesTestCase, fixpath


class Sir0TestCase(SkyTempleFilesTestCase[Sir0Handler, Sir0Protocol]):
    handler = Sir0Handler

    def setUp(self) -> None:
        self.fixture1 = self._load_main_fixture(self._fix_path(0))
        self.fixture2 = self._load_main_fixture(self._fix_path(1))
        self.fixture3 = self._load_main_fixture(self._fix_path(2))
        self.fixture4 = self._load_main_fixture(self._fix_path(3))

    def test_read(self):
        EXPECTED_DATA = [
            {
                "content": pad([1, 2, 3, 4]),
                "data_pointer": 0,
                "content_pointer_offsets": [],
            },
            {
                "content": pad([32, 32, 32, 32, 34, 34, 34, 34]),
                "data_pointer": 0,
                "content_pointer_offsets": [0, 4],
            },
            {
                "content": pad(
                    [
                        1,
                        2,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        1,
                        0,
                        0,
                        0,
                        20,
                        0,
                        0,
                        0,
                        21,
                        0,
                        0,
                        0,
                        3,
                        4,
                        3,
                        4,
                        5,
                        6,
                    ]
                ),
                "data_pointer": 2,
                "content_pointer_offsets": [4, 8, 12, 16],
            },
            {
                "content": pad(
                    [
                        12,
                        34,
                        0xD2,
                        0x04,
                        0,
                        0,
                        0,
                        0,
                        1,
                        0,
                        0,
                        0,
                        20,
                        0,
                        0,
                        0,
                        21,
                        0,
                        0,
                        0,
                        56,
                        78,
                        3,
                        4,
                        5,
                        6,
                    ]
                ),
                "data_pointer": 2,
                "content_pointer_offsets": [4, 8, 12, 16],
            },
        ]

        self.assertEqual(EXPECTED_DATA[0]["content"], self.fixture1.content)
        self.assertEqual(EXPECTED_DATA[0]["data_pointer"], self.fixture1.data_pointer)
        self.assertEqual(
            EXPECTED_DATA[0]["content_pointer_offsets"],
            self.fixture1.content_pointer_offsets,
        )
        self.assertEqual(EXPECTED_DATA[1]["content"], self.fixture2.content)
        self.assertEqual(EXPECTED_DATA[1]["data_pointer"], self.fixture2.data_pointer)
        self.assertEqual(
            EXPECTED_DATA[1]["content_pointer_offsets"],
            self.fixture2.content_pointer_offsets,
        )
        self.assertEqual(EXPECTED_DATA[2]["content"], self.fixture3.content)
        self.assertEqual(EXPECTED_DATA[2]["data_pointer"], self.fixture3.data_pointer)
        self.assertEqual(
            EXPECTED_DATA[2]["content_pointer_offsets"],
            self.fixture3.content_pointer_offsets,
        )
        self.assertEqual(EXPECTED_DATA[3]["content"], self.fixture4.content)
        self.assertEqual(EXPECTED_DATA[3]["data_pointer"], self.fixture4.data_pointer)
        self.assertEqual(
            EXPECTED_DATA[3]["content_pointer_offsets"],
            self.fixture4.content_pointer_offsets,
        )

    def test_write(self):
        fixture1reloaded = self._save_and_reload_main_fixture(self.fixture1)
        self.assertEqual(self.fixture1.data_pointer, fixture1reloaded.data_pointer)
        self.assertEqual(self.fixture1.content, fixture1reloaded.content)
        self.assertEqual(
            self.fixture1.content_pointer_offsets,
            fixture1reloaded.content_pointer_offsets,
        )
        fixture2reloaded = self._save_and_reload_main_fixture(self.fixture2)
        self.assertEqual(self.fixture2.data_pointer, fixture2reloaded.data_pointer)
        self.assertEqual(self.fixture2.content, fixture2reloaded.content)
        self.assertEqual(
            self.fixture2.content_pointer_offsets,
            fixture2reloaded.content_pointer_offsets,
        )
        fixture3reloaded = self._save_and_reload_main_fixture(self.fixture3)
        self.assertEqual(self.fixture3.data_pointer, fixture3reloaded.data_pointer)
        self.assertEqual(self.fixture3.content, fixture3reloaded.content)
        self.assertEqual(
            self.fixture3.content_pointer_offsets,
            fixture3reloaded.content_pointer_offsets,
        )
        fixture4reloaded = self._save_and_reload_main_fixture(self.fixture4)
        self.assertEqual(self.fixture4.data_pointer, fixture4reloaded.data_pointer)
        self.assertEqual(self.fixture4.content, fixture4reloaded.content)
        self.assertEqual(
            self.fixture4.content_pointer_offsets,
            fixture4reloaded.content_pointer_offsets,
        )

    @parameterized.expand(DUMMY_FIXTURES)
    def test_wrap(self, _idx, dummy: DummySir0Serializable):
        sir0ed = self.handler.wrap(*dummy.sir0_serialize_parts())
        sir0ed_bytes = self.handler.serialize(sir0ed)
        self.assertSir0StructureValid(sir0ed_bytes)
        self.assertPointersInSir0Valid(sir0ed_bytes)

    @parameterized.expand(DUMMY_FIXTURES)
    def test_wrap_obj(self, _idx, dummy: DummySir0Serializable):
        sir0ed = self.handler.wrap_obj(dummy)
        sir0ed_bytes = self.handler.serialize(sir0ed)
        self.assertSir0StructureValid(sir0ed_bytes)
        self.assertPointersInSir0Valid(sir0ed_bytes)

    @parameterized.expand(DUMMY_FIXTURES)
    def test_unwrap_obj(self, _idx, dummy: DummySir0Serializable):
        sir0ed = self.handler.wrap_obj(dummy)
        sir0ed_bytes = self.handler.serialize(sir0ed)
        sir0ed_back = self.handler.deserialize(sir0ed_bytes)
        unwrapped = self.handler.unwrap_obj(sir0ed_back, DummySir0Serializable)
        self.assertEqual(dummy.a, unwrapped.a)
        self.assertEqual(dummy.b, unwrapped.b)
        self.assertEqual(dummy.c, unwrapped.c)
        self.assertEqual(dummy.d, unwrapped.d)
        self.assertEqual(dummy.header_val, unwrapped.header_val)

    def assertSir0StructureValid(self, dummy_as_sir0_bytes: bytes):
        """
        This asserts that the structure of the provided DummySir0Serializable is valid.
        """
        self.assertEqual(read_bytes(dummy_as_sir0_bytes, 0, 4), b"SIR0")
        data_ptr = read_u32(dummy_as_sir0_bytes, 4)
        self.assertEqual(data_ptr, 2 + HEADER_LEN)
        ptr_start = read_u32(dummy_as_sir0_bytes, 8)
        expected_encoded_pointers = b"\x04\x04\x0c\x04\x04\x04\x00"
        self.assertEqual(
            expected_encoded_pointers,
            dummy_as_sir0_bytes[ptr_start : ptr_start + len(expected_encoded_pointers)],
        )

    def assertPointersInSir0Valid(self, dummy_as_sir0_bytes: bytes):
        """
        This asserts that the sir0+bytes-encoded representation of DummySir0Serializable has valid sir0
        encoded pointer offsets.
        """
        self.assertEqual(
            16, read_u32(dummy_as_sir0_bytes[HEADER_LEN + 4 : HEADER_LEN + 8])
        )
        self.assertEqual(
            17, read_u32(dummy_as_sir0_bytes[HEADER_LEN + 8 : HEADER_LEN + 12])
        )
        self.assertEqual(
            36, read_u32(dummy_as_sir0_bytes[HEADER_LEN + 12 : HEADER_LEN + 16])
        )
        self.assertEqual(
            37, read_u32(dummy_as_sir0_bytes[HEADER_LEN + 16 : HEADER_LEN + 20])
        )

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path(cls, idx: int):
        return "fixtures", f"{idx}.bin"


def pad(inp: typing.List[int]) -> bytes:
    """Pad to be aligned with 16 bytes."""
    val = bytes(inp)
    if len(val) % 16 == 0:
        return val
    return val + bytes([0xAA] * (16 - (len(val) % 16)))
