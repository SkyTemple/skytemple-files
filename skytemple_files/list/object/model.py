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

from typing import List

from range_typed_integers import u16_checked

from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptObject
from skytemple_files.common.util import AutoString, read_u16, read_u8

LEN_OBJECT_ENTRY = 16


class ObjectListBin(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.list: List[Pmd2ScriptObject] = []

        for i in range(0, len(data) // LEN_OBJECT_ENTRY):
            offset = i * LEN_OBJECT_ENTRY
            obj_name = ""
            char = offset + 5
            while data[char] != 0:
                obj_name += chr(data[char])
                char += 1
            if obj_name == "":
                obj_name = "NULL"
            self.list.append(
                Pmd2ScriptObject(
                    id=u16_checked(i),
                    unk1=read_u16(data, offset + 0),
                    unk2=read_u16(data, offset + 2),
                    unk3=read_u8(data, offset + 4),
                    name=obj_name,
                )
            )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ObjectListBin):
            return False
        return self.list == other.list
