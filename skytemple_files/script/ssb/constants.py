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
from __future__ import annotations

from enum import Enum
from typing import TypeVar, Union
from collections.abc import Iterable

from explorerscript.ssb_converting.ssb_data_types import (
    DungeonModeConstants,
    SsbOpParamConstant,
)

from skytemple_files.common.i18n_util import _, f
from skytemple_files.common.ppmdu_config.script_data import (
    Pmd2ScriptBgm,
    Pmd2ScriptFacePositionMode,
    Pmd2ScriptMenu,
    Pmd2ScriptLevel,
    Pmd2ScriptObject,
    Pmd2ScriptDirection,
    Pmd2ScriptGameVar,
    Pmd2ScriptRoutine,
    Pmd2ScriptSpriteEffect,
    Pmd2ScriptSpecial,
    Pmd2ScriptFaceName,
    Pmd2ScriptData,
    Pmd2ScriptEntity,
    ScriptDataConstant,
    camel_to_screaming_snake_case,
    PREFIX_DIRECTION,
    PREFIX_PROCESS_SPECIAL,
    PREFIX_MENU,
    PREFIX_LEVEL,
    PREFIX_FACE_POS,
    PREFIX_FACE,
    PREFIX_OBJECT,
    PREFIX_ACTOR,
    PREFIX_EFFECT,
    PREFIX_CORO,
    PREFIX_BGM,
    PREFIX_VAR,
    PREFIX_DMODE,
)
from skytemple_files.user_error import UserValueError

# Mappings for renamed constants, for backwards compatibility
CONSTANT_ALIASES = {
    "MENU_DUNGEON_RESULT": "MENU_DUNGEON_INITIALIZE_TEAM",
    # Bug in SkyTemple 0.0.4, where the direction IDs were mapped against the SSA ids.
    "DIRECTION_DOWN": "DIR_DOWNRIGHT",
    "DIRECTION_DOWNRIGHT": "DIR_RIGHT",
    "DIRECTION_RIGHT": "DIR_UPRIGHT",
    "DIRECTION_UPRIGHT": "DIR_UP",
    "DIRECTION_UP": "DIR_UPLEFT",
    "DIRECTION_UPLEFT": "DIR_LEFT",
    "DIRECTION_LEFT": "DIR_DOWNLEFT",
}


class DungeonMode(Enum):
    CLOSED = 0
    OPEN = 1
    REQUEST = 2
    OPEN_AND_REQUEST = 3

    @property
    def id(self):
        # Compatibility with SsbNamedId
        return self.value

    @classmethod
    def create_for(cls, string):
        if string == "CLOSED":
            return cls.CLOSED
        if string == "OPEN":
            return cls.OPEN
        if string == "REQUEST":
            return cls.REQUEST
        if string == "OPEN_AND_REQUEST":
            return cls.OPEN_AND_REQUEST
        raise UserValueError(f(_("Invalid DungeonMode: {string}")))


SsbConstantPmdScriptMappable = Union[
    ScriptDataConstant,
    DungeonMode,
]
T = TypeVar("T")


class SsbConstant(SsbOpParamConstant):
    """
    Class to map entries from the PPMDU script config (and other sources)
    to constants for use in ssb representations.

    Pmd2Script* objects can be converted into this by using create_for.

    The representation as a string can be retrieved using str(self) or repr(self).

    The constructor can be used with any string that this class represents,
    (and an instance of Pmd2ScriptData) and be converted back with convert_to_script_entity.
    Giving it an unknown constant_as_string value will raise a ValueError.
    """

    def __init__(
        self,
        constant_as_string: str,
        script_data: Pmd2ScriptData | None = None,
        value: SsbConstantPmdScriptMappable | None = None,
    ):
        """Either script_data or the value argument must be present."""
        super().__init__(constant_as_string)

        # Init value if not set
        if not value:
            if not script_data:
                raise ValueError("Either value or script_data must be provided.")
            value = self._map_back(constant_as_string, script_data)

        self.value = value
        self.name = constant_as_string

    @classmethod
    def create_for(cls, value: SsbConstantPmdScriptMappable) -> SsbConstant:
        if isinstance(value, Pmd2ScriptEntity):
            return cls(PREFIX_ACTOR + value.name, value=value)
        elif isinstance(value, Pmd2ScriptObject):
            return cls(PREFIX_OBJECT + value.unique_name.upper(), value=value)
        elif isinstance(value, Pmd2ScriptRoutine):
            return cls(PREFIX_CORO + value.name, value=value)
        elif isinstance(value, Pmd2ScriptFaceName):
            return cls(PREFIX_FACE + value.name.replace("-", "_"), value=value)
        elif isinstance(value, Pmd2ScriptFacePositionMode):
            return cls(PREFIX_FACE_POS + value.name.upper(), value=value)
        elif isinstance(value, Pmd2ScriptGameVar):
            return cls(PREFIX_VAR + value.name, value=value)
        elif isinstance(value, Pmd2ScriptLevel):
            return cls(PREFIX_LEVEL + value.name, value=value)
        elif isinstance(value, Pmd2ScriptMenu):
            return cls(PREFIX_MENU + camel_to_screaming_snake_case(value.name), value=value)
        elif isinstance(value, Pmd2ScriptSpecial):
            return cls(PREFIX_PROCESS_SPECIAL + camel_to_screaming_snake_case(value.name), value=value)
        elif isinstance(value, Pmd2ScriptBgm):
            return cls(PREFIX_BGM + camel_to_screaming_snake_case(value.name), value=value)
        elif isinstance(value, Pmd2ScriptSpriteEffect):
            return cls(PREFIX_EFFECT + camel_to_screaming_snake_case(value.name), value=value)
        elif isinstance(value, Pmd2ScriptDirection):
            return cls(PREFIX_DIRECTION + value.name.upper(), value=value)
        elif isinstance(value, DungeonMode):
            return cls(PREFIX_DMODE + value.name, value=value)
        raise TypeError("value must be of type SsbConstantPmdScriptMappable.")

    @classmethod
    def _map_back(cls, constant_as_string: str, script_data: Pmd2ScriptData) -> SsbConstantPmdScriptMappable:
        """Inverse of create_for."""
        # Backwards compatibility
        if constant_as_string in CONSTANT_ALIASES:
            constant_as_string = CONSTANT_ALIASES[constant_as_string]

        try:
            return script_data.all_script_constants__by_name[constant_as_string]
        except KeyError:
            pass

        if constant_as_string.startswith(PREFIX_DMODE):
            try:
                return DungeonMode.create_for(constant_as_string[len(PREFIX_DMODE) :])
            except KeyError:
                pass

        raise UserValueError(f(_("Unknown constant {constant_as_string}.")))

    @staticmethod
    def _cvrt_camel_inverse(string) -> str:
        return "".join(word.title() for word in string.split("_"))

    def convert_to_script_entity(self):
        return self.value

    def __repr__(self):
        return str(self)

    @classmethod
    def collect_all(cls, rom_data: Pmd2ScriptData) -> Iterable[SsbConstant]:
        """Collects all possible constants from the given ROM data"""
        for a in rom_data.level_entities:
            yield cls.create_for(a)
        for b in rom_data.objects:
            yield cls.create_for(b)
        for c in rom_data.common_routine_info:
            yield cls.create_for(c)
        for d in rom_data.face_names:
            yield cls.create_for(d)
        for e in rom_data.face_position_modes:
            yield cls.create_for(e)
        for ff in rom_data.game_variables:
            yield cls.create_for(ff)
        for g in rom_data.level_list:
            yield cls.create_for(g)
        for h in rom_data.menus:
            yield cls.create_for(h)
        for i in rom_data.process_specials:
            yield cls.create_for(i)
        for j in rom_data.bgms:
            yield cls.create_for(j)
        for k in rom_data.sprite_effects:
            yield cls.create_for(k)
        for ll in rom_data.directions.values():
            yield cls.create_for(ll)
        for m in [
            DungeonMode.CLOSED,
            DungeonMode.OPEN,
            DungeonMode.REQUEST,
            DungeonMode.OPEN_AND_REQUEST,
        ]:
            yield cls.create_for(m)

    @classmethod
    def get_dungeon_mode_constants(cls):
        return DungeonModeConstants(
            PREFIX_DMODE + DungeonMode.CLOSED.name,
            PREFIX_DMODE + DungeonMode.OPEN.name,
            PREFIX_DMODE + DungeonMode.REQUEST.name,
            PREFIX_DMODE + DungeonMode.OPEN_AND_REQUEST.name,
        )
