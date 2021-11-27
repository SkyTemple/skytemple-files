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
from tempfile import TemporaryFile
from typing import Generic, TypeVar, Callable, Iterable, Protocol, overload, Optional, Tuple, Mapping, Any, Type, Union, \
    Sequence

from PIL import Image, ImageChops

U = TypeVar('U')


class BoundDataHandler(Protocol[U]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> U: ...

    @classmethod
    def serialize(cls, data: U, **kwargs) -> bytes: ...


T = TypeVar('T', bound=BoundDataHandler)


# noinspection PyPep8Naming
def fixpath(func):
    @functools.wraps(func)
    def ffunc(cls, *args, **kwargs) -> str:
        return os.path.join(os.path.dirname(sys.modules[cls.__module__].__file__), *func(cls, *args, **kwargs))
    return ffunc


class SkyTempleFilesTestCase(unittest.TestCase, Generic[T, U], ABC):
    @classmethod
    @property
    @abstractmethod
    def handler(cls) -> Type[T]: pass

    @staticmethod
    def _load_image(path: str) -> Image.Image:
        return Image.open(path)

    @classmethod
    def _load_main_fixture(cls, path: str, **kwargs) -> U:
        with open(path, 'rb') as f:
            return cls.handler.deserialize(f.read(), **kwargs)  # type: ignore

    @classmethod
    def _save_and_reload_main_fixture(
            cls, model: U, ser_kwargs: Mapping[str, Any] = None,
            deser_kwargs: Mapping[str, Any] = None
    ) -> U:
        if deser_kwargs is None:
            deser_kwargs = {}
        raw = cls._save_and_reload_main_fixture_raw(model, ser_kwargs)
        return cls.handler.deserialize(raw, **deser_kwargs)  # type: ignore

    @classmethod
    def _save_and_reload_main_fixture_raw(
            cls, model: U, ser_kwargs: Mapping[str, Any] = None
    ) -> bytes:
        if ser_kwargs is None:
            ser_kwargs = {}
        with TemporaryFile(mode='rb+') as f:
            f.write(cls.handler.serialize(model, **ser_kwargs))  # type: ignore
            f.seek(0)
            return f.read()

    def assetImagesEqual(
            self, expected: Union[str, Image.Image], input_img: Image.Image,
            palette_filter: Optional[Callable[[Sequence[int], Sequence[int]], Sequence[int]]] = None,
            rgb_diff=False
    ):
        self._assertImageEqual(expected, input_img, palette_filter, rgb_diff, equal=True)

    def assetImagesNotEqual(
            self, expected: Union[str, Image.Image], input_img: Image.Image,
            palette_filter: Optional[Callable[[Sequence[int], Sequence[int]], Sequence[int]]] = None,
            rgb_diff=False
    ):
        self._assertImageEqual(expected, input_img, palette_filter, rgb_diff, equal=False)

    def _assertImageEqual(
            self, expected: Union[str, Image.Image], input_img: Image.Image,
            palette_filter: Optional[Callable[[Sequence[int], Sequence[int]], Sequence[int]]] = None,
            rgb_diff=False, *, equal
    ):
        self.assertIsInstance(input_img, Image.Image)
        if isinstance(expected, str):
            expected = self._load_image(expected)
        if palette_filter is not None:
            assert expected.mode == 'P'
            self.assertEqual('P', input_img.mode)
            expected.putpalette(palette_filter(expected.getpalette(), input_img.getpalette()))
        if rgb_diff:
            # Gotta love the jankiness of PIL
            # Sometimes RGBA conversion diff fails on the alpha channel for whatever reason
            # On the other hand RGB conversion doesn't generate 100% accurate colors all of the time
            # Guess we can just hope that at least one always works...:
            try:
                expected = expected.convert('RGBA')
                input_img = input_img.convert('RGBA')
                diff = ImageChops.difference(expected, input_img)
                if equal:
                    self.assertIsNone(diff.getbbox())
                else:
                    self.assertIsNotNone(diff.getbbox())
                return
            except AssertionError:
                expected = expected.convert('RGB')
                input_img = input_img.convert('RGB')
        diff = ImageChops.difference(expected, input_img)
        if equal:
            self.assertIsNone(diff.getbbox())
        else:
            self.assertIsNotNone(diff.getbbox())
