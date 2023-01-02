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
from skytemple_files.graphics.bg_list_dat.protocol import (
    BgListEntryProtocol,
    BgListProtocol,
)

if TYPE_CHECKING:
    pass


class BgListDatHandler(HybridDataHandler[BgListProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[BgListProtocol]:
        from skytemple_files.graphics.bg_list_dat._model import BgList

        return BgList

    @classmethod
    def load_native_model(cls) -> Type[BgListProtocol]:
        from skytemple_rust.st_bg_list_dat import (
            BgList,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return BgList

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol["PyBgList"]]:  # type: ignore
        from skytemple_files.graphics.bg_list_dat._writer import BgListWriter

        return BgListWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol["NativeBgList"]]:  # type: ignore
        from skytemple_rust.st_bg_list_dat import (
            BgListWriter,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return BgListWriter

    @classmethod
    def get_entry_model_cls(cls) -> Type[BgListEntryProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_bg_list_dat import (
                BgListEntry as BgListEntryNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return BgListEntryNative
        from skytemple_files.graphics.bg_list_dat._model import BgListEntry

        return BgListEntry

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> BgListProtocol:
        return cls.get_model_cls()(bytes(data))

    @classmethod
    def serialize(cls, data: BgListProtocol, **kwargs: OptionalKwargs) -> bytes:
        return cls.get_writer_cls()().write(data)
