"""
The script_data section of the main static configuration.
For now, the documentation of fields is in the pmd2scriptdata.xml.
"""
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
import warnings
from enum import Enum, IntEnum
from typing import List, Dict, Optional

from explorerscript.ssb_converting.ssb_data_types import SsbOpCode, SsbCoroutine
from skytemple_files.common.util import AutoString
from skytemple_files.common.i18n_util import f, _


class GameVariableType(IntEnum):
    NULL = 0,
    BIT = 1,
    STRING = 2,  # Theory.
    UINT8 = 3,
    INT8 = 4,
    UINT16 = 5,
    INT16 = 6,
    UINT32 = 7,
    INT32 = 8,
    SPECIAL = 9


# XXX: I could have sworn, there was a way to get a enum instance by value...? But I can't find it.
def game_variable_type_by_value(i: int) -> GameVariableType:
    if i == 0:
        return GameVariableType.NULL
    if i == 1:
        return GameVariableType.BIT
    if i == 2:
        return GameVariableType.STRING
    if i == 3:
        return GameVariableType.UINT8
    if i == 4:
        return GameVariableType.INT8
    if i == 5:
        return GameVariableType.UINT16
    if i == 6:
        return GameVariableType.INT16
    if i == 7:
        return GameVariableType.UINT32
    if i == 8:
        return GameVariableType.UINT32
    if i == 9:
        return GameVariableType.SPECIAL
    raise ValueError(f"Unknown GameVariableType: {i}")


class Pmd2ScriptGameVar(AutoString):
    def __init__(self, id: int, type: int, unk1: int, memoffset: int, bitshift: int,
                 nbvalues: int, unk4: int, name: str, is_local: bool):
        self.id: int = id
        self.type: GameVariableType = game_variable_type_by_value(type)
        self.unk1 = unk1
        self.memoffset = memoffset
        self.bitshift = bitshift
        self.nbvalues = nbvalues
        self.unk4 = unk4
        self.name = name
        self.is_local = is_local


class Pmd2ScriptObject(AutoString):
    def __init__(self, id: int, unk1: int, unk2: int, unk3: int, name: str):
        self.id = id
        self.unk1 = unk1
        self.unk2 = unk2
        self.unk3 = unk3
        self.name = name
        self.unique_name = f'{name}_{id}'


class Pmd2ScriptRoutine(SsbCoroutine):
    def __init__(self, id: int, unk1: int, name: str):
        super().__init__(id, name)
        self.unk1 = unk1


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


class Pmd2ScriptBgm(AutoString):
    def __init__(self, id: int, name: str, loops=False):
        self.id = id
        self.name = name
        self.loops = loops


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

    def __eq__(self, other):
        if not isinstance(other, Pmd2ScriptEntity):
            return False
        return self.id == other.id and self.entid == other.entid and \
               self.name == other.name and self.type == other.type and \
               self.unk3 == other.unk3 and self.unk4 == other.unk4


class Pmd2ScriptOpCodeArgument(AutoString):
    def __init__(self, id: int, type: str, name: str):
        self.id = id
        self.type = type
        self.name = name


class Pmd2ScriptOpCodeRepeatingArgumentGroup(AutoString):
    def __init__(self, id: int, arguments: List[Pmd2ScriptOpCodeArgument]):
        self.id = id
        self.arguments = arguments

    def __getitem__(self, item):
        return self.arguments[item]


class Pmd2ScriptOpCode(SsbOpCode):
    def __init__(self,
                 id: int, name: str, params: int,
                 stringidx: int, unk2: int, unk3: int,
                 arguments: List[Pmd2ScriptOpCodeArgument],
                 repeating_argument_group: Optional[Pmd2ScriptOpCodeRepeatingArgumentGroup]):
        super().__init__(id, name)
        self.params = params
        self.stringidx = stringidx
        self.unk2 = unk2
        self.unk3 = unk3
        self.arguments: List[Pmd2ScriptOpCodeArgument] = arguments
        self.arguments__by_id: Dict[int, Pmd2ScriptOpCodeArgument] = {o.id: o for o in self.arguments}
        self.repeating_argument_group: Pmd2ScriptOpCodeRepeatingArgumentGroup = repeating_argument_group
        self.description = _("This function has no description.")  # todo


class Pmd2ScriptGroundStateStruct(AutoString):
    def __init__(self, offset: int, entrylength: int, maxentries: int):
        self.offset = offset
        self.entrylength = entrylength
        self.maxentries = maxentries


class Pmd2ScriptFaceName(AutoString):
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Pmd2ScriptFacePositionMode(AutoString):
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Pmd2ScriptDirection(AutoString):
    def __init__(self, ssa_id: int, name: str, ssb_id: int = None):
        self.ssa_id = ssa_id
        self.ssb_id = ssb_id if ssb_id is not None else ssa_id - 1
        self.name = name

    @property
    def id(self):
        """
        For backwards compatibility.
        """
        warnings.warn("Please use self.ssa_id instead.", DeprecationWarning)
        return self.ssa_id

    @property
    def print_name(self):
        if self.ssa_id == 1:
            return _('Down')  # TRANSLATORS: Direction
        elif self.ssa_id == 2:
            return _('Down Right')  # TRANSLATORS: Direction
        elif self.ssa_id == 3:
            return _('Right')  # TRANSLATORS: Direction
        elif self.ssa_id == 4:
            return _('Up Right')  # TRANSLATORS: Direction
        elif self.ssa_id == 5:
            return _('Up')  # TRANSLATORS: Direction
        elif self.ssa_id == 6:
            return _('Up Left')  # TRANSLATORS: Direction
        elif self.ssa_id == 7:
            return _('Left')  # TRANSLATORS: Direction
        elif self.ssa_id == 8:
            return _('Down Left')  # TRANSLATORS: Direction
        return self.name


class Pmd2ScriptData(AutoString):
    """TODO: Cache the __by_xyz properties."""
    def __init__(self,
                 game_variables_table: List[Pmd2ScriptGameVar],
                 objects_list: List[Pmd2ScriptObject],
                 face_names: List[Pmd2ScriptFaceName],
                 face_position_modes: List[Pmd2ScriptFacePositionMode],
                 directions: Dict[int, Pmd2ScriptDirection],
                 common_routine_info: List[Pmd2ScriptRoutine],
                 menu_ids: List[Pmd2ScriptMenu],
                 process_special_ids: List[Pmd2ScriptSpecial],
                 sprite_effect_ids: List[Pmd2ScriptSpriteEffect],
                 bgms: List[Pmd2ScriptBgm],
                 level_list: List[Pmd2ScriptLevel],
                 level_entity_table: List[Pmd2ScriptEntity],
                 op_codes: List[Pmd2ScriptOpCode],
                 ground_state_structs: Dict[str, Pmd2ScriptGroundStateStruct]):
        self._game_variables = game_variables_table
        self._objects = objects_list
        self._face_names = face_names
        self._face_position_modes = face_position_modes
        self._directions = directions
        self._common_routine_info = common_routine_info
        self._menus = menu_ids
        self._process_specials = process_special_ids
        self._sprite_effects = sprite_effect_ids
        self._bgms = bgms
        self._level_list = level_list
        self._level_entities = level_entity_table
        self._op_codes = op_codes
        self._ground_state_structs = ground_state_structs

    @property
    def game_variables(self):
        return self._game_variables

    @game_variables.setter
    def game_variables(self, value):
        self._game_variables = value

    @property
    def game_variables__by_id(self) -> Dict[int, Pmd2ScriptGameVar]:
        return {var.id: var for var in self.game_variables}

    @property
    def game_variables__by_name(self) -> Dict[str, Pmd2ScriptGameVar]:
        return {var.name: var for var in self.game_variables}

    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, value):
        self._objects = value

    @property
    def objects__by_id(self) -> Dict[int, Pmd2ScriptObject]:
        return {o.id: o for o in self.objects}

    @property
    def objects__by_unique_name(self):
        return {o.unique_name: o for o in self.objects}

    @property
    def face_names(self):
        return self._face_names

    @face_names.setter
    def face_names(self, value):
        self._face_names = value

    @property
    def face_names__by_id(self):
        return {n.id: n for n in self.face_names}

    @property
    def face_names__by_name(self):
        return {n.name: n for n in self.face_names}

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
        return {n.name: n for n in self.face_position_modes}

    @property
    def directions(self) -> Dict[int, Pmd2ScriptDirection]:
        return self._directions

    @directions.setter
    def directions(self, value):
        self._directions = value

    @property
    def directions__by_ssa_id(self) -> Dict[int, Pmd2ScriptDirection]:
        return self.directions

    @property
    def directions__by_ssb_id(self) -> Dict[int, Pmd2ScriptDirection]:
        return {d.ssb_id: d for d in self._directions.values()}

    @property
    def directions__by_name(self):
        return {b.name: b for b in self.directions.values()}

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
    def bgms(self):
        return self._bgms

    @bgms.setter
    def bgms(self, value):
        self._bgms = value

    @property
    def bgms__by_id(self):
        return {o.id: o for o in self.bgms}

    @property
    def bgms__by_name(self):
        return {o.name: o for o in self.bgms}

    @property
    def level_list(self):
        return self._level_list

    @level_list.setter
    def level_list(self, value):
        self._level_list = value

    @property
    def level_list__by_id(self) -> Dict[int, Pmd2ScriptLevel]:
        return {o.id: o for o in self.level_list}

    @property
    def level_list__by_name(self) -> Dict[str, Pmd2ScriptLevel]:
        return {o.name: o for o in self.level_list}

    @property
    def level_entities(self):
        return self._level_entities

    @level_entities.setter
    def level_entities(self, value):
        self._level_entities = value

    @property
    def level_entities__by_id(self) -> Dict[int, Pmd2ScriptEntity]:
        return {o.id: o for o in self.level_entities}

    @property
    def level_entities__by_name(self):
        return {o.name: o for o in self.level_entities}

    @property
    def op_codes(self):
        return self._op_codes

    @op_codes.setter
    def op_codes(self, value):
        self._op_codes = value

    @property
    def op_codes__by_id(self) -> Dict[int, Pmd2ScriptOpCode]:
        return {o.id: o for o in self.op_codes}

    @property
    def op_codes__by_name(self) -> Dict[str, List[Pmd2ScriptOpCode]]:
        opcs = {}
        for o in self._op_codes:
            if o.name not in opcs:
                opcs[o.name] = []
            opcs[o.name].append(o)
        return opcs

    @property
    def ground_state_structs(self):
        return self._ground_state_structs
