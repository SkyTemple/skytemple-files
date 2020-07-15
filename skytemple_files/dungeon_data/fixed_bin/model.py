#  Copyright 2020 Parakoopa
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
from typing import Optional

from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable


class FixedBin(Sir0Serializable):

    def __init__(self, data: bytes, header_start: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.dungeon_data.fixed_bin.writer import FixedBinWriter
        return FixedBinWriter(self).write()

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int, static_data: Optional[Pmd2Data] = None) -> 'FixedBin':
        return cls(content_data, data_pointer)
