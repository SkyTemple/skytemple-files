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
from __future__ import annotations

import filecmp
import functools
import os
import sys
import typing
from abc import ABC
from pathlib import Path
from tempfile import TemporaryFile
from typing import Any, Generic, Mapping, Optional, Protocol, Type, TypeVar
from unittest import SkipTest

from PIL import Image

from skytemple_files.common.util import (
    OptionalKwargs,
    get_files_from_rom_with_extension,
    get_ppmdu_config_for_rom,
)
from skytemple_files_test.image import ImageTestCaseAbc
from skytemple_files_test.xml import XmlTestCaseAbc

SKYTEMPLE_TEST_ROM_ENV = "SKYTEMPLE_TEST_ROM"
U = TypeVar("U")


class BoundDataHandler(Protocol[U]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> U: ...

    @classmethod
    def serialize(cls, data: U, **kwargs: OptionalKwargs) -> bytes: ...


T = TypeVar("T", bound=BoundDataHandler)  # type: ignore


class SkyTempleFilesTestCase(ImageTestCaseAbc, XmlTestCaseAbc, Generic[T, U], ABC):
    handler: Type[T]

    @classmethod
    def _load_main_fixture(cls, path: str, **kwargs: OptionalKwargs) -> U:  # type: ignore
        with open(path, "rb") as f:
            return cls.handler.deserialize(f.read(), **kwargs)  # type: ignore

    @classmethod
    def _save_and_reload_main_fixture(  # type: ignore
        cls,
        model: U,
        ser_kwargs: Optional[Mapping[str, Any]] = None,
        deser_kwargs: Optional[Mapping[str, Any]] = None,
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
        with TemporaryFile(mode="rb+") as f:
            f.write(cls.handler.serialize(model, **ser_kwargs))  # type: ignore
            f.seek(0)
            return f.read()  # type: ignore

    def assertDirsEqual(self, dir1: str, dir2: str, msg: str = "Failed", *, ignore_contents: list[str] | None = None):
        ignore_contents = ignore_contents or []
        cmp = filecmp.dircmp(dir1, dir2)
        self.assertEqual(0, len(cmp.left_only), f"{msg}: Files exist in {dir1} but not in {dir2}: {cmp.left}")
        self.assertEqual(0, len(cmp.right_only), f"{msg}: Files exist in {dir2} but not in {dir1}: {cmp.right}")
        self.assertEqual(
            0, len(cmp.funny_files), f"{msg}: Some files in {dir1} and {dir2} could not be compared: {cmp.funny_files}"
        )
        self.assertEqual(
            0,
            len(cmp.common_funny),
            f"{msg}: Some files in {dir1} and {dir2} could not be compared: {cmp.common_funny}",
        )

        # For all differing files we now need to run some checks that they actually differ.
        for file_path in cmp.diff_files:
            if file_path in ignore_contents:
                continue
            if file_path.lower().endswith(".xml"):
                self.assertXmlEqual(
                    os.path.join(dir1, file_path),
                    os.path.join(dir2, file_path),
                    f"{msg}: XML File {file_path} is not equal in {dir1} and {dir2}",
                )
            elif file_path.lower().endswith(".png"):
                self.assertImagesEqual(
                    Image.open(os.path.join(dir1, file_path)),
                    Image.open(os.path.join(dir2, file_path)),
                    None,
                    f"{msg}: PNG File {file_path} is not equal in {dir1} and {dir2}",
                )
            else:
                assert False, f"{msg}: File {file_path} is not equal in {dir1} and {dir2}"


@typing.no_type_check
def fixpath(func):
    @functools.wraps(func)
    def ffunc(cls, *args, **kwargs):
        return os.path.join(
            os.path.dirname(sys.modules[cls.__module__].__file__),
            *func(cls, *args, **kwargs),
        )

    return ffunc


def romtest(*, file_names=None, file_ext=None, path):
    """
    Runs tests against a real ROM.
    file_ext is the file extensions checked and path the path prefix.
    The env var SKYTEMPLE_TEST_ROM must contain the path to the ROM otherwise the test is skipped.
    Tests are marked with the pytest mark "romtest".
    """

    def _outer_wrapper(wrapped_function):
        import inspect
        from unittest import SkipTest

        import pytest
        from ndspy.rom import NintendoDSRom
        from parameterized import parameterized

        rom = None
        if SKYTEMPLE_TEST_ROM_ENV in os.environ and os.environ[SKYTEMPLE_TEST_ROM_ENV] != "":
            rom = NintendoDSRom.fromFile(os.environ[SKYTEMPLE_TEST_ROM_ENV])

        if rom:

            def dataset_name_func(testcase_func, _, param):
                return f"{testcase_func.__name__}/{param.args[0]}"

            if file_ext is not None and file_names is not None:
                raise TypeError("file_ext and file_names can not be set at the same time.")
            if file_ext is not None:
                files = [
                    (x, rom.getFileByName(x))
                    for x in get_files_from_rom_with_extension(rom, file_ext)
                    if x.startswith(path)
                ]
            elif file_names is not None:
                files = [(x, rom.getFileByName(path + x)) for x in file_names]
            else:
                raise TypeError("Either file_ext or file_names can not be set at the same time.")

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
                    if local_name.startswith("test_"):
                        frame_locals[local_name] = local

        else:

            def no_tests(*args, **kwargs):
                raise SkipTest("No ROM file provided or ROM not found.")

            return pytest.mark.romtest(no_tests)

    return _outer_wrapper


def with_fixtures(*, file_ext=None, path):
    """
    Run a test for all files in a directory (optionally filterable by file_ext).
    """

    def _outer_wrapper(wrapped_function):
        import inspect

        from parameterized import parameterized

        def dataset_name_func(testcase_func, _, param):
            return f"{testcase_func.__name__}/{os.path.basename(param.args[0])}"

        files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        if file_ext is not None:
            files = [f for f in files if os.path.basename(f).split(".")[-1] == file_ext]

        assert len(files) > 0, f"No fixtures found at {path}"

        parameterized.expand(files, name_func=dataset_name_func)(wrapped_function)
        # since expands now adds the tests to our locals, we need to pass them back...
        # this isn't hacky at all wdym??????ßßß
        frame_locals = inspect.currentframe().f_back.f_locals  # type: ignore
        for local_name, local in inspect.currentframe().f_locals.items():  # type: ignore
            if local_name.startswith("test_"):
                frame_locals[local_name] = local

    return _outer_wrapper


def load_rom_path() -> Path:
    if SKYTEMPLE_TEST_ROM_ENV in os.environ and os.environ[SKYTEMPLE_TEST_ROM_ENV] != "":
        return Path(os.environ[SKYTEMPLE_TEST_ROM_ENV])
    else:
        raise SkipTest("No ROM file provided or ROM not found.")
