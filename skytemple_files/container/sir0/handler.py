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

from typing import Optional, List, Type, TypeVar

from range_typed_integers import u32

from skytemple_files.common.types.hybrid_data_handler import HybridDataHandler
from skytemple_files.common.util import OptionalKwargs, read_bytes
from skytemple_files.container.sir0.protocol import Sir0Protocol
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.common.types.hybrid_data_handler import WriterProtocol

T = TypeVar("T", bound=Sir0Serializable)


class Sir0Handler(HybridDataHandler[Sir0Protocol]):
    @classmethod
    def load_python_model(cls) -> Type[Sir0Protocol]:
        from skytemple_files.container.sir0._model import Sir0

        return Sir0

    @classmethod
    def load_native_model(cls) -> Type[Sir0Protocol]:
        from skytemple_rust.st_sir0 import (
            Sir0,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return Sir0

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol["PySir0"]]:  # type: ignore
        from skytemple_files.container.sir0._writer import Sir0Writer

        return Sir0Writer

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol["NativeSir0"]]:  # type: ignore
        from skytemple_rust.st_sir0 import (
            Sir0Writer,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return Sir0Writer

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> Sir0Protocol:
        if not cls.matches(data):
            raise ValueError("This is not valid Sir0.")
        return cls.get_model_cls().from_bin(bytes(data))

    @classmethod
    def serialize(cls, data: Sir0Protocol, **kwargs: OptionalKwargs) -> bytes:
        return cls.get_writer_cls()().write(data)

    @classmethod
    def matches(cls, data: bytes, byte_offset=0):
        """Check if the given data stream is a Sir0 container"""
        return read_bytes(data, byte_offset, 4) == b"SIR0"

    @classmethod
    def wrap(
        cls,
        content: bytes,
        pointer_offsets: List[u32],
        data_pointer: Optional[int] = None,
    ) -> Sir0Protocol:
        """Wraps existing data in Sir0."""
        return cls.get_model_cls()(content, pointer_offsets, data_pointer)

    @classmethod
    def wrap_obj(cls, obj: Sir0Serializable) -> Sir0Protocol:
        return cls.wrap(*obj.sir0_serialize_parts())

    @classmethod
    def unwrap_obj(cls, data: Sir0Protocol, spec: Type[T]) -> T:
        return spec.sir0_unwrap(data.content, data.data_pointer)  # type: ignore
