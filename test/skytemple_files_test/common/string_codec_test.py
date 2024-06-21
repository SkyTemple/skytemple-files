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

from abc import abstractmethod
from typing import Protocol, Type

from parameterized import parameterized

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.types.hybrid_data_handler import (
    HybridDataHandler,
    WriterProtocol,
)
from skytemple_files.common.util import OptionalKwargs
from skytemple_files_test.compression_container.util import dataset_name_func
from skytemple_files_test.case import SkyTempleFilesTestCase, romtest


class _TstStringProtocol(Protocol):
    def __init__(self, _data: bytes): ...

    @abstractmethod
    def __str__(self) -> str: ...


class _TstStringHandler(HybridDataHandler[_TstStringProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[_TstStringProtocol]:
        return _TstPy

    @classmethod
    def load_native_model(cls) -> Type[_TstStringProtocol]:
        from skytemple_rust.st_string import StPmd2String

        return StPmd2String

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol[_TstStringProtocol]]:
        return _TstPyWriter  # type: ignore

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol[_TstStringProtocol]]:
        from skytemple_rust.st_string import StPmd2StringEncoder

        return StPmd2StringEncoder  # type: ignore

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> _TstStringProtocol:
        return cls.get_model_cls()(data)

    @classmethod
    def serialize(cls, data: _TstStringProtocol, **kwargs: OptionalKwargs) -> bytes:
        return cls.get_writer_cls()().write(data)


class _TstPy(_TstStringProtocol):
    def __init__(self, data: bytes):
        from skytemple_files.common.string_codec import PMD2_STR_ENCODER, init

        init()
        self.str: str = str(data, PMD2_STR_ENCODER)

    def __str__(self):
        return self.str


class _TstPyWriter(WriterProtocol[_TstPy]):
    def write(self, model: _TstPy) -> bytes:
        from skytemple_files.common.string_codec import PMD2_STR_ENCODER, init

        init()
        return bytes(model.str, PMD2_STR_ENCODER)


def string_dataset():
    return [
        ("0", "Hello World", b"Hello World"),
        ("1", "Checking some ANSI!! äöüß", b"Checking some ANSI!! \xe4\xf6\xfc\xdf"),
        (
            "2",
            "●★ Checking some SHIFT-JIS!! ★●",
            b"\x81\x9c\x81\x9a Checking some SHIFT-JIS!! \x81\x9a\x81\x9c",
        ),
        (
            "3",
            ".  º  .  °  ¸ º   • .   .  ° • .  ¸ .    • , º   ¨   •  ."
            "[HR][CS:B][CLUM_SET:105]œ[CN]Ð[HR][CR][HR]"
            " •  º .  °[CLUM_SET:54]Red was not an impostor.  "
            "•  ¸  º   •   ° [CLUM_SET:170]  ° • . ¨ .",
            b".  \xba  .  \xb0  \xb8 \xba   \x95 .   .  \xb0 \x95 .  \xb8 .    \x95 , \xba   \xa8   \x95  ."
            b"[HR][CS:B][CLUM_SET:105]\x9c[CN]\xd0[HR][CR][HR]"
            b" \x95  \xba .  \xb0[CLUM_SET:54]Red was not an impostor.  "
            b"\x95  \xb8  \xba   \x95   \xb0 [CLUM_SET:170]  \xb0 \x95 . \xa8 .",
        ),
    ]


class StringCodecTestCase(SkyTempleFilesTestCase[_TstStringHandler, _TstStringProtocol]):
    handler = _TstStringHandler

    @parameterized.expand(string_dataset(), name_func=dataset_name_func)
    def test_strings(self, _, expected, input_bytes):
        string = self.handler.deserialize(input_bytes)
        self.assertEqual(input_bytes, self.handler.serialize(string))
        self.assertEqual(expected, str(string))

    @romtest(file_ext="str", path="MESSAGE/")
    def test_using_rom_str(self, _, file):
        # This test assumes the Python STR model works!
        # This can only test basic consistency.
        from skytemple_files.data.str.model import Str

        for by in Str.internal__get_all_raw_strings_from(file):
            self.assertEqual(by, self.handler.serialize(self.handler.deserialize(by)))

    @romtest(file_ext="ssb", path="SCRIPT/")
    def test_using_rom_ssb(self, _, file, *, pmd2_data: Pmd2Data):
        # This test assumes the Python SSB model works!
        # This can only test basic consistency.
        from skytemple_files.script.ssb.model import Ssb

        for by in Ssb.internal__get_all_raw_strings_from(file, pmd2_data.game_region):
            self.assertEqual(by, self.handler.serialize(self.handler.deserialize(by)))
