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

from skytemple_files.hardcoded.symbols.c_type import CType


class CTypeTestCase(unittest.TestCase):
    def test_from_str_1(self):
        c_type = CType.from_str("int")
        self.assertEqual("int", c_type.base_type)
        self.assertEqual([], c_type.dim_sizes)

    def test_from_str_2(self):
        c_type = CType.from_str("int[3]")
        self.assertEqual("int", c_type.base_type)
        self.assertEqual([3], c_type.dim_sizes)

    def test_from_str_3(self):
        c_type = CType.from_str("int[3][4]")
        self.assertEqual("int", c_type.base_type)
        self.assertEqual([3, 4], c_type.dim_sizes)

    def test_from_str_4(self):
        c_type = CType.from_str("struct thing[2][2]")
        self.assertEqual("struct thing", c_type.base_type)
        self.assertEqual([2, 2], c_type.dim_sizes)

    def test_from_str_5(self):
        with self.assertRaises(ValueError):
            CType.from_str("int[]")

    def test_from_str_6(self):
        with self.assertRaises(ValueError):
            CType.from_str("int[2]aaaa")

    def test_from_str_7(self):
        with self.assertRaises(ValueError):
            CType.from_str("aaaa int[2]")

    def test_from_str_8(self):
        with self.assertRaises(ValueError):
            CType.from_str("int[2] int[2]")

    def test_from_str_9(self):
        with self.assertRaises(ValueError):
            CType.from_str("")

    def test_dim_down_array_1(self):
        c_type = CType.from_str("int[10][5][3]")
        new_type = CType.dim_down_array_type(c_type)
        self.assertEqual("int", new_type.base_type)
        self.assertEqual([5, 3], new_type.dim_sizes)

    def test_dim_down_array_2(self):
        c_type = CType.from_str("int[5][3]")
        new_type = CType.dim_down_array_type(c_type)
        self.assertEqual("int", new_type.base_type)
        self.assertEqual([3], new_type.dim_sizes)

    def test_dim_down_array_3(self):
        c_type = CType.from_str("int[3]")
        new_type = CType.dim_down_array_type(c_type)
        self.assertEqual("int", new_type.base_type)
        self.assertEqual([], new_type.dim_sizes)

    def test_dim_down_array_4(self):
        c_type = CType.from_str("int")
        with self.assertRaises(ValueError):
            CType.dim_down_array_type(c_type)

    def test_get_total_num_elements_1(self):
        c_type = CType.from_str("int")
        self.assertEqual(1, c_type.get_total_num_elements())

    def test_get_total_num_elements_2(self):
        c_type = CType.from_str("int[3]")
        self.assertEqual(3, c_type.get_total_num_elements())

    def test_get_total_num_elements_3(self):
        c_type = CType.from_str("int[3][4]")
        self.assertEqual(12, c_type.get_total_num_elements())

    def test_get_total_num_elements_4(self):
        c_type = CType.from_str("int[3][4][5]")
        self.assertEqual(60, c_type.get_total_num_elements())

    def test_get_size_1(self):
        c_type = CType.from_str("int")
        self.assertEqual(4, c_type.get_size())

    def test_get_size_2(self):
        c_type = CType.from_str("int[4]")
        self.assertEqual(16, c_type.get_size())

    def test_get_size_3(self):
        c_type = CType.from_str("uint8[10]")
        self.assertEqual(10, c_type.get_size())

    def test_get_size_4(self):
        c_type = CType.from_str("uint8[10][3]")
        self.assertEqual(30, c_type.get_size())

    def test_get_size_5(self):
        c_type = CType.from_str("struct rgba[5]")
        self.assertEqual(20, c_type.get_size())
