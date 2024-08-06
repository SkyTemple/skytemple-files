"""
The script_data section of the main static configuration.
For now, the documentation of fields is in the pmd2scriptdata.xml.
"""

from __future__ import annotations

#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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
from contextlib import contextmanager
import re
import warnings
from enum import Enum, IntEnum
from typing import Union
from collections.abc import Iterator, Sequence, Mapping

from explorerscript.ssb_converting.ssb_data_types import SsbCoroutine, SsbOpCode
from range_typed_integers import i16, u8, u16

from skytemple_files.common.i18n_util import _
from skytemple_files.common.util import AutoString
from skytemple_files.common.warnings import DeprecatedToBeRemovedWarning


class GameVariableType(IntEnum):
    NULL = (0,)
    BIT = (1,)
    STRING = (2,)  # Theory.
    UINT8 = (3,)
    INT8 = (4,)
    UINT16 = (5,)
    INT16 = (6,)
    UINT32 = (7,)
    INT32 = (8,)
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
    def __init__(
        self,
        id: int,
        type: int,
        unk1: int,
        memoffset: int,
        bitshift: int,
        nbvalues: int,
        unk4: int,
        name: str,
        is_local: bool,
    ):
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
    def __init__(self, id: u16, unk1: u16, unk2: u16, unk3: u8, name: str):
        self.id = id
        self.unk1 = unk1
        self.unk2 = unk2
        self.unk3 = unk3
        self.name = name
        self.unique_name = f"{name}_{id}"


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
    def __init__(self, id: int, name: str, loops: bool = False):
        self.id = id
        self.name = name
        self.loops = loops


class Pmd2ScriptLevelMapType(Enum):
    LAYER1_0 = 0, _("One Layer (#00)")
    LAYER1_1 = 1, _("One Layer (#01)")
    LAYER1_2 = 2, _("One Layer (#02)")
    LAYER1_3 = 3, _("One Layer (#03)")
    LAYER1_4 = 4, _("One Layer (#04)")
    LAYER1_5 = 5, _("Two Layers (#05)")
    LAYER1_6 = 6, _("Two Layers (#06)")
    LAYER1_7 = 7, _("Two Layers (#07)")
    LAYER1_8 = 8, _("Two Layers (#08)")
    LAYER1_9 = 9, _("Two Layers (#09)")
    TILESET = 10, _("Dungeon Tileset (#10)")
    FIXED_ROOM = 11, _("Use Fixed Room (#11)")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, name_localized: str | None):
        self.name_localized: str = name_localized  # type: ignore

    def __str__(self) -> str:
        return f"Pmd2ScriptLevelMapType.{self.name}"

    def __repr__(self) -> str:
        return str(self)


class Pmd2ScriptLevel(AutoString):
    def __init__(self, id: int, mapid: u16, name: str, mapty: u16, nameid: u16, weather: i16):
        self.id = id
        self.mapid = mapid
        self.name = name
        self.mapty = mapty
        self.nameid = nameid
        self.weather = weather

    @property
    def mapty_enum(self) -> Pmd2ScriptLevelMapType:
        return Pmd2ScriptLevelMapType(self.mapty)  # type: ignore

    # Backwards compat:
    @property
    def unk2(self) -> u16:
        return self.nameid

    @unk2.setter
    def unk2(self, value: u16) -> None:
        self.nameid = value

    @property
    def unk4(self) -> i16:
        return self.weather

    @unk4.setter
    def unk4(self, value: i16) -> None:
        self.weather = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pmd2ScriptLevel):
            return False
        return (
            self.id == other.id
            and self.mapid == other.mapid
            and self.name == other.name
            and self.mapty == other.mapty
            and self.nameid == other.nameid
            and self.weather == other.weather
        )


class Pmd2ScriptEntity(AutoString):
    """aka. Actor"""

    def __init__(self, id: u16, entid: u16, name: str, type: u16, unk3: u16, unk4: u16):
        self.id = id
        self.entid = entid
        self.name = name
        self.type = type
        self.unk3 = unk3
        self.unk4 = unk4

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pmd2ScriptEntity):
            return False
        return (
            self.id == other.id
            and self.entid == other.entid
            and self.name == other.name
            and self.type == other.type
            and self.unk3 == other.unk3
            and self.unk4 == other.unk4
        )


class Pmd2ScriptOpCodeArgument(AutoString):
    def __init__(self, id: int, type: str, name: str):
        self.id = id
        self.type = type
        self.name = name


class Pmd2ScriptOpCodeRepeatingArgumentGroup(AutoString):
    def __init__(self, id: int, arguments: list[Pmd2ScriptOpCodeArgument]):
        self.id = id
        self.arguments = arguments

    def __getitem__(self, item: int) -> Pmd2ScriptOpCodeArgument:
        return self.arguments[item]


class Pmd2ScriptOpCode(SsbOpCode):
    def __init__(
        self,
        id: int,
        name: str,
        params: int,
        stringidx: int,
        unk2: int,
        unk3: int,
        arguments: list[Pmd2ScriptOpCodeArgument],
        repeating_argument_group: Pmd2ScriptOpCodeRepeatingArgumentGroup | None,
    ):
        super().__init__(id, name)
        self.params = params
        self.stringidx = stringidx
        self.unk2 = unk2
        self.unk3 = unk3
        self.arguments: list[Pmd2ScriptOpCodeArgument] = arguments
        self.arguments__by_id: dict[int, Pmd2ScriptOpCodeArgument] = {o.id: o for o in self.arguments}
        self.repeating_argument_group: None | (Pmd2ScriptOpCodeRepeatingArgumentGroup) = repeating_argument_group
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
    def __init__(self, ssa_id: int, name: str, ssb_id: int | None = None):
        self.ssa_id = ssa_id
        self.ssb_id = ssb_id if ssb_id is not None else ssa_id - 1
        self.name = name

    @property
    def id(self) -> int:
        """
        For backwards compatibility.
        """
        warnings.warn(
            DeprecatedToBeRemovedWarning("Please use self.ssa_id instead.", (2, 0, 0)),
            stacklevel=2,
        )
        return self.ssa_id

    @property
    def print_name(self) -> str:
        if self.ssa_id == 1:
            return _("Down")  # TRANSLATORS: Direction
        elif self.ssa_id == 2:
            return _("Down Right")  # TRANSLATORS: Direction
        elif self.ssa_id == 3:
            return _("Right")  # TRANSLATORS: Direction
        elif self.ssa_id == 4:
            return _("Up Right")  # TRANSLATORS: Direction
        elif self.ssa_id == 5:
            return _("Up")  # TRANSLATORS: Direction
        elif self.ssa_id == 6:
            return _("Up Left")  # TRANSLATORS: Direction
        elif self.ssa_id == 7:
            return _("Left")  # TRANSLATORS: Direction
        elif self.ssa_id == 8:
            return _("Down Left")  # TRANSLATORS: Direction
        return self.name


class Pmd2ScriptDirectionSsb(AutoString):
    """
    Same as `Pmd2ScriptDirection`, but the `id` matches the SSB constant
    """

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


ScriptDataConstant = Union[
    Pmd2ScriptEntity,
    Pmd2ScriptObject,
    Pmd2ScriptRoutine,
    Pmd2ScriptFaceName,
    Pmd2ScriptFacePositionMode,
    Pmd2ScriptGameVar,
    Pmd2ScriptLevel,
    Pmd2ScriptMenu,
    Pmd2ScriptSpecial,
    Pmd2ScriptDirection,
    Pmd2ScriptDirectionSsb,
    Pmd2ScriptBgm,
    Pmd2ScriptSpriteEffect,
]

PREFIX_DIRECTION = "DIR_"
PREFIX_PROCESS_SPECIAL = "PROCESS_SPECIAL_"
PREFIX_MENU = "MENU_"
PREFIX_LEVEL = "LEVEL_"
PREFIX_FACE_POS = "FACE_POS_"
PREFIX_FACE = "FACE_"
PREFIX_OBJECT = "OBJECT_"
PREFIX_ACTOR = "ACTOR_"
PREFIX_EFFECT = "EFFECT_"
PREFIX_CORO = "CORO_"
PREFIX_BGM = "BGM_"
PREFIX_VAR = "$"
PREFIX_DMODE = "DMODE_"

CAMEL_REGEX = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_screaming_snake_case(string) -> str:
    return CAMEL_REGEX.sub("_", string).upper()


class _ScriptDataStorage(AutoString):
    def __init__(
        self,
        game_variables_table: list[Pmd2ScriptGameVar],
        objects_list: list[Pmd2ScriptObject],
        face_names: list[Pmd2ScriptFaceName],
        face_position_modes: list[Pmd2ScriptFacePositionMode],
        directions: dict[int, Pmd2ScriptDirection],
        common_routine_info: list[Pmd2ScriptRoutine],
        menu_ids: list[Pmd2ScriptMenu],
        process_special_ids: list[Pmd2ScriptSpecial],
        sprite_effect_ids: list[Pmd2ScriptSpriteEffect],
        bgms: list[Pmd2ScriptBgm],
        level_list: list[Pmd2ScriptLevel],
        level_entity_table: list[Pmd2ScriptEntity],
        op_codes: list[Pmd2ScriptOpCode],
        ground_state_structs: dict[str, Pmd2ScriptGroundStateStruct],
    ):
        self.game_variables = game_variables_table
        self.objects = objects_list
        self.face_names = face_names
        self.face_position_modes = face_position_modes
        self.directions = directions
        self.common_routine_info = common_routine_info
        self.menus = menu_ids
        self.process_specials = process_special_ids
        self.sprite_effects = sprite_effect_ids
        self.bgms = bgms
        self.level_list = level_list
        self.level_entities = level_entity_table
        self.op_codes = op_codes
        self.ground_state_structs = ground_state_structs

        self.rebuild_constant_lookup()

    def rebuild_constant_lookup(self) -> None:
        """
        Must be called after modifying any constants.
        """
        self._all_script_constants__by_name: dict[str, ScriptDataConstant] = {}
        self._insert_constants_with_prefix(self._game_variables, PREFIX_VAR)
        for obj_var in self._objects:
            self._all_script_constants__by_name[PREFIX_OBJECT + obj_var.unique_name.upper()] = obj_var
        for face_var in self._face_names:
            self._all_script_constants__by_name[PREFIX_FACE + face_var.name.replace("-", "_")] = face_var
        self._insert_constants_with_prefix(self._face_position_modes, PREFIX_FACE_POS)
        self._insert_constants_with_prefix(list(self._directions_ssb.values()), PREFIX_DIRECTION)
        self._insert_constants_with_prefix(self._common_routine_info, PREFIX_CORO)
        self._insert_constants_with_prefix_convert_camel(self._menus, PREFIX_MENU)
        self._insert_constants_with_prefix_convert_camel(self._process_specials, PREFIX_PROCESS_SPECIAL)
        self._insert_constants_with_prefix_convert_camel(self._sprite_effects, PREFIX_EFFECT)
        self._insert_constants_with_prefix_convert_camel(self._bgms, PREFIX_BGM)
        self._insert_constants_with_prefix(self._level_list, PREFIX_LEVEL)
        self._insert_constants_with_prefix(self._level_entities, PREFIX_ACTOR)

    def _insert_constants_with_prefix(self, vars: Sequence[ScriptDataConstant], prefix: str) -> None:
        for var in vars:
            self._all_script_constants__by_name[prefix + var.name.upper()] = var

    def _insert_constants_with_prefix_convert_camel(self, vars: Sequence[ScriptDataConstant], prefix: str) -> None:
        for var in vars:
            self._all_script_constants__by_name[prefix + camel_to_screaming_snake_case(var.name)] = var

    @property
    def game_variables(self) -> list[Pmd2ScriptGameVar]:
        return self._game_variables

    @game_variables.setter
    def game_variables(self, value: list[Pmd2ScriptGameVar]) -> None:
        self._game_variables = value
        self._game_variables__by_id = {var.id: var for var in self._game_variables}
        self._game_variables__by_name = {var.name: var for var in self._game_variables}

    @property
    def game_variables__by_id(self) -> Mapping[int, Pmd2ScriptGameVar]:
        return self._game_variables__by_id

    @property
    def game_variables__by_name(self) -> Mapping[str, Pmd2ScriptGameVar]:
        return self._game_variables__by_name

    @property
    def objects(self) -> list[Pmd2ScriptObject]:
        return self._objects

    @objects.setter
    def objects(self, value: list[Pmd2ScriptObject]) -> None:
        self._objects = value
        self._objects__by_id = {o.id: o for o in self._objects}
        self._objects__by_unique_name = {o.unique_name: o for o in self._objects}

    @property
    def objects__by_id(self) -> Mapping[u16, Pmd2ScriptObject]:
        return self._objects__by_id

    @property
    def objects__by_unique_name(self) -> Mapping[str, Pmd2ScriptObject]:
        return self._objects__by_unique_name

    @property
    def face_names(self) -> list[Pmd2ScriptFaceName]:
        return self._face_names

    @face_names.setter
    def face_names(self, value: list[Pmd2ScriptFaceName]) -> None:
        self._face_names = value
        self._face_names__by_id = {n.id: n for n in self._face_names}
        self._face_names__by_name = {n.name: n for n in self._face_names}

    @property
    def face_names__by_id(self) -> Mapping[int, Pmd2ScriptFaceName]:
        return self._face_names__by_id

    @property
    def face_names__by_name(self) -> Mapping[str, Pmd2ScriptFaceName]:
        return self._face_names__by_name

    @property
    def face_position_modes(self) -> list[Pmd2ScriptFacePositionMode]:
        return self._face_position_modes

    @face_position_modes.setter
    def face_position_modes(self, value: list[Pmd2ScriptFacePositionMode]) -> None:
        self._face_position_modes = value
        self._face_position_modes__by_id = {n.id: n for n in self._face_position_modes}
        self._face_position_modes__by_name = {n.name: n for n in self._face_position_modes}

    @property
    def face_position_modes__by_id(self) -> Mapping[int, Pmd2ScriptFacePositionMode]:
        return self._face_position_modes__by_id

    @property
    def face_position_modes__by_name(self) -> Mapping[str, Pmd2ScriptFacePositionMode]:
        return self._face_position_modes__by_name

    @property
    def directions(self) -> dict[int, Pmd2ScriptDirection]:
        return self._directions

    @directions.setter
    def directions(self, value: dict[int, Pmd2ScriptDirection]) -> None:
        self._directions = value
        self._directions__by_ssb_id = {d.ssb_id: d for d in self._directions.values()}
        self._directions__by_name = {b.name: b for b in self.directions.values()}
        self._directions_ssb = {d.ssb_id: Pmd2ScriptDirectionSsb(d.ssb_id, d.name) for d in self._directions.values()}

    @property
    def directions__by_ssa_id(self) -> Mapping[int, Pmd2ScriptDirection]:
        return self.directions

    @property
    def directions__by_ssb_id(self) -> Mapping[int, Pmd2ScriptDirection]:
        return self._directions__by_ssb_id

    @property
    def directions__by_name(self) -> Mapping[str, Pmd2ScriptDirection]:
        return self._directions__by_name

    @property
    def common_routine_info(self) -> list[Pmd2ScriptRoutine]:
        return self._common_routine_info

    @common_routine_info.setter
    def common_routine_info(self, value: list[Pmd2ScriptRoutine]) -> None:
        self._common_routine_info = value
        self._common_routine_info__by_id = {o.id: o for o in self.common_routine_info}
        self._common_routine_info__by_name = {o.name: o for o in self.common_routine_info}

    @property
    def common_routine_info__by_id(self) -> dict[int, Pmd2ScriptRoutine]:
        return self._common_routine_info__by_id

    @property
    def common_routine_info__by_name(self) -> dict[str, Pmd2ScriptRoutine]:
        return self._common_routine_info__by_name

    @property
    def menus(self) -> list[Pmd2ScriptMenu]:
        return self._menus

    @menus.setter
    def menus(self, value: list[Pmd2ScriptMenu]) -> None:
        self._menus = value
        self._menus__by_id = {o.id: o for o in self.menus}
        self._menus__by_name = {o.name: o for o in self.menus}

    @property
    def menus__by_id(self) -> Mapping[int, Pmd2ScriptMenu]:
        return self._menus__by_id

    @property
    def menus__by_name(self) -> Mapping[str, Pmd2ScriptMenu]:
        return self._menus__by_name

    @property
    def process_specials(self) -> list[Pmd2ScriptSpecial]:
        return self._process_specials

    @process_specials.setter
    def process_specials(self, value: list[Pmd2ScriptSpecial]) -> None:
        self._process_specials = value
        self._process_specials__by_id = {o.id: o for o in self.process_specials}
        self._process_specials__by_name = {o.name: o for o in self.process_specials}

    @property
    def process_specials__by_id(self) -> Mapping[int, Pmd2ScriptSpecial]:
        return self._process_specials__by_id

    @property
    def process_specials__by_name(self) -> Mapping[str, Pmd2ScriptSpecial]:
        return self._process_specials__by_name

    @property
    def sprite_effects(self) -> list[Pmd2ScriptSpriteEffect]:
        return self._sprite_effects

    @sprite_effects.setter
    def sprite_effects(self, value: list[Pmd2ScriptSpriteEffect]) -> None:
        self._sprite_effects = value
        self._sprite_effects__by_id = {o.id: o for o in self.sprite_effects}
        self._sprite_effects__by_name = {o.name: o for o in self.sprite_effects}

    @property
    def sprite_effects__by_id(self) -> Mapping[int, Pmd2ScriptSpriteEffect]:
        return self._sprite_effects__by_id

    @property
    def sprite_effects__by_name(self) -> Mapping[str, Pmd2ScriptSpriteEffect]:
        return self._sprite_effects__by_name

    @property
    def bgms(self) -> list[Pmd2ScriptBgm]:
        return self._bgms

    @bgms.setter
    def bgms(self, value: list[Pmd2ScriptBgm]) -> None:
        self._bgms = value
        self._bgms__by_id = {o.id: o for o in self.bgms}
        self._bgms__by_name = {o.name: o for o in self.bgms}

    @property
    def bgms__by_id(self) -> Mapping[int, Pmd2ScriptBgm]:
        return self._bgms__by_id

    @property
    def bgms__by_name(self) -> Mapping[str, Pmd2ScriptBgm]:
        return self._bgms__by_name

    @property
    def level_list(self) -> list[Pmd2ScriptLevel]:
        return self._level_list

    @level_list.setter
    def level_list(self, value: list[Pmd2ScriptLevel]) -> None:
        self._level_list = value
        self._level_list__by_id = {o.id: o for o in self.level_list}
        self._level_list__by_name = {o.name: o for o in self.level_list}

    @property
    def level_list__by_id(self) -> Mapping[int, Pmd2ScriptLevel]:
        return self._level_list__by_id

    @property
    def level_list__by_name(self) -> Mapping[str, Pmd2ScriptLevel]:
        return self._level_list__by_name

    @property
    def level_entities(self) -> list[Pmd2ScriptEntity]:
        return self._level_entities

    @level_entities.setter
    def level_entities(self, value: list[Pmd2ScriptEntity]) -> None:
        self._level_entities = value
        self._level_entities__by_id = {o.id: o for o in self.level_entities}
        self._level_entities__by_name = {o.name: o for o in self.level_entities}

    @property
    def level_entities__by_id(self) -> Mapping[u16, Pmd2ScriptEntity]:
        return self._level_entities__by_id

    @property
    def level_entities__by_name(self) -> Mapping[str, Pmd2ScriptEntity]:
        return self._level_entities__by_name

    @property
    def op_codes(self) -> Sequence[Pmd2ScriptOpCode]:
        return list(self._op_codes_by_id.values())

    @op_codes.setter
    def op_codes(self, value: Sequence[Pmd2ScriptOpCode]) -> None:
        self._op_codes_by_id: dict[int, Pmd2ScriptOpCode] = {o.id: o for o in value}
        self._op_codes_by_name: dict[str, list[Pmd2ScriptOpCode]] = {}
        for o in value:
            if o.name not in self._op_codes_by_name:
                self._op_codes_by_name[o.name] = []
            self._op_codes_by_name[o.name].append(o)

    @property
    def op_codes__by_id(self) -> Mapping[int, Pmd2ScriptOpCode]:
        return self._op_codes_by_id

    @property
    def op_codes__by_name(self) -> Mapping[str, list[Pmd2ScriptOpCode]]:
        return self._op_codes_by_name

    @property
    def ground_state_structs(self) -> dict[str, Pmd2ScriptGroundStateStruct]:
        return self._ground_state_structs

    @ground_state_structs.setter
    def ground_state_structs(self, value: dict[str, Pmd2ScriptGroundStateStruct]) -> None:
        self._ground_state_structs = value

    @property
    def all_script_constants__by_name(self) -> Mapping[str, ScriptDataConstant]:
        return self._all_script_constants__by_name


class Pmd2ScriptData(AutoString):
    def __init__(
        self,
        game_variables_table: list[Pmd2ScriptGameVar],
        objects_list: list[Pmd2ScriptObject],
        face_names: list[Pmd2ScriptFaceName],
        face_position_modes: list[Pmd2ScriptFacePositionMode],
        directions: dict[int, Pmd2ScriptDirection],
        common_routine_info: list[Pmd2ScriptRoutine],
        menu_ids: list[Pmd2ScriptMenu],
        process_special_ids: list[Pmd2ScriptSpecial],
        sprite_effect_ids: list[Pmd2ScriptSpriteEffect],
        bgms: list[Pmd2ScriptBgm],
        level_list: list[Pmd2ScriptLevel],
        level_entity_table: list[Pmd2ScriptEntity],
        op_codes: list[Pmd2ScriptOpCode],
        ground_state_structs: dict[str, Pmd2ScriptGroundStateStruct],
    ):
        self._storage = _ScriptDataStorage(
            game_variables_table,
            objects_list,
            face_names,
            face_position_modes,
            directions,
            common_routine_info,
            menu_ids,
            process_special_ids,
            sprite_effect_ids,
            bgms,
            level_list,
            level_entity_table,
            op_codes,
            ground_state_structs,
        )

    @contextmanager
    def modify(self) -> Iterator[_ScriptDataStorage]:
        yield self._storage
        self._storage.rebuild_constant_lookup()

    @property
    def game_variables(self) -> list[Pmd2ScriptGameVar]:
        return self._storage._game_variables

    @game_variables.setter
    def game_variables(self, value: list[Pmd2ScriptGameVar]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.game_variables = value

    @property
    def game_variables__by_id(self) -> Mapping[int, Pmd2ScriptGameVar]:
        return self._storage._game_variables__by_id

    @property
    def game_variables__by_name(self) -> Mapping[str, Pmd2ScriptGameVar]:
        return self._storage._game_variables__by_name

    @property
    def objects(self) -> list[Pmd2ScriptObject]:
        return self._storage._objects

    @objects.setter
    def objects(self, value: list[Pmd2ScriptObject]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.objects = value

    @property
    def objects__by_id(self) -> Mapping[u16, Pmd2ScriptObject]:
        return self._storage._objects__by_id

    @property
    def objects__by_unique_name(self) -> Mapping[str, Pmd2ScriptObject]:
        return self._storage._objects__by_unique_name

    @property
    def face_names(self) -> list[Pmd2ScriptFaceName]:
        return self._storage._face_names

    @face_names.setter
    def face_names(self, value: list[Pmd2ScriptFaceName]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.face_names = value

    @property
    def face_names__by_id(self) -> Mapping[int, Pmd2ScriptFaceName]:
        return self._storage._face_names__by_id

    @property
    def face_names__by_name(self) -> Mapping[str, Pmd2ScriptFaceName]:
        return self._storage._face_names__by_name

    @property
    def face_position_modes(self) -> list[Pmd2ScriptFacePositionMode]:
        return self._storage._face_position_modes

    @face_position_modes.setter
    def face_position_modes(self, value: list[Pmd2ScriptFacePositionMode]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.face_position_modes = value

    @property
    def face_position_modes__by_id(self) -> Mapping[int, Pmd2ScriptFacePositionMode]:
        return self._storage._face_position_modes__by_id

    @property
    def face_position_modes__by_name(self) -> Mapping[str, Pmd2ScriptFacePositionMode]:
        return self._storage._face_position_modes__by_name

    @property
    def directions(self) -> dict[int, Pmd2ScriptDirection]:
        return self._storage._directions

    @directions.setter
    def directions(self, value: dict[int, Pmd2ScriptDirection]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.directions = value

    @property
    def directions__by_ssa_id(self) -> Mapping[int, Pmd2ScriptDirection]:
        return self._storage._directions

    @property
    def directions__by_ssb_id(self) -> Mapping[int, Pmd2ScriptDirection]:
        return self._storage._directions__by_ssb_id

    @property
    def directions__by_name(self) -> Mapping[str, Pmd2ScriptDirection]:
        return self._storage._directions__by_name

    @property
    def common_routine_info(self) -> list[Pmd2ScriptRoutine]:
        return self._storage._common_routine_info

    @common_routine_info.setter
    def common_routine_info(self, value: list[Pmd2ScriptRoutine]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.common_routine_info = value

    @property
    def common_routine_info__by_id(self) -> dict[int, Pmd2ScriptRoutine]:
        return self._storage._common_routine_info__by_id

    @property
    def common_routine_info__by_name(self) -> dict[str, Pmd2ScriptRoutine]:
        return self._storage._common_routine_info__by_name

    @property
    def menus(self) -> list[Pmd2ScriptMenu]:
        return self._storage._menus

    @menus.setter
    def menus(self, value: list[Pmd2ScriptMenu]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.menus = value

    @property
    def menus__by_id(self) -> Mapping[int, Pmd2ScriptMenu]:
        return self._storage._menus__by_id

    @property
    def menus__by_name(self) -> Mapping[str, Pmd2ScriptMenu]:
        return self._storage._menus__by_name

    @property
    def process_specials(self) -> list[Pmd2ScriptSpecial]:
        return self._storage._process_specials

    @process_specials.setter
    def process_specials(self, value: list[Pmd2ScriptSpecial]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.process_specials = value

    @property
    def process_specials__by_id(self) -> Mapping[int, Pmd2ScriptSpecial]:
        return self._storage._process_specials__by_id

    @property
    def process_specials__by_name(self) -> Mapping[str, Pmd2ScriptSpecial]:
        return self._storage._process_specials__by_name

    @property
    def sprite_effects(self) -> list[Pmd2ScriptSpriteEffect]:
        return self._storage._sprite_effects

    @sprite_effects.setter
    def sprite_effects(self, value: list[Pmd2ScriptSpriteEffect]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.sprite_effects = value

    @property
    def sprite_effects__by_id(self) -> Mapping[int, Pmd2ScriptSpriteEffect]:
        return self._storage._sprite_effects__by_id

    @property
    def sprite_effects__by_name(self) -> Mapping[str, Pmd2ScriptSpriteEffect]:
        return self._storage._sprite_effects__by_name

    @property
    def bgms(self) -> list[Pmd2ScriptBgm]:
        return self._storage._bgms

    @bgms.setter
    def bgms(self, value: list[Pmd2ScriptBgm]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.bgms = value

    @property
    def bgms__by_id(self) -> Mapping[int, Pmd2ScriptBgm]:
        return self._storage._bgms__by_id

    @property
    def bgms__by_name(self) -> Mapping[str, Pmd2ScriptBgm]:
        return self._storage._bgms__by_name

    @property
    def level_list(self) -> list[Pmd2ScriptLevel]:
        return self._storage._level_list

    @level_list.setter
    def level_list(self, value: list[Pmd2ScriptLevel]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.level_list = value

    @property
    def level_list__by_id(self) -> Mapping[int, Pmd2ScriptLevel]:
        return self._storage._level_list__by_id

    @property
    def level_list__by_name(self) -> Mapping[str, Pmd2ScriptLevel]:
        return self._storage._level_list__by_name

    @property
    def level_entities(self) -> list[Pmd2ScriptEntity]:
        return self._storage._level_entities

    @level_entities.setter
    def level_entities(self, value: list[Pmd2ScriptEntity]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.level_entities = value

    @property
    def level_entities__by_id(self) -> Mapping[u16, Pmd2ScriptEntity]:
        return self._storage._level_entities__by_id

    @property
    def level_entities__by_name(self) -> Mapping[str, Pmd2ScriptEntity]:
        return self._storage._level_entities__by_name

    @property
    def op_codes(self) -> Sequence[Pmd2ScriptOpCode]:
        return self._storage.op_codes

    @op_codes.setter
    def op_codes(self, value: Sequence[Pmd2ScriptOpCode]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.op_codes = value

    @property
    def op_codes__by_id(self) -> Mapping[int, Pmd2ScriptOpCode]:
        return self._storage._op_codes_by_id

    @property
    def op_codes__by_name(self) -> Mapping[str, list[Pmd2ScriptOpCode]]:
        return self._storage._op_codes_by_name

    @property
    def ground_state_structs(self) -> dict[str, Pmd2ScriptGroundStateStruct]:
        return self._storage._ground_state_structs

    @ground_state_structs.setter
    def ground_state_structs(self, value: dict[str, Pmd2ScriptGroundStateStruct]) -> None:
        warnings.warn(
            DeprecatedToBeRemovedWarning("Script data should be modified via the `modify` context manager", (2, 0, 0)),
            stacklevel=2,
        )
        with self.modify() as storage:
            storage.ground_state_structs = value

    @property
    def all_script_constants__by_name(self) -> Mapping[str, ScriptDataConstant]:
        return self._storage._all_script_constants__by_name
