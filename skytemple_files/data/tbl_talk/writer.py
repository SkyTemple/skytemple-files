"""Converts Md models back into the binary format used by the game"""
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
from skytemple_files.data.tbl_talk import *
from skytemple_files.data.tbl_talk.model import TblTalk


class TblTalkWriter:
    def __init__(self, model: TblTalk):
        self.model = model

    def write(self) -> bytes:
        data = bytearray(len(self.model.groups)*TBL_TALK_PERSONALITY_LEN*2+2)
        last_ptr = len(data)
        write_uintle(data, last_ptr, 0, 2)
        for g in range(len(self.model.groups)):
            for i in range(TBL_TALK_PERSONALITY_LEN):
                for t in self.model.groups[g][i]:
                    buffer = bytearray(2)
                    write_uintle(buffer, t, 0, 2)
                    data += buffer
                    last_ptr += 2
                write_uintle(data, last_ptr, 2+(i+g*TBL_TALK_PERSONALITY_LEN)*2, 2)

        data += bytes(self.model.monster_personalities)+bytes(self.model.special_personalities)
        return data
