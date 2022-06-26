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

from typing import Type, TYPE_CHECKING

from skytemple_files.common.types.hybrid_data_handler import (
    HybridDataHandler,
    WriterProtocol,
)
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.graphics.dbg.protocol import DbgProtocol

if TYPE_CHECKING:
    pass


class DbgHandler(HybridDataHandler[DbgProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[DbgProtocol]:
        from skytemple_files.graphics.dbg._model import Dbg

        return Dbg

    @classmethod
    def load_native_model(cls) -> Type[DbgProtocol]:
        from skytemple_rust.st_dbg import (
            Dbg,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return Dbg

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol["PyDbg"]]:  # type: ignore
        from skytemple_files.graphics.dbg._writer import DbgWriter

        return DbgWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol["NativeDbg"]]:  # type: ignore
        from skytemple_rust.st_dbg import (
            DbgWriter,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return DbgWriter

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> DbgProtocol:
        return cls.get_model_cls()(bytes(data))

    @classmethod
    def serialize(cls, data: DbgProtocol, **kwargs: OptionalKwargs) -> bytes:
        return cls.get_writer_cls()().write(data)
