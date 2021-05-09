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
from skytemple_files.audio.swdl.model import Swdl
from skytemple_files.audio.swdl.writer import SwdlWriter


class SwdlHandler(DataHandler[Swdl]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Swdl:
        return Swdl(data)

    @classmethod
    def serialize(cls, data: Swdl, **kwargs) -> bytes:
        return SwdlWriter(data).write()
