#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
from typing import Type

from skytemple_files.common.types.hybrid_data_handler import HybridDataHandler, WriterProtocol
from skytemple_files.common.util import *
from skytemple_files.graphics.kao.model import Kao, SUBENTRIES, SUBENTRY_LEN
from skytemple_files.graphics.kao.protocol import KaoProtocol


class KaoHandler(HybridDataHandler[KaoProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[KaoProtocol]:
        return Kao

    @classmethod
    def load_native_model(cls) -> Type[KaoProtocol]:
        raise NotImplementedError()  # TODO

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol[Kao]]:  # type: ignore
        from skytemple_files.graphics.kao.writer import KaoWriter
        return KaoWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol[KaoProtocol]]:
        raise NotImplementedError()  # TODO

    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> KaoProtocol:
        return cls.get_model_cls()(data)

    @classmethod
    def serialize(cls, data: KaoProtocol, **kwargs) -> bytes:
        return cls.get_writer_cls()().write(data)
