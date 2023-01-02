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

from skytemple_files.common.types.hybrid_data_handler import (
    HybridDataHandler,
    WriterProtocol,
)
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.graphics.bpc.protocol import BpcProtocol

if TYPE_CHECKING:
    pass


class BpcHandler(HybridDataHandler[BpcProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[BpcProtocol]:
        from skytemple_files.graphics.bpc._model import Bpc

        return Bpc

    @classmethod
    def load_native_model(cls) -> Type[BpcProtocol]:
        from skytemple_rust.st_bpc import (
            Bpc,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return Bpc

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol["PyBpc"]]:  # type: ignore
        from skytemple_files.graphics.bpc._writer import BpcWriter

        return BpcWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol["NativeBpc"]]:  # type: ignore
        from skytemple_rust.st_bpc import (
            BpcWriter,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return BpcWriter

    @classmethod
    def deserialize(cls, data: bytes, tiling_width: int = 3, tiling_height: int = 3, **kwargs: OptionalKwargs) -> BpcProtocol:  # type: ignore
        """
        Creates a BPC. A BPC contains two layers of image data. The image data is
        grouped in 8x8 tiles, and these tiles are grouped in {tiling_width}x{tiling_height}
        chunks using a tile mapping.
        These chunks are referenced in the BMA tile to build the actual image.
        The tiling sizes are also stored in the BMA file.
        Each tile mapping is aso assigned a palette number. The palettes are stored in the BPL
        file for the map background and always contain 16 colors.

        The default for tiling_width and height are 3x3, because the game seems to be hardcoded this way.
        """
        return cls.get_model_cls()(bytes(data), tiling_width, tiling_height)

    @classmethod
    def serialize(cls, data: BpcProtocol, **kwargs: OptionalKwargs) -> bytes:
        return cls.get_writer_cls()().write(data)
