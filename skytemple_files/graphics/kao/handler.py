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
from skytemple_files.graphics.kao.writer import KaoWriter


class KaoHandler(HybridDataHandler[KaoProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[KaoProtocol]:
        return Kao

    @classmethod
    def load_native_model(cls) -> Type[KaoProtocol]:
        raise NotImplementedError()  # TODO

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol[Kao]]:  # type: ignore
        return KaoWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol[KaoProtocol]]:
        raise NotImplementedError()  # TODO

    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> KaoProtocol:
        if not isinstance(data, memoryview):
            data = memoryview(data)
        # First 160 bytes are padding
        first_toc = (SUBENTRIES*SUBENTRY_LEN)
        # The following line won't work; what if the first byte of the first pointer is 0?
        # first_toc = next(x for x, val in enumerate(data) if val != 0)
        assert first_toc % SUBENTRIES*SUBENTRY_LEN == 0  # Padding should be a whole TOC entry
        # first pointer = end of TOC
        first_pointer = read_uintle(data, first_toc, SUBENTRY_LEN)
        toc_len = int((first_pointer - first_toc) / (SUBENTRIES*SUBENTRY_LEN))
        return Kao(data, first_toc, toc_len)

    @classmethod
    def serialize(cls, data: KaoProtocol, **kwargs) -> bytes:
        return cls.get_writer()().write(data)
