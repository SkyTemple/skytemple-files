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
from skytemple_files.common.util import *


class Sir0:
    def __init__(self, content: bytes, pointer_offsets: List[int], data_pointer: int = None):
        self.content = content
        self.content_pointer_offsets = pointer_offsets
        if data_pointer is None:
            data_pointer = 0
        self.data_pointer = data_pointer

    @classmethod
    def from_bin(cls, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        # TODO
        raise NotImplementedError()
