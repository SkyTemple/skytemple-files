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
from typing import TYPE_CHECKING, List
from xml.etree.ElementTree import Element

from skytemple_files.common.util import read_uintle, AutoString, write_uintle
from skytemple_files.common.xml_util import XmlSerializable, validate_xml_tag, validate_xml_attribs
from skytemple_files.dungeon_data.mappa_bin import *

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin.model import MappaBinReadContainer
DUMMY_MD_INDEX = 0x229
LEVEL_MULTIPLIER = 512


class MappaMonster(AutoString, XmlSerializable):
    def __init__(self, level: int, weight: int, weight2: int, md_index: id):
        self.level = level
        self.weight = weight
        self.weight2 = weight2
        self.md_index = md_index

    @classmethod
    def list_from_mappa(cls, read: 'MappaBinReadContainer', pointer: int) -> List['MappaMonster']:
        monsters = []
        while not cls._is_end_of_entries(read.data, pointer):
            monsters.append(MappaMonster(
                int(read_uintle(read.data, pointer + 0, 2) / LEVEL_MULTIPLIER),
                read_uintle(read.data, pointer + 2, 2),
                read_uintle(read.data, pointer + 4, 2),
                read_uintle(read.data, pointer + 6, 2),
            ))
            pointer += 8
        return monsters

    def to_mappa(self):
        data = bytearray(8)
        write_uintle(data, self.level * LEVEL_MULTIPLIER, 0x00, 2)
        write_uintle(data, self.weight, 0x02, 2)
        write_uintle(data, self.weight2, 0x04, 2)
        write_uintle(data, self.md_index, 0x06, 2)
        return data

    @classmethod
    def _is_end_of_entries(cls, data: memoryview, pointer):
        return read_uintle(data, pointer + 6, 2) == 0

    def to_xml(self) -> Element:
        return Element(XML_MONSTER, {
            XML_MONSTER__LEVEL: str(self.level),
            XML_MONSTER__WEIGHT: str(self.weight),
            XML_MONSTER__WEIGHT2: str(self.weight2),
            XML_MONSTER__MD_INDEX: str(self.md_index),
        })

    @classmethod
    def from_xml(cls, ele: Element) -> 'MappaMonster':
        validate_xml_tag(ele, XML_MONSTER)
        validate_xml_attribs(ele, [
            XML_MONSTER__LEVEL, XML_MONSTER__WEIGHT, XML_MONSTER__WEIGHT2, XML_MONSTER__MD_INDEX
        ])
        return cls(
            int(ele.get(XML_MONSTER__LEVEL)),
            int(ele.get(XML_MONSTER__WEIGHT)),
            int(ele.get(XML_MONSTER__WEIGHT2)),
            int(ele.get(XML_MONSTER__MD_INDEX)),
        )

    def __eq__(self, other):
        if not isinstance(other, MappaMonster):
            return False
        return self.md_index == other.md_index \
               and self.level == other.level \
               and self.weight == other.weight \
               and self.weight2 == other.weight2
