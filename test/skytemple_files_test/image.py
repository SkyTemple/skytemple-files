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

import os
import unittest
from abc import ABC
from tempfile import mkstemp
from typing import Callable, Optional, Sequence, Union

from PIL import Image, ImageChops, ImageDraw


class ImageTestCaseAbc(unittest.TestCase, ABC):
    def assertImagesEqual(
        self,
        expected: Union[str, Image.Image],
        input_img: Image.Image,
        palette_filter: Optional[
            Callable[[Sequence[int], Sequence[int]], Sequence[int]]
        ] = None,
        msg: Optional[str] = None,
    ) -> None:
        self._assertImageEqual(expected, input_img, palette_filter, msg, equal=True)

    def assertImagesNotEqual(
        self,
        expected: Union[str, Image.Image],
        input_img: Image.Image,
        palette_filter: Optional[
            Callable[[Sequence[int], Sequence[int]], Sequence[int]]
        ] = None,
        msg: Optional[str] = None,
    ) -> None:
        self._assertImageEqual(expected, input_img, palette_filter, msg, equal=False)

    @staticmethod
    def _load_image(path: str) -> Image.Image:
        return Image.open(path)

    def _assertImageEqual(
        self,
        expected: Union[str, Image.Image],
        input_img: Image.Image,
        palette_filter: Optional[
            Callable[[Sequence[int], Sequence[int]], Sequence[int]]
        ] = None,
        msg: Optional[str] = None,
        *,
        equal: bool,
    ) -> None:
        if msg is None:
            msg = ""
        self.assertIsInstance(input_img, Image.Image)
        if isinstance(expected, str):
            expected = self._load_image(expected)
        if palette_filter is not None:
            assert expected.mode == "P"
            self.assertEqual("P", input_img.mode)
            expected.putpalette(
                palette_filter(expected.getpalette(), input_img.getpalette())
            )  # type: ignore
        try:
            if equal:
                self.assertTrue(
                    are_images_equal(expected, input_img),
                    f"Images must be identical. {msg}",
                )
            else:
                self.assertFalse(
                    are_images_equal(expected, input_img),
                    f"Images must not be identical. {msg}",
                )
        except AssertionError as e:
            tempfile, tempfile_path = mkstemp(suffix=".png")
            comparision_image = Image.new(
                "RGB",
                (
                    expected.width + 5 + input_img.width,
                    max(expected.height, input_img.height) + 20,
                ),
                (255, 255, 255),
            )
            draw = ImageDraw.Draw(comparision_image)
            draw.text((2, 1), "Expected", (0, 0, 0))
            draw.text((expected.width + 7, 1), "Actual", (0, 0, 0))
            comparision_image.paste(expected, (0, 15))
            comparision_image.paste(input_img, (expected.width + 5, 15))
            comparision_image.save(os.fdopen(tempfile, mode="wb"), format="PNG")
            raise AssertionError(
                f"Assertion failed: Comparison image output to {tempfile_path}"
            ) from e


def are_images_equal(img1: Image.Image, img2: Image.Image) -> bool:
    equal_size = img1.height == img2.height and img1.width == img2.width

    if img1.mode == img2.mode == "RGBA":  # type: ignore
        img1_alphas = [pixel[3] for pixel in img1.getdata()]
        img2_alphas = [pixel[3] for pixel in img2.getdata()]
        equal_alphas = img1_alphas == img2_alphas
    else:
        equal_alphas = True

    equal_content = not ImageChops.difference(
        img1.convert("RGB"), img2.convert("RGB")
    ).getbbox()

    return equal_size and equal_alphas and equal_content
