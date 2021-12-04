#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
import functools
import os
import sys
import unittest
from abc import ABC, abstractmethod
from tempfile import TemporaryFile, mkstemp
from typing import Generic, TypeVar, Callable, Iterable, Protocol, overload, Optional, Tuple, Mapping, Any, Type, Union, \
    Sequence, Dict, List

import typing
from PIL import Image, ImageChops, ImageDraw

from skytemple_files.common.util import OptionalKwargs

U = TypeVar('U')


class BoundDataHandler(Protocol[U]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> U: ...

    @classmethod
    def serialize(cls, data: U, **kwargs: OptionalKwargs) -> bytes: ...


T = TypeVar('T', bound=BoundDataHandler)  # type: ignore


class SkyTempleFilesTestCase(unittest.TestCase, Generic[T, U], ABC):
    @classmethod
    @property
    @abstractmethod
    def handler(cls) -> Type[T]: pass  # type: ignore

    @staticmethod
    def _load_image(path: str) -> Image.Image:
        return Image.open(path)

    @classmethod
    def _load_main_fixture(cls, path: str, **kwargs: OptionalKwargs) -> U:  # type: ignore
        with open(path, 'rb') as f:
            return cls.handler.deserialize(f.read(), **kwargs)  # type: ignore

    @classmethod
    def _save_and_reload_main_fixture(  # type: ignore
            cls, model: U, ser_kwargs: Optional[Mapping[str, Any]] = None,
            deser_kwargs: Optional[Mapping[str, Any]] = None
    ) -> U:
        if deser_kwargs is None:
            deser_kwargs = {}
        raw = cls._save_and_reload_main_fixture_raw(model, ser_kwargs)
        return cls.handler.deserialize(raw, **deser_kwargs)  # type: ignore

    @classmethod
    def _save_and_reload_main_fixture_raw(  # type: ignore
            cls, model: U, ser_kwargs: Optional[Mapping[str, Any]] = None
    ) -> bytes:
        if ser_kwargs is None:
            ser_kwargs = {}
        with TemporaryFile(mode='rb+') as f:
            f.write(cls.handler.serialize(model, **ser_kwargs))  # type: ignore
            f.seek(0)
            return f.read()  # type: ignore

    def assertImagesEqual(
            self, expected: Union[str, Image.Image], input_img: Image.Image,
            palette_filter: Optional[Callable[[Sequence[int], Sequence[int]], Sequence[int]]] = None,
            rgb_diff: bool = False
    ) -> None:
        self._assertImageEqual(expected, input_img, palette_filter, rgb_diff, equal=True)

    def assertImagesNotEqual(
            self, expected: Union[str, Image.Image], input_img: Image.Image,
            palette_filter: Optional[Callable[[Sequence[int], Sequence[int]], Sequence[int]]] = None,
            rgb_diff: bool = False
    ) -> None:
        self._assertImageEqual(expected, input_img, palette_filter, rgb_diff, equal=False)

    def _assertImageEqual(
            self, expected: Union[str, Image.Image], input_img: Image.Image,
            palette_filter: Optional[Callable[[Sequence[int], Sequence[int]], Sequence[int]]] = None,
            rgb_diff: bool = False, *, equal: bool
    ) -> None:
        self.assertIsInstance(input_img, Image.Image)
        if isinstance(expected, str):
            expected = self._load_image(expected)
        if palette_filter is not None:
            assert expected.mode == 'P'
            self.assertEqual('P', input_img.mode)
            expected.putpalette(palette_filter(expected.getpalette(), input_img.getpalette()))  # type: ignore
        if rgb_diff:
            try:
                if equal:
                    self.assertTrue(are_images_equal(expected, input_img), "Images must be identical.")
                else:
                    self.assertFalse(are_images_equal(expected, input_img), "Images must not be identical.")
            except AssertionError as e:
                tempfile, tempfile_path = mkstemp(suffix=".png")
                comparision_image = Image.new('RGB', (expected.width + 5 + input_img.width, max(expected.height, input_img.height) + 20), (255, 255, 255))
                draw = ImageDraw.Draw(comparision_image)
                draw.text((2, 1), "Expected", (0, 0, 0))
                draw.text((expected.width + 7, 1), "Actual", (0, 0, 0))
                comparision_image.paste(expected, (0, 15))
                comparision_image.paste(input_img, (expected.width + 5, 15))
                comparision_image.save(os.fdopen(tempfile, mode='wb'), format="PNG")
                raise AssertionError(f"Assertion failed: Comparison image output to {tempfile_path}") from e


def are_images_equal(img1: Image.Image, img2: Image.Image) -> bool:
    equal_size = img1.height == img2.height and img1.width == img2.width

    if img1.mode == img2.mode == "RGBA":
        img1_alphas = [pixel[3] for pixel in img1.getdata()]
        img2_alphas = [pixel[3] for pixel in img2.getdata()]
        equal_alphas = img1_alphas == img2_alphas
    else:
        equal_alphas = True

    equal_content = not ImageChops.difference(
        img1.convert("RGB"), img2.convert("RGB")
    ).getbbox()

    return equal_size and equal_alphas and equal_content


X = TypeVar('X', bound=SkyTempleFilesTestCase)  # type: ignore
G = TypeVar('G', bound=Sequence[str], covariant=True)


class SomeMethod(Protocol[G]):
    def __call__(self, c: Type[X], *args: List[Any], **kwargs: Dict[str, Any]) -> G: ...


class SomeMethodDecorated(Protocol):
    def __call__(self, c: Type[X], *args: List[Any], **kwargs: Dict[str, Any]) -> str: ...


@typing.no_type_check
def fixpath(func):
    @functools.wraps(func)
    def ffunc(cls, *args, **kwargs):
        return os.path.join(os.path.dirname(sys.modules[cls.__module__].__file__), *func(cls, *args, **kwargs))
    return ffunc
