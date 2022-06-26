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
from skytemple_files.compression_container.common_at.handler import (
    COMMON_AT_MUST_COMPRESS_4,
)
from skytemple_files.graphics.bgp.protocol import BgpProtocol

if TYPE_CHECKING:
    pass


class BgpHandler(HybridDataHandler[BgpProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[BgpProtocol]:
        from skytemple_files.graphics.bgp._model import Bgp

        return Bgp

    @classmethod
    def load_native_model(cls) -> Type[BgpProtocol]:
        from skytemple_rust.st_bgp import (
            Bgp,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        # Tilemap protocol issue:
        return Bgp  # type: ignore

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol["PyBgp"]]:  # type: ignore
        from skytemple_files.graphics.bgp._writer import BgpWriter

        return BgpWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol["NativeBgp"]]:  # type: ignore
        from skytemple_rust.st_bgp import (
            BgpWriter,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return BgpWriter

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> BgpProtocol:
        from skytemple_files.common.types.file_types import FileType

        return cls.get_model_cls()(
            bytes(FileType.COMMON_AT.deserialize(data).decompress())
        )

    @classmethod
    def serialize(cls, data: BgpProtocol, **kwargs: OptionalKwargs) -> bytes:
        from skytemple_files.common.types.file_types import FileType

        return FileType.COMMON_AT.serialize(
            FileType.COMMON_AT.compress(
                cls.get_writer_cls()().write(data), COMMON_AT_MUST_COMPRESS_4
            )
        )
