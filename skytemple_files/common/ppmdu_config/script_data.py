"""
The script_data section of the main static configuration.
For now, the documentation of fields is in the pmd2scriptdata.xml.
"""
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
from typing import List, Dict

from skytemple_files.common.util import AutoString


class Pmd2ScriptGameVar(AutoString):
    def __init__(self, type: int, unk1: int, memoffset: int, bitshift: int, unk3: int, unk4: int, name: str):
        self.type = type
        self.unk1 = unk1
        self.memoffset = memoffset
        self.bitshift = bitshift
        self.unk3 = unk3
        self.unk4 = unk4
        self.name = name


class Pmd2ScriptObject(AutoString):
    def __init__(self, id: int, unk1: int, unk2: int, unk3: int, name: str):
        self.id = id
        self.unk1 = unk1
        self.unk2 = unk2
        self.unk3 = unk3
        self.name = name


class Pmd2ScriptRoutine(AutoString):
    def __init__(self, id: int, unk1: int, name: str):
        self.id = id
        self.unk1 = unk1
        self.name = name


class Pmd2ScriptMenu(AutoString):
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Pmd2ScriptSpecial(AutoString):
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Pmd2ScriptSpriteEffect(AutoString):
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Pmd2ScriptLevel(AutoString):
    def __init__(self, id: int, mapid: int, name: str, mapty: int, unk2: int, unk4: int):
        self.id = id
        self.mapid = mapid
        self.name = name
        self.mapty = mapty
        self.unk2 = unk2
        self.unk4 = unk4


class Pmd2ScriptEntity(AutoString):
    def __init__(self, id: int, entid: int, name: str, type: int, unk3: int, unk4: int):
        self.id = id
        self.entid = entid
        self.name = name
        self.type = type
        self.unk3 = unk3
        self.unk4 = unk4


class Pmd2ScriptData(AutoString):
    """TODO: Cache the __by_xyz properties."""
    def __init__(self,
                 game_variables_table: List[Pmd2ScriptGameVar],
                 objects_list: List[Pmd2ScriptObject],
                 face_names: List[str],
                 face_position_modes: List[str],
                 directions: Dict[int, str],
                 common_routine_info: List[Pmd2ScriptRoutine],
                 menu_ids: List[Pmd2ScriptMenu],
                 process_special_ids: List[Pmd2ScriptSpecial],
                 sprite_effect_ids: List[Pmd2ScriptSpriteEffect],
                 level_list: List[Pmd2ScriptLevel],
                 level_entity_table: List[Pmd2ScriptEntity]):
        self._game_variables = game_variables_table
        self._objects = objects_list
        self._face_names = face_names
        self._face_position_modes = face_position_modes
        self._directions = directions
        self._common_routine_info = common_routine_info
        self._menus = menu_ids
        self._process_specials = process_special_ids
        self._sprite_effects = sprite_effect_ids
        self._level_list = level_list
        self._level_entities = level_entity_table

    @property
    def game_variables(self):
        return self._game_variables

    @game_variables.setter
    def game_variables(self, value):
        self._game_variables = value

    @property
    def game_variables__by_id(self):
        return self.game_variables

    @property
    def game_variables__by_name(self):
        return {var.name: var for var in self.game_variables}

    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, value):
        self._objects = value

    @property
    def objects__by_id(self):
        return {o.id: o for o in self.objects}

    @property
    def objects__by_name(self):
        return {o.name: o for o in self.objects if o.name != 'NULL'}

    @property
    def face_names(self):
        return self._face_names

    @face_names.setter
    def face_names(self, value):
        self._face_names = value

    @property
    def face_names__by_id(self):
        return self.face_names

    @property
    def face_names__by_name(self):
        return {n: i for i, n in enumerate(self.face_names)}

    @property
    def face_position_modes(self):
        return self._face_position_modes

    @face_position_modes.setter
    def face_position_modes(self, value):
        self._face_position_modes = value

    @property
    def face_position_modes__by_id(self):
        return self.face_position_modes

    @property
    def face_position_modes__by_name(self):
        return {n: i for i, n in enumerate(self.face_position_modes)}

    @property
    def directions(self):
        return self._directions

    @directions.setter
    def directions(self, value):
        self._directions = value

    @property
    def directions__by_id(self):
        return self.directions

    @property
    def directions__by_name(self):
        return {b: a for a, b in self.directions.items()}

    @property
    def common_routine_info(self):
        return self._common_routine_info

    @common_routine_info.setter
    def common_routine_info(self, value):
        self._common_routine_info = value

    @property
    def common_routine_info__by_id(self):
        return self.common_routine_info

    @property
    def common_routine_info__by_name(self):
        return {o.name: o for o in self.common_routine_info}

    @property
    def menus(self):
        return self._menus

    @menus.setter
    def menus(self, value):
        self._menus = value

    @property
    def menus__by_id(self):
        return {o.id: o for o in self.menus}

    @property
    def menus__by_name(self):
        return {o.name: o for o in self.menus}

    @property
    def process_specials(self):
        return self._process_specials

    @process_specials.setter
    def process_specials(self, value):
        self._process_specials = value

    @property
    def process_specials__by_id(self):
        return {o.id: o for o in self.process_specials}

    @property
    def process_specials__by_name(self):
        return {o.name: o for o in self.process_specials}

    @property
    def sprite_effects(self):
        return self._sprite_effects

    @sprite_effects.setter
    def sprite_effects(self, value):
        self._sprite_effects = value

    @property
    def sprite_effects__by_id(self):
        return {o.id: o for o in self.sprite_effects}

    @property
    def sprite_effects__by_name(self):
        return {o.name: o for o in self.sprite_effects}

    @property
    def level_list(self):
        return self._level_list

    @level_list.setter
    def level_list(self, value):
        self._level_list = value

    @property
    def level_list__by_id(self):
        return {o.id: o for o in self.level_list}

    @property
    def level_list__by_name(self):
        return {o.name: o for o in self.level_list}

    @property
    def level_entities(self):
        return self._level_entities

    @level_entities.setter
    def level_entities(self, value):
        self._level_entities = value

    @property
    def level_entities__by_id(self):
        return {o.id: o for o in self.level_entities}

    @property
    def level_entities__by_name(self):
        return {o.name: o for o in self.level_entities}
