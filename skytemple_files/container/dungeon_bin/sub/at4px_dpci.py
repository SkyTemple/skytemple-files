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
from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.dpci.model import Dpci
from skytemple_files.compression_container.common_at.handler import COMMON_AT_BEST_3

class DbinAt4pxDpciHandler(DataHandler[Dpci]):

    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Dpci:
        from skytemple_files.common.types.file_types import FileType
        at = FileType.COMMON_AT.deserialize(data)
        return FileType.DPCI.deserialize(at.decompress())

    @classmethod
    def serialize(cls, data: Dpci, **kwargs) -> bytes:
        from skytemple_files.common.types.file_types import FileType
        serialized = FileType.DPCI.serialize(data)
        return FileType.COMMON_AT.serialize(
            FileType.COMMON_AT.compress(serialized, COMMON_AT_BEST_3)
        )
