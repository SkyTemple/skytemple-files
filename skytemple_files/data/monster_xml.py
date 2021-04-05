"""
XML export / import for MD, WAZA_P and LEVEL_BIN_ENTRY.
Theoretically compatible with ppmdu, but contains some new field names for some things.
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
from abc import ABC, abstractmethod
from base64 import b64encode, b64decode
from typing import Optional, List, Tuple, Dict, Generic, TypeVar
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from skytemple_files.common.xml_util import validate_xml_tag, XmlValidateError
from skytemple_files.data.level_bin_entry.model import LevelBinEntry, LevelEntry
from skytemple_files.data.md.model import Md, MdEntry, EvolutionMethod, Gender, Ability, ShadowSize, PokeType, \
    AdditionalRequirement, MovementType, IQGroup
from skytemple_files.data.waza_p.model import MoveLearnset, LevelUpMove
from skytemple_files.graphics.kao.model import KaoImage
from skytemple_files.common.i18n_util import f, _


XML_MONSTER = "Pokemon"
XML_MONSTER__GAME_VERSION = "gameVersion"
XML_STRINGS = "Strings"
XML_STRINGS__NAME = "Name"
XML_STRINGS__CATEGORY = "Category"
XML_GENENT = "GenderedEntity"
XML_GENENT_ENTID = "PokeID"
XML_GENENT_UNK31 = "Unk31"
XML_GENENT_NATIONAL_POKEDEX_NUMBER = "PokedexNumber"
XML_GENENT_BASE_MOVEMENT_SPEED = "MovementSpeed"  # todo: this is still Unk1 in StatsUtil
XML_GENENT_EVOLUTION_REQ = "EvolutionReq"
XML_GENENT_EVOLUTION_REQ__PRE_EVO_INDEX = "PreEvoIndex"
XML_GENENT_EVOLUTION_REQ__EVO_METHOD = "Method"
XML_GENENT_EVOLUTION_REQ__EVO_PRAM1 = "Param1"
XML_GENENT_EVOLUTION_REQ__EVO_PRAM2 = "Param2"
XML_GENENT_SPRITE_INDEX = "SpriteIndex"
XML_GENENT_GENDER = "Gender"
XML_GENENT_BODY_SIZE = "BodySize"
XML_GENENT_TYPE_PRIMARY = "PrimaryType"
XML_GENENT_TYPE_SECONDARY = "SecondaryType"
XML_GENENT_MOVEMENT_TYPE = "MovementType"
XML_GENENT_IQ_GROUP = "IQGroup"
XML_GENENT_ABILITY_PRIMARY = "PrimaryAbility"
XML_GENENT_ABILITY_SECONDARY = "SecondaryAbility"
XML_GENENT_BITFLAG1 = "Bitfield"
XML_GENENT_BITFLAG1__UNK0 = "Unk0"
XML_GENENT_BITFLAG1__UNK1 = "Unk1"
XML_GENENT_BITFLAG1__UNK2 = "Unk2"
XML_GENENT_BITFLAG1__UNK3 = "Unk3"
XML_GENENT_BITFLAG1__UNK4 = "CanMove"
XML_GENENT_BITFLAG1__UNK5 = "Unk5"
XML_GENENT_BITFLAG1__UNK6 = "CanEvolve"
XML_GENENT_BITFLAG1__UNK7 = "ItemRequiredForSpawning"
XML_GENENT_EXP_YIELD = "ExpYield"
XML_GENENT_RECRUIT_RATE1 = "RecruitRate1"
XML_GENENT_RECRUIT_RATE2 = "RecruitRate2"
XML_GENENT_BASE_STATS = "BaseStats"
XML_GENENT_BASE_STATS__HP = "HP"
XML_GENENT_BASE_STATS__ATTACK = "Attack"
XML_GENENT_BASE_STATS__SP_ATTACK = "SpAttack"
XML_GENENT_BASE_STATS__DEFENSE = "Defense"
XML_GENENT_BASE_STATS__SP_DEFENSE = "SpDefense"
XML_GENENT_WEIGHT = "Weight"
XML_GENENT_SIZE = "Size"
XML_GENENT_UNK17 = "Unk17"
XML_GENENT_UNK18 = "Unk18"
XML_GENENT_SHADOW_SIZE = "ShadowSize"  # todo: this is still Unk19 in StatsUtil
XML_GENENT_CHANCE_SPAWN_ASLEEP = "AsleepChance"  # todo: this is still Unk20 in StatsUtil
XML_GENENT_HP_REGENERATION = "HpRegen"  # todo: this is still Unk21 in StatsUtil (lower)
XML_GENENT_UNK21H = "Unk21h"  # todo: this is still Unk21 in StatsUtil (higher)
XML_GENENT_BASE_FORM_INDEX = "BasePokemonIndex"
XML_GENENT_EXCLUSIVE_ITEMS = "ExclusiveItems"
XML_GENENT_EXCLUSIVE_ITEMS__ITEM_ID = "ItemID"
XML_GENENT_UNK27 = "Unk27"
XML_GENENT_UNK28 = "Unk28"
XML_GENENT_UNK29 = "Unk29"
XML_GENENT_UNK30 = "Unk30"
XML_MOVESET = "Moveset"
XML_MOVESET_LEVEL_UP = "LevelUpMoves"
XML_MOVESET_LEVEL_UP__LEARN = "Learn"
XML_MOVESET_LEVEL_UP__LEVEL = "Level"
XML_MOVESET_EGG = "EggMoves"
XML_MOVESET_HM_TM = "HmTmMoves"
XML_MOVESET__MOVE_ID = "MoveID"
XML_STATS_GROWTH = "StatsGrowth"
XML_STATS_GROWTH_LEVEL = "Level"
XML_STATS_GROWTH_LEVEL__REQUIRED_EXP = "RequiredExp"
XML_STATS_GROWTH_LEVEL__HP = "HP"
XML_STATS_GROWTH_LEVEL__ATTACK = "Attack"
XML_STATS_GROWTH_LEVEL__SP_ATTACK = "SpAttack"
XML_STATS_GROWTH_LEVEL__DEFENSE = "Defense"
XML_STATS_GROWTH_LEVEL__SP_DEFENSE = "SpDefense"
XML_PORTRAITS = "Portraits"
XML_PORTRAITS_PORTRAIT = "Portrait"
XML_PORTRAITS_PORTRAIT__IMAGE = "At4pxImage" #TODO: Change this to AtImage (could broke already exported xml data)
XML_PORTRAITS_PORTRAIT__PALETTE = "Palette"

XML_GENENT__MAP__SIMPLE = {
    XML_GENENT_ENTID: 'entid',
    XML_GENENT_UNK31: 'unk31',
    XML_GENENT_NATIONAL_POKEDEX_NUMBER: 'national_pokedex_number',
    XML_GENENT_BASE_MOVEMENT_SPEED: 'base_movement_speed',
    XML_GENENT_SPRITE_INDEX: 'sprite_index',
    XML_GENENT_GENDER: 'gender',
    XML_GENENT_BODY_SIZE: 'body_size',
    XML_GENENT_TYPE_PRIMARY: 'type_primary',
    XML_GENENT_TYPE_SECONDARY: 'type_secondary',
    XML_GENENT_MOVEMENT_TYPE: 'movement_type',
    XML_GENENT_IQ_GROUP: 'iq_group',
    XML_GENENT_ABILITY_PRIMARY: 'ability_primary',
    XML_GENENT_ABILITY_SECONDARY: 'ability_secondary',
    XML_GENENT_EXP_YIELD: 'exp_yield',
    XML_GENENT_RECRUIT_RATE1: 'recruit_rate1',
    XML_GENENT_RECRUIT_RATE2: 'recruit_rate2',
    XML_GENENT_WEIGHT: 'weight',
    XML_GENENT_SIZE: 'size',
    XML_GENENT_UNK17: 'unk17',
    XML_GENENT_UNK18: 'unk18',
    XML_GENENT_SHADOW_SIZE: 'shadow_size',
    XML_GENENT_CHANCE_SPAWN_ASLEEP: 'chance_spawn_asleep',
    XML_GENENT_HP_REGENERATION: 'hp_regeneration',
    XML_GENENT_UNK21H: 'unk21_h',
    XML_GENENT_BASE_FORM_INDEX: 'base_form_index',
    XML_GENENT_UNK27: 'unk27',
    XML_GENENT_UNK28: 'unk28',
    XML_GENENT_UNK29: 'unk29',
    XML_GENENT_UNK30: 'unk30'
}
XML_GENENT__MAP__ENUMS = {
    'evo_method': EvolutionMethod,
    'gender': Gender,
    'type_primary': PokeType,
    'type_secondary': PokeType,
    'movement_type': MovementType,
    'iq_group': IQGroup,
    'ability_primary': Ability,
    'ability_secondary': Ability,
    'shadow_size': ShadowSize,
}

T = TypeVar('T')


def create_elem_w_text(tag, text, **attribs) -> Element:
    ele = Element(tag, **attribs)
    ele.text = str(text)
    return ele


class XmlConverter(Generic[T], ABC):
    @classmethod
    @abstractmethod
    def to_xml(cls, value: T) -> Element:
        pass

    @classmethod
    @abstractmethod
    def from_xml(cls, xml: Element, value_to_update: T):
        pass


class StringsXml(XmlConverter[Dict[str, Tuple[str, str]]]):

    @classmethod
    def to_xml(cls, values: T) -> Element:
        xml = Element(XML_STRINGS)
        for language, (name, category) in values.items():
            lang = Element(language)
            name_node = Element(XML_STRINGS__NAME)
            name_node.text = name
            category_node = Element(XML_STRINGS__CATEGORY)
            category_node.text = category
            lang.append(name_node)
            lang.append(category_node)
            xml.append(lang)
        return xml

    @classmethod
    def from_xml(cls, xml: Element, value_to_update: Dict[str, Tuple[str, str]]):
        for xml_lang in xml:
            if xml_lang.tag in value_to_update.keys():
                name = None
                category = None
                for xml_sub in xml_lang:
                    if xml_sub.tag == XML_STRINGS__NAME:
                        name = xml_sub.text
                    if xml_sub.tag == XML_STRINGS__CATEGORY:
                        category = xml_sub.text
                if name is None:
                    raise XmlValidateError(f(_("Invalid XML. '{XML_STRINGS__NAME}' missing for language {xml_lang.tag}.")))
                if category is None:
                    raise XmlValidateError(f(_("Invalid XML. '{XML_STRINGS__CATEGORY}' missing for language {xml_lang.tag}.")))
                value_to_update[xml_lang.tag] = (name, category)


class GenderedEntityXml(XmlConverter[MdEntry]):
    @classmethod
    def to_xml(cls, value: MdEntry) -> Element:
        xml = Element(XML_GENENT)
        for xml_name, attr_name in XML_GENENT__MAP__SIMPLE.items():
            attr_val = getattr(value, attr_name)
            if hasattr(attr_val, 'value'):
                attr_val = attr_val.value
            xml.append(create_elem_w_text(xml_name, attr_val))
        # Evolution requirements
        evo = Element(XML_GENENT_EVOLUTION_REQ)
        evo.append(create_elem_w_text(XML_GENENT_EVOLUTION_REQ__PRE_EVO_INDEX, value.pre_evo_index))
        evo.append(create_elem_w_text(XML_GENENT_EVOLUTION_REQ__EVO_METHOD, value.evo_method.value))
        evo.append(create_elem_w_text(XML_GENENT_EVOLUTION_REQ__EVO_PRAM1, value.evo_param1))
        evo.append(create_elem_w_text(XML_GENENT_EVOLUTION_REQ__EVO_PRAM2, value.evo_param2.value))
        xml.append(evo)
        # Base stats
        stats = Element(XML_GENENT_BASE_STATS)
        stats.append(create_elem_w_text(XML_GENENT_BASE_STATS__HP, value.base_hp))
        stats.append(create_elem_w_text(XML_GENENT_BASE_STATS__ATTACK, value.base_atk))
        stats.append(create_elem_w_text(XML_GENENT_BASE_STATS__SP_ATTACK, value.base_sp_atk))
        stats.append(create_elem_w_text(XML_GENENT_BASE_STATS__DEFENSE, value.base_def))
        stats.append(create_elem_w_text(XML_GENENT_BASE_STATS__SP_DEFENSE, value.base_sp_def))
        xml.append(stats)
        # Exclusive items
        items = Element(XML_GENENT_EXCLUSIVE_ITEMS)
        items.append(create_elem_w_text(XML_GENENT_EXCLUSIVE_ITEMS__ITEM_ID, value.exclusive_item1))
        items.append(create_elem_w_text(XML_GENENT_EXCLUSIVE_ITEMS__ITEM_ID, value.exclusive_item2))
        items.append(create_elem_w_text(XML_GENENT_EXCLUSIVE_ITEMS__ITEM_ID, value.exclusive_item3))
        items.append(create_elem_w_text(XML_GENENT_EXCLUSIVE_ITEMS__ITEM_ID, value.exclusive_item4))
        xml.append(items)
        # Bitfield
        items = Element(XML_GENENT_BITFLAG1)
        items.append(create_elem_w_text(XML_GENENT_BITFLAG1__UNK0, int(value.bitfield1_0)))
        items.append(create_elem_w_text(XML_GENENT_BITFLAG1__UNK1, int(value.bitfield1_1)))
        items.append(create_elem_w_text(XML_GENENT_BITFLAG1__UNK2, int(value.bitfield1_2)))
        items.append(create_elem_w_text(XML_GENENT_BITFLAG1__UNK3, int(value.bitfield1_3)))
        items.append(create_elem_w_text(XML_GENENT_BITFLAG1__UNK4, int(value.can_move)))
        items.append(create_elem_w_text(XML_GENENT_BITFLAG1__UNK5, int(value.bitfield1_5)))
        items.append(create_elem_w_text(XML_GENENT_BITFLAG1__UNK6, int(value.can_evolve)))
        items.append(create_elem_w_text(XML_GENENT_BITFLAG1__UNK7, int(value.item_required_for_spawning)))
        xml.append(items)
        return xml

    @classmethod
    def from_xml(cls, xml: Element, value_to_update: MdEntry):
        for sub_xml in xml:
            if sub_xml.tag in XML_GENENT__MAP__SIMPLE.keys():
                attr_name = XML_GENENT__MAP__SIMPLE[sub_xml.tag]
                if attr_name in XML_GENENT__MAP__ENUMS.keys():
                    # Enum
                    setattr(value_to_update, attr_name, XML_GENENT__MAP__ENUMS[attr_name](int(sub_xml.text)))
                else:
                    # Simple value
                    setattr(value_to_update, attr_name, int(sub_xml.text))
            if sub_xml.tag == XML_GENENT_EVOLUTION_REQ:
                pre_evo_index = None
                method = None
                param1 = None
                param2 = None
                for value_xml in sub_xml:
                    if value_xml.tag == XML_GENENT_EVOLUTION_REQ__PRE_EVO_INDEX:
                        pre_evo_index = int(value_xml.text)
                    elif value_xml.tag == XML_GENENT_EVOLUTION_REQ__EVO_METHOD:
                        method = EvolutionMethod(int(value_xml.text))
                    elif value_xml.tag == XML_GENENT_EVOLUTION_REQ__EVO_PRAM1:
                        param1 = int(value_xml.text)
                    elif value_xml.tag == XML_GENENT_EVOLUTION_REQ__EVO_PRAM2:
                        param2 = AdditionalRequirement(int(value_xml.text))
                if pre_evo_index is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_EVOLUTION_REQ__PRE_EVO_INDEX, XML_GENENT_EVOLUTION_REQ)
                    )
                if method is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_EVOLUTION_REQ__EVO_METHOD, XML_GENENT_EVOLUTION_REQ)
                    )
                if param1 is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_EVOLUTION_REQ__EVO_PRAM1, XML_GENENT_EVOLUTION_REQ)
                    )
                if param2 is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_EVOLUTION_REQ__EVO_PRAM2, XML_GENENT_EVOLUTION_REQ)
                    )
                value_to_update.pre_evo_index = pre_evo_index
                value_to_update.evo_method = method
                value_to_update.evo_param1 = param1
                value_to_update.evo_param2 = param2
            if sub_xml.tag == XML_GENENT_BASE_STATS:
                hp = None
                attack = None
                sp_attack = None
                defense = None
                sp_defense = None
                for value_xml in sub_xml:
                    if value_xml.tag == XML_GENENT_BASE_STATS__HP:
                        hp = int(value_xml.text)
                    elif value_xml.tag == XML_GENENT_BASE_STATS__ATTACK:
                        attack = int(value_xml.text)
                    elif value_xml.tag == XML_GENENT_BASE_STATS__SP_ATTACK:
                        sp_attack = int(value_xml.text)
                    elif value_xml.tag == XML_GENENT_BASE_STATS__DEFENSE:
                        defense = int(value_xml.text)
                    elif value_xml.tag == XML_GENENT_BASE_STATS__SP_DEFENSE:
                        sp_defense = int(value_xml.text)
                if hp is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_BASE_STATS__HP, XML_GENENT_BASE_STATS)
                    )
                if attack is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_BASE_STATS__ATTACK, XML_GENENT_BASE_STATS)
                    )
                if sp_attack is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_BASE_STATS__SP_ATTACK, XML_GENENT_BASE_STATS)
                    )
                if defense is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_BASE_STATS__DEFENSE, XML_GENENT_BASE_STATS)
                    )
                if sp_defense is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_STATS_GROWTH_LEVEL__SP_DEFENSE, XML_GENENT_BASE_STATS)
                    )
                value_to_update.base_hp = hp
                value_to_update.base_atk = attack
                value_to_update.base_sp_atk = sp_attack
                value_to_update.base_def = defense
                value_to_update.base_sp_def = sp_defense
            if sub_xml.tag == XML_GENENT_EXCLUSIVE_ITEMS:
                if len(sub_xml) != 4:
                    raise XmlValidateError(
                        f(_("Invalid XML. '{XML_GENENT_EXCLUSIVE_ITEMS}' needs four item IDs."))
                    )
                update = ('exclusive_item1', 'exclusive_item2', 'exclusive_item3', 'exclusive_item4')
                for item_xml, attr_name in zip(sub_xml, update):
                    validate_xml_tag(item_xml, XML_GENENT_EXCLUSIVE_ITEMS__ITEM_ID)
                    setattr(value_to_update, attr_name, int(item_xml.text))
            if sub_xml.tag == XML_GENENT_BITFLAG1:
                unk0 = None
                unk1 = None
                unk2 = None
                unk3 = None
                unk4 = None
                unk5 = None
                unk6 = None
                unk7 = None
                for value_xml in sub_xml:
                    if value_xml.tag == XML_GENENT_BITFLAG1__UNK0:
                        unk0 = bool(int(value_xml.text))
                    elif value_xml.tag == XML_GENENT_BITFLAG1__UNK1:
                        unk1 = bool(int(value_xml.text))
                    elif value_xml.tag == XML_GENENT_BITFLAG1__UNK2:
                        unk2 = bool(int(value_xml.text))
                    elif value_xml.tag == XML_GENENT_BITFLAG1__UNK3:
                        unk3 = bool(int(value_xml.text))
                    elif value_xml.tag == XML_GENENT_BITFLAG1__UNK4:
                        unk4 = bool(int(value_xml.text))
                    elif value_xml.tag == XML_GENENT_BITFLAG1__UNK5:
                        unk5 = bool(int(value_xml.text))
                    elif value_xml.tag == XML_GENENT_BITFLAG1__UNK6:
                        unk6 = bool(int(value_xml.text))
                    elif value_xml.tag == XML_GENENT_BITFLAG1__UNK7:
                        unk7 = bool(int(value_xml.text))
                if unk0 is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_BITFLAG1__UNK0, XML_GENENT_BASE_STATS)
                    )
                if unk1 is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_BITFLAG1__UNK1, XML_GENENT_BASE_STATS)
                    )
                if unk2 is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_BITFLAG1__UNK2, XML_GENENT_BASE_STATS)
                    )
                if unk3 is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_BITFLAG1__UNK3, XML_GENENT_BASE_STATS)
                    )
                if unk4 is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_BITFLAG1__UNK4, XML_GENENT_BASE_STATS)
                    )
                if unk5 is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_BITFLAG1__UNK5, XML_GENENT_BASE_STATS)
                    )
                if unk6 is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_BITFLAG1__UNK6, XML_GENENT_BASE_STATS)
                    )
                if unk7 is None:
                    raise XmlValidateError(
                        cls._missing_err(XML_GENENT_BITFLAG1__UNK7, XML_GENENT_BASE_STATS)
                    )
                value_to_update.bitfield1_0 = unk0
                value_to_update.bitfield1_1 = unk1
                value_to_update.bitfield1_2 = unk2
                value_to_update.bitfield1_3 = unk3
                value_to_update.can_move = unk4
                value_to_update.bitfield1_5 = unk5
                value_to_update.can_evolve = unk6
                value_to_update.item_required_for_spawning = unk7

    @classmethod
    def _missing_err(cls, a, b):
        return f(_("Invalid XML. '{a}' missing for a {b}."))


class MovesetXml(XmlConverter[MoveLearnset]):
    @classmethod
    def to_xml(cls, value: MoveLearnset) -> Element:
        xml = Element(XML_MOVESET)
        level_up = Element(XML_MOVESET_LEVEL_UP)
        for level_up_move in value.level_up_moves:
            learn = Element(XML_MOVESET_LEVEL_UP__LEARN)
            learn.append(create_elem_w_text(XML_MOVESET_LEVEL_UP__LEVEL, level_up_move.level_id))
            learn.append(create_elem_w_text(XML_MOVESET__MOVE_ID, level_up_move.move_id))
            level_up.append(learn)

        egg = Element(XML_MOVESET_EGG)
        for move_id in value.egg_moves:
            egg.append(create_elem_w_text(XML_MOVESET__MOVE_ID, move_id))
        hm_tm = Element(XML_MOVESET_HM_TM)
        for move_id in value.tm_hm_moves:
            hm_tm.append(create_elem_w_text(XML_MOVESET__MOVE_ID, move_id))

        xml.append(level_up)
        xml.append(egg)
        xml.append(hm_tm)
        return xml

    @classmethod
    def from_xml(cls, xml: Element, value_to_update: MoveLearnset):
        for xml_type in xml:
            if xml_type.tag == XML_MOVESET_LEVEL_UP:
                new_level_up = []
                for xml_learn in xml_type:
                    validate_xml_tag(xml_learn, XML_MOVESET_LEVEL_UP__LEARN)
                    level = None
                    move_id = None
                    for xml_level_or_move in xml_learn:
                        if xml_level_or_move.tag == XML_MOVESET_LEVEL_UP__LEVEL:
                            level = int(xml_level_or_move.text)
                        elif xml_level_or_move.tag == XML_MOVESET__MOVE_ID:
                            move_id = int(xml_level_or_move.text)
                    if level is None:
                        raise XmlValidateError(
                            f(_("Invalid XML. '{XML_MOVESET_LEVEL_UP__LEVEL}' missing for a level up moveset entry."))
                        )
                    if move_id is None:
                        raise XmlValidateError(
                            f(_("Invalid XML. '{XML_MOVESET__MOVE_ID}' missing for a level up moveset entry."))
                        )
                    new_level_up.append(LevelUpMove(move_id, level))
                value_to_update.level_up_moves = new_level_up
            elif xml_type.tag == XML_MOVESET_EGG:
                new_eggs = []
                for xml_move_id in xml_type:
                    validate_xml_tag(xml_move_id, XML_MOVESET__MOVE_ID)
                    new_eggs.append(int(xml_move_id.text))
                value_to_update.egg_moves = new_eggs
            elif xml_type.tag == XML_MOVESET_HM_TM:
                new_hm_tm = []
                for xml_move_id in xml_type:
                    validate_xml_tag(xml_move_id, XML_MOVESET__MOVE_ID)
                    new_hm_tm.append(int(xml_move_id.text))
                value_to_update.tm_hm_moves = new_hm_tm


class StatsGrowthXml(XmlConverter[LevelBinEntry]):
    @classmethod
    def to_xml(cls, value: LevelBinEntry) -> Element:
        xml = Element(XML_STATS_GROWTH)
        for level in value.levels:
            level_xml = Element(XML_STATS_GROWTH_LEVEL)
            level_xml.append(create_elem_w_text(XML_STATS_GROWTH_LEVEL__REQUIRED_EXP, level.experience_required))
            level_xml.append(create_elem_w_text(XML_STATS_GROWTH_LEVEL__HP, level.hp_growth))
            level_xml.append(create_elem_w_text(XML_STATS_GROWTH_LEVEL__ATTACK, level.attack_growth))
            level_xml.append(create_elem_w_text(XML_STATS_GROWTH_LEVEL__SP_ATTACK, level.special_attack_growth))
            level_xml.append(create_elem_w_text(XML_STATS_GROWTH_LEVEL__DEFENSE, level.defense_growth))
            level_xml.append(create_elem_w_text(XML_STATS_GROWTH_LEVEL__SP_DEFENSE, level.special_defense_growth))
            xml.append(level_xml)
        return xml

    # noinspection PyUnusedLocal
    @classmethod
    def from_xml(cls, xml: Element, value_to_update: LevelBinEntry):
        if len(xml) != 100:
            raise XmlValidateError(_("Invalid XML. StatsGrowth must have exactly 100 levels."))
        for i, xml_level in enumerate(xml):
            validate_xml_tag(xml_level, XML_STATS_GROWTH_LEVEL)
            required_exp = None
            hp = None
            attack = None
            sp_attack = None
            defense = None
            sp_defense = None
            for xml_stat in xml_level:
                if xml_stat.tag == XML_STATS_GROWTH_LEVEL__REQUIRED_EXP:
                    required_exp = int(xml_stat.text)
                elif xml_stat.tag == XML_STATS_GROWTH_LEVEL__HP:
                    hp = int(xml_stat.text)
                elif xml_stat.tag == XML_STATS_GROWTH_LEVEL__ATTACK:
                    attack = int(xml_stat.text)
                elif xml_stat.tag == XML_STATS_GROWTH_LEVEL__SP_ATTACK:
                    sp_attack = int(xml_stat.text)
                elif xml_stat.tag == XML_STATS_GROWTH_LEVEL__DEFENSE:
                    defense = int(xml_stat.text)
                elif xml_stat.tag == XML_STATS_GROWTH_LEVEL__SP_DEFENSE:
                    sp_defense = int(xml_stat.text)
            if required_exp is None:
                x = XML_STATS_GROWTH_LEVEL__REQUIRED_EXP
                raise XmlValidateError(
                    f(_("Invalid XML. '{x}' missing for a stats growth level entry."))
                )
            if hp is None:
                x = XML_STATS_GROWTH_LEVEL__HP
                raise XmlValidateError(
                    f(_("Invalid XML. '{x}' missing for a stats growth level entry."))
                )
            if attack is None:
                x = XML_STATS_GROWTH_LEVEL__ATTACK
                raise XmlValidateError(
                    f(_("Invalid XML. '{x}' missing for a stats growth level entry."))
                )
            if sp_attack is None:
                x = XML_STATS_GROWTH_LEVEL__SP_ATTACK
                raise XmlValidateError(
                    f(_("Invalid XML. '{x}' missing for a stats growth level entry."))
                )
            if defense is None:
                x = XML_STATS_GROWTH_LEVEL__DEFENSE
                raise XmlValidateError(
                    f(_("Invalid XML. '{x}' missing for a stats growth level entry."))
                )
            if sp_defense is None:
                x = XML_STATS_GROWTH_LEVEL__SP_DEFENSE
                raise XmlValidateError(
                    f(_("Invalid XML. '{x}' missing for a stats growth level entry."))
                )
            value_to_update.levels[i] = LevelEntry(
                required_exp, hp, attack, sp_attack, defense, sp_defense, 0
            )


class PortraitsXml(XmlConverter[List[Optional[KaoImage]]]):
    @classmethod
    def to_xml(cls, values: List[Optional[KaoImage]]) -> Element:
        xml = Element(XML_PORTRAITS)
        for kao in values:
            kao_xml = Element(XML_PORTRAITS_PORTRAIT)
            if kao is not None:
                image = str(b64encode(kao.compressed_img_data), 'ascii')
                pal = str(b64encode(kao.pal_data), 'ascii')
                kao_xml.append(create_elem_w_text(XML_PORTRAITS_PORTRAIT__IMAGE, image))
                kao_xml.append(create_elem_w_text(XML_PORTRAITS_PORTRAIT__PALETTE, pal))
            xml.append(kao_xml)
        return xml

    @classmethod
    def from_xml(cls, xml: Element, value_to_update: List[Optional[KaoImage]]):
        if len(value_to_update) != len(xml):
            raise XmlValidateError(
                f(_("Incompatible XML. The number of portraits don't match with the expected value of {len(value_to_update)}"))
            )
        for i, xml_portrait in enumerate(xml):
            validate_xml_tag(xml_portrait, XML_PORTRAITS_PORTRAIT)
            if len(xml_portrait) > 0:
                image = None
                palette = None
                for xml_image_or_pal in xml_portrait:
                    if xml_image_or_pal.tag == XML_PORTRAITS_PORTRAIT__IMAGE:
                        image = xml_image_or_pal.text
                    elif xml_image_or_pal.tag == XML_PORTRAITS_PORTRAIT__PALETTE:
                        palette = xml_image_or_pal.text
                if image is None:
                    raise XmlValidateError(
                        f(_("Invalid XML. '{XML_PORTRAITS_PORTRAIT__IMAGE}' missing for a portrait."))
                    )
                if palette is None:
                    raise XmlValidateError(
                        f(_("Invalid XML. '{XML_PORTRAITS_PORTRAIT__PALETTE}' missing for a portrait."))
                    )
                try:
                    value_to_update[i] = KaoImage(
                        b64decode(palette.encode('ascii')) + b64decode(image.encode('ascii')), 0
                    )
                except Exception as err:
                    raise XmlValidateError(
                        f(_("Invalid XML. The portrait data of one of the portraits is invalid: {err}"))
                    ) from err
            else:
                value_to_update[i] = None


def monster_xml_export(game_version: str, md_gender1: Optional[MdEntry], md_gender2: Optional[MdEntry],
                       names: Optional[Dict[str, Tuple[str, str]]],
                       moveset: Optional[MoveLearnset], moveset2: Optional[MoveLearnset],
                       stats: Optional[LevelBinEntry],
                       portraits: Optional[List[KaoImage]], portraits2: Optional[List[KaoImage]]
                       ) -> ElementTree:
    """
    Exports properties of all given things as an XML file. If a second Md entry is given,
    the first must also be given.
    Names are a dict wher each key is the language and values are (Name, Category).
    """
    xml = Element(XML_MONSTER, {XML_MONSTER__GAME_VERSION: game_version})
    if names:
        xml.append(StringsXml.to_xml(names))
    if md_gender1:
        xml.append(GenderedEntityXml.to_xml(md_gender1))
    if md_gender2:
        xml.append(GenderedEntityXml.to_xml(md_gender2))
    if moveset:
        xml.append(MovesetXml.to_xml(moveset))
    if moveset2:
        xml.append(MovesetXml.to_xml(moveset2))
    if stats:
        xml.append(StatsGrowthXml.to_xml(stats))
    if portraits:
        xml.append(PortraitsXml.to_xml(portraits))
    if portraits2:
        xml.append(PortraitsXml.to_xml(portraits2))
    return xml


def monster_xml_import(xml: ElementTree,
                       md_gender1: Optional[MdEntry], md_gender2: Optional[MdEntry],
                       names: Optional[Dict[str, Tuple[str, str]]],
                       moveset: Optional[MoveLearnset], moveset2: Optional[MoveLearnset],
                       stats: Optional[LevelBinEntry],
                       portraits: Optional[List[KaoImage]], portraits2: Optional[List[KaoImage]]) -> str:
    """
    Imports the available data from the XML into the models and lists given.
    The lists can already be filled, they will be cleared and re-filled when data is avaiable.
    Returns the game version.
    """
    genent_counter = 1 if md_gender1 is None and len([s for s in xml if s.tag == XML_GENENT]) == 1 else 0
    moveset_counter = 0
    portraits_counter = 1 if portraits is None and len([s for s in xml if s.tag == XML_PORTRAITS]) == 1 else 0
    for sub_node in xml:
        if sub_node.tag == XML_GENENT:
            if genent_counter == 0:
                genent_counter += 1
                if md_gender1:
                    GenderedEntityXml.from_xml(sub_node, md_gender1)
            elif genent_counter == 1:
                genent_counter += 1
                if md_gender2:
                    GenderedEntityXml.from_xml(sub_node, md_gender2)
        elif sub_node.tag == XML_STRINGS:
            if names:
                StringsXml.from_xml(sub_node, names)
        elif sub_node.tag == XML_MOVESET:
            if moveset_counter == 0:
                moveset_counter += 1
                if moveset:
                    MovesetXml.from_xml(sub_node, moveset)
            elif moveset_counter == 1:
                moveset_counter += 1
                if moveset2:
                    MovesetXml.from_xml(sub_node, moveset2)
        elif sub_node.tag == XML_STATS_GROWTH:
            if stats:
                StatsGrowthXml.from_xml(sub_node, stats)
        elif sub_node.tag == XML_PORTRAITS:
            if portraits_counter == 0:
                portraits_counter += 1
                if portraits:
                    PortraitsXml.from_xml(sub_node, portraits)
            elif portraits_counter == 1:
                portraits_counter += 1
                if portraits2:
                    PortraitsXml.from_xml(sub_node, portraits2)
    return xml.attrib[XML_MONSTER__GAME_VERSION]
