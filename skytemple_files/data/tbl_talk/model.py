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
from enum import Enum

from skytemple_files.data.tbl_talk import *
from skytemple_files.common.util import *
from skytemple_files.common.i18n_util import f, _


class TalkType(Enum):
    HEALTHY = 0x0, _('Healthy')
    HALF_LIFE = 0x1, _('Half Life')
    PINCH = 0x2, _('Pinch')
    LEVEL_UP = 0x3, _('Level Up')
    WAIT = 0x4, _('Wait')
    GROUND_WAIT = 0x5, _('Ground Wait')

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, description: str):
        self.description = description

class TblTalk:
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.groups = []
        last_ptr = read_uintle(data, 0, 2)
        nbgroups = ((last_ptr//2)-1)//TBL_TALK_PERSONALITY_LEN
        for g in range(nbgroups):
            personality = []
            for i in range(TBL_TALK_PERSONALITY_LEN):
                next_ptr = read_uintle(data, 2+g*TBL_TALK_PERSONALITY_LEN*2+i*2, 2)
                talk_type = []
                while last_ptr!=next_ptr:
                    talk_type.append(read_uintle(data, last_ptr, 2))
                    last_ptr += 2
                personality.append(talk_type)
            self.groups.append(personality)
        self.monster_personalities = []
        while last_ptr<len(data):
            self.monster_personalities.append(read_uintle(data, last_ptr))
            last_ptr += 1
        self.special_personalities = self.monster_personalities[-TBL_TALK_SPEC_LEN:]
        self.monster_personalities = self.monster_personalities[:-TBL_TALK_SPEC_LEN]

    def remove_group(self, group: int):
        #IMPORTANT! This doesn't work because the game needs a specific number of groups 
        del self.groups[group]
    
    def add_group(self):
        #IMPORTANT! This doesn't work because the game needs a specific number of groups 
        self.groups.append([])
        for _ in range(TBL_TALK_PERSONALITY_LEN):
            self.groups[-1].append([])

    def get_dialogues(self, group: int, talk_type: TalkType):
        return self.groups[group][talk_type.value]
    
    def set_dialogues(self, group: int, talk_type: TalkType, dialogues: List[int]):
        self.groups[group][talk_type.value] = dialogues

    def get_nb_groups(self) -> int:
        return len(self.groups)
    
    def get_monster_personality(self, ent_id) -> int:
        return self.monster_personalities[ent_id]
    
    def get_nb_monsters(self) -> int:
        return len(self.monster_personalities)
    
    def set_monster_personality(self, ent_id, personality):
        self.monster_personalities[ent_id] = personality
        
    def add_monster_personality(self, personality):
        self.monster_personalities.append(personality)

    def get_special_personality(self, spec_id) -> int:
        return self.special_personalities[spec_id]
    
    def set_special_personality(self, spec_id, personality):
        self.special_personalities[spec_id] = personality
    
    
