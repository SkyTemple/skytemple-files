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
from __future__ import annotations

import unittest

from explorerscript.error import SsbCompilerError
from explorerscript.ssb_converting.ssb_data_types import SsbOpParamFixedPoint

from skytemple_files.script.ssb.ssb_number import (
    parse_ssb_encoding,
    fixed_point_to_ssb_encoding,
)

FP = 0x8000


class SsbNumberTestCase(unittest.TestCase):
    def test_parse_ssb_encoding_ints(self):
        self.assertEqual(0, parse_ssb_encoding(0))
        self.assertEqual(1, parse_ssb_encoding(1))
        self.assertEqual(-0x4000, parse_ssb_encoding(0x4000))
        self.assertEqual(-0x3FFF, parse_ssb_encoding(0x4001))
        self.assertEqual(0x3FFF, parse_ssb_encoding(0x3FFF))
        self.assertEqual(0x3FFE, parse_ssb_encoding(0x3FFE))
        self.assertEqual(-1, parse_ssb_encoding(0x7FFF))
        self.assertEqual(-2, parse_ssb_encoding(0x7FFE))

    def test_parse_ssb_encoding_fixed_points(self):
        self.assertEqual(SsbOpParamFixedPoint(0, "0"), parse_ssb_encoding(FP + 0))
        self.assertEqual(SsbOpParamFixedPoint(0, "0039"), parse_ssb_encoding(FP + 1))
        self.assertEqual(SsbOpParamFixedPoint(0, "0078"), parse_ssb_encoding(FP + 2))
        self.assertEqual(SsbOpParamFixedPoint(1, "0039"), parse_ssb_encoding(FP + 0x0101))
        self.assertEqual(
            SsbOpParamFixedPoint(-64, "0"),
            parse_ssb_encoding(FP + 0x4000),
        )
        self.assertEqual(SsbOpParamFixedPoint(-63, "9961"), parse_ssb_encoding(FP + 0x4001))
        self.assertEqual(SsbOpParamFixedPoint(63, "9961"), parse_ssb_encoding(FP + 0x3FFF))
        self.assertEqual(SsbOpParamFixedPoint(63, "9922"), parse_ssb_encoding(FP + 0x3FFE))
        self.assertEqual(
            SsbOpParamFixedPoint(SsbOpParamFixedPoint.NegativeZero, "0039"),
            parse_ssb_encoding(FP + 0x7FFF),
        )
        self.assertEqual(
            SsbOpParamFixedPoint(SsbOpParamFixedPoint.NegativeZero, "0078"),
            parse_ssb_encoding(FP + 0x7FFE),
        )
        self.assertEqual(
            SsbOpParamFixedPoint(-10, "0"),
            parse_ssb_encoding(FP + 0x7600),
        )

    def test_fixed_point_to_ssb_encoding(self):
        self.assertEqual(FP + 0, fixed_point_to_ssb_encoding(SsbOpParamFixedPoint(0, "0")))
        self.assertEqual(FP + 1, fixed_point_to_ssb_encoding(SsbOpParamFixedPoint(0, "0039")))
        self.assertEqual(FP + 2, fixed_point_to_ssb_encoding(SsbOpParamFixedPoint(0, "0078")))
        self.assertEqual(FP + 0x0101, fixed_point_to_ssb_encoding(SsbOpParamFixedPoint(1, "0039")))
        self.assertEqual(FP + 0x4000, fixed_point_to_ssb_encoding(SsbOpParamFixedPoint(-64, "0")))
        self.assertEqual(FP + 0x4001, fixed_point_to_ssb_encoding(SsbOpParamFixedPoint(-63, "9961")))
        self.assertEqual(FP + 0x3FFF, fixed_point_to_ssb_encoding(SsbOpParamFixedPoint(63, "9961")))
        self.assertEqual(FP + 0x3FFE, fixed_point_to_ssb_encoding(SsbOpParamFixedPoint(63, "9922")))
        self.assertEqual(
            FP + 0x7FFF,
            fixed_point_to_ssb_encoding(SsbOpParamFixedPoint(SsbOpParamFixedPoint.NegativeZero, "0039")),
        )
        self.assertEqual(
            FP + 0x7FFE,
            fixed_point_to_ssb_encoding(SsbOpParamFixedPoint(SsbOpParamFixedPoint.NegativeZero, "0078")),
        )
        self.assertEqual(
            FP + 0x7600,
            fixed_point_to_ssb_encoding(SsbOpParamFixedPoint(-10, "0")),
        )

    def test_fixed_point_to_ssb_encoding_out_of_bounds(self):
        self.assertRaises(
            SsbCompilerError,
            lambda: fixed_point_to_ssb_encoding(SsbOpParamFixedPoint(64, "0")),
        )
        self.assertRaises(
            SsbCompilerError,
            lambda: fixed_point_to_ssb_encoding(SsbOpParamFixedPoint(-64, "0039")),
        )
