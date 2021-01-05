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
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.import math

from skytemple_files.common.types.data_handler import DataHandler
from chara_wan.model import WanFile
from chara_wan.writer import ImportWan, ExportWan

class CharaWanHandler(DataHandler[WanFile]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> 'WanFile':
        return ImportWan(bytes)

    @classmethod
    def serialize(cls, data: 'WanFile', **kwargs) -> bytes:
        return ExportWan(data)