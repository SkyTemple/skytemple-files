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
from abc import abstractmethod
from typing import Type, TYPE_CHECKING, TypeVar

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.common.types.hybrid_data_handler import HybridDataHandler, WriterProtocol
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.script.ssb.protocol import SsbProtocol, ScriptDataProtocol

if TYPE_CHECKING:
    from skytemple_files.script.ssb._model import Ssb as PySsb
    from skytemple_rust.st_ssb import Ssb as NativeSsb


U = TypeVar('U', contravariant=True)


class SsbWriterProtocol(WriterProtocol[U]):
    @abstractmethod
    def __init__(self, script_data: ScriptDataProtocol, game_region: str, string_codec: str):
        ...


class SsbHandler(HybridDataHandler[SsbProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[SsbProtocol]:
        from skytemple_files.script.ssb._model import Ssb
        return Ssb

    @classmethod
    def load_native_model(cls) -> Type[SsbProtocol]:
        from skytemple_rust.st_ssb import Ssb
        return Ssb

    @classmethod
    def load_python_writer(cls) -> Type[SsbWriterProtocol['PySsb']]:  # type: ignore
        from skytemple_files.script.ssb._writer import SsbWriter
        return SsbWriter

    @classmethod
    def load_native_writer(cls) -> Type[SsbWriterProtocol['NativeSsb']]:  # type: ignore
        from skytemple_rust.st_ssb import SsbWriter
        return SsbWriter  # type: ignore

    @classmethod
    def deserialize(cls, data: bytes, static_data: Pmd2Data = None, **kwargs: OptionalKwargs) -> SsbProtocol:  # type: ignore
        if static_data is None:
            static_data = Pmd2XmlReader.load_default()

        return cls.get_model_cls()(data, static_data.script_data, static_data.game_region, static_data.string_encoding)

    @classmethod
    def serialize(cls, data: SsbProtocol, static_data: Pmd2Data = None, **kwargs: OptionalKwargs) -> bytes:  # type: ignore
        if static_data is None:
            static_data = Pmd2XmlReader.load_default()

        return cls.get_writer_cls()(static_data.script_data, static_data.game_region, static_data.string_encoding).write(data)  # type: ignore

    @classmethod
    def create(cls, static_data: Pmd2Data = None) -> SsbProtocol:
        """Create a new empty script"""
        if static_data is None:
            static_data = Pmd2XmlReader.load_default()

        return cls.get_model_cls().create_empty(static_data.script_data, static_data.game_region)
