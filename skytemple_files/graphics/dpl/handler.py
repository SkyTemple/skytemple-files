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
from skytemple_files.graphics.dpl.protocol import DplProtocol

if TYPE_CHECKING:
    pass


class DplHandler(HybridDataHandler[DplProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[DplProtocol]:
        from skytemple_files.graphics.dpl._model import Dpl

        return Dpl

    @classmethod
    def load_native_model(cls) -> Type[DplProtocol]:
        from skytemple_rust.st_dpl import (
            Dpl,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return Dpl

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol["PyDpl"]]:  # type: ignore
        from skytemple_files.graphics.dpl._writer import DplWriter

        return DplWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol["NativeDpl"]]:  # type: ignore
        from skytemple_rust.st_dpl import (
            DplWriter,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return DplWriter

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> DplProtocol:
        return cls.get_model_cls()(bytes(data))

    @classmethod
    def serialize(cls, data: DplProtocol, **kwargs: OptionalKwargs) -> bytes:
        return cls.get_writer_cls()().write(data)
