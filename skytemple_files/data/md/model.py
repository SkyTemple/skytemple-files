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
import typing
from enum import Enum
from typing import Dict, Iterator

from skytemple_files.common.util import *
from skytemple_files.common.i18n_util import f, _


# Honestly, I don't know a better way to do that
class MdProperties:
    NUM_ENTITIES = 600
    MAX_POSSIBLE = 554

# This is only for compatibility issues
# The one that should be used is in MdProperties
NUM_ENTITIES = 600

MD_ENTRY_LEN = 68


class Gender(Enum):
    INVALID = 0, _('Invalid')
    MALE = 1, _('Male')
    FEMALE = 2, _('Female')
    GENDERLESS = 3, _('Genderless')

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, print_name: Optional[str] = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f'Gender.{self.name}'

    @property
    def print_name(self) -> str:
        return self._print_name_


class PokeType(Enum):
    NONE = 0, _("None")
    NORMAL = 1, _("Normal")
    FIRE = 2, _("Fire")
    WATER = 3, _("Water")
    GRASS = 4, _("Grass")
    ELECTRIC = 5, _("Electric")
    ICE = 6, _("Ice")
    FIGHTING = 7, _("Fighting")
    POISON = 8, _("Poison")
    GROUND = 9, _("Ground")
    FLYING = 10, _("Flying")
    PSYCHIC = 11, _("Psychic")
    BUG = 12, _("Bug")
    ROCK = 13, _("Rock")
    GHOST = 14, _("Ghost")
    DRAGON = 15, _("Dragon")
    DARK = 16, _("Dark")
    STEEL = 17, _("Steel")
    NEUTRAL = 18, _("Neutral")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, print_name: Optional[str] = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f'PokeType.{self.name}'

    @property
    def print_name(self) -> str:
        return self._print_name_


class Ability(Enum):
    STENCH = 0x1, _('Stench')
    THICK_FAT = 0x2, _('Thick Fat')
    RAIN_DISH = 0x3, _('Rain Dish')
    DRIZZLE = 0x4, _('Drizzle')
    ARENA_TRAP = 0x5, _('Arena Trap')
    INTIMIDATE = 0x6, _('Intimidate')
    ROCK_HEAD = 0x7, _('Rock Head')
    AIR_LOCK = 0x8, _('Air Lock')
    HYPER_CUTTER = 0x9, _('Hyper Cutter')
    SHADOW_TAG = 0xA, _('Shadow tag')
    SPEED_BOOST = 0xB, _('Speed Boost')
    BATTLE_ARMOR = 0xC, _('Battle Armor')
    STURDY = 0xD, _('Sturdy')
    SUCTION_CUPS = 0xE, _('Suction Cups')
    CLEAR_BODY = 0xF, _('Clear Body')
    TORRENT = 0x10, _('Torrent')
    GUTS = 0x11, _('Guts')
    ROUGH_SKIN = 0x12, _('Rough Skin')
    SHELL_ARMOR = 0x13, _('Shell Armor')
    NATURAL_CURE = 0x14, _('Natural Cure')
    DAMP = 0x15, _('Damp')
    LIMBER = 0x16, _('Limber')
    MAGNET_PULL = 0x17, _('Magnet Pull')
    WHITE_SMOKE = 0x18, _('White Smoke')
    SYNCHRONIZE = 0x19, _('Synchronize')
    OVERGROW = 0x1A, _('Overgrow')
    SWIFT_SWIM = 0x1B, _('Swift Swim')
    SAND_STREAM = 0x1C, _('Sand Stream')
    SAND_VEIL = 0x1D, _('Sand Veil')
    KEEN_EYE = 0x1E, _('Keen Eye')
    INNER_FOCUS = 0x1F, _('Inner Focus')
    STATIC = 0x20, _('Static')
    SHED_SKIN = 0x21, _('Shed Skin')
    HUGE_POWER = 0x22, _('Huge Power')
    VOLT_ABSORB = 0x23, _('Volt Absorb')
    WATER_ABSORB = 0x24, _('Water Absorb')
    FORECAST = 0x25, _('Forecast')
    SERENE_GRACE = 0x26, _('Serene Grace')
    POISON_POINT = 0x27, _('Poison Point')
    TRACE = 0x28, _('Trace')
    OBLIVIOUS = 0x29, _('Oblivious')
    TRUANT = 0x2A, _('Truant')
    RUN_AWAY = 0x2B, _('Run Away')
    STICKY_HOLD = 0x2C, _('Sticky Hold')
    CLOUD_NINE = 0x2D, _('Cloud Nine')
    ILLUMINATE = 0x2E, _('Illuminate')
    EARLY_BIRD = 0x2F, _('Early Bird')
    HUSTLE = 0x30, _('Hustle')
    DROUGHT = 0x31, _('Drought')
    LIGHTNINGROD = 0x32, _('LightningRod')
    COMPOUNDEYES = 0x33, _('CompoundEyes')
    MARVEL_SCALE = 0x34, _('Marvel Scale')
    WONDER_GUARD = 0x35, _('Wonder Guard')
    INSOMNIA = 0x36, _('Insomnia')
    LEVITATE = 0x37, _('Levitate')
    PLUS = 0x38, _('Plus')
    PRESSURE = 0x39, _('Pressure')
    LIQUID_OOZE = 0x3A, _('Liquid Ooze')
    COLOR_CHANGE = 0x3B, _('Color Change')
    SOUNDPROOF = 0x3C, _('Soundproof')
    EFFECT_SPORE = 0x3D, _('Effect Spore')
    FLAME_BODY = 0x3E, _('Flame Body')
    MINUS = 0x3F, _('Minus')
    OWN_TEMPO = 0x40, _('Own Tempo')
    MAGMA_ARMOR = 0x41, _('Magma Armor')
    WATER_VEIL = 0x42, _('Water Veil')
    SWARM = 0x43, _('Swarm')
    CUTE_CHARM = 0x44, _('Cute Charm')
    IMMUNITY = 0x45, _('Immunity')
    BLAZE = 0x46, _('Blaze')
    PICKUP = 0x47, _('Pickup')
    FLASH_FIRE = 0x48, _('Flash Fire')
    VITAL_SPIRIT = 0x49, _('Vital Spirit')
    CHLOROPHYLL = 0x4A, _('Chlorophyll')
    PURE_POWER = 0x4B, _('Pure Power')
    SHIELD_DUST = 0x4C, _('Shield Dust')
    ICE_BODY = 0x4D, _('Ice Body')
    STALL = 0x4E, _('Stall')
    ANGER_POINT = 0x4F, _('Anger Point')
    TINTED_LENS = 0x50, _('Tinted Lens')
    HYDRATION = 0x51, _('Hydration')
    FRISK = 0x52, _('Frisk')
    MOLD_BREAKER = 0x53, _('Mold Breaker')
    UNBURDEN = 0x54, _('Unburden')
    DRY_SKIN = 0x55, _('Dry Skin')
    ANTICIPATION = 0x56, _('Anticipation')
    SCRAPPY = 0x57, _('Scrappy')
    SUPER_LUCK = 0x58, _('Super Luck')
    GLUTTONY = 0x59, _('Gluttony')
    SOLAR_POWER = 0x5A, _('Solar Power')
    SKILL_LINK = 0x5B, _('Skill Link')
    RECKLESS = 0x5C, _('Reckless')
    SNIPER = 0x5D, _('Sniper')
    SLOW_START = 0x5E, _('Slow Start')
    HEATPROOF = 0x5F, _('Heatproof')
    DOWNLOAD = 0x60, _('Download')
    SIMPLE = 0x61, _('Simple')
    TANGLED_FEET = 0x62, _('Tangled Feet')
    ADAPTABILITY = 0x63, _('Adaptability')
    TECHNICIAN = 0x64, _('Technician')
    IRON_FIST = 0x65, _('Iron Fist')
    MOTOR_DRIVE = 0x66, _('Motor Drive')
    UNAWARE = 0x67, _('Unaware')
    RIVALRY = 0x68, _('Rivalry')
    BAD_DREAMS = 0x69, _('Bad Dreams')
    NO_GUARD = 0x6A, _('No Guard')
    NORMALIZE = 0x6B, _('Normalize')
    SOLID_ROCK = 0x6C, _('Solid Rock')
    QUICK_FEET = 0x6D, _('Quick Feet')
    FILTER = 0x6E, _('Filter')
    KLUTZ = 0x6F, _('Klutz')
    STEDFAST = 0x70, _('Steadfast')
    FLOWER_GIFT = 0x71, _('Flower Gift')
    POISION_HEAL = 0x72, _('Poison Heal')
    MAGIC_GUARD = 0x73, _('Magic Guard')
    INVALID = 0x74, _('$$$')
    HONEY_GATHER = 0x75, _('Honey Gather')
    AFTERMATH = 0x76, _('Aftermath')
    SNOW_CLOAK = 0x77, _('Snow Cloak')
    SNOW_WARNING = 0x78, _('Snow Warning')
    FOREWARN = 0x79, _('Forewarn')
    STORM_DRAIN = 0x7A, _('Storm Drain')
    LEAF_GUARD = 0x7B, _('Leaf Guard')
    NONE = 0xFF, _('NONE')
    NULL = 0x00, _('NULL')

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, print_name: Optional[str] = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f'Ability.{self.name}'

    @property
    def print_name(self) -> str:
        return self._print_name_


class IQGroup(Enum):
    A = 0x0, 'A'
    B = 0x1, 'B'
    C = 0x2, 'C'
    D = 0x3, 'D'
    E = 0x4, 'E'
    F = 0x5, 'F'
    G = 0x6, 'G'
    H = 0x7, 'H'
    UNUSED8 = 0x8, _('Unused') + ' 8'
    UNUSED9 = 0x9, _('Unused') + ' 9'
    I = 0xA, 'I'
    J = 0xB, 'J'
    UNUSEDC = 0xC, _('Unused') + ' C'
    UNUSEDD = 0xD, _('Unused') + ' D'
    UNUSEDE = 0xE, _('Unused') + ' E'
    INVALID = 0xF, _('Invalid')

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, print_name: Optional[str] = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f'IQGroup.{self.name}'

    @property
    def print_name(self) -> str:
        return self._print_name_


class EvolutionMethod(Enum):
    NONE = 0, _("Not an Evolved Form.")
    LEVEL = 1, _('Level')
    IQ = 2, _('IQ')
    ITEMS = 3, _('Items')
    RECRUITED = 4, _('Recruited')
    NO_REQ = 5, _('No Main Requirement')

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, print_name: Optional[str] = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f'EvolutionMethod.{self.name}'

    @property
    def print_name(self) -> str:
        return self._print_name_


class AdditionalRequirement(Enum):
    NONE = 0, _('None')
    LINK_CABLE = 1, _('Link Cable')
    ATK_G_DEF = 2, _('Attack > Defense')
    ATK_L_DEF = 3, _('Attack < Defense')
    ATK_E_DEF = 4, _('Attack = Defense')
    SUN_RIBBON = 5, _('Sun Ribbon')
    LUNAR_RIBBON = 6, _('Lunar Ribbon')
    BEAUTY_SCARF = 7, _('Beauty Scarf')
    INT_VAL_1 = 8, _('Internal Value 0x1 = 1')
    INT_VAL_0 = 9, _('Internal Value 0x1 = 0')
    MALE = 10, _('Male (1st form)')
    FEMALE = 11, _('Female (2nd form)')
    ANCIENT_POWER = 12, _('Knows AncientPower')
    ROLLOUT = 13, _('Knows Rollout')
    DOUBLE_HIT = 14, _('Knows Double Hit')
    MIMIC = 15, _('Knows Mimic')

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, print_name: Optional[str] = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f'EvolutionMethod.{self.name}'

    @property
    def print_name(self) -> str:
        return self._print_name_


class MovementType(Enum):
    STANDARD = 0, _("Standard")
    UNKNOWN1 = 1, _("Unknown") + ' 1'
    HOVERING = 2, _("Hovering")
    PHASE_THROUGH_WALLS = 3, _("Phase Through Walls")   # TRANSLATORS: Movement Type
    LAVA = 4, _("Lava")
    WATER = 5, _("Water")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, print_name: Optional[str] = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f'MovementType.{self.name}'

    @property
    def print_name(self) -> str:
        return self._print_name_


class ShadowSize(Enum):
    SMALL = 0, _('Small')
    MEDIUM = 1, _('Medium')
    LARGE = 2, _('Large')

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, print_name: Optional[str] = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f'ShadowSize.{self.name}'

    @property
    def print_name(self) -> str:
        return self._print_name_


class MdEntry(AutoString, CheckedIntWrites):
    md_index: u32
    entid: u16
    unk31: u16
    national_pokedex_number: u16
    base_movement_speed: u16
    pre_evo_index: u16
    evo_method: EvolutionMethod
    evo_param1: u16
    evo_param2: AdditionalRequirement
    sprite_index: i16
    gender: Gender
    body_size: u8
    type_primary: PokeType
    type_secondary: PokeType
    movement_type: MovementType
    iq_group: IQGroup
    ability_primary: Ability
    ability_secondary: Ability
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
    shadow_size: ShadowSize
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
            self, *,
            md_index: u32,
            entid: u16,
            unk31: u16,
            national_pokedex_number: u16,
            base_movement_speed: u16,
            pre_evo_index: u16,
            evo_method: EvolutionMethod,
            evo_param1: u16,
            evo_param2: AdditionalRequirement,
            sprite_index: i16,
            gender: Gender,
            body_size: u8,
            type_primary: PokeType,
            type_secondary: PokeType,
            movement_type: MovementType,
            iq_group: IQGroup,
            ability_primary: Ability,
            ability_secondary: Ability,
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
            shadow_size: ShadowSize,
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
        self.bitfield1_0, self.bitfield1_1, self.bitfield1_2, self.bitfield1_3, \
        self.can_move, self.bitfield1_5, self.can_evolve, self.item_required_for_spawning = \
            (bool(bitflag1 >> i & 1) for i in range(8))

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
    def new_empty(cls, entid: u16) -> 'MdEntry':
        return MdEntry(
                md_index=u32(0),
                entid=entid,
                unk31=u16(0),
                national_pokedex_number=u16(0),
                base_movement_speed=u16(0),
                pre_evo_index=u16(0),
                evo_method=EvolutionMethod.NONE,
                evo_param1=u16(0),
                evo_param2=AdditionalRequirement.NONE,
                sprite_index=i16(0),
                gender=Gender.INVALID,
                body_size=u8(0),
                type_primary=PokeType.NONE,
                type_secondary=PokeType.NONE,
                movement_type=MovementType.UNKNOWN1,
                iq_group=IQGroup.INVALID,
                ability_primary=Ability.NONE,
                ability_secondary=Ability.NONE,
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
                shadow_size=ShadowSize.SMALL,
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
        return self.md_index % MdProperties.NUM_ENTITIES


class Md:
    @typing.no_type_check
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        number_entries = read_u32(data, 4)

        self.entries: List[MdEntry] = []
        self._entries_by_entid: Dict[int, List[Tuple[int, MdEntry]]] = {}
        for i in range(0, number_entries):
            start = (i * MD_ENTRY_LEN)
            entry = MdEntry(
                md_index=u32(i),
                entid=read_u16(data, start + 0x00),
                unk31=read_u16(data, start + 0x02),
                national_pokedex_number=read_u16(data, start + 0x04),
                base_movement_speed=read_u16(data, start + 0x06),
                pre_evo_index=read_u16(data, start + 0x08),
                evo_method=EvolutionMethod(read_u16(data, start + 0x0A)),
                evo_param1=read_u16(data, start + 0x0C),
                evo_param2=AdditionalRequirement(read_u16(data, start + 0x0E)),
                sprite_index=read_i16(data, start + 0x10),
                gender=Gender(read_u8(data, start + 0x12)),
                body_size=read_u8(data, start + 0x13),
                type_primary=PokeType(read_u8(data, start + 0x14)),
                type_secondary=PokeType(read_u8(data, start + 0x15)),
                movement_type=MovementType(read_u8(data, start + 0x16)),
                iq_group=IQGroup(read_u8(data, start + 0x17)),
                ability_primary=Ability(read_u8(data, start + 0x18)),
                ability_secondary=Ability(read_u8(data, start + 0x19)),
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
                shadow_size=ShadowSize(read_i8(data, start + 0x2E)),
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
