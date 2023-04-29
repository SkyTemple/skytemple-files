"""Converts WazaP models back into the binary format used by the game"""
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

from skytemple_files.common.util import write_u8, write_u16
from skytemple_files.list.object.model import LEN_OBJECT_ENTRY, ObjectListBin


class ObjectListBinWriter:
    def __init__(self, model: ObjectListBin):
        self.model = model

    def write(self) -> bytes:
        object_list = []
        for o in self.model.list:
            obj_data = bytearray(LEN_OBJECT_ENTRY)
            write_u16(obj_data, o.unk1, 0)
            write_u16(obj_data, o.unk2, 2)
            write_u8(obj_data, o.unk3, 4)
            if o.name != "NULL":
                count = 0
                for c in o.name:
                    if count >= 10:
                        raise ValueError(
                            "Invalid string length (more than 10 characters)"
                        )
                    if ord(c) >= 256:
                        raise ValueError("Invalid string (non-ASCII characters)")
                    obj_data[5 + count] = ord(c)
                    count += 1
            object_list.append(obj_data)
        return b"".join(object_list)
