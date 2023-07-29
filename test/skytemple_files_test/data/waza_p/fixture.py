#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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

from typing import MutableSequence, Sequence

from range_typed_integers import u16, u8, u32

from skytemple_files.common.util import AutoString
from skytemple_files.data.waza_p.protocol import LevelUpMoveProtocol, MoveLearnsetProtocol, WazaMoveProtocol


def eq_level_up_move_list(one: Sequence[LevelUpMoveProtocol], two: Sequence[LevelUpMoveProtocol]) -> bool:
    if len(one) != len(two):
        return False
    for x, y in zip(one, two):
        if not eq_level_up_move(x, y):
            return False
    return True


def eq_level_up_move(one: LevelUpMoveProtocol, two: LevelUpMoveProtocol) -> bool:
    return (
        one.move_id == two.move_id and
        one.level_id == two.level_id
    )


def eq_learnset_list(one: Sequence[MoveLearnsetProtocol], two: Sequence[MoveLearnsetProtocol]) -> bool:
    if len(one) != len(two):
        return False
    for x, y in zip(one, two):
        if not eq_learnset(x, y):
            return False
    return True


def eq_learnset(one: MoveLearnsetProtocol, two: MoveLearnsetProtocol) -> bool:
    return (
        eq_level_up_move_list(one.level_up_moves, two.level_up_moves) and
        list(one.egg_moves) == list(two.egg_moves) and
        list(one.tm_hm_moves) == list(two.tm_hm_moves)
    )


def eq_move_list(one: Sequence[WazaMoveProtocol], two: Sequence[WazaMoveProtocol]) -> bool:
    if len(one) != len(two):
        return False
    for x, y in zip(one, two):
        if not eq_move(x, y):
            return False
    return True


def eq_move(one: WazaMoveProtocol, two: WazaMoveProtocol) -> bool:
    return (
        one.base_power == two.base_power and
        one.type == two.type and
        one.category == two.category and
        int(one.settings_range) == int(two.settings_range) and
        int(one.settings_range_ai) == int(two.settings_range_ai) and
        one.base_pp == two.base_pp and
        one.ai_weight == two.ai_weight and
        one.miss_accuracy == two.miss_accuracy and
        one.accuracy == two.accuracy and
        one.ai_condition1_chance == two.ai_condition1_chance and
        one.number_chained_hits == two.number_chained_hits and
        one.max_upgrade_level == two.max_upgrade_level and
        one.crit_chance == two.crit_chance and
        one.affected_by_magic_coat == two.affected_by_magic_coat and
        one.is_snatchable == two.is_snatchable and
        one.uses_mouth == two.uses_mouth and
        one.ai_frozen_check == two.ai_frozen_check and
        one.ignores_taunted == two.ignores_taunted and
        one.range_check_text == two.range_check_text and
        one.move_id == two.move_id and
        one.message_id == two.message_id
    )


class LevelUpMoveStub(LevelUpMoveProtocol, AutoString):
    move_id: u16
    level_id: u16

    def __init__(self, move_id: u16, level_id: u16):
        self.level_id = level_id
        self.move_id = move_id

    @classmethod
    def stub_new(
        cls,
        level_id: u16,
        move_id: u16,
    ) -> LevelUpMoveStub:
        return cls(move_id, level_id)

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError("not implemented for stub")


class WazaLearnsetStub(MoveLearnsetProtocol[LevelUpMoveStub]):
    level_up_moves: MutableSequence[LevelUpMoveStub]
    tm_hm_moves: MutableSequence[u32]
    egg_moves: MutableSequence[u32]

    def __init__(self, level_up_moves: Sequence[LevelUpMoveStub], tm_hm_moves: Sequence[u32], egg_moves: Sequence[u32]):
        self.level_up_moves = list(level_up_moves)
        self.tm_hm_moves = list(tm_hm_moves)
        self.egg_moves = list(egg_moves)

    @classmethod
    def stub_new(
        cls,
        level_up_moves: MutableSequence[LevelUpMoveStub],
        tm_hm_moves: MutableSequence[u32],
        egg_moves: MutableSequence[u32],
    ) -> WazaLearnsetStub:
        return cls(level_up_moves, tm_hm_moves, egg_moves)

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError("not implemented for stub")


class WazaMoveStub(WazaMoveProtocol[int]):  # type: ignore
    base_power: u16
    type: u8
    category: u8
    settings_range: int  # type: ignore
    settings_range_ai: int  # type: ignore
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
    
    @classmethod
    def stub_new(
        cls,
        base_power: u16,
        type: u8,
        category: u8,
        settings_range: int,
        settings_range_ai: int,
        base_pp: u8,
        ai_weight: u8,
        miss_accuracy: u8,
        accuracy: u8,
        ai_condition1_chance: u8,
        number_chained_hits: u8,
        max_upgrade_level: u8,
        crit_chance: u8,
        affected_by_magic_coat: bool,
        is_snatchable: bool,
        uses_mouth: bool,
        ai_frozen_check: u8,
        ignores_taunted: bool,
        range_check_text: u8,
        move_id: u16,
        message_id: u8,
    ) -> WazaMoveStub:
        self = cls.__new__(cls)
        self.base_power = base_power
        self.type = type
        self.category = category
        self.settings_range = settings_range
        self.settings_range_ai = settings_range_ai
        self.base_pp = base_pp
        self.ai_weight = ai_weight
        self.miss_accuracy = miss_accuracy
        self.accuracy = accuracy
        self.ai_condition1_chance = ai_condition1_chance
        self.number_chained_hits = number_chained_hits
        self.max_upgrade_level = max_upgrade_level
        self.crit_chance = crit_chance
        self.affected_by_magic_coat = affected_by_magic_coat
        self.is_snatchable = is_snatchable
        self.uses_mouth = uses_mouth
        self.ai_frozen_check = ai_frozen_check
        self.ignores_taunted = ignores_taunted
        self.range_check_text = range_check_text
        self.move_id = move_id
        self.message_id = message_id
        return self

    def __init__(self, data: bytes):
        raise NotImplementedError("not implemented for stub")

    def to_bytes(self) -> bytes:
        raise NotImplementedError("not implemented for stub")

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError("not implemented for stub")


FIX_MOVE_RANGE_SETTINGS = [
    (bytes([0x00, 0x00]), {'target': 0, 'range': 0, 'condition': 0, 'unused': 0}, 0),
    (bytes([0x34, 0x12]), {'target': 4, 'range': 3, 'condition': 2, 'unused': 1}, 0x1234),
    (bytes([0x12, 0x34]), {'target': 2, 'range': 1, 'condition': 4, 'unused': 3}, 0x3412),
    (bytes([0xCD, 0xEF]), {'target': 13, 'range': 12, 'condition': 15, 'unused': 14}, 0xEFCD),
    (bytes([0xFA, 0xB1]), {'target': 10, 'range': 15, 'condition': 1, 'unused': 11}, 0xB1FA),
]
