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
from skytemple_files.common.util import read_uintle
from skytemple_files.graphics.w16.model import W16, TOC_ENTRY_LEN
from skytemple_files.graphics.w16.writer import W16Writer


class W16Handler(DataHandler[W16]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> W16:
        if not isinstance(data, memoryview):
            data = memoryview(data)
        return W16(data)

    @classmethod
    def serialize(cls, data: W16, **kwargs) -> bytes:
        return W16Writer(data).write()
