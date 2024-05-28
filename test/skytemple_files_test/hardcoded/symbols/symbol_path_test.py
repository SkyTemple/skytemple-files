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

from skytemple_files.hardcoded.symbols.symbol_path import SymbolPath


class SymbolPathTestCase(unittest.TestCase):

    def test_get_next_array_1(self):
        path = SymbolPath("[12].thing[7]")
        array_path, rest_of_path = path.get_next_array()
        self.assertEqual([12], array_path)
        self.assertEqual(rest_of_path, ".thing[7]")

    def test_get_next_array_2(self):
        path = SymbolPath("[12][34].thing[7]")
        array_path, rest_of_path = path.get_next_array()
        self.assertEqual([12, 34], array_path)
        self.assertEqual(rest_of_path, ".thing[7]")

    def test_get_next_array_3(self):
        path = SymbolPath(".something[12][34].thing[7]")
        with self.assertRaises(ValueError):
            path.get_next_array()

    def test_get_next_array_4(self):
        path = SymbolPath("")
        with self.assertRaises(ValueError):
            path.get_next_array()

    def test_get_next_array_flat_1(self):
        path = SymbolPath("[12].thing[7]")
        array_path, rest_of_path = path.get_next_array_flat()
        self.assertEqual(12, array_path)
        self.assertEqual(rest_of_path, ".thing[7]")

    def test_get_next_array_flat_2(self):
        path = SymbolPath("[12][34].thing[7]")
        array_path, rest_of_path = path.get_next_array_flat()
        self.assertEqual(408, array_path)
        self.assertEqual(rest_of_path, ".thing[7]")

    def test_get_next_array_flat_3(self):
        path = SymbolPath("[12][34][56].thing[7]")
        array_path, rest_of_path = path.get_next_array_flat()
        self.assertEqual(22848, array_path)
        self.assertEqual(rest_of_path, ".thing[7]")

    def test_get_next_field_1(self):
        path = SymbolPath(".thing[7][12].other")
        array_path, rest_of_path = path.get_next_field()
        self.assertEqual("thing", array_path)
        self.assertEqual(rest_of_path, "[7][12].other")

    def test_get_next_field_2(self):
        path = SymbolPath(".thing.something[7][12].other")
        array_path, rest_of_path = path.get_next_field()
        self.assertEqual("thing", array_path)
        self.assertEqual(rest_of_path, ".something[7][12].other")

    def test_get_next_field_3(self):
        path = SymbolPath("[12][34].thing[7]")
        with self.assertRaises(ValueError):
            path.get_next_field()

    def test_get_next_field_4(self):
        path = SymbolPath("")
        with self.assertRaises(ValueError):
            path.get_next_field()
