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
from skytemple_files.common.util import read_bytes
from skytemple_files.data.md.model import Md
from skytemple_files.data.md.writer import MdWriter


class MdHandler(DataHandler[Md]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Md:
        if not cls.matches(data):
            raise ValueError("The provided data is not an MD file.")
        return Md(data)

    @classmethod
    def matches(cls, data: bytes, byte_offset=0):
        """Check if the given data stream has the magic string for MD files."""
        return read_bytes(data, byte_offset, 4) == b'MD\0\0'

    @classmethod
    def serialize(cls, data: Md, **kwargs) -> bytes:
        return MdWriter(data).write()
