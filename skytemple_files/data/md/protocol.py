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
from typing import Protocol, TypeVar
from collections.abc import Sequence, Iterator

from range_typed_integers import u32, u8, u16, i8, i16

from skytemple_files.common.i18n_util import _


DEFAULT_NUM_ENTITIES = 600
DEFAULT_MAX_POSSIBLE = 554


class _MdPropertiesProtocol(Protocol):
    """
    Implementations must provide an implementation of this.
    This keeps track of "changeable" constants.

    The values must default to the values below, users may
    change it via the MdHandler, if for example a patch to expand
    the monster list is applied.
    """

    num_entities: int  # Must default to DEFAULT_NUM_ENTITIES.
    max_possible: int  # Must default to DEFAULT_MAX_POSSIBLE.

    @classmethod
    @abstractmethod
    def instance(cls) -> _MdPropertiesProtocol:
        """This is a singleton."""
        ...


MD_ENTRY_LEN = 68


_EvolutionMethod = u16
_AdditionalRequirement = u16
_Gender = u8
_PokeType = u8
_MovementType = u8
_IQGroup = u8
_Ability = u8
_ShadowSize = i8


class Gender(Enum):
    INVALID = 0, _("Invalid")
    MALE = 1, _("Male")
    FEMALE = 2, _("Female")
    GENDERLESS = 3, _("Genderless")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, print_name: str | None = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f"Gender.{self.name}"

    @property
    def print_name(self) -> str:
        return self._print_name_


class PokeType(Enum):
    NONE = 0, "None"
    NORMAL = 1, "Normal"
    FIRE = 2, "Fire"
    WATER = 3, "Water"
    GRASS = 4, "Grass"
    ELECTRIC = 5, "Electric"
    ICE = 6, "Ice"
    FIGHTING = 7, "Fighting"
    POISON = 8, "Poison"
    GROUND = 9, "Ground"
    FLYING = 10, "Flying"
    PSYCHIC = 11, "Psychic"
    BUG = 12, "Bug"
    ROCK = 13, "Rock"
    GHOST = 14, "Ghost"
    DRAGON = 15, "Dragon"
    DARK = 16, "Dark"
    STEEL = 17, "Steel"
    NEUTRAL = 18, "Neutral"

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, print_name: str | None = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f"PokeType.{self.name}"

    @property
    def print_name(self) -> str:
        return self._print_name_


class Ability(Enum):
    STENCH = 0x1, "Stench"
    THICK_FAT = 0x2, "Thick Fat"
    RAIN_DISH = 0x3, "Rain Dish"
    DRIZZLE = 0x4, "Drizzle"
    ARENA_TRAP = 0x5, "Arena Trap"
    INTIMIDATE = 0x6, "Intimidate"
    ROCK_HEAD = 0x7, "Rock Head"
    AIR_LOCK = 0x8, "Air Lock"
    HYPER_CUTTER = 0x9, "Hyper Cutter"
    SHADOW_TAG = 0xA, "Shadow tag"
    SPEED_BOOST = 0xB, "Speed Boost"
    BATTLE_ARMOR = 0xC, "Battle Armor"
    STURDY = 0xD, "Sturdy"
    SUCTION_CUPS = 0xE, "Suction Cups"
    CLEAR_BODY = 0xF, "Clear Body"
    TORRENT = 0x10, "Torrent"
    GUTS = 0x11, "Guts"
    ROUGH_SKIN = 0x12, "Rough Skin"
    SHELL_ARMOR = 0x13, "Shell Armor"
    NATURAL_CURE = 0x14, "Natural Cure"
    DAMP = 0x15, "Damp"
    LIMBER = 0x16, "Limber"
    MAGNET_PULL = 0x17, "Magnet Pull"
    WHITE_SMOKE = 0x18, "White Smoke"
    SYNCHRONIZE = 0x19, "Synchronize"
    OVERGROW = 0x1A, "Overgrow"
    SWIFT_SWIM = 0x1B, "Swift Swim"
    SAND_STREAM = 0x1C, "Sand Stream"
    SAND_VEIL = 0x1D, "Sand Veil"
    KEEN_EYE = 0x1E, "Keen Eye"
    INNER_FOCUS = 0x1F, "Inner Focus"
    STATIC = 0x20, "Static"
    SHED_SKIN = 0x21, "Shed Skin"
    HUGE_POWER = 0x22, "Huge Power"
    VOLT_ABSORB = 0x23, "Volt Absorb"
    WATER_ABSORB = 0x24, "Water Absorb"
    FORECAST = 0x25, "Forecast"
    SERENE_GRACE = 0x26, "Serene Grace"
    POISON_POINT = 0x27, "Poison Point"
    TRACE = 0x28, "Trace"
    OBLIVIOUS = 0x29, "Oblivious"
    TRUANT = 0x2A, "Truant"
    RUN_AWAY = 0x2B, "Run Away"
    STICKY_HOLD = 0x2C, "Sticky Hold"
    CLOUD_NINE = 0x2D, "Cloud Nine"
    ILLUMINATE = 0x2E, "Illuminate"
    EARLY_BIRD = 0x2F, "Early Bird"
    HUSTLE = 0x30, "Hustle"
    DROUGHT = 0x31, "Drought"
    LIGHTNINGROD = 0x32, "LightningRod"
    COMPOUNDEYES = 0x33, "CompoundEyes"
    MARVEL_SCALE = 0x34, "Marvel Scale"
    WONDER_GUARD = 0x35, "Wonder Guard"
    INSOMNIA = 0x36, "Insomnia"
    LEVITATE = 0x37, "Levitate"
    PLUS = 0x38, "Plus"
    PRESSURE = 0x39, "Pressure"
    LIQUID_OOZE = 0x3A, "Liquid Ooze"
    COLOR_CHANGE = 0x3B, "Color Change"
    SOUNDPROOF = 0x3C, "Soundproof"
    EFFECT_SPORE = 0x3D, "Effect Spore"
    FLAME_BODY = 0x3E, "Flame Body"
    MINUS = 0x3F, "Minus"
    OWN_TEMPO = 0x40, "Own Tempo"
    MAGMA_ARMOR = 0x41, "Magma Armor"
    WATER_VEIL = 0x42, "Water Veil"
    SWARM = 0x43, "Swarm"
    CUTE_CHARM = 0x44, "Cute Charm"
    IMMUNITY = 0x45, "Immunity"
    BLAZE = 0x46, "Blaze"
    PICKUP = 0x47, "Pickup"
    FLASH_FIRE = 0x48, "Flash Fire"
    VITAL_SPIRIT = 0x49, "Vital Spirit"
    CHLOROPHYLL = 0x4A, "Chlorophyll"
    PURE_POWER = 0x4B, "Pure Power"
    SHIELD_DUST = 0x4C, "Shield Dust"
    ICE_BODY = 0x4D, "Ice Body"
    STALL = 0x4E, "Stall"
    ANGER_POINT = 0x4F, "Anger Point"
    TINTED_LENS = 0x50, "Tinted Lens"
    HYDRATION = 0x51, "Hydration"
    FRISK = 0x52, "Frisk"
    MOLD_BREAKER = 0x53, "Mold Breaker"
    UNBURDEN = 0x54, "Unburden"
    DRY_SKIN = 0x55, "Dry Skin"
    ANTICIPATION = 0x56, "Anticipation"
    SCRAPPY = 0x57, "Scrappy"
    SUPER_LUCK = 0x58, "Super Luck"
    GLUTTONY = 0x59, "Gluttony"
    SOLAR_POWER = 0x5A, "Solar Power"
    SKILL_LINK = 0x5B, "Skill Link"
    RECKLESS = 0x5C, "Reckless"
    SNIPER = 0x5D, "Sniper"
    SLOW_START = 0x5E, "Slow Start"
    HEATPROOF = 0x5F, "Heatproof"
    DOWNLOAD = 0x60, "Download"
    SIMPLE = 0x61, "Simple"
    TANGLED_FEET = 0x62, "Tangled Feet"
    ADAPTABILITY = 0x63, "Adaptability"
    TECHNICIAN = 0x64, "Technician"
    IRON_FIST = 0x65, "Iron Fist"
    MOTOR_DRIVE = 0x66, "Motor Drive"
    UNAWARE = 0x67, "Unaware"
    RIVALRY = 0x68, "Rivalry"
    BAD_DREAMS = 0x69, "Bad Dreams"
    NO_GUARD = 0x6A, "No Guard"
    NORMALIZE = 0x6B, "Normalize"
    SOLID_ROCK = 0x6C, "Solid Rock"
    QUICK_FEET = 0x6D, "Quick Feet"
    FILTER = 0x6E, "Filter"
    KLUTZ = 0x6F, "Klutz"
    STEDFAST = 0x70, "Steadfast"
    FLOWER_GIFT = 0x71, "Flower Gift"
    POISION_HEAL = 0x72, "Poison Heal"
    MAGIC_GUARD = 0x73, "Magic Guard"
    # This is named $$$ in the NA/EU ROM and マルチタイプ in the JP ROM. It is Multitype.
    # But it's unused in the final game.
    MULTITYPE = 0x74, "Multitype"  # TRANSLATORS: Name of the ability.
    HONEY_GATHER = 0x75, "Honey Gather"
    AFTERMATH = 0x76, "Aftermath"
    SNOW_CLOAK = 0x77, "Snow Cloak"
    SNOW_WARNING = 0x78, "Snow Warning"
    FOREWARN = 0x79, "Forewarn"
    STORM_DRAIN = 0x7A, "Storm Drain"
    LEAF_GUARD = 0x7B, "Leaf Guard"
    UNUSED_0x7C = 0x7C, "Unused" + "_0x7C"
    UNUSED_0x7D = 0x7D, "Unused" + "_0x7D"
    UNUSED_0x7E = 0x7E, "Unused" + "_0x7E"
    UNUSED_0x7F = 0x7F, "Unused" + "_0x7F"
    UNUSED_0x80 = 0x80, "Unused" + "_0x80"
    UNUSED_0x81 = 0x81, "Unused" + "_0x81"
    UNUSED_0x82 = 0x82, "Unused" + "_0x82"
    UNUSED_0x83 = 0x83, "Unused" + "_0x83"
    UNUSED_0x84 = 0x84, "Unused" + "_0x84"
    UNUSED_0x85 = 0x85, "Unused" + "_0x85"
    UNUSED_0x86 = 0x86, "Unused" + "_0x86"
    UNUSED_0x87 = 0x87, "Unused" + "_0x87"
    UNUSED_0x88 = 0x88, "Unused" + "_0x88"
    UNUSED_0x89 = 0x89, "Unused" + "_0x89"
    UNUSED_0x8A = 0x8A, "Unused" + "_0x8A"
    UNUSED_0x8B = 0x8B, "Unused" + "_0x8B"
    UNUSED_0x8C = 0x8C, "Unused" + "_0x8C"
    UNUSED_0x8D = 0x8D, "Unused" + "_0x8D"
    UNUSED_0x8E = 0x8E, "Unused" + "_0x8E"
    UNUSED_0x8F = 0x8F, "Unused" + "_0x8F"
    UNUSED_0x90 = 0x90, "Unused" + "_0x90"
    UNUSED_0x91 = 0x91, "Unused" + "_0x91"
    UNUSED_0x92 = 0x92, "Unused" + "_0x92"
    UNUSED_0x93 = 0x93, "Unused" + "_0x93"
    UNUSED_0x94 = 0x94, "Unused" + "_0x94"
    UNUSED_0x95 = 0x95, "Unused" + "_0x95"
    UNUSED_0x96 = 0x96, "Unused" + "_0x96"
    UNUSED_0x97 = 0x97, "Unused" + "_0x97"
    UNUSED_0x98 = 0x98, "Unused" + "_0x98"
    UNUSED_0x99 = 0x99, "Unused" + "_0x99"
    UNUSED_0x9A = 0x9A, "Unused" + "_0x9A"
    UNUSED_0x9B = 0x9B, "Unused" + "_0x9B"
    UNUSED_0x9C = 0x9C, "Unused" + "_0x9C"
    UNUSED_0x9D = 0x9D, "Unused" + "_0x9D"
    UNUSED_0x9E = 0x9E, "Unused" + "_0x9E"
    UNUSED_0x9F = 0x9F, "Unused" + "_0x9F"
    UNUSED_0xA0 = 0xA0, "Unused" + "_0xA0"
    UNUSED_0xA1 = 0xA1, "Unused" + "_0xA1"
    UNUSED_0xA2 = 0xA2, "Unused" + "_0xA2"
    UNUSED_0xA3 = 0xA3, "Unused" + "_0xA3"
    UNUSED_0xA4 = 0xA4, "Unused" + "_0xA4"
    UNUSED_0xA5 = 0xA5, "Unused" + "_0xA5"
    UNUSED_0xA6 = 0xA6, "Unused" + "_0xA6"
    UNUSED_0xA7 = 0xA7, "Unused" + "_0xA7"
    UNUSED_0xA8 = 0xA8, "Unused" + "_0xA8"
    UNUSED_0xA9 = 0xA9, "Unused" + "_0xA9"
    UNUSED_0xAA = 0xAA, "Unused" + "_0xAA"
    UNUSED_0xAB = 0xAB, "Unused" + "_0xAB"
    UNUSED_0xAC = 0xAC, "Unused" + "_0xAC"
    UNUSED_0xAD = 0xAD, "Unused" + "_0xAD"
    UNUSED_0xAE = 0xAE, "Unused" + "_0xAE"
    UNUSED_0xAF = 0xAF, "Unused" + "_0xAF"
    UNUSED_0xB0 = 0xB0, "Unused" + "_0xB0"
    UNUSED_0xB1 = 0xB1, "Unused" + "_0xB1"
    UNUSED_0xB2 = 0xB2, "Unused" + "_0xB2"
    UNUSED_0xB3 = 0xB3, "Unused" + "_0xB3"
    UNUSED_0xB4 = 0xB4, "Unused" + "_0xB4"
    UNUSED_0xB5 = 0xB5, "Unused" + "_0xB5"
    UNUSED_0xB6 = 0xB6, "Unused" + "_0xB6"
    UNUSED_0xB7 = 0xB7, "Unused" + "_0xB7"
    UNUSED_0xB8 = 0xB8, "Unused" + "_0xB8"
    UNUSED_0xB9 = 0xB9, "Unused" + "_0xB9"
    UNUSED_0xBA = 0xBA, "Unused" + "_0xBA"
    UNUSED_0xBB = 0xBB, "Unused" + "_0xBB"
    UNUSED_0xBC = 0xBC, "Unused" + "_0xBC"
    UNUSED_0xBD = 0xBD, "Unused" + "_0xBD"
    UNUSED_0xBE = 0xBE, "Unused" + "_0xBE"
    UNUSED_0xBF = 0xBF, "Unused" + "_0xBF"
    UNUSED_0xC0 = 0xC0, "Unused" + "_0xC0"
    UNUSED_0xC1 = 0xC1, "Unused" + "_0xC1"
    UNUSED_0xC2 = 0xC2, "Unused" + "_0xC2"
    UNUSED_0xC3 = 0xC3, "Unused" + "_0xC3"
    UNUSED_0xC4 = 0xC4, "Unused" + "_0xC4"
    UNUSED_0xC5 = 0xC5, "Unused" + "_0xC5"
    UNUSED_0xC6 = 0xC6, "Unused" + "_0xC6"
    UNUSED_0xC7 = 0xC7, "Unused" + "_0xC7"
    UNUSED_0xC8 = 0xC8, "Unused" + "_0xC8"
    UNUSED_0xC9 = 0xC9, "Unused" + "_0xC9"
    UNUSED_0xCA = 0xCA, "Unused" + "_0xCA"
    UNUSED_0xCB = 0xCB, "Unused" + "_0xCB"
    UNUSED_0xCC = 0xCC, "Unused" + "_0xCC"
    UNUSED_0xCD = 0xCD, "Unused" + "_0xCD"
    UNUSED_0xCE = 0xCE, "Unused" + "_0xCE"
    UNUSED_0xCF = 0xCF, "Unused" + "_0xCF"
    UNUSED_0xD0 = 0xD0, "Unused" + "_0xD0"
    UNUSED_0xD1 = 0xD1, "Unused" + "_0xD1"
    UNUSED_0xD2 = 0xD2, "Unused" + "_0xD2"
    UNUSED_0xD3 = 0xD3, "Unused" + "_0xD3"
    UNUSED_0xD4 = 0xD4, "Unused" + "_0xD4"
    UNUSED_0xD5 = 0xD5, "Unused" + "_0xD5"
    UNUSED_0xD6 = 0xD6, "Unused" + "_0xD6"
    UNUSED_0xD7 = 0xD7, "Unused" + "_0xD7"
    UNUSED_0xD8 = 0xD8, "Unused" + "_0xD8"
    UNUSED_0xD9 = 0xD9, "Unused" + "_0xD9"
    UNUSED_0xDA = 0xDA, "Unused" + "_0xDA"
    UNUSED_0xDB = 0xDB, "Unused" + "_0xDB"
    UNUSED_0xDC = 0xDC, "Unused" + "_0xDC"
    UNUSED_0xDD = 0xDD, "Unused" + "_0xDD"
    UNUSED_0xDE = 0xDE, "Unused" + "_0xDE"
    UNUSED_0xDF = 0xDF, "Unused" + "_0xDF"
    UNUSED_0xE0 = 0xE0, "Unused" + "_0xE0"
    UNUSED_0xE1 = 0xE1, "Unused" + "_0xE1"
    UNUSED_0xE2 = 0xE2, "Unused" + "_0xE2"
    UNUSED_0xE3 = 0xE3, "Unused" + "_0xE3"
    UNUSED_0xE4 = 0xE4, "Unused" + "_0xE4"
    UNUSED_0xE5 = 0xE5, "Unused" + "_0xE5"
    UNUSED_0xE6 = 0xE6, "Unused" + "_0xE6"
    UNUSED_0xE7 = 0xE7, "Unused" + "_0xE7"
    UNUSED_0xE8 = 0xE8, "Unused" + "_0xE8"
    UNUSED_0xE9 = 0xE9, "Unused" + "_0xE9"
    UNUSED_0xEA = 0xEA, "Unused" + "_0xEA"
    UNUSED_0xEB = 0xEB, "Unused" + "_0xEB"
    UNUSED_0xEC = 0xEC, "Unused" + "_0xEC"
    UNUSED_0xED = 0xED, "Unused" + "_0xED"
    UNUSED_0xEE = 0xEE, "Unused" + "_0xEE"
    UNUSED_0xEF = 0xEF, "Unused" + "_0xEF"
    UNUSED_0xF0 = 0xF0, "Unused" + "_0xF0"
    UNUSED_0xF1 = 0xF1, "Unused" + "_0xF1"
    UNUSED_0xF2 = 0xF2, "Unused" + "_0xF2"
    UNUSED_0xF3 = 0xF3, "Unused" + "_0xF3"
    UNUSED_0xF4 = 0xF4, "Unused" + "_0xF4"
    UNUSED_0xF5 = 0xF5, "Unused" + "_0xF5"
    UNUSED_0xF6 = 0xF6, "Unused" + "_0xF6"
    UNUSED_0xF7 = 0xF7, "Unused" + "_0xF7"
    UNUSED_0xF8 = 0xF8, "Unused" + "_0xF8"
    UNUSED_0xF9 = 0xF9, "Unused" + "_0xF9"
    UNUSED_0xFA = 0xFA, "Unused" + "_0xFA"
    UNUSED_0xFB = 0xFB, "Unused" + "_0xFB"
    UNUSED_0xFC = 0xFC, "Unused" + "_0xFC"
    UNUSED_0xFD = 0xFD, "Unused" + "_0xFD"
    UNUSED_0xFE = 0xFE, "Unused" + "_0xFE"
    NONE = 0xFF, "NONE"
    NULL = 0x00, "NULL"

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, print_name: str | None = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f"Ability.{self.name}"

    @property
    def print_name(self) -> str:
        return self._print_name_


class IQGroup(Enum):
    A = 0x0, "A"
    B = 0x1, "B"
    C = 0x2, "C"
    D = 0x3, "D"
    E = 0x4, "E"
    F = 0x5, "F"
    G = 0x6, "G"
    H = 0x7, "H"
    UNUSED8 = 0x8, _("Unused") + " 8"
    UNUSED9 = 0x9, _("Unused") + " 9"
    I = 0xA, "I"
    J = 0xB, "J"
    UNUSEDC = 0xC, _("Unused") + " C"
    UNUSEDD = 0xD, _("Unused") + " D"
    UNUSEDE = 0xE, _("Unused") + " E"
    INVALID = 0xF, _("Invalid")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, print_name: str | None = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f"IQGroup.{self.name}"

    @property
    def print_name(self) -> str:
        return self._print_name_


class EvolutionMethod(Enum):
    NONE = 0, _("Not an Evolved Form.")
    LEVEL = 1, _("Level")
    IQ = 2, _("IQ")
    ITEMS = 3, _("Items")
    RECRUITED = 4, _("Recruited")
    NO_REQ = 5, _("No Main Requirement")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, print_name: str | None = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f"EvolutionMethod.{self.name}"

    @property
    def print_name(self) -> str:
        return self._print_name_


class AdditionalRequirement(Enum):
    NONE = 0, _("None")
    LINK_CABLE = 1, _("Link Cable")
    ATK_G_DEF = 2, _("Attack > Defense")
    ATK_L_DEF = 3, _("Attack < Defense")
    ATK_E_DEF = 4, _("Attack = Defense")
    SUN_RIBBON = 5, _("Sun Ribbon")
    LUNAR_RIBBON = 6, _("Lunar Ribbon")
    BEAUTY_SCARF = 7, _("Beauty Scarf")
    INT_VAL_1 = 8, _("Internal Value 0x1 = 1")
    INT_VAL_0 = 9, _("Internal Value 0x1 = 0")
    MALE = 10, _("Male (1st form)")
    FEMALE = 11, _("Female (2nd form)")
    ANCIENT_POWER = 12, _("Knows AncientPower")
    ROLLOUT = 13, _("Knows Rollout")
    DOUBLE_HIT = 14, _("Knows Double Hit")
    MIMIC = 15, _("Knows Mimic")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, print_name: str | None = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f"EvolutionMethod.{self.name}"

    @property
    def print_name(self) -> str:
        return self._print_name_


class MovementType(Enum):
    STANDARD = 0, _("Standard")
    UNKNOWN1 = 1, _("Unknown") + " 1"
    HOVERING = 2, _("Hovering")
    PHASE_THROUGH_WALLS = 3, _("Phase Through Walls")  # TRANSLATORS: Movement Type
    LAVA = 4, _("Lava")
    WATER = 5, _("Water")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, print_name: str | None = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f"MovementType.{self.name}"

    @property
    def print_name(self) -> str:
        return self._print_name_


class ShadowSize(Enum):
    SMALL = 0, _("Small")
    MEDIUM = 1, _("Medium")
    LARGE = 2, _("Large")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, print_name: str | None = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self) -> str:
        return self._print_name_

    def __repr__(self) -> str:
        return f"ShadowSize.{self.name}"

    @property
    def print_name(self) -> str:
        return self._print_name_


class MdEntryProtocol(Protocol):
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

    @classmethod
    @abstractmethod
    def new_empty(cls, entid: u16) -> MdEntryProtocol:
        ...

    @property
    @abstractmethod
    def md_index_base(self) -> int:
        ...


E = TypeVar("E", bound=MdEntryProtocol)


class MdProtocol(Protocol[E]):
    entries: Sequence[E]

    @abstractmethod
    def __init__(self, data: bytes):
        ...

    @abstractmethod
    def get_by_index(self, index: int) -> E:
        ...

    @abstractmethod
    def get_by_entity_id(self, index: int) -> list[tuple[int, E]]:
        ...

    @abstractmethod
    def __len__(self) -> int:
        ...

    @abstractmethod
    def __getitem__(self, key: int) -> E:
        ...

    @abstractmethod
    def __setitem__(self, key: int, value: E) -> None:
        ...

    @abstractmethod
    def __delitem__(self, key: int) -> None:
        ...

    @abstractmethod
    def __iter__(self) -> Iterator[E]:
        ...
