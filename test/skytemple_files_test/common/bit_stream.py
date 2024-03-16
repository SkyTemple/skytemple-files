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

from skytemple_files.common.bit_stream import BitStream


class BitStreamTestCase(unittest.TestCase):
    # Note: A lot of tests rely on the BitStream being correctly convertible to a list[bool].
    #       This already asserts some of the tested list operations work correctly. Check
    #       those first on test failures.
    def test_empty(self):
        self.assertEqual([], list(BitStream([])))

    def test_init_bool_list(self):
        expected = [True, False, False, False, True]
        self.assertEqual(expected, list(BitStream(expected)))

    def test_init_int_list(self):
        input_list = [4, 22]
        # fmt: off
        expected = [
            # 128   64     32     16     8      4      2      1
            False, False, False, False, False, True, False, False,
            False, False, False, True, False, True, True, False,
        ]
        # fmt: on
        self.assertEqual(expected, list(BitStream(input_list)))

    def test_init_bytes(self):
        input_list = b"\x04\x1e"
        # fmt: off
        expected = [
            # 128   64     32     16     8      4      2      1
            False, False, False, False, False, True, False, False,
            False, False, False, True, True, True, True, False,
        ]
        # fmt: on
        self.assertEqual(expected, list(BitStream(input_list)))

    def test_init_bit_stream(self):
        expected = [True, False, False, False, True]
        before = BitStream(expected)
        after = BitStream(before)
        self.assertEqual(expected, list(after))

    def test_length(self):
        self.assertEqual(5, len(BitStream([True, False, False, False, True])))
        self.assertEqual(16, len(BitStream([4, 5])))
        self.assertEqual(0, len(BitStream([])))
        self.assertEqual(1, BitStream([True, False, False, False, True]).len_in_bytes())
        self.assertEqual(2, BitStream([4, 5]).len_in_bytes())
        self.assertEqual(0, BitStream([]).len_in_bytes())

    def test_iter(self):
        expected_first = [True, False, False, False, True]
        bs_first = BitStream(expected_first)
        bs_second = BitStream([])
        for expected, actual in zip(expected_first, bs_first, strict=True):
            self.assertEqual(expected, actual)
        self.assertRaises(StopIteration, lambda: next(iter(bs_second)))

    def test_to_bytes(self):
        self.assertEqual(bytes(b"\x04\x1e"), BitStream(b"\x04\x1e").to_bytes())
        self.assertEqual(
            bytes([136]), BitStream([True, False, False, False, True]).to_bytes()
        )

    def test_to_bytes_subview(self):
        # 00000100 00011110
        #  00001000 001/////
        self.assertEqual(bytes(b"\x08\x20"), BitStream(b"\x04\x1e")[1:12].to_bytes())

    def test_to_number(self):
        self.assertEqual(17, BitStream([True, False, False, False, True]).to_number())
        self.assertEqual(0x041E, BitStream(b"\x04\x1e").to_number())
        self.assertEqual(0x041E, BitStream(b"\x04\x1e").to_number("big"))
        self.assertEqual(0x1E04, BitStream(b"\x04\x1e").to_number("little"))
        self.assertEqual(0x041E, BitStream(b"\x04\x1e").to_number("big", signed=True))
        self.assertEqual(0x041E, BitStream(b"\x04\x1e").to_number("big", False))
        self.assertEqual(-3042, BitStream(b"\xf4\x1e").to_number("big", signed=True))
        self.assertEqual(0xF41E, BitStream(b"\xf4\x1e").to_number("big", False))
        # fmt: off
        twelve = [
            # byte 1:
            True, False, False, False, True, False, False, False,  # 0x88
            # byte 2:
            # False, False, False, False, False, False, False,     # 0x00
            False
        ]
        # fmt: on
        self.assertEqual(
            0x8800,
            BitStream(twelve).to_number("big"),
        )
        self.assertEqual(
            0x0088,
            BitStream(twelve).to_number("little"),
        )

    def test_from_number(self):
        self.assertEqual([], list(BitStream.from_number(0)))
        self.assertEqual([True], list(BitStream.from_number(1)))
        self.assertEqual([False, False, True], list(BitStream.from_number(1, 3)))
        self.assertEqual([True, False, False, False], list(BitStream.from_number(8)))
        self.assertEqual([True, False, False, False], list(BitStream.from_number(8, 4)))
        self.assertEqual(
            [False, True, False, False, False], list(BitStream.from_number(8, 5))
        )
        self.assertEqual([True] + [False] * 8, list(BitStream.from_number(256)))
        self.assertEqual([True] + [False] * 8, list(BitStream.from_number(256, 9)))
        self.assertEqual(
            [False, True] + [False] * 8, list(BitStream.from_number(256, 10))
        )
        self.assertRaises(OverflowError, lambda: BitStream.from_number(8, 3))

    def test_append(self):
        before = [True, False, False, False, True]
        after = [True, False, False, False, True, False]
        test = BitStream(before)
        test.append(False)
        self.assertEqual(after, list(test))
        self.assertEqual(6, len(test))
        self.assertEqual(1, test.len_in_bytes())
        test.append(False)
        test.append(False)
        self.assertEqual(1, test.len_in_bytes())
        test.append(False)
        self.assertEqual(2, test.len_in_bytes())

    def test_extend(self):
        # fmt: off
        before = [True, False, False, False, True]
        after1 = [True, False, False, False, True, False, True]
        after2 = [True, False, False, False, True, False, True, False, False, False, False, False, False, True, False]
        after3 = [True, False, False, False, True, False, True, False, False, False, False, False, False, True, False, False, True]
        # fmt: on
        test = BitStream(before)
        test.extend([False, True])
        self.assertEqual(after1, list(test))
        self.assertEqual(7, len(test))
        self.assertEqual(1, test.len_in_bytes())
        test.extend([2])
        self.assertEqual(after2, list(test))
        self.assertEqual(2, test.len_in_bytes())
        test.extend(BitStream([False, True]))
        self.assertEqual(after3, list(test))
        self.assertEqual(3, test.len_in_bytes())

    def test_iadd(self):
        # fmt: off
        before = [True, False, False, False, True]
        after1 = [True, False, False, False, True, False, True]
        after2 = [True, False, False, False, True, False, True, False, False, False, False, False, False, True, False]
        after3 = [True, False, False, False, True, False, True, False, False, False, False, False, False, True, False, False, True]
        # fmt: on
        test = BitStream(before)
        test += [False, True]
        self.assertEqual(after1, list(test))
        self.assertEqual(7, len(test))
        self.assertEqual(1, test.len_in_bytes())
        test += [2]
        self.assertEqual(after2, list(test))
        self.assertEqual(2, test.len_in_bytes())
        test += BitStream([False, True])
        self.assertEqual(after3, list(test))
        self.assertEqual(3, test.len_in_bytes())

    def test_add(self):
        # fmt: off
        before = [True, False, False, False, True]
        after1 = [True, False, False, False, True, False, True]
        after2 = [True, False, False, False, True, False, True, False, False, False, False, False, False, True, False]
        after3 = [True, False, False, False, True, False, True, False, False, False, False, False, False, True, False, False, True]
        # fmt: on
        test_a = BitStream(before)
        test = test_a + [False, True]
        self.assertEqual(after1, list(test))
        self.assertEqual(7, len(test))
        self.assertEqual(1, test.len_in_bytes())
        test = test + [2]
        self.assertEqual(after2, list(test))
        self.assertEqual(2, test.len_in_bytes())
        test = test + BitStream([False, True])
        self.assertEqual(after3, list(test))
        self.assertEqual(3, test.len_in_bytes())

    def test_append_subview(self):
        sub_view = [False, False, True]
        sub_view_start = 2
        sub_view_len = len(sub_view)
        full_view = [True, False, *sub_view, False, False]

        full = BitStream(full_view)
        sub = full[sub_view_start : sub_view_start + sub_view_len]

        self.assertRaises(ValueError, lambda: sub.append(True))

    def test_getitem_single(self):
        test = BitStream([True, False, True])
        self.assertEqual(True, test[0])
        self.assertEqual(False, test[1])
        self.assertEqual(True, test[2])
        self.assertEqual(True, test[-1])
        self.assertEqual(False, test[-2])
        self.assertRaises(IndexError, lambda: test[3])

    def test_getitem_slice(self):
        sub_view = [False, False, True]
        sub_view_start = 2
        sub_view_len = len(sub_view)
        full_view = [True, False, *sub_view, False, False]

        full = BitStream(full_view)
        sub = full[sub_view_start : sub_view_start + sub_view_len]

        self.assertIsInstance(sub, BitStream)
        self.assertEqual(sub_view, list(sub))

    def test_getitem_slice_oob(self):
        sub_view = [False, False, True]
        sub_view_start = 2
        sub_view_len = len(sub_view)
        full_view = [True, False, *sub_view]

        full = BitStream(full_view)
        sub = full[sub_view_start : sub_view_start + sub_view_len + 10]

        self.assertEqual(sub_view, list(sub))
        self.assertEqual(sub_view_len, len(sub))

    def test_getitem_slice_subview_oob(self):
        sub_view = [False, False, True]
        sub_view_start = 2
        sub_view_len = len(sub_view)
        full_view = [True, False, *sub_view, False, False]

        full = BitStream(full_view)
        sub = full[sub_view_start : sub_view_start + sub_view_len]
        # This must now not read oob into the full view. So the length must be `sub_view_len`.
        sub2 = sub[0 : sub_view_len + 1]

        self.assertEqual(sub_view, list(sub2))
        self.assertEqual(sub_view_len, len(sub2))

    def test_subview_manipulation(self):
        sub_view = [False, False, True]
        sub_view_start = 2
        sub_view_len = len(sub_view)
        full_view = [True, False, *sub_view, False, False]

        full = BitStream(full_view)
        sub = full[sub_view_start : sub_view_start + sub_view_len]

        sub[0] = True
        self.assertEqual([True, False, True], list(sub))
        self.assertEqual([True, False, True, False, True, False, False], list(full))

    def test_len_subview(self):
        sub_view = [False, False, True]
        sub_view_start = 2
        sub_view_len = len(sub_view)
        full_view = [True, False, *sub_view, False, False]

        full = BitStream(full_view)
        sub = full[sub_view_start : sub_view_start + sub_view_len]

        self.assertEqual(sub_view_len, len(sub))

    def test_iter_subview(self):
        sub_view = [False, False, True]
        sub_view_start = 2
        sub_view_len = len(sub_view)
        full_view = [True, False, *sub_view, False, False]

        full = BitStream(full_view)
        sub = full[sub_view_start : sub_view_start + sub_view_len]

        for expected, actual in zip(sub_view, sub, strict=True):
            self.assertEqual(expected, actual)

    def test_nested_subview(self):
        sub_sub_view = [False, False, False, True]
        sub_sub_view_start = 1
        sub_sub_view_len = len(sub_sub_view)
        sub_view = [False, *sub_sub_view, True]
        sub_view_start = 2
        sub_view_len = len(sub_view)
        full_view = [True, False, *sub_view, False, False]

        full = BitStream(full_view)
        sub = full[sub_view_start : sub_view_start + sub_view_len]
        sub_sub = sub[sub_sub_view_start : sub_sub_view_start + sub_sub_view_len]

        self.assertEqual(sub_sub_view, list(sub_sub))
        sub_sub[0] = True
        # fmt: off
        self.assertEqual([True, False, False, True], list(sub_sub))
        self.assertEqual([False, True, False, False, True, True], list(sub))
        self.assertEqual([True, False, False, True, False, False, True, True, False, False], list(full))
        # fmt: on

    def test_setitem_single(self):
        before = [True, False, True]
        after = [True, True, False]
        view = BitStream(before)
        view[1] = True
        view[2] = False
        self.assertEqual(after, list(view))

    def test_setitem_slice_empty(self):
        before = [True, False, True]
        view = BitStream(before)
        view[2:2] = []
        self.assertEqual(before, list(view))

    def test_setitem_slice_bool_list(self):
        before = [True, False, True]
        after = [True, True, False]
        view = BitStream(before)
        view[1:3] = [True, False]
        self.assertEqual(after, list(view))

    def test_setitem_single_int(self):
        # fmt: off
        before = [
            True, False, True, True, False, True, True, True,
            False, False, False, True, False, False, False, False
        ]
        after1 = [
            True, False, True, True, False, True, True, True,
            False, False, False, False, True, True, False, False
        ]
        after2 = [
            True, False, True, True, False, True, True, True,
            True, True, False, False, True, True, False, False
        ]
        # fmt: on
        view = BitStream(before)
        view[8:16] = 12
        self.assertEqual(after1, list(view))
        # Since 12 is small, it can also fit into less space
        view[8:12] = 12
        self.assertEqual(after2, list(view))

        # But 12 is not small enough for 3 bits
        def do():
            view[13:16] = 12

        self.assertRaises(ValueError, do)

    def test_setitem_slice_int_list(self):
        # fmt: off
        before = [
            True, False, True, True, False, True, True, True,
            False, False, False, True, False, False, False, False
        ]
        after = [
            True, False, True, True, False, True, True, True,
            True, True, True, True, True, True, True, False
        ]
        # fmt: on
        view = BitStream(before)
        view[8:16] = [254]
        self.assertEqual(after, list(view))

    def test_setitem_slice_bytes(self):
        # fmt: off
        before = [
            True, False, True, True, False, True, True, True,
            False, False, False, True, False, False, False, False
        ]
        after = [
            True, False, True, True, False, True, True, True,
            True, True, True, True, True, True, True, False
        ]
        # fmt: on
        view = BitStream(before)
        view[8:16] = bytes([0xFE])
        self.assertEqual(after, list(view))

    def test_setitem_slice_bit_stream(self):
        # fmt: off
        before = [
            True, False, True, True, False, True, True, True,
            False, False, False, True, False, False, False, False
        ]
        after = [
            True, False, True, True, False, True, True, True,
            True, True, True, True, True, True, True, False
        ]
        # fmt: on
        view = BitStream(before)
        view[8:16] = BitStream([0xFE])
        self.assertEqual(after, list(view))

    def test_setitem_slice_subview_oob(self):
        sub_view = [False, False, True]
        sub_view_start = 2
        sub_view_len = len(sub_view)
        full_view = [True, False, *sub_view, False, False]

        full = BitStream(full_view)
        sub = full[sub_view_start : sub_view_start + sub_view_len]

        def manip():
            sub[0 : sub_view_len + 1] = sub_view + [True]

        # This must now raise an index error, since it would attempt to write out of bounds.
        self.assertRaises(IndexError, manip)

    def test_eq_and_identity(self):
        # Tests that equality checks between BitStream instances work correctly and the identity
        # of underlying buffers as preserved.
        # Not tested are interactions with sub-view, see `test_eq_and_identity_subview`.
        # This also needs __setitem__ for single indices to work properly.
        expected = [True, False, False, False, True]
        expected_before = [False, False, False, False, True]
        before = BitStream(expected)
        after = BitStream(before)
        before[0] = False
        self.assertEqual(expected, [True, False, False, False, True])
        self.assertEqual(expected_before, [False, False, False, False, True])
        self.assertEqual(expected, list(after))
        self.assertEqual(expected_before, list(before))
        self.assertEqual(after, after)
        self.assertEqual(after, BitStream(after))
        self.assertEqual(after, BitStream([True, False, False, False, True]))
        self.assertNotEqual(after, before)
        self.assertNotEqual(after, BitStream(before))
        self.assertNotEqual(after, BitStream([False, False, False, False, True]))

    def test_eq_and_identity_subview(self):
        # Tests the identity and equality constraints of sub-views.
        sub_view = [False, False, True]
        sub_view_start = 2
        sub_view_len = len(sub_view)
        full_view = [True, False, *sub_view, False, False]

        full = BitStream(full_view)
        sub = full[sub_view_start : sub_view_start + sub_view_len]

        self.assertEqual(full_view, list(full))
        self.assertNotEqual(full, sub)
        self.assertEqual(sub, BitStream(sub_view))
