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
from skytemple_files.common.util import AutoString, read_uintle


class DseDate(AutoString):
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: int, centisecond: int):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.centisecond = centisecond

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(
            read_uintle(data, 0x00, 2),
            read_uintle(data, 0x02, 1),
            read_uintle(data, 0x03, 1),
            read_uintle(data, 0x04, 1),
            read_uintle(data, 0x05, 1),
            read_uintle(data, 0x06, 1),
            read_uintle(data, 0x07, 1)
        )
