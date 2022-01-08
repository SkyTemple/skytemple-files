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
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Protocol, Type

from skytemple_files.common.impl_cfg import get_implementation_type, ImplementationType
from skytemple_files.common.types.data_handler import DataHandler


U = TypeVar('U', contravariant=True)


class WriterProtocol(Protocol[U]):
    @abstractmethod
    def write(self, _model: U) -> bytes:
        pass


P = TypeVar('P')


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
