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
import functools
import os
import sys
import typing
from abc import ABC, abstractmethod
from tempfile import TemporaryFile
from typing import Generic, TypeVar, Protocol, Optional, Mapping, Any, Type

from PIL import Image

from skytemple_files.common.util import OptionalKwargs, get_files_from_rom_with_extension, get_ppmdu_config_for_rom
from skytemple_files.test.image import ImageTestCaseAbc

U = TypeVar('U')


class BoundDataHandler(Protocol[U]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> U: ...

    @classmethod
    def serialize(cls, data: U, **kwargs: OptionalKwargs) -> bytes: ...


T = TypeVar('T', bound=BoundDataHandler)  # type: ignore


class SkyTempleFilesTestCase(ImageTestCaseAbc, Generic[T, U], ABC):
    @classmethod
    @property
    @abstractmethod
    def handler(cls) -> Type[T]: pass  # type: ignore

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


@typing.no_type_check
def fixpath(func):
    @functools.wraps(func)
    def ffunc(cls, *args, **kwargs):
        return os.path.join(os.path.dirname(sys.modules[cls.__module__].__file__), *func(cls, *args, **kwargs))
    return ffunc


def romtest(*, file_ext, path):
    """
    Runs tests against a real ROM.
    file_ext is the file extensions checked and path the path prefix.
    The env var SKYTEMPLE_TEST_ROM must contain the path to the ROM otherwise the test is skipped.
    Tests are marked with the pytest mark "romtest".
    """
    def _outer_wrapper(wrapped_function):
        import inspect
        import pytest
        from ndspy.rom import NintendoDSRom
        from unittest import SkipTest
        from parameterized import parameterized
        rom = None
        if 'SKYTEMPLE_TEST_ROM' in os.environ and os.environ['SKYTEMPLE_TEST_ROM'] != '':
            rom = NintendoDSRom.fromFile(os.environ['SKYTEMPLE_TEST_ROM'])

        if rom:
            def dataset_name_func(testcase_func, _, param):
                return f'{testcase_func.__name__}/{param.args[0]}'
            files = [(x, rom.getFileByName(x)) for x in get_files_from_rom_with_extension(rom, file_ext) if x.startswith(path)]

            if len(files) < 1:
                def no_files(*args, **kwargs):
                    raise SkipTest("No matching files were found in the ROM.")

                return pytest.mark.romtest(no_files)
            else:
                spec = inspect.getfullargspec(wrapped_function)
                if "pmd2_data" in spec.args or "pmd2_data" in spec.kwonlyargs:
                    pmd2_data = get_ppmdu_config_for_rom(rom)

                    def pmd2datawrapper(*args, **kwargs):
                        return wrapped_function(*args, **kwargs, pmd2_data=pmd2_data)
                    pmd2datawrapper.__name__ = wrapped_function.__name__

                    parameterized.expand(files, name_func=dataset_name_func)(pytest.mark.romtest(pmd2datawrapper))
                else:
                    parameterized.expand(files, name_func=dataset_name_func)(pytest.mark.romtest(wrapped_function))
                # since expands now adds the tests to our locals, we need to pass them back...
                # this isn't hacky at all wdym??????ßßß
                frame_locals = inspect.currentframe().f_back.f_locals  # type: ignore
                for local_name, local in inspect.currentframe().f_locals.items():  # type: ignore
                    if local_name.startswith('test_'):
                        frame_locals[local_name] = local

        else:
            def no_tests(*args, **kwargs):
                raise SkipTest("No ROM file provided or ROM not found.")

            return pytest.mark.romtest(no_tests)
    return _outer_wrapper


