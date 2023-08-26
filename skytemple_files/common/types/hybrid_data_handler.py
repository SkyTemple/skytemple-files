#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Protocol, Type

from skytemple_files.common.impl_cfg import get_implementation_type, ImplementationType
from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable

U = TypeVar("U", contravariant=True)


class WriterProtocol(Protocol[U]):
    @abstractmethod
    def write(self, _model: U) -> bytes:
        pass


P = TypeVar("P")
PS = TypeVar("PS", bound=Sir0Serializable)


class HybridDataHandler(Generic[P], DataHandler[P], ABC):
    """
    Handler that supports both a Python and a native implementation
    for its file type. Which one is used is controlled by the implementation
    configuration module.

    The load methods should import on-demand.
    """

    @classmethod
    @abstractmethod
    def load_python_model(cls) -> Type[P]:
        pass

    @classmethod
    @abstractmethod
    def load_native_model(cls) -> Type[P]:
        pass

    @classmethod
    @abstractmethod
    def load_python_writer(cls) -> Type[WriterProtocol[P]]:
        pass

    @classmethod
    @abstractmethod
    def load_native_writer(cls) -> Type[WriterProtocol[P]]:
        pass

    @classmethod
    def get_model_cls(cls) -> Type[P]:
        if get_implementation_type() == ImplementationType.NATIVE:
            return cls.load_native_model()
        return cls.load_python_model()

    @classmethod
    def get_writer_cls(cls) -> Type[WriterProtocol[P]]:
        if get_implementation_type() == ImplementationType.NATIVE:
            return cls.load_native_writer()
        return cls.load_python_writer()


class HybridSir0DataHandler(Generic[PS], DataHandler[PS]):
    """
    Handler that supports both a Python and a native implementation
    for its file type. Which one is used is controlled by the implementation
    configuration module.
    This is a special variant for Sir0 wrapped models.

    The load methods should import on-demand.
    """

    @classmethod
    @abstractmethod
    def load_python_model(cls) -> Type[PS]:
        pass

    @classmethod
    @abstractmethod
    def load_native_model(cls) -> Type[PS]:
        pass

    @classmethod
    def get_model_cls(cls) -> Type[PS]:
        if get_implementation_type() == ImplementationType.NATIVE:
            return cls.load_native_model()
        return cls.load_python_model()

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> PS:
        from skytemple_files.common.types.file_types import FileType

        sir0 = FileType.SIR0.deserialize(data)
        return FileType.SIR0.unwrap_obj(sir0, cls.get_model_cls())

    @classmethod
    def serialize(cls, data: PS, **kwargs: OptionalKwargs) -> bytes:
        from skytemple_files.common.types.file_types import FileType

        sir0 = FileType.SIR0.wrap_obj(data)
        return FileType.SIR0.serialize(sir0)

    @classmethod
    @abstractmethod
    def deserialize_raw(cls, data: bytes, **kwargs: OptionalKwargs) -> PS:
        pass

    @classmethod
    @abstractmethod
    def serialize_raw(cls, data: PS, **kwargs: OptionalKwargs) -> bytes:
        pass
