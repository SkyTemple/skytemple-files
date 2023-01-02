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
from typing import Type, TypeVar

from skytemple_files.common.types.hybrid_data_handler import (
    HybridDataHandler,
    WriterProtocol,
)
from skytemple_files.common.util import OptionalKwargs, read_bytes
from skytemple_files.compression_container.protocol import CompressionContainerProtocol

T = TypeVar("T", bound=CompressionContainerProtocol)


class CompressionContainerHandler(HybridDataHandler[T], ABC):
    @classmethod
    @abstractmethod
    def magic_word(cls) -> bytes:
        """Magic word identifier at the beginning of the data."""
        pass

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol[T]]:
        return CompressionContainerWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol[T]]:
        return CompressionContainerWriter

    @classmethod
    def serialize(cls, data: T, **kwargs: OptionalKwargs) -> bytes:
        """Convert the high-level container representation back into bytes."""
        return cls.get_writer_cls()().write(data)

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> T:
        """Load a container into a high-level representation"""
        if not cls.matches(data):
            raise ValueError(
                f"The provided data is not a {str(cls.magic_word(), 'ascii')} container."
            )
        return cls.get_model_cls()(bytes(data))

    @classmethod
    def matches(cls, data: bytes, byte_offset: int = 0) -> bool:
        """Check if the given data is a container of its type"""
        return read_bytes(data, byte_offset, len(cls.magic_word())) == cls.magic_word()

    @classmethod
    def compress(cls, data: bytes) -> CompressionContainerProtocol:
        """Turn uncompressed data into a new compressed container"""
        return cls.get_model_cls().compress(bytes(data))

    @classmethod
    def cont_size(cls, data: bytes, byte_offset: int = 0) -> bool:
        """Get the size of a container starting at the given offset in data."""
        if not cls.matches(data, byte_offset):
            raise ValueError(
                f"The provided data is not a {str(cls.magic_word(), 'ascii')} container."
            )
        return cls.get_model_cls().cont_size(bytes(data), byte_offset)


class CompressionContainerWriter(WriterProtocol[CompressionContainerProtocol]):
    def write(self, model: CompressionContainerProtocol) -> bytes:
        return model.to_bytes()
