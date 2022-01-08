#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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
from typing import Type, TYPE_CHECKING

from skytemple_files.common.impl_cfg import get_implementation_type, ImplementationType
from skytemple_files.common.types.hybrid_data_handler import HybridDataHandler, WriterProtocol
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.graphics.bma.protocol import BmaProtocol

if TYPE_CHECKING:
    from skytemple_files.graphics.bma._model import Bma as PyBma
    from skytemple_rust.st_bma import Bma as NativeBma


class BmaHandler(HybridDataHandler[BmaProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[BmaProtocol]:
        from skytemple_files.graphics.bma._model import Bma
        return Bma

    @classmethod
    def load_native_model(cls) -> Type[BmaProtocol]:
        from skytemple_rust.st_bma import Bma
        return Bma

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol['PyBma']]:  # type: ignore
        from skytemple_files.graphics.bma._writer import BmaWriter
        return BmaWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol['NativeBma']]:  # type: ignore
        from skytemple_rust.st_bma import BmaWriter
        return BmaWriter

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> BmaProtocol:
        return cls.get_model_cls()(bytes(data))

    @classmethod
    def serialize(cls, data: BmaProtocol, **kwargs: OptionalKwargs) -> bytes:
        return cls.get_writer_cls()().write(data)
