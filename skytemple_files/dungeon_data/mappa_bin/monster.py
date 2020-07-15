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
from typing import TYPE_CHECKING, List
from xml.etree.ElementTree import Element

from skytemple_files.common.util import read_uintle, AutoString
from skytemple_files.common.xml_util import XmlSerializable, validate_xml_tag, validate_xml_attribs
from skytemple_files.dungeon_data.mappa_bin import *

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin.model import MappaBinReadContainer
DUMMY_MD_INDEX = 0x229
LEVEL_MULTIPLIER = 512


class MappaMonster(AutoString, XmlSerializable):
    def __init__(self, level: int, spawn_weight: int, spawn_weight2: int, md_index: id):
        self.level = level
        self.spawn_weight = spawn_weight
        self.spawn_weight2 = spawn_weight2
        self.md_index = md_index

    @classmethod
    def list_from_mappa(cls, read: 'MappaBinReadContainer', pointer: int) -> List['MappaMonster']:
        monsters = []
        while not cls._is_dummy_entry(read.data, pointer):
            monsters.append(MappaMonster(
                int(read_uintle(read.data, pointer + 0, 2) / LEVEL_MULTIPLIER),
                read_uintle(read.data, pointer + 2, 2),
                read_uintle(read.data, pointer + 4, 2),
                read_uintle(read.data, pointer + 6, 2),
            ))
            pointer += 8
        return monsters

    @classmethod
    def _is_dummy_entry(cls, data: memoryview, pointer):
        return read_uintle(data, pointer + 6, 2) == DUMMY_MD_INDEX

    def to_xml(self) -> Element:
        return Element(XML_MONSTER, {
            XML_MONSTER__LEVEL: str(self.level),
            XML_MONSTER__SPAWN_WEIGHT: str(self.spawn_weight),
            XML_MONSTER__SPAWN_WEIGHT2: str(self.spawn_weight2),
            XML_MONSTER__MD_INDEX: str(self.md_index),
        })

    @classmethod
    def from_xml(cls, ele: Element) -> 'MappaMonster':
        validate_xml_tag(ele, XML_MONSTER)
        validate_xml_attribs(ele, [
            XML_MONSTER__LEVEL, XML_MONSTER__SPAWN_WEIGHT, XML_MONSTER__SPAWN_WEIGHT2, XML_MONSTER__MD_INDEX
        ])
        return cls(
            int(ele.get(XML_MONSTER__LEVEL)),
            int(ele.get(XML_MONSTER__SPAWN_WEIGHT)),
            int(ele.get(XML_MONSTER__SPAWN_WEIGHT2)),
            int(ele.get(XML_MONSTER__MD_INDEX)),
        )

    def __eq__(self, other):
        if not isinstance(other, MappaMonster):
            return False
        return self.level == other.level \
            and self.spawn_weight == other.spawn_weight \
            and self.spawn_weight2 == other.spawn_weight2
