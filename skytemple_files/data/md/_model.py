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

from typing import Iterator, List, Tuple, Dict, no_type_check, Optional

from range_typed_integers import u32, u16, u8, i16, i8

from skytemple_files.common.util import (
    AutoString,
    read_u16,
    read_u8,
    read_i16,
    read_u32,
    read_i8,
)
from skytemple_files.data.md.protocol import (
    MdProtocol,
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
    MD_ENTRY_LEN,
    _MdPropertiesProtocol,
    DEFAULT_NUM_ENTITIES,
    DEFAULT_MAX_POSSIBLE,
)


class MdPropertiesState(_MdPropertiesProtocol):
    _instance: Optional[MdPropertiesState] = None
    num_entities: int
    max_possible: int

    def __init__(self, num_entities: int, max_possible: int):
        self.num_entities = num_entities
        self.max_possible = max_possible

    @classmethod
    def instance(cls) -> MdPropertiesState:
        if cls._instance is None:
            cls._instance = MdPropertiesState(
                DEFAULT_NUM_ENTITIES, DEFAULT_MAX_POSSIBLE
            )
        return cls._instance


class MdEntry(MdEntryProtocol, AutoString):
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
    # @End:
    # The % of HP that this pokémon species regenerates at the end of each turn is equal to 1/(value * 2)
    # (Before applying any modifiers)
    # The final value is capped between 1/30 and 1/500
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

    def __init__(
        self,
        *,
        md_index: u32,
        entid: u16,
        unk31: u16,
        national_pokedex_number: u16,
        base_movement_speed: u16,
        pre_evo_index: u16,
        evo_method: _EvolutionMethod,
        evo_param1: u16,
        evo_param2: _AdditionalRequirement,
        sprite_index: i16,
        gender: _Gender,
        body_size: u8,
        type_primary: _PokeType,
        type_secondary: _PokeType,
        movement_type: _MovementType,
        iq_group: _IQGroup,
        ability_primary: _Ability,
        ability_secondary: _Ability,
        exp_yield: u16,
        recruit_rate1: i16,
        base_hp: u16,
        recruit_rate2: i16,
        base_atk: u8,
        base_sp_atk: u8,
        base_def: u8,
        base_sp_def: u8,
        weight: i16,
        size: i16,
        unk17: u8,
        unk18: u8,
        shadow_size: _ShadowSize,
        chance_spawn_asleep: i8,
        hp_regeneration: u8,
        unk21_h: i8,
        base_form_index: i16,
        exclusive_item1: i16,
        exclusive_item2: i16,
        exclusive_item3: i16,
        exclusive_item4: i16,
        unk27: i16,
        unk28: i16,
        unk29: i16,
        unk30: i16,
        bitflag1: u16,
    ):
        (
            self.bitfield1_0,
            self.bitfield1_1,
            self.bitfield1_2,
            self.bitfield1_3,
            self.can_move,
            self.bitfield1_5,
            self.can_evolve,
            self.item_required_for_spawning,
        ) = (bool(bitflag1 >> i & 1) for i in range(8))

        self.md_index = md_index
        self.entid = entid
        self.unk31 = unk31
        self.national_pokedex_number = national_pokedex_number
        self.base_movement_speed = base_movement_speed
        self.pre_evo_index = pre_evo_index
        self.evo_method = evo_method
        self.evo_param1 = evo_param1
        self.evo_param2 = evo_param2
        self.sprite_index = sprite_index
        self.gender = gender
        self.body_size = body_size
        self.type_primary = type_primary
        self.type_secondary = type_secondary
        self.movement_type = movement_type
        self.iq_group = iq_group
        self.ability_primary = ability_primary
        self.ability_secondary = ability_secondary
        self.exp_yield = exp_yield
        self.recruit_rate1 = recruit_rate1
        self.base_hp = base_hp
        self.recruit_rate2 = recruit_rate2
        self.base_atk = base_atk
        self.base_sp_atk = base_sp_atk
        self.base_def = base_def
        self.base_sp_def = base_sp_def
        self.weight = weight
        self.size = size
        self.unk17 = unk17
        self.unk18 = unk18
        self.shadow_size = shadow_size
        self.chance_spawn_asleep = chance_spawn_asleep
        self.hp_regeneration = hp_regeneration
        self.unk21_h = unk21_h
        self.base_form_index = base_form_index
        self.exclusive_item1 = exclusive_item1
        self.exclusive_item2 = exclusive_item2
        self.exclusive_item3 = exclusive_item3
        self.exclusive_item4 = exclusive_item4
        self.unk27 = unk27
        self.unk28 = unk28
        self.unk29 = unk29
        self.unk30 = unk30

    @classmethod
    def new_empty(cls, entid: u16) -> "MdEntry":
        return MdEntry(
            md_index=u32(0),
            entid=entid,
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
            bitflag1=u16(0),
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
        )

    @property
    def md_index_base(self) -> int:
        return self.md_index % MdPropertiesState.instance().num_entities


class Md(MdProtocol[MdEntry]):
    @no_type_check
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        number_entries = read_u32(data, 4)

        self.entries: List[MdEntry] = []
        self._entries_by_entid: Dict[int, List[Tuple[int, MdEntry]]] = {}
        for i in range(0, number_entries):
            start = 8 + (i * MD_ENTRY_LEN)
            entry = MdEntry(
                md_index=u32(i),
                entid=read_u16(data, start + 0x00),
                unk31=read_u16(data, start + 0x02),
                national_pokedex_number=read_u16(data, start + 0x04),
                base_movement_speed=read_u16(data, start + 0x06),
                pre_evo_index=read_u16(data, start + 0x08),
                evo_method=read_u16(data, start + 0x0A),
                evo_param1=read_u16(data, start + 0x0C),
                evo_param2=read_u16(data, start + 0x0E),
                sprite_index=read_i16(data, start + 0x10),
                gender=read_u8(data, start + 0x12),
                body_size=read_u8(data, start + 0x13),
                type_primary=read_u8(data, start + 0x14),
                type_secondary=read_u8(data, start + 0x15),
                movement_type=read_u8(data, start + 0x16),
                iq_group=read_u8(data, start + 0x17),
                ability_primary=read_u8(data, start + 0x18),
                ability_secondary=read_u8(data, start + 0x19),
                bitflag1=read_u16(data, start + 0x1A),
                exp_yield=read_u16(data, start + 0x1C),
                recruit_rate1=read_i16(data, start + 0x1E),
                base_hp=read_u16(data, start + 0x20),
                recruit_rate2=read_i16(data, start + 0x22),
                base_atk=read_u8(data, start + 0x24),
                base_sp_atk=read_u8(data, start + 0x25),
                base_def=read_u8(data, start + 0x26),
                base_sp_def=read_u8(data, start + 0x27),
                weight=read_i16(data, start + 0x28),
                size=read_i16(data, start + 0x2A),
                unk17=read_u8(data, start + 0x2C),
                unk18=read_u8(data, start + 0x2D),
                shadow_size=read_i8(data, start + 0x2E),
                chance_spawn_asleep=read_i8(data, start + 0x2F),
                hp_regeneration=read_u8(data, start + 0x30),
                unk21_h=read_i8(data, start + 0x31),
                base_form_index=read_i16(data, start + 0x32),
                exclusive_item1=read_i16(data, start + 0x34),
                exclusive_item2=read_i16(data, start + 0x36),
                exclusive_item3=read_i16(data, start + 0x38),
                exclusive_item4=read_i16(data, start + 0x3A),
                unk27=read_i16(data, start + 0x3C),
                unk28=read_i16(data, start + 0x3E),
                unk29=read_i16(data, start + 0x40),
                unk30=read_i16(data, start + 0x42),
            )

            self.entries.append(entry)
            if entry.entid not in self._entries_by_entid:
                self._entries_by_entid[entry.entid] = []
            self._entries_by_entid[entry.entid].append((i, entry))

    def get_by_index(self, index: int) -> MdEntry:
        return self.entries[index]

    def get_by_entity_id(self, index: int) -> List[Tuple[int, MdEntry]]:
        return self._entries_by_entid[index]

    def __len__(self) -> int:
        return len(self.entries)

    def __getitem__(self, key: int) -> MdEntry:
        return self.get_by_index(key)

    def __setitem__(self, key: int, value: MdEntry) -> None:
        self.entries[key] = value

    def __delitem__(self, key: int) -> None:
        del self.entries[key]

    def __iter__(self) -> Iterator[MdEntry]:
        return iter(self.entries)
