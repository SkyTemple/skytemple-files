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
from skytemple_files.graphics.bpl.protocol import BplAnimationSpecProtocol, BplProtocol

if TYPE_CHECKING:
    pass


class BplHandler(HybridDataHandler[BplProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[BplProtocol]:
        from skytemple_files.graphics.bpl._model import Bpl

        return Bpl

    @classmethod
    def load_native_model(cls) -> Type[BplProtocol]:
        from skytemple_rust.st_bpl import (  # pylint: disable=no-name-in-module,no-member,import-error
            Bpl,
        )

        return Bpl

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol["PyBpl"]]:  # type: ignore
        from skytemple_files.graphics.bpl._writer import BplWriter

        return BplWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol["NativeBpl"]]:  # type: ignore
        from skytemple_rust.st_bpl import (
            BplWriter,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return BplWriter

    @classmethod
    def get_animation_spec_model_cls(cls) -> Type[BplAnimationSpecProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_bpl import (
                BplAnimationSpec as BplAnimationSpecNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return BplAnimationSpecNative
        from skytemple_files.graphics.bpl._model import BplAnimationSpec

        return BplAnimationSpec

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> BplProtocol:
        return cls.get_model_cls()(bytes(data))

    @classmethod
    def serialize(cls, data: BplProtocol, **kwargs: OptionalKwargs) -> bytes:
        return cls.get_writer_cls()().write(data)
