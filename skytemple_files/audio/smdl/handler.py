#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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

from skytemple_files.common.types.hybrid_data_handler import HybridDataHandler, WriterProtocol
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.audio.smdl.protocol import SmdlProtocol

if TYPE_CHECKING:
    from skytemple_files.audio.smdl._model import Smdl as PySmdl
    from skytemple_rust.st_smdl import Smdl as NativeSmdl


class SmdlHandler(HybridDataHandler[SmdlProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[SmdlProtocol]:
        from skytemple_files.audio.smdl._model import Smdl
        return Smdl

    @classmethod
    def load_native_model(cls) -> Type[SmdlProtocol]:
        from skytemple_rust.st_smdl import Smdl
        return Smdl

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol['PySmdl']]:  # type: ignore
        from skytemple_files.audio.smdl._writer import SmdlWriter
        return SmdlWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol['NativeSmdl']]:  # type: ignore
        from skytemple_rust.st_smdl import SmdlWriter
        return SmdlWriter

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> SmdlProtocol:
        return cls.get_model_cls()(bytes(data))

    @classmethod
    def serialize(cls, data: SmdlProtocol, **kwargs: OptionalKwargs) -> bytes:
        return cls.get_writer_cls()().write(data)
