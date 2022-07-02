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

# The fixture MD file contains 9 entries:
#   #000
#     -> $0000
#     -> $0006
#   #001
#     -> $0001
#     -> $0007
#   #002
#     -> $0002
#     -> $0008
#   #003
#     -> $0003
#     -> $0009
#   #004
#     -> $0004
#   #005
#     -> $0005
from dataclasses import dataclass

from range_typed_integers import u16, u32, i16, u8, i8

from skytemple_files.common.util import AutoString
from skytemple_files.data.md.protocol import (
    MdEntryProtocol,
    _EvolutionMethod,
    _AdditionalRequirement,
    _Gender,
    _PokeType,
    _MovementType,
    _IQGroup,
    _Ability,
    _ShadowSize,
    EvolutionMethod,
    AdditionalRequirement,
    Gender,
    PokeType,
    MovementType,
    IQGroup,
    Ability,
    ShadowSize,
)


# MD Parameters for the fixture test file:
FIX_NUM_ENTITIES = 6
FIX_MAX_POSSIBLE = 9


# Compares ANY implementation of two MdEntryProtocols.
def eq_md_protocol(one: MdEntryProtocol, two: MdEntryProtocol) -> bool:
    return (
        one.md_index == two.md_index
        and one.entid == two.entid
        and one.unk31 == two.unk31
        and one.national_pokedex_number == two.national_pokedex_number
        and one.base_movement_speed == two.base_movement_speed
        and one.pre_evo_index == two.pre_evo_index
        and one.evo_method == two.evo_method
        and one.evo_param1 == two.evo_param1
        and one.evo_param2 == two.evo_param2
        and one.sprite_index == two.sprite_index
        and one.gender == two.gender
        and one.body_size == two.body_size
        and one.type_primary == two.type_primary
        and one.type_secondary == two.type_secondary
        and one.movement_type == two.movement_type
        and one.iq_group == two.iq_group
        and one.ability_primary == two.ability_primary
        and one.ability_secondary == two.ability_secondary
        and one.exp_yield == two.exp_yield
        and one.recruit_rate1 == two.recruit_rate1
        and one.base_hp == two.base_hp
        and one.recruit_rate2 == two.recruit_rate2
        and one.base_atk == two.base_atk
        and one.base_sp_atk == two.base_sp_atk
        and one.base_def == two.base_def
        and one.base_sp_def == two.base_sp_def
        and one.weight == two.weight
        and one.size == two.size
        and one.unk17 == two.unk17
        and one.unk18 == two.unk18
        and one.shadow_size == two.shadow_size
        and one.chance_spawn_asleep == two.chance_spawn_asleep
        and one.hp_regeneration == two.hp_regeneration
        and one.unk21_h == two.unk21_h
        and one.base_form_index == two.base_form_index
        and one.exclusive_item1 == two.exclusive_item1
        and one.exclusive_item2 == two.exclusive_item2
        and one.exclusive_item3 == two.exclusive_item3
        and one.exclusive_item4 == two.exclusive_item4
        and one.unk27 == two.unk27
        and one.unk28 == two.unk28
        and one.unk29 == two.unk29
        and one.unk30 == two.unk30
        and one.bitfield1_0 == two.bitfield1_0
        and one.bitfield1_1 == two.bitfield1_1
        and one.bitfield1_2 == two.bitfield1_2
        and one.bitfield1_3 == two.bitfield1_3
        and one.can_move == two.can_move
        and one.bitfield1_5 == two.bitfield1_5
        and one.can_evolve == two.can_evolve
        and one.item_required_for_spawning == two.item_required_for_spawning
    )


# Similar to the "actual" MdEntry Python implementation
# but used for storing expected Fixture values.
@dataclass(eq=False)
class ExpectedMdEntry(MdEntryProtocol, AutoString):
    md_index: u32
    entid: u16
    unk31: u16
    national_pokedex_number: u16
    base_movement_speed: u16
    pre_evo_index: u16
    evo_method: _EvolutionMethod
    evo_param1: u16
    evo_param2: _AdditionalRequirement
    sprite_index: i16
    gender: _Gender
    body_size: u8
    type_primary: _PokeType
    type_secondary: _PokeType
    movement_type: _MovementType
    iq_group: _IQGroup
    ability_primary: _Ability
    ability_secondary: _Ability
    exp_yield: u16
    recruit_rate1: i16
    base_hp: u16
    recruit_rate2: i16
    base_atk: u8
    base_sp_atk: u8
    base_def: u8
    base_sp_def: u8
    weight: i16
    size: i16
    unk17: u8
    unk18: u8
    shadow_size: _ShadowSize
    chance_spawn_asleep: i8
    hp_regeneration: u8
    unk21_h: i8
    base_form_index: i16
    exclusive_item1: i16
    exclusive_item2: i16
    exclusive_item3: i16
    exclusive_item4: i16
    unk27: i16
    unk28: i16
    unk29: i16
    unk30: i16
    bitfield1_0: bool
    bitfield1_1: bool
    bitfield1_2: bool
    bitfield1_3: bool
    can_move: bool
    bitfield1_5: bool
    can_evolve: bool
    item_required_for_spawning: bool

    @classmethod
    def new_empty(cls, entid: u16) -> MdEntryProtocol:
        raise NotImplementedError()

    @property
    def md_index_base(self) -> int:
        raise NotImplementedError()


EXPECTED_NEW_ENTRY_BASE_ID = u16(1234)
EXPECTED_NEW_ENTRY = ExpectedMdEntry(
    md_index=u32(0),
    entid=EXPECTED_NEW_ENTRY_BASE_ID,
    unk31=u16(0),
    national_pokedex_number=u16(0),
    base_movement_speed=u16(0),
    pre_evo_index=u16(0),
    evo_method=u16(EvolutionMethod.NONE.value),
    evo_param1=u16(0),
    evo_param2=u16(AdditionalRequirement.NONE.value),
    sprite_index=i16(0),
    gender=u8(Gender.INVALID.value),
    body_size=u8(0),
    type_primary=u8(PokeType.NONE.value),
    type_secondary=u8(PokeType.NONE.value),
    movement_type=u8(MovementType.UNKNOWN1.value),
    iq_group=u8(IQGroup.INVALID.value),
    ability_primary=u8(Ability.NONE.value),
    ability_secondary=u8(Ability.NONE.value),
    exp_yield=u16(0),
    recruit_rate1=i16(0),
    base_hp=u16(0),
    recruit_rate2=i16(0),
    base_atk=u8(0),
    base_sp_atk=u8(0),
    base_def=u8(0),
    base_sp_def=u8(0),
    weight=i16(0),
    size=i16(0),
    unk17=u8(0),
    unk18=u8(0),
    shadow_size=i8(ShadowSize.SMALL.value),
    chance_spawn_asleep=i8(0),
    hp_regeneration=u8(0),
    unk21_h=i8(0),
    base_form_index=i16(0),
    exclusive_item1=i16(0),
    exclusive_item2=i16(0),
    exclusive_item3=i16(0),
    exclusive_item4=i16(0),
    unk27=i16(0),
    unk28=i16(0),
    unk29=i16(0),
    unk30=i16(0),
    bitfield1_0=False,
    bitfield1_1=False,
    bitfield1_2=False,
    bitfield1_3=False,
    can_move=False,
    bitfield1_5=False,
    can_evolve=False,
    item_required_for_spawning=False,
)


EXPECTED_BASE_INDICES = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3]


EXPECTED_MD_ENTRIES = [
    ExpectedMdEntry(
        u32(0),
        u16(0),
        u16(0),
        u16(0),
        u16(1),
        u16(0),
        u16(0),
        u16(0),
        u16(0),
        i16(-1),
        u8(0),
        u8(1),
        u8(1),
        u8(0),
        u8(0),
        u8(15),
        u8(26),
        u8(0),
        u16(80),
        i16(-999),
        u16(1),
        i16(-999),
        u8(0),
        u8(0),
        u8(0),
        u8(1),
        i16(256),
        i16(99),
        u8(10),
        u8(10),
        i8(2),
        i8(8),
        u8(100),
        i8(0),
        i16(0),
        i16(0),
        i16(0),
        i16(0),
        i16(0),
        i16(1),
        i16(0),
        i16(0),
        i16(0),
        False,
        False,
        False,
        False,
        True,
        True,
        False,
        False,
    ),
    ExpectedMdEntry(
        u32(1),
        u16(1),
        u16(26166),
        u16(20542),
        u16(867),
        u16(35245),
        u16(1),
        u16(55866),
        u16(7),
        i16(-3641),
        u8(2),
        u8(151),
        u8(17),
        u8(3),
        u8(0),
        u8(13),
        u8(106),
        u8(106),
        u16(35246),
        i16(-26452),
        u16(10),
        i16(-20029),
        u8(195),
        u8(194),
        u8(25),
        u8(111),
        i16(-20709),
        i16(-9625),
        u8(144),
        u8(200),
        i8(1),
        i8(-117),
        u8(49),
        i8(45),
        i16(-16649),
        i16(6359),
        i16(21869),
        i16(-20621),
        i16(6121),
        i16(-13868),
        i16(23251),
        i16(-23392),
        i16(32630),
        True,
        True,
        False,
        False,
        False,
        False,
        False,
        True,
    ),
    ExpectedMdEntry(
        u32(2),
        u16(2),
        u16(22941),
        u16(15564),
        u16(14118),
        u16(57606),
        u16(2),
        u16(33127),
        u16(12),
        i16(-23757),
        u8(0),
        u8(97),
        u8(18),
        u8(6),
        u8(2),
        u8(0),
        u8(120),
        u8(123),
        u16(53598),
        i16(-8064),
        u16(0),
        i16(-8778),
        u8(62),
        u8(252),
        u8(107),
        u8(157),
        i16(5293),
        i16(-23667),
        u8(186),
        u8(214),
        i8(0),
        i8(-51),
        u8(183),
        i8(10),
        i16(-15131),
        i16(-32521),
        i16(157),
        i16(3665),
        i16(7850),
        i16(-23524),
        i16(21685),
        i16(-24276),
        i16(-7495),
        True,
        False,
        False,
        False,
        True,
        True,
        False,
        False,
    ),
    ExpectedMdEntry(
        u32(3),
        u16(3),
        u16(34160),
        u16(52643),
        u16(8957),
        u16(33918),
        u16(4),
        u16(42497),
        u16(10),
        i16(27965),
        u8(2),
        u8(91),
        u8(18),
        u8(17),
        u8(5),
        u8(4),
        u8(90),
        u8(108),
        u16(48014),
        i16(-26124),
        u16(6),
        i16(-13376),
        u8(173),
        u8(89),
        u8(247),
        u8(12),
        i16(-8889),
        i16(10300),
        u8(97),
        u8(111),
        i8(0),
        i8(-122),
        u8(208),
        i8(-67),
        i16(2744),
        i16(-23522),
        i16(-14581),
        i16(13532),
        i16(-28078),
        i16(24755),
        i16(-31040),
        i16(11136),
        i16(-18581),
        True,
        False,
        False,
        True,
        True,
        False,
        True,
        False,
    ),
    ExpectedMdEntry(
        u32(4),
        u16(4),
        u16(59162),
        u16(55559),
        u16(8274),
        u16(63222),
        u16(4),
        u16(60987),
        u16(2),
        i16(-9176),
        u8(2),
        u8(116),
        u8(2),
        u8(9),
        u8(4),
        u8(0),
        u8(109),
        u8(14),
        u16(18791),
        i16(8288),
        u16(14),
        i16(22907),
        u8(228),
        u8(101),
        u8(157),
        u8(34),
        i16(26626),
        i16(17542),
        u8(60),
        u8(243),
        i8(0),
        i8(-116),
        u8(174),
        i8(-5),
        i16(1070),
        i16(-6088),
        i16(690),
        i16(31714),
        i16(6009),
        i16(-27113),
        i16(21008),
        i16(-9647),
        i16(-19324),
        True,
        True,
        False,
        True,
        False,
        False,
        False,
        False,
    ),
    ExpectedMdEntry(
        u32(5),
        u16(5),
        u16(45751),
        u16(63641),
        u16(63762),
        u16(21000),
        u16(3),
        u16(734),
        u16(8),
        i16(-26773),
        u8(0),
        u8(163),
        u8(5),
        u8(7),
        u8(0),
        u8(6),
        u8(27),
        u8(83),
        u16(57823),
        i16(31474),
        u16(11),
        i16(267),
        u8(148),
        u8(49),
        u8(94),
        u8(84),
        i16(5014),
        i16(-7426),
        u8(184),
        u8(161),
        i8(0),
        i8(4),
        u8(223),
        i8(3),
        i16(-2370),
        i16(-24678),
        i16(-12803),
        i16(-3248),
        i16(-20811),
        i16(27465),
        i16(2738),
        i16(-31223),
        i16(-16018),
        False,
        True,
        False,
        False,
        True,
        True,
        True,
        True,
    ),
    ExpectedMdEntry(
        u32(6),
        u16(0),
        u16(0),
        u16(0),
        u16(1),
        u16(0),
        u16(0),
        u16(0),
        u16(0),
        i16(-1),
        u8(0),
        u8(1),
        u8(1),
        u8(0),
        u8(0),
        u8(0),
        u8(26),
        u8(0),
        u16(80),
        i16(-999),
        u16(30),
        i16(-999),
        u8(10),
        u8(10),
        u8(10),
        u8(10),
        i16(256),
        i16(99),
        u8(10),
        u8(10),
        i8(2),
        i8(8),
        u8(100),
        i8(0),
        i16(0),
        i16(0),
        i16(0),
        i16(0),
        i16(0),
        i16(1),
        i16(0),
        i16(0),
        i16(0),
        False,
        False,
        False,
        False,
        True,
        True,
        True,
        False,
    ),
    ExpectedMdEntry(
        u32(7),
        u16(1),
        u16(24126),
        u16(57210),
        u16(53714),
        u16(33494),
        u16(1),
        u16(7626),
        u16(2),
        i16(-4815),
        u8(0),
        u8(26),
        u8(16),
        u8(0),
        u8(1),
        u8(12),
        u8(122),
        u8(31),
        u16(45208),
        i16(9821),
        u16(7),
        i16(-14262),
        u8(248),
        u8(80),
        u8(53),
        u8(28),
        i16(7778),
        i16(16595),
        u8(82),
        u8(132),
        i8(2),
        i8(28),
        u8(22),
        i8(-101),
        i16(-2428),
        i16(-20942),
        i16(-25854),
        i16(31535),
        i16(-28378),
        i16(12804),
        i16(8438),
        i16(-16205),
        i16(4273),
        False,
        False,
        False,
        True,
        True,
        False,
        False,
        True,
    ),
    ExpectedMdEntry(
        u32(8),
        u16(2),
        u16(22715),
        u16(59740),
        u16(19745),
        u16(8189),
        u16(2),
        u16(23421),
        u16(0),
        i16(-16368),
        u8(1),
        u8(212),
        u8(9),
        u8(7),
        u8(5),
        u8(15),
        u8(56),
        u8(70),
        u16(25158),
        i16(14960),
        u16(7),
        i16(20947),
        u8(222),
        u8(33),
        u8(50),
        u8(181),
        i16(23334),
        i16(8665),
        u8(122),
        u8(63),
        i8(1),
        i8(-64),
        u8(112),
        i8(-4),
        i16(27149),
        i16(-4130),
        i16(17990),
        i16(-31604),
        i16(5354),
        i16(1461),
        i16(11830),
        i16(19838),
        i16(-2198),
        True,
        False,
        False,
        False,
        False,
        False,
        True,
        False,
    ),
    ExpectedMdEntry(
        u32(9),
        u16(3),
        u16(38087),
        u16(8792),
        u16(48375),
        u16(33412),
        u16(0),
        u16(4644),
        u16(3),
        i16(-12606),
        u8(0),
        u8(108),
        u8(0),
        u8(11),
        u8(3),
        u8(14),
        u8(30),
        u8(106),
        u16(54865),
        i16(-1967),
        u16(3),
        i16(31692),
        u8(255),
        u8(247),
        u8(148),
        u8(156),
        i16(-10355),
        i16(20981),
        u8(111),
        u8(182),
        i8(0),
        i8(-82),
        u8(81),
        i8(-88),
        i16(-10380),
        i16(-10810),
        i16(-27183),
        i16(-1863),
        i16(22275),
        i16(-19175),
        i16(18205),
        i16(-21246),
        i16(17313),
        True,
        False,
        False,
        True,
        True,
        True,
        True,
        False,
    ),
]
