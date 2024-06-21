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
# mypy: ignore-errors
from __future__ import annotations

import typing
from typing import Dict, List

from skytemple_files.common.util import read_i32
from skytemple_files.graphics.kao.handler import KaoHandler
from skytemple_files.graphics.kao.protocol import KaoImageProtocol, KaoProtocol
from skytemple_files_test.case import SkyTempleFilesTestCase, fixpath, romtest

FIX_IN_TEST_MAP: Dict[int, List[int]] = {
    0: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 32, 34],
    552: [0, 2, 4, 6, 8, 10],
    1153: [],
}
FIX_IN_LEN = 1154
FIX_IN_LEN_SUB = 40
FIX_COMPLEX_IDS = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 32, 34]


class KaoTestCase(SkyTempleFilesTestCase[KaoHandler, KaoProtocol[KaoImageProtocol]]):
    handler = KaoHandler

    def setUp(self) -> None:
        self.kao = self._load_main_fixture(self._fix_path_kao())
        self.assertIsNotNone(self.kao)

    def test_get(self) -> None:
        for idx, sidxs in FIX_IN_TEST_MAP.items():
            for sidx in sidxs:
                kaoimg = self.kao.get(idx, sidx)
                self.assertGreater(kaoimg.size(), 0)
                # Kaos are not guaranteed to use the same exact palette after storing.
                self.assertImagesEqual(self._fix_path_png(idx, sidx), kaoimg.get())
                self.assertImagesEqual(self._fix_path_png(idx, sidx, rgb=True), kaoimg.get())

    def test_get_missing(self) -> None:
        self.assertIsNone(self.kao.get(552, 1))
        with self.assertRaises(ValueError):
            self.kao.get(0, FIX_IN_LEN_SUB)
        with self.assertRaises(ValueError):
            self.kao.get(FIX_IN_LEN, 0)

    def test_get_complex(self) -> None:
        self.kao = self._load_main_fixture(self._fix_path_complex())
        for i in FIX_COMPLEX_IDS:
            self.assertImagesEqual(self._fix_path_complex_png(i), self.kao.get(0, i).get())

    def test_set_complex(self) -> None:
        self.kao = self._load_main_fixture(self._fix_path_complex())
        for i in FIX_COMPLEX_IDS:
            self.kao.set_from_img(0, i, self._load_image(self._fix_path_complex_png(i)))
        new_kao = self._save_and_reload_main_fixture(self.kao)
        for i in FIX_COMPLEX_IDS:
            self.assertImagesEqual(self._fix_path_complex_png(i), new_kao.get(0, i).get())

    def test_set_from_img(self) -> None:
        img = self._load_image(self._fix_path_png(0, 1))
        self.kao.set_from_img(552, 8, img)
        self.kao.set_from_img(1153, 4, img)
        self.kao.get(0, 6).set(img)
        self.kao.set(100, 8, self.kao.get(552, 8))
        new_kao = self._save_and_reload_main_fixture(self.kao)
        self.assertImagesNotEqual(img, new_kao.get(0, 2).get())
        self.assertImagesEqual(img, new_kao.get(552, 8).get())
        self.assertImagesNotEqual(img, new_kao.get(552, 4).get())
        self.assertImagesEqual(img, new_kao.get(1153, 4).get())
        self.assertImagesEqual(img, new_kao.get(0, 6).get())
        self.assertImagesEqual(img, new_kao.get(100, 8).get())
        self.assertIsNone(new_kao.get(1153, 0))

    def test_set_reference_behaviour(self) -> None:
        img = self._load_image(self._fix_path_png(0, 1))
        img_zero = self.kao.get(0, 0)
        # This must NOT copy the image
        self.kao.set(0, 2, img_zero)
        img_zero.set(img)
        self.assertImagesEqual(img, self.kao.get(0, 0).get())
        self.assertImagesEqual(img, self.kao.get(0, 2).get())
        new_kao = self._save_and_reload_main_fixture(self.kao)
        self.assertImagesEqual(img, new_kao.get(0, 0).get())
        self.assertImagesEqual(img, new_kao.get(0, 2).get())

    def test_clone(self) -> None:
        img = self._load_image(self._fix_path_png(0, 1))
        one = self.kao.get(0, 0)
        two = one.clone()
        two.set(img)
        self.assertImagesNotEqual(one.get(), two.get())

    def test_set_from_img_rgb(self) -> None:
        img = self._load_image(self._fix_path_png(0, 1, rgb=True))
        self.kao.set_from_img(552, 8, img)
        self.kao.set_from_img(1153, 4, img)
        self.kao.get(0, 6).set(img)
        self.kao.set(100, 8, self.kao.get(552, 8))
        new_kao = self._save_and_reload_main_fixture(self.kao)
        self.assertImagesNotEqual(img, new_kao.get(0, 2).get())
        self.assertImagesEqual(img, new_kao.get(552, 8).get())
        self.assertImagesNotEqual(img, new_kao.get(552, 4).get())
        self.assertImagesEqual(img, new_kao.get(1153, 4).get())
        self.assertImagesEqual(img, new_kao.get(0, 6).get())
        self.assertImagesEqual(img, new_kao.get(100, 8).get())
        self.assertIsNone(new_kao.get(1153, 0))

    def test_delete(self) -> None:
        self.kao.delete(552, 4)
        self.kao.delete(1232132, 432131)
        self.kao.delete(552, 1)
        new_kao = self._save_and_reload_main_fixture(self.kao)
        self.assertIsNotNone(new_kao.get(0, 2))
        self.assertIsNotNone(new_kao.get(552, 8))
        self.assertIsNone(new_kao.get(0, 1))
        self.assertIsNotNone(new_kao.get(552, 0))
        self.assertIsNone(new_kao.get(552, 1))
        self.assertIsNotNone(new_kao.get(552, 2))
        self.assertIsNone(new_kao.get(552, 4))
        self.assertIsNotNone(new_kao.get(552, 6))

    def test_n_entries(self) -> None:
        kao2 = self._load_main_fixture(self._fix_path_compression_algo())
        kao3 = self._load_main_fixture(self._fix_path_complex())
        self.assertEqual(1154, self.kao.n_entries())
        self.assertEqual(1, kao2.n_entries())
        self.assertEqual(1, kao3.n_entries())

    def test_expand(self) -> None:
        with self.assertRaises(ValueError):
            self.kao.get(2000, 0)
        self.kao.expand(2001)
        new_kao = self._save_and_reload_main_fixture(self.kao)
        with self.assertRaises(ValueError):
            new_kao.get(2001, 0)
        self.assertIsNone(new_kao.get(2000, 0))

    def test_raw(self) -> None:
        kaoimg = self.kao.get(0, 2)
        raw = kaoimg.raw()
        kaoimg = self.handler.get_image_model_cls().create_from_raw(*raw)
        self.assertIsInstance(kaoimg, self.handler.get_image_model_cls())
        self.kao.get(552, 8)
        self.kao.get(1153, 4)
        self.kao.set(552, 8, kaoimg)
        self.kao.set(1153, 4, kaoimg)
        new_kao = self._save_and_reload_main_fixture(self.kao)
        self.assertImagesEqual(kaoimg.get(), new_kao.get(0, 2).get())
        self.assertImagesNotEqual(kaoimg.get(), new_kao.get(0, 4).get())
        self.assertImagesEqual(kaoimg.get(), new_kao.get(552, 8).get())
        self.assertImagesNotEqual(kaoimg.get(), new_kao.get(552, 4).get())
        self.assertImagesEqual(kaoimg.get(), new_kao.get(1153, 4).get())
        self.assertIsNone(new_kao.get(1153, 0))

    def test_iterate(self) -> None:
        previous_idx = -1
        previous_sidx = -1
        for idx, sidx, kaoimg in self.kao:
            if previous_sidx < 0:
                self.assertEqual(0, sidx)
                self.assertEqual(previous_idx + 1, idx)
                previous_idx = idx
            else:
                self.assertEqual(previous_sidx + 1, sidx)
            if sidx == FIX_IN_LEN_SUB - 1:
                previous_sidx = -1
            else:
                previous_sidx += 1
            if idx in FIX_IN_TEST_MAP:
                if sidx in FIX_IN_TEST_MAP[idx]:
                    self.assertImagesEqual(self._fix_path_png(idx, sidx), kaoimg.get())
                else:
                    self.assertIsNone(kaoimg)

            self.assertLess(previous_sidx, FIX_IN_LEN_SUB)

        self.assertGreater(previous_idx, -1)
        self.assertLess(previous_idx, FIX_IN_LEN)

    def test_compression_support(self) -> None:
        """Tests if the Kao model can at least read all compression formats"""
        # ... except for AT4PN, since that one can not fit in 800 bytes.
        self.kao = self._load_main_fixture(self._fix_path_compression_algo())
        self.assertIsNotNone(self.kao)

        # AT3PX
        self.assertImagesEqual(self._load_image(self._fix_path_png(0, 0)), self.kao.get(0, 0).get())
        # AT4PX
        self.assertImagesEqual(self._load_image(self._fix_path_png(0, 1)), self.kao.get(0, 1).get())
        # PKDPX
        self.assertImagesEqual(self._load_image(self._fix_path_png(0, 2)), self.kao.get(0, 2).get())
        # ATUPX
        self.assertImagesEqual(self._load_image(self._fix_path_png(0, 3)), self.kao.get(0, 3).get())

    def test_proper_toc_layout_writes(self) -> None:
        kao_data = self._save_and_reload_main_fixture_raw(self.kao)
        self.assertEqual(bytes(160), kao_data[:160])
        first_pnt = read_i32(kao_data, 160)
        number_entries = 0
        toc_cur = 164
        self.assertGreater(first_pnt, 0)
        last_non_zero_pnt = first_pnt
        while toc_cur < first_pnt:
            current_pnt = read_i32(kao_data, toc_cur)
            if current_pnt > 0:
                self.assertGreater(current_pnt, last_non_zero_pnt)
                last_non_zero_pnt = current_pnt
            else:
                self.assertGreater(-last_non_zero_pnt, current_pnt)
            toc_cur += 4
            number_entries += 1

    @romtest(file_ext="kao", path="FONT/")
    def test_using_rom(self, _, file):
        kao_before = self.handler.deserialize(file)

        kao: KaoProtocol = self.handler.deserialize(file)
        # Load and save all images in the fixture again
        for idx, sidx, img in kao:
            # TODO: This currently fails on the native model due too big compression, probably an error
            #       in reorder_palettes :(
            if (idx == 191 and sidx == 20) or (idx == 563 and sidx == 20):
                continue
            if img is not None:
                try:
                    img.set(img.get())
                except Exception as ex:
                    raise AssertionError(f"Seting the image must not fail for image at {idx},{sidx}.") from ex
        kao = self._save_and_reload_main_fixture(kao)

        # Compare all images
        for (idxb, sidxb, img1), (idx, sidx, img2) in zip(kao_before, kao):
            self.assertEqual(
                idxb,
                idx,
                "When iterating over the Kao after saving it, indices must advance the same.",
            )
            self.assertEqual(
                sidxb,
                sidx,
                "When iterating over the Kao after saving it, subindices must advance the same.",
            )
            if img1 is None and img2 is not None:
                self.fail(f"If image was None before, must be None after. [idx={idx}, sidx={sidx}]")
            elif img2 is None and img1 is not None:
                self.fail(f"If image was not None before, must not be None after. [idx={idx}, sidx={sidx}]")
            elif img2 is not None:
                self.assertImagesEqual(img1.get(), img2.get(), msg="[idx={idx}, sidx={sidx}]")

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_kao(cls) -> str:
        return "fixtures", "kaomado.kao"

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_compression_algo(cls) -> str:
        return "fixtures", "compression_algo.kao"

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_complex(cls) -> str:
        return "fixtures", "complex.kao"

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_png(cls, idx: int, sidx: int, rgb: bool = False) -> str:
        if rgb:
            return "fixtures", "rgb", f"{idx:04}", f"{sidx:02}.png"
        return "fixtures", f"{idx:04}", f"{sidx:02}.png"

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_complex_png(cls, sidx: int) -> str:
        return "fixtures", "complex", f"1_{sidx}.png"
