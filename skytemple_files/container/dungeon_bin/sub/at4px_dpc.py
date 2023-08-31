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

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.graphics.dpc.protocol import DpcProtocol
from skytemple_files.compression_container.common_at.handler import COMMON_AT_BEST_3


class DbinAt4pxDpcHandler(DataHandler[DpcProtocol]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> DpcProtocol:
        from skytemple_files.common.types.file_types import FileType

        at = FileType.COMMON_AT.deserialize(data)
        return FileType.DPC.deserialize(at.decompress())

    @classmethod
    def serialize(cls, data: DpcProtocol, **kwargs: OptionalKwargs) -> bytes:
        from skytemple_files.common.types.file_types import FileType

        serialized = FileType.DPC.serialize(data)
        return FileType.COMMON_AT.serialize(
            FileType.COMMON_AT.compress(serialized, COMMON_AT_BEST_3)
        )
