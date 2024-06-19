#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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
import unittest
from typing import Optional, cast

from pmdsky_debug_py.protocol import Symbol

from skytemple_files.common.rw_value import RWInt32Value, RWFx6416Value
from skytemple_files.hardcoded.symbols.manual.structs import StructField
from skytemple_files.hardcoded.symbols.rw_symbol import RWSymbol, RWSimpleSymbol, RWArraySymbol, RWStructSymbol
from skytemple_files.hardcoded.symbols.unsupported_type_error import UnsupportedTypeError


SAMPLE_STRUCT_FIELDS = [
    StructField("field_0x0", 0, "int"),
    StructField("field_0x4", 4, "bool"),
    StructField("field_0x8", 8, "struct fx64_16")
]


class RWSymbolTestCase(unittest.TestCase):

    sample_symbol: Symbol[Optional[list[int]], None]

    def setUp(self) -> None:
        self.sample_symbol = Symbol(
            [0x1234],
            [0x02001234],
            0x4,
            "sample_symbol",
            "A sample symbol",
            "int",
        )

    def test_from_basic_data_1(self):
        rw = RWSymbol.from_basic_data("test", 0, "int")
        self.assertIsInstance(rw, RWSimpleSymbol)
        self.assertEqual("test", rw.name)

    def test_from_basic_data_2(self):
        rw = RWSymbol.from_basic_data("test", 0, "char[25]")
        self.assertIsInstance(rw, RWSimpleSymbol)

    def test_from_basic_data_3(self):
        rw = RWSymbol.from_basic_data("test", 0, "int[25]")
        self.assertIsInstance(rw, RWArraySymbol)

    def test_from_basic_data_4(self):
        rw = RWSymbol.from_basic_data("test", 0, "struct rgba")
        self.assertIsInstance(rw, RWStructSymbol)

    def test_from_basic_data_5(self):
        rw = RWSymbol.from_basic_data("test", 0, "struct monster_id_8")
        self.assertIsInstance(rw, RWSimpleSymbol)

    def test_from_basic_data_6(self):
        with self.assertRaises(UnsupportedTypeError):
            RWSymbol.from_basic_data("test", 0, "int *")

    def test_from_basic_data_7(self):
        with self.assertRaises(UnsupportedTypeError):
            RWSymbol.from_basic_data("test", 0, "int[0]")

    def test_from_symbol(self):
        rw = RWSymbol.from_symbol(self.sample_symbol)
        self.assertIsInstance(rw, RWSimpleSymbol)
        self.assertEqual("sample_symbol", rw.name)

    # RWArraySymbol tests

    def test_array_symbol(self):
        rw = RWArraySymbol("test", 0, "int[3]")
        self.assertEqual(3, len(rw.elements))
        self.assertIsInstance(rw.elements[2], RWSimpleSymbol)

        rw_2: RWSimpleSymbol = cast(RWSimpleSymbol, rw.elements[2])
        rw_value = rw_2.get_rw_value()
        self.assertIsInstance(rw_value, RWInt32Value)
        self.assertEqual(8, rw_value.offset)

    # RWStructSymbol tests

    def test_struct_symbol(self):
        rw = RWStructSymbol("test", 0, SAMPLE_STRUCT_FIELDS)
        self.assertIsInstance(rw.fields["field_0x8"], RWSimpleSymbol)

        rw_0x8: RWSimpleSymbol = cast(RWSimpleSymbol, rw.fields["field_0x8"])
        rw_value = rw_0x8.get_rw_value()
        self.assertIsInstance(rw_value, RWFx6416Value)
        self.assertEqual(8, rw_value.offset)
