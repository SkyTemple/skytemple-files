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

from typing import TYPE_CHECKING, Type

from skytemple_files.common.impl_cfg import ImplementationType, get_implementation_type
from skytemple_files.common.types.hybrid_data_handler import (
    HybridDataHandler,
    WriterProtocol,
)
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.graphics.bpa.protocol import BpaFrameInfoProtocol, BpaProtocol

if TYPE_CHECKING:
    pass


class BpaHandler(HybridDataHandler[BpaProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[BpaProtocol]:
        from skytemple_files.graphics.bpa._model import Bpa

        return Bpa

    @classmethod
    def load_native_model(cls) -> Type[BpaProtocol]:
        from skytemple_rust.st_bpa import (  # pylint: disable=no-name-in-module,no-member,import-error
            Bpa,
        )

        return Bpa

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol["PyBpa"]]:  # type: ignore
        from skytemple_files.graphics.bpa._writer import BpaWriter

        return BpaWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol["NativeBpa"]]:  # type: ignore
        from skytemple_rust.st_bpa import (
            BpaWriter,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return BpaWriter

    @classmethod
    def get_frame_info_model_cls(cls) -> Type[BpaFrameInfoProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_bpa import (
                BpaFrameInfo as BpaFrameInfoNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return BpaFrameInfoNative
        from skytemple_files.graphics.bpa._model import BpaFrameInfo

        return BpaFrameInfo

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> BpaProtocol:
        return cls.get_model_cls()(bytes(data))

    @classmethod
    def serialize(cls, data: BpaProtocol, **kwargs: OptionalKwargs) -> bytes:
        return cls.get_writer_cls()().write(data)

    @classmethod
    def new(cls) -> BpaProtocol:
        return cls.get_model_cls().new_empty()
