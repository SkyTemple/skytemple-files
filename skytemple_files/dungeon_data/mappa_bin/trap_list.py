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
from enum import Enum
from typing import TYPE_CHECKING, List, Dict, Union
from xml.etree.ElementTree import Element

from skytemple_files.common.util import read_uintle, AutoString, write_uintle
from skytemple_files.common.xml_util import XmlSerializable, validate_xml_tag, XmlValidateError, validate_xml_attribs
from skytemple_files.dungeon_data.mappa_bin import XML_TRAP_LIST, XML_TRAP, XML_TRAP__NAME, XML_TRAP__WEIGHT
from skytemple_files.common.i18n_util import f, _

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin.model import MappaBinReadContainer


class MappaTrapType(Enum):
    UNUSED = 0, _("Unused")
    MUD_TRAP = 1, _("Mud Trap")
    STICKY_TRAP = 2, _("Sticky Trap")
    GRIMY_TRAP = 3, _("Grimy Trap")
    SUMMON_TRAP = 4, _("Summon Trap")
    PITFALL_TRAP = 5, _("Pitfall Trap")
    WARP_TRAP = 6, _("Warp Trap")
    GUST_TRAP = 7, _("Gust Trap")
    SPIN_TRAP = 8, _("Spin Trap")
    SLUMBER_TRAP = 9, _("Slumber Trap")
    SLOW_TRAP = 10, _("Slow Trap")
    SEAL_TRAP = 11, _("Seal Trap")
    POISON_TRAP = 12, _("Poison Trap")
    SELFDESTRUCT_TRAP = 13, _("Selfdestruct Trap")
    EXPLOSION_TRAP = 14, _("Explosion Trap")
    PP_ZERO_TRAP = 15, _("Pp Zero Trap")
    CHESTNUT_TRAP = 16, _("Chestnut Trap")
    WONDER_TILE = 17, _("Wonder Tile")
    POKEMON_TRAP = 18, _("Pokemon Trap")
    SPIKED_TILE = 19, _("Spiked Tile")
    STEALTH_ROCK = 20, _("Stealth Rock")
    TOXIC_SPIKES = 21, _("Toxic Spikes")
    TRIP_TRAP = 22, _("Trip Trap")
    RANDOM_TRAP = 23, _("Random Trap")
    GRUDGE_TRAP = 24, _("Grudge Trap")

    @property
    def print_name(self):
        return self._print_name_

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, print_name: str = None):
        self._print_name_ = print_name

    def __str__(self):
        return self._print_name_

    def __repr__(self):
        return f'MappaTrapType.{self.name}'


class MappaTrapList(AutoString, XmlSerializable):
    def __init__(self, weights: Union[List[int], Dict[MappaTrapType, int]]):
        if isinstance(weights, list):
            if len(weights) != 25:
                raise ValueError("MappaTrapList constructor needs a weight value for all of the 25 traps.")
            self.weights = {}
            for i, value in enumerate(weights):
                self.weights[MappaTrapType(i)] = value
        elif isinstance(weights, dict):
            self.weights = weights
            if set((x.value for x in self.weights.keys())) != set(range(0, 25)):
                raise ValueError("MappaTrapList constructor needs a weight value for all of the 25 traps.")
        else:
            raise ValueError(f"Invalid type for MappaTrapList {type(weights)}")

    @classmethod
    def from_mappa(cls, read: 'MappaBinReadContainer', pointer: int) -> 'MappaTrapList':
        weights = []
        for i in range(pointer, pointer + 50, 2):
            weights.append(read_uintle(read.data, i, 2))
        return MappaTrapList(weights)

    def to_mappa(self):
        data = bytearray(50)
        for i in range(0, 25):
            write_uintle(data, self.weights[MappaTrapType(i)], i * 2, 2)
        return data

    def to_xml(self) -> Element:
        xml_trap_list = Element(XML_TRAP_LIST)
        for trap, weight in self.weights.items():
            xml_trap_list.append(Element(XML_TRAP, {
                XML_TRAP__NAME: str(trap.name),
                XML_TRAP__WEIGHT: str(weight)
            }))
        return xml_trap_list

    @classmethod
    def from_xml(cls, ele: Element) -> 'XmlSerializable':
        validate_xml_tag(ele, XML_TRAP_LIST)
        weights = {}
        for child in ele:
            validate_xml_tag(child, XML_TRAP)
            validate_xml_attribs(child, [XML_TRAP__NAME, XML_TRAP__WEIGHT])
            name = child.get(XML_TRAP__NAME)
            if not hasattr(MappaTrapType, name):
                raise XmlValidateError(f(_("Unknown trap {name}.")))
            weights[getattr(MappaTrapType, name)] = int(child.get(XML_TRAP__WEIGHT))
        try:
            return cls(weights)
        except ValueError as ex:
            raise XmlValidateError(_("Trap lists need an entry for all of the 25 traps")) from ex

    def __eq__(self, other):
        if not isinstance(other, MappaTrapList):
            return False
        return self.weights == other.weights
