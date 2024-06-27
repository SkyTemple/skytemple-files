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

from range_typed_integers import i32, i16, i8, u32, u16, u8

from skytemple_files.common.rw_value import RWValue, RWInt32Value, RWCharArrayValue, RWUInt32Value, RWInt16Value, \
    RWInt8Value, RWUInt8Value, RWUInt16Value, RWFx6416Value, RWFx3216Value, RWFx328Value, RWShiftedImmediateValue  # fmt: skip
from skytemple_files.hardcoded.symbols.unsupported_type_error import UnsupportedTypeError


class RWValueTestCase(unittest.TestCase):
    binary_to_read: bytes
    binary_to_write: bytearray

    def setUp(self) -> None:
        with open("skytemple_files_test/common/fixtures/sample_binary.bin", "rb") as f:
            self.binary_to_read = f.read()
        self.binary_to_write = bytearray(self.binary_to_read)

    def test_from_c_type_1(self):
        self.assertIsInstance(RWValue.from_c_type("int", 0), RWInt32Value)

    def test_from_c_type_2(self):
        rw = RWValue.from_c_type("char[16]", 0x10)
        self.assertIsInstance(rw, RWCharArrayValue)
        self.assertEqual(16, rw.size)

    def test_from_c_type_3(self):
        with self.assertRaises(UnsupportedTypeError):
            RWValue.from_c_type("int64", 0)

    def test_from_c_type_4(self):
        with self.assertRaises(UnsupportedTypeError):
            RWValue.from_c_type("char[3][3]", 0)

    def test_read_int_1(self):
        rw = RWInt32Value(0x0)
        self.assertEqual(0, rw.read(self.binary_to_read))
        self.assertEqual("0", rw.read_str(self.binary_to_read))

    def test_read_int_2(self):
        rw = RWInt32Value(0x4)
        self.assertEqual(1, rw.read(self.binary_to_read))
        self.assertEqual("1", rw.read_str(self.binary_to_read))

    def test_read_int_3(self):
        rw = RWInt32Value(0x20)
        self.assertEqual(-1, rw.read(self.binary_to_read))
        self.assertEqual("-1", rw.read_str(self.binary_to_read))

    def test_read_uint_1(self):
        rw = RWUInt32Value(0x0)
        self.assertEqual(0, rw.read(self.binary_to_read))
        self.assertEqual("0", rw.read_str(self.binary_to_read))

    def test_read_uint_2(self):
        rw = RWUInt32Value(0x4)
        self.assertEqual(1, rw.read(self.binary_to_read))
        self.assertEqual("1", rw.read_str(self.binary_to_read))

    def test_read_uint_3(self):
        rw = RWUInt32Value(0x20)
        self.assertEqual(0xFFFFFFFF, rw.read(self.binary_to_read))
        self.assertEqual("4294967295", rw.read_str(self.binary_to_read))

    def test_read_int_16_1(self):
        rw = RWInt16Value(0x0)
        self.assertEqual(0, rw.read(self.binary_to_read))
        self.assertEqual("0", rw.read_str(self.binary_to_read))

    def test_read_int_16_2(self):
        rw = RWInt16Value(0xA)
        self.assertEqual(3, rw.read(self.binary_to_read))
        self.assertEqual("3", rw.read_str(self.binary_to_read))

    def test_read_int_16_3(self):
        rw = RWInt16Value(0x24)
        self.assertEqual(-2, rw.read(self.binary_to_read))
        self.assertEqual("-2", rw.read_str(self.binary_to_read))

    def test_read_uint_16_1(self):
        rw = RWUInt16Value(0x0)
        self.assertEqual(0, rw.read(self.binary_to_read))
        self.assertEqual("0", rw.read_str(self.binary_to_read))

    def test_read_uint_16_2(self):
        rw = RWUInt16Value(0xA)
        self.assertEqual(3, rw.read(self.binary_to_read))
        self.assertEqual("3", rw.read_str(self.binary_to_read))

    def test_read_uint_16_3(self):
        rw = RWUInt16Value(0x24)
        self.assertEqual(0xFFFE, rw.read(self.binary_to_read))
        self.assertEqual("65534", rw.read_str(self.binary_to_read))

    def test_read_int_8_1(self):
        rw = RWInt8Value(0x0)
        self.assertEqual(0, rw.read(self.binary_to_read))
        self.assertEqual("0", rw.read_str(self.binary_to_read))

    def test_read_int_8_2(self):
        rw = RWInt8Value(0xA)
        self.assertEqual(3, rw.read(self.binary_to_read))
        self.assertEqual("3", rw.read_str(self.binary_to_read))

    def test_read_int_8_3(self):
        rw = RWInt8Value(0x24)
        self.assertEqual(-2, rw.read(self.binary_to_read))
        self.assertEqual("-2", rw.read_str(self.binary_to_read))

    def test_read_uint_8_1(self):
        rw = RWUInt8Value(0x0)
        self.assertEqual(0, rw.read(self.binary_to_read))
        self.assertEqual("0", rw.read_str(self.binary_to_read))

    def test_read_uint_8_2(self):
        rw = RWUInt8Value(0xA)
        self.assertEqual(3, rw.read(self.binary_to_read))
        self.assertEqual("3", rw.read_str(self.binary_to_read))

    def test_read_uint_8_3(self):
        rw = RWUInt8Value(0x24)
        self.assertEqual(0xFE, rw.read(self.binary_to_read))
        self.assertEqual("254", rw.read_str(self.binary_to_read))

    def test_read_fx_64_16_1(self):
        rw = RWFx6416Value(0x28)
        self.assertEqual(0.0, rw.read(self.binary_to_read))
        self.assertEqual("0.0", rw.read_str(self.binary_to_read))

    def test_read_fx_64_16_2(self):
        rw = RWFx6416Value(0x60)
        self.assertEqual(1.0, rw.read(self.binary_to_read))
        self.assertEqual("1.0", rw.read_str(self.binary_to_read))

    def test_read_fx_64_16_3(self):
        rw = RWFx6416Value(0x30)
        self.assertAlmostEqual(1.1, rw.read(self.binary_to_read), 4)
        self.assertTrue(
            rw.read_str(self.binary_to_read).startswith("1.1") or rw.read_str(self.binary_to_read).startswith("1.09")
        )

    def test_read_fx_32_16_1(self):
        rw = RWFx3216Value(0x28)
        self.assertEqual(0.0, rw.read(self.binary_to_read))
        self.assertEqual("0.0", rw.read_str(self.binary_to_read))

    def test_read_fx_32_16_2(self):
        rw = RWFx3216Value(0x2)
        self.assertEqual(1.0, rw.read(self.binary_to_read))
        self.assertEqual("1.0", rw.read_str(self.binary_to_read))

    def test_read_fx_32_16_3(self):
        rw = RWFx3216Value(0x34)
        self.assertAlmostEqual(1.1, rw.read(self.binary_to_read), 4)
        self.assertTrue(
            rw.read_str(self.binary_to_read).startswith("1.1") or rw.read_str(self.binary_to_read).startswith("1.09")
        )

    def test_read_fx_32_8_1(self):
        rw = RWFx328Value(0x28)
        self.assertEqual(0.0, rw.read(self.binary_to_read))
        self.assertEqual("0.0", rw.read_str(self.binary_to_read))

    def test_read_fx_32_8_2(self):
        rw = RWFx328Value(0x3)
        self.assertEqual(1.0, rw.read(self.binary_to_read))
        self.assertEqual("1.0", rw.read_str(self.binary_to_read))

    def test_read_fx_32_8_3(self):
        rw = RWFx328Value(0x2)
        self.assertEqual(256.0, rw.read(self.binary_to_read))
        self.assertEqual("256.0", rw.read_str(self.binary_to_read))

    def test_read_fx_32_8_4(self):
        rw = RWFx328Value(0x38)
        self.assertEqual(1.75, rw.read(self.binary_to_read))

    def test_read_fx_32_8_5(self):
        rw = RWFx328Value(0x3C)
        self.assertAlmostEqual(1.4, rw.read(self.binary_to_read), 2)
        self.assertTrue(
            rw.read_str(self.binary_to_read).startswith("1.4") or rw.read_str(self.binary_to_read).startswith("1.39")
        )

    def test_read_sh_imm_1(self):
        rw = RWShiftedImmediateValue(0x40)
        self.assertEqual(1, rw.read(self.binary_to_read))

    def test_read_sh_imm_2(self):
        rw = RWShiftedImmediateValue(0x44)
        self.assertEqual(0xFF, rw.read(self.binary_to_read))

    def test_read_sh_imm_3(self):
        rw = RWShiftedImmediateValue(0x48)
        self.assertEqual(0x100, rw.read(self.binary_to_read))

    def test_read_sh_imm_4(self):
        rw = RWShiftedImmediateValue(0x4C)
        self.assertEqual(0x400, rw.read(self.binary_to_read))

    def test_read_sh_imm_5(self):
        rw = RWShiftedImmediateValue(0x50)
        self.assertEqual(0x128, rw.read(self.binary_to_read))

    def test_read_sh_imm_6(self):
        rw = RWShiftedImmediateValue(0x54)
        self.assertEqual(0x10000000, rw.read(self.binary_to_read))

    def test_read_sh_imm_7(self):
        rw = RWShiftedImmediateValue(0x58)
        self.assertEqual(0x30000000, rw.read(self.binary_to_read))

    def test_read_sh_imm_8(self):
        rw = RWShiftedImmediateValue(0x5C)
        self.assertEqual(0, rw.read(self.binary_to_read))

    def test_read_char_array_1(self):
        rw = RWCharArrayValue(0x0, 1)
        self.assertEqual("", rw.read(self.binary_to_read))

    def test_read_char_array_2(self):
        rw = RWCharArrayValue(0x0, 4)
        self.assertEqual("", rw.read(self.binary_to_read))

    def test_read_char_array_3(self):
        rw = RWCharArrayValue(0x10, 16)
        self.assertEqual("sample string", rw.read(self.binary_to_read))

    def test_read_char_array_4(self):
        rw = RWCharArrayValue(0x10, 13)
        self.assertEqual("sample string", rw.read(self.binary_to_read))

    def test_read_char_array_5(self):
        rw = RWCharArrayValue(0x10, 8)
        self.assertEqual("sample s", rw.read(self.binary_to_read))

    def test_read_char_array_6(self):
        rw = RWCharArrayValue(0x10, 7)
        self.assertEqual("sample ", rw.read(self.binary_to_read))

    def test_read_char_array_7(self):
        rw = RWCharArrayValue(0x10, 32)
        self.assertEqual("sample string", rw.read(self.binary_to_read))

    # Write tests
    # They assume that read tests are correct, since they use the read functions to check if the value was correctly
    # written.

    def test_write_int_1(self):
        rw = RWInt32Value(0x68)
        rw.write(self.binary_to_write, i32(0))
        self.assertEqual(0, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "0")
        self.assertEqual(0, rw.read(bytes(self.binary_to_write)))

    def test_write_int_2(self):
        rw = RWInt32Value(0x68)
        rw.write(self.binary_to_write, i32(123))
        self.assertEqual(123, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "124")
        self.assertEqual(124, rw.read(bytes(self.binary_to_write)))

    def test_write_int_3(self):
        rw = RWInt32Value(0x68)
        rw.write(self.binary_to_write, i32(-12))
        self.assertEqual(-12, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "-13")
        self.assertEqual(-13, rw.read(bytes(self.binary_to_write)))

    def test_write_uint_1(self):
        rw = RWUInt32Value(0x68)
        rw.write(self.binary_to_write, u32(0))
        self.assertEqual(0, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "0")
        self.assertEqual(0, rw.read(bytes(self.binary_to_write)))

    def test_write_uint_2(self):
        rw = RWUInt32Value(0x68)
        rw.write(self.binary_to_write, u32(123))
        self.assertEqual(123, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "124")
        self.assertEqual(124, rw.read(bytes(self.binary_to_write)))

    def test_write_uint_3(self):
        rw = RWUInt32Value(0x68)
        rw.write(self.binary_to_write, u32(0xFFFFFFFF))
        self.assertEqual(0xFFFFFFFF, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "4294967294")
        self.assertEqual(0xFFFFFFFE, rw.read(bytes(self.binary_to_write)))

    def test_write_int16_1(self):
        rw = RWInt16Value(0x68)
        rw.write(self.binary_to_write, i16(0))
        self.assertEqual(0, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "0")
        self.assertEqual(0, rw.read(bytes(self.binary_to_write)))

    def test_write_int16_2(self):
        rw = RWInt16Value(0x68)
        rw.write(self.binary_to_write, i16(123))
        self.assertEqual(123, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "124")
        self.assertEqual(124, rw.read(bytes(self.binary_to_write)))

    def test_write_int16_3(self):
        rw = RWInt16Value(0x68)
        rw.write(self.binary_to_write, i16(-12))
        self.assertEqual(-12, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "-13")
        self.assertEqual(-13, rw.read(bytes(self.binary_to_write)))

    def test_write_uint16_1(self):
        rw = RWUInt16Value(0x68)
        rw.write(self.binary_to_write, u16(0))
        self.assertEqual(0, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "0")
        self.assertEqual(0, rw.read(bytes(self.binary_to_write)))

    def test_write_uint16_2(self):
        rw = RWUInt16Value(0x68)
        rw.write(self.binary_to_write, u16(123))
        self.assertEqual(123, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "124")
        self.assertEqual(124, rw.read(bytes(self.binary_to_write)))

    def test_write_uint16_3(self):
        rw = RWUInt16Value(0x68)
        rw.write(self.binary_to_write, u16(0xFFFF))
        self.assertEqual(0xFFFF, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "65534")
        self.assertEqual(0xFFFE, rw.read(bytes(self.binary_to_write)))

    def test_write_int8_1(self):
        rw = RWInt8Value(0x68)
        rw.write(self.binary_to_write, i8(0))
        self.assertEqual(0, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "0")
        self.assertEqual(0, rw.read(bytes(self.binary_to_write)))

    def test_write_int8_2(self):
        rw = RWInt8Value(0x68)
        rw.write(self.binary_to_write, i8(123))
        self.assertEqual(123, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "124")
        self.assertEqual(124, rw.read(bytes(self.binary_to_write)))

    def test_write_int8_3(self):
        rw = RWInt8Value(0x68)
        rw.write(self.binary_to_write, i8(-12))
        self.assertEqual(-12, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "-13")
        self.assertEqual(-13, rw.read(bytes(self.binary_to_write)))

    def test_write_uint8_1(self):
        rw = RWUInt8Value(0x68)
        rw.write(self.binary_to_write, u8(0))
        self.assertEqual(0, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "0")
        self.assertEqual(0, rw.read(bytes(self.binary_to_write)))

    def test_write_uint8_2(self):
        rw = RWUInt8Value(0x68)
        rw.write(self.binary_to_write, u8(123))
        self.assertEqual(123, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "124")
        self.assertEqual(124, rw.read(bytes(self.binary_to_write)))

    def test_write_uint8_3(self):
        rw = RWUInt8Value(0x68)
        rw.write(self.binary_to_write, u8(0xFF))
        self.assertEqual(0xFF, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "254")
        self.assertEqual(0xFE, rw.read(bytes(self.binary_to_write)))

    def test_write_fx64_16_1(self):
        rw = RWFx6416Value(0x68)
        rw.write(self.binary_to_write, 0.0)
        self.assertEqual(0.0, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "0.0")
        self.assertEqual(0.0, rw.read(bytes(self.binary_to_write)))

    def test_write_fx64_16_2(self):
        rw = RWFx6416Value(0x68)
        rw.write(self.binary_to_write, 1.0)
        self.assertEqual(1.0, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "1.0")
        self.assertEqual(1.0, rw.read(bytes(self.binary_to_write)))

    def test_write_fx64_16_3(self):
        rw = RWFx6416Value(0x68)
        rw.write(self.binary_to_write, 1.1)
        self.assertAlmostEqual(1.1, rw.read(bytes(self.binary_to_write)), 4)
        rw.write_str(self.binary_to_write, "1.2")
        self.assertAlmostEqual(1.2, rw.read(bytes(self.binary_to_write)), 4)

    def test_write_fx32_16_1(self):
        rw = RWFx3216Value(0x68)
        rw.write(self.binary_to_write, 0.0)
        self.assertEqual(0.0, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "0.0")
        self.assertEqual(0.0, rw.read(bytes(self.binary_to_write)))

    def test_write_fx32_16_2(self):
        rw = RWFx3216Value(0x68)
        rw.write(self.binary_to_write, 1.0)
        self.assertEqual(1.0, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "1.0")
        self.assertEqual(1.0, rw.read(bytes(self.binary_to_write)))

    def test_write_fx32_16_3(self):
        rw = RWFx3216Value(0x68)
        rw.write(self.binary_to_write, 1.1)
        self.assertAlmostEqual(1.1, rw.read(bytes(self.binary_to_write)), 4)
        rw.write_str(self.binary_to_write, "1.2")
        self.assertAlmostEqual(1.2, rw.read(bytes(self.binary_to_write)), 4)

    def test_write_fx32_8_1(self):
        rw = RWFx328Value(0x68)
        rw.write(self.binary_to_write, 0.0)
        self.assertEqual(0.0, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "0.0")
        self.assertEqual(0.0, rw.read(bytes(self.binary_to_write)))

    def test_write_fx32_8_2(self):
        rw = RWFx328Value(0x68)
        rw.write(self.binary_to_write, 1.0)
        self.assertEqual(1.0, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "1.0")
        self.assertEqual(1.0, rw.read(bytes(self.binary_to_write)))

    def test_write_fx32_8_3(self):
        rw = RWFx328Value(0x68)
        rw.write(self.binary_to_write, 256.0)
        self.assertEqual(256.0, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "257.0")
        self.assertEqual(257.0, rw.read(bytes(self.binary_to_write)))

    def test_write_fx32_8_4(self):
        rw = RWFx328Value(0x68)
        rw.write(self.binary_to_write, 1.75)
        self.assertEqual(1.75, rw.read(bytes(self.binary_to_write)))
        rw.write_str(self.binary_to_write, "1.5")
        self.assertEqual(1.5, rw.read(bytes(self.binary_to_write)))

    def test_write_fx32_8_5(self):
        rw = RWFx328Value(0x68)
        rw.write(self.binary_to_write, 1.4)
        self.assertAlmostEqual(1.4, rw.read(bytes(self.binary_to_write)), 2)
        rw.write_str(self.binary_to_write, "1.6")
        self.assertAlmostEqual(1.6, rw.read(bytes(self.binary_to_write)), 2)

    def test_write_sh_imm_1(self):
        rw = RWShiftedImmediateValue(0x68)
        rw.write(self.binary_to_write, 1)
        self.assertEqual(1, rw.read(bytes(self.binary_to_write)))

    def test_write_sh_imm_2(self):
        rw = RWShiftedImmediateValue(0x68)
        rw.write(self.binary_to_write, 0xFF)
        self.assertEqual(0xFF, rw.read(bytes(self.binary_to_write)))

    def test_write_sh_imm_3(self):
        rw = RWShiftedImmediateValue(0x68)
        rw.write(self.binary_to_write, 0x100)
        self.assertEqual(0x100, rw.read(bytes(self.binary_to_write)))

    def test_write_sh_imm_4(self):
        rw = RWShiftedImmediateValue(0x68)
        rw.write(self.binary_to_write, 0x400)
        self.assertEqual(0x400, rw.read(bytes(self.binary_to_write)))

    def test_write_sh_imm_5(self):
        rw = RWShiftedImmediateValue(0x68)
        rw.write(self.binary_to_write, 0x128)
        self.assertEqual(0x128, rw.read(bytes(self.binary_to_write)))

    def test_write_sh_imm_6(self):
        rw = RWShiftedImmediateValue(0x68)
        rw.write(self.binary_to_write, 0x10000000)
        self.assertEqual(0x10000000, rw.read(bytes(self.binary_to_write)))

    def test_write_sh_imm_7(self):
        rw = RWShiftedImmediateValue(0x68)
        rw.write(self.binary_to_write, 0x30000000)
        self.assertEqual(0x30000000, rw.read(bytes(self.binary_to_write)))

    def test_write_sh_imm_8(self):
        rw = RWShiftedImmediateValue(0x68)
        rw.write(self.binary_to_write, 0)
        self.assertEqual(0, rw.read(bytes(self.binary_to_write)))

    def test_write_sh_imm_9(self):
        rw = RWShiftedImmediateValue(0x68)
        with self.assertRaises(ValueError):
            rw.write(self.binary_to_write, 0x101)

    def test_write_sh_imm_10(self):
        rw = RWShiftedImmediateValue(0x68)
        with self.assertRaises(ValueError):
            rw.write(self.binary_to_write, 0x25A)

    def test_write_sh_imm_11(self):
        rw = RWShiftedImmediateValue(0x68)
        with self.assertRaises(ValueError):
            rw.write(self.binary_to_write, 0x100000000)

    def test_write_char_array_1(self):
        rw = RWCharArrayValue(0x10, 16)
        rw.write(self.binary_to_write, "")
        self.assertEqual("", rw.read(bytes(self.binary_to_write)))

    def test_write_char_array_2(self):
        rw = RWCharArrayValue(0x10, 16)
        rw.write(self.binary_to_write, "another thing")
        self.assertEqual("another thing", rw.read(bytes(self.binary_to_write)))

    def test_write_char_array_3(self):
        rw = RWCharArrayValue(0x10, 16)
        rw.write(self.binary_to_write, "exactly 16 char")
        self.assertEqual("exactly 16 char", rw.read(bytes(self.binary_to_write)))

    def test_write_char_array_4(self):
        rw = RWCharArrayValue(0x10, 16)
        with self.assertRaises(ValueError):
            rw.write(self.binary_to_write, "way too many characters")
