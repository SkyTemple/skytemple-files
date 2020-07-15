#  Copyright 2020 Parakoopa
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

from skytemple_files.common.util import read_uintle, AutoString
from skytemple_files.common.xml_util import XmlSerializable, validate_xml_tag, XmlValidateError, validate_xml_attribs
from skytemple_files.dungeon_data.mappa_bin import XML_TRAP_LIST, XML_TRAP, XML_TRAP__NAME, XML_TRAP__CHANCE

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin.model import MappaBinReadContainer


class MappaTrapType(Enum):
    UNUSED = 0
    MUD_TRAP = 1
    STICKY_TRAP = 2
    GRIMY_TRAP = 3
    SUMMON_TRAP = 4
    PITFALL_TRAP = 5
    WARP_TRAP = 6
    GUST_TRAP = 7
    SPIN_TRAP = 8
    SLUMBER_TRAP = 9
    SLOW_TRAP = 10
    SEAL_TRAP = 11
    POISON_TRAP = 12
    SELFDESTRUCT_TRAP = 13
    EXPLOSION_TRAP = 14
    PP_ZERO_TRAP = 15
    CHESTNUT_TRAP = 16
    WONDER_TILE = 17
    POKEMON_TRAP = 18
    SPIKED_TILE = 19
    STEALTH_ROCK = 20
    TOXIC_SPIKES = 21
    TRIP_TRAP = 22
    RANDOM_TRAP = 23
    GRUDGE_TRAP = 24


class MappaTrapList(AutoString, XmlSerializable):
    def __init__(self, chances: Union[List[int], Dict[MappaTrapType, int]]):
        if isinstance(chances, list):
            if len(chances) != 25:
                raise ValueError("MappaTrapList constructor needs a chance value for all of the 25 traps.")
            self.chances = {}
            for i, value in enumerate(chances):
                self.chances[MappaTrapType(i)] = value
        elif isinstance(chances, dict):
            self.chances = chances
            if set((x.value for x in self.chances.keys())) != set(range(0, 25)):
                raise ValueError("MappaTrapList constructor needs a chance value for all of the 25 traps.")
        else:
            raise ValueError(f"Invalid type for MappaTrapList {type(chances)}")

    @classmethod
    def from_mappa(cls, read: 'MappaBinReadContainer', pointer: int) -> 'MappaTrapList':
        chances = []
        for i in range(pointer, pointer + 50, 2):
            chances.append(read_uintle(read.data, i, 2))
        return MappaTrapList(chances)

    def to_xml(self) -> Element:
        xml_trap_list = Element(XML_TRAP_LIST)
        for trap, chance in self.chances.items():
            xml_trap_list.append(Element(XML_TRAP, {
                XML_TRAP__NAME: str(trap.name),
                XML_TRAP__CHANCE: str(chance)
            }))
        return xml_trap_list

    @classmethod
    def from_xml(cls, ele: Element) -> 'XmlSerializable':
        validate_xml_tag(ele, XML_TRAP_LIST)
        chances = {}
        for child in ele:
            validate_xml_tag(child, XML_TRAP)
            validate_xml_attribs(child, [XML_TRAP__NAME, XML_TRAP__CHANCE])
            name = child.get(XML_TRAP__NAME)
            if not hasattr(MappaTrapType, name):
                raise XmlValidateError(f"Unknown trap {name}.")
            chances[getattr(MappaTrapType, name)] = int(child.get(XML_TRAP__CHANCE))
        try:
            return cls(chances)
        except ValueError as ex:
            raise XmlValidateError("Trap lists need an entry for all of the 25 traps") from ex

    def __eq__(self, other):
        if not isinstance(other, MappaTrapList):
            return False
        return self.chances == other.chances
