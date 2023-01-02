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

from typing import Type

from skytemple_files.common.impl_cfg import get_implementation_type, ImplementationType
from skytemple_files.common.types.hybrid_data_handler import (
    HybridDataHandler,
    WriterProtocol,
)
from skytemple_files.common.util import OptionalKwargs, read_bytes
from skytemple_files.data.md.protocol import (
    MdProtocol,
    _MdPropertiesProtocol,
    MdEntryProtocol,
)


class MdHandler(HybridDataHandler[MdProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[MdProtocol]:
        from skytemple_files.data.md._model import Md

        return Md

    @classmethod
    def load_native_model(cls) -> Type[MdProtocol]:
        from skytemple_rust.st_md import (
            Md,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return Md

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol["PyMd"]]:  # type: ignore
        from skytemple_files.data.md._writer import MdWriter

        return MdWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol["NativeMd"]]:  # type: ignore
        from skytemple_rust.st_md import (
            MdWriter,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return MdWriter

    @classmethod
    def properties(cls) -> _MdPropertiesProtocol:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_md import (
                MdPropertiesState as MdPropertiesNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return MdPropertiesNative.instance()

        from skytemple_files.data.md._model import MdPropertiesState

        return MdPropertiesState.instance()

    @classmethod
    def get_entry_model_cls(cls) -> Type[MdEntryProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_md import (
                MdEntry as MdEntryNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return MdEntryNative
        from skytemple_files.data.md._model import MdEntry

        return MdEntry

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> MdProtocol:
        return cls.get_model_cls()(bytes(data))

    @classmethod
    def serialize(cls, data: MdProtocol, **kwargs: OptionalKwargs) -> bytes:
        return cls.get_writer_cls()().write(data)

    @classmethod
    def matches(cls, data: bytes, byte_offset=0):
        """Check if the given data stream has the magic string for MD files."""
        return read_bytes(data, byte_offset, 4) == b"MD\0\0"
