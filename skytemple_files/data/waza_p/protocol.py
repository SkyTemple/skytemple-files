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

from abc import abstractmethod
from enum import Enum
from typing import MutableSequence, Protocol, TypeVar, Sequence

from range_typed_integers import u8, u16, u32

from skytemple_files.common.i18n_util import _
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable


_WazaMoveCategory = u8
_PokeType = u8


class WazaMoveCategory(Enum):
    PHYSICAL = 0, _("Physical Move")
    SPECIAL = 1, _("Special Move")
    STATUS = 2, _("Status Move")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, name_localized: str):
        self.name_localized = name_localized

    def __str__(self):
        return f"WazaMoveCategory.{self.name}"

    def __repr__(self):
        return str(self)

    @property
    def print_name(self):
        return self.name_localized


class WazaMoveRangeTarget(Enum):
    ENEMIES = 0, _("Enemies")
    ALLIES = 1, _("Allies")
    EVERYONE = 2, _("Everyone")
    USER = 3, _("User")
    TWO_TURN = 4, _("Two-turn move")
    EVERYONE_EXCEPT_USER = 5, _("Everyone except user")
    ALLIES_EXCEPT_USER = 6, _("All allies except user")
    U7 = 7, _("Invalid ") + "7"
    U8 = 8, _("Invalid ") + "8"
    U9 = 9, _("Invalid ") + "9"
    U10 = 10, _("Invalid ") + "10"
    U11 = 11, _("Invalid ") + "11"
    U12 = 12, _("Invalid ") + "12"
    U13 = 13, _("Invalid ") + "13"
    U14 = 14, _("Invalid ") + "14"
    SPECIAL = 15, _("Special / Invalid")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, name_localized: str):
        self.name_localized = name_localized

    def __str__(self):
        return f"WazaMoveRangeTarget.{self.name}"

    def __repr__(self):
        return str(self)

    @property
    def print_name(self):
        return self.name_localized


class WazaMoveRangeRange(Enum):
    IN_FRONT = 0, _("In front")
    TRHEE_IN_FRONT = 1, _("In front + adjacent (like Wide Slash)")
    AROUND = 2, _("8 tiles around user")
    ROOM = 3, _("Room")
    TWO_TILES = 4, _(
        "Two tiles away"
    )  # Also cuts corners, but the AI doesn't account for that
    STRAIGHT_LINE = 5, _("Straight line")
    FLOOR = 6, _("Floor")
    USER = 7, _("User")
    IN_FRONT_CORNERS = 8, _("In front; cuts corners")
    TWO_TILES_CORNERS = 9, _("Two tiles away; cuts corners")
    U10 = 10, _("Invalid ") + "10"
    U11 = 11, _("Invalid ") + "11"
    U12 = 12, _("Invalid ") + "12"
    U13 = 13, _("Invalid ") + "13"
    U14 = 14, _("Invalid ") + "14"
    SPECIAL = 15, _("Special / Invalid")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, name_localized: str):
        self.name_localized = name_localized

    def __str__(self):
        return f"WazaMoveRangeRange.{self.name}"

    def __repr__(self):
        return str(self)

    @property
    def print_name(self):
        return self.name_localized


class WazaMoveRangeCondition(Enum):
    """Only relevant for AI setting."""

    NO_CONDITION = 0, _("No condition")
    CHANCE_AI_WEIGHT = 1, _("Based on AI Condition 1 Chance")
    CRITICAL_HP = 2, _("Current HP <= 25%")
    NEGATIVE_STATUS = 3, _("Has at least one negative status condition")
    ASLEEP = 4, _("Is asleep, in a nightmare or napping")
    GHOST = 5, _("Is a ghost-type Pokémon and does not have the exposed status")
    CRITICAL_HP_NEGATIVE_STATUS = 6, _(
        "Current HP <= 25% or has at least one negative status condition"
    )
    U7 = 7, _("Invalid ") + "7"
    U8 = 8, _("Invalid ") + "8"
    U9 = 9, _("Invalid ") + "9"
    U10 = 10, _("Invalid ") + "10"
    U11 = 11, _("Invalid ") + "11"
    U12 = 12, _("Invalid ") + "12"
    U13 = 13, _("Invalid ") + "13"
    U14 = 14, _("Invalid ") + "14"
    U15 = 15, _("Invalid ") + "15"

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, name_localized: str):
        self.name_localized = name_localized

    def __str__(self):
        return f"WazaMoveRangeCondition.{self.name}"

    def __repr__(self):
        return str(self)

    @property
    def print_name(self):
        return self.name_localized


class LevelUpMoveProtocol(Protocol):
    move_id: u16
    level_id: u16

    @abstractmethod
    def __init__(self, move_id: u16, level_id: u16):
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...


LUM = TypeVar("LUM", bound=LevelUpMoveProtocol)


class MoveLearnsetProtocol(Protocol[LUM]):
    level_up_moves: MutableSequence[LUM]
    tm_hm_moves: MutableSequence[u32]
    egg_moves: MutableSequence[u32]

    @abstractmethod
    def __init__(
        self,
        level_up_moves: Sequence[LUM],
        tm_hm_moves: Sequence[u32],
        egg_moves: Sequence[u32],
    ):
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...


class WazaMoveRangeSettingsProtocol(Protocol):
    target: int
    range: int
    condition: int
    unused: int

    @abstractmethod
    def __init__(self, data: bytes):
        ...

    @abstractmethod
    def __int__(self):
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...


R = TypeVar("R", bound=WazaMoveRangeSettingsProtocol)


class WazaMoveProtocol(Protocol[R]):
    base_power: u16
    type: _PokeType
    category: _WazaMoveCategory
    settings_range: R
    settings_range_ai: R
    base_pp: u8
    ai_weight: u8
    miss_accuracy: u8
    accuracy: u8
    ai_condition1_chance: u8
    number_chained_hits: u8
    max_upgrade_level: u8
    crit_chance: u8
    affected_by_magic_coat: bool
    is_snatchable: bool
    uses_mouth: bool
    ai_frozen_check: bool
    ignores_taunted: bool
    range_check_text: u8
    move_id: u16
    message_id: u8

    @abstractmethod
    def __init__(self, data: bytes):
        ...

    @abstractmethod
    def to_bytes(self) -> bytes:
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...


M = TypeVar("M", bound=WazaMoveProtocol)
L = TypeVar("L", bound=MoveLearnsetProtocol)


class WazaPProtocol(Sir0Serializable, Protocol[M, L]):
    moves: MutableSequence[M]
    learnsets: MutableSequence[L]

    @abstractmethod
    def __init__(self, data: bytes, waza_content_pointer: int):
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...
