"""Converts FloorAttribute models back into the binary format used by the game"""
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
from skytemple_files.common.util import *
from skytemple_files.dungeon_data.floor_attribute import *
from skytemple_files.dungeon_data.floor_attribute.model import FloorAttribute


class FloorAttributeWriter:
    def __init__(self, model: FloorAttribute):
        self.model = model

    def write(self) -> bytes:
        header = bytearray(len(self.model.attrs)*4)
        data = bytearray(0)
        for i, g_list in enumerate(self.model.attrs):
            current_ptr = len(header)+len(data)
            d_list = bytearray(g_list)
            if len(d_list)%4!=0:
                d_list += bytearray(4-(len(d_list)%4))
            write_uintle(header, current_ptr, i*4, 4)
            data += d_list
        data = header+data
        return bytes(data)
