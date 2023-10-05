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
from skytemple_files.data.val_list.model import ValList
from skytemple_files.data.val_list.writer import ValListWriter


class ValListHandler(DataHandler[ValList]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> ValList:
        return ValList(data)

    @classmethod
    def serialize(cls, data: ValList, **kwargs: OptionalKwargs) -> bytes:
        return ValListWriter(data).write()
