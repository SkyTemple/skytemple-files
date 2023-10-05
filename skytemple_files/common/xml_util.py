"""Utility module for (de)serializing objects from and to XML."""
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

from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from skytemple_files.common.i18n_util import _, f


class XmlValidateError(ValueError):
    pass


def validate_xml_tag(ele: Element, tag: str):
    if ele.tag != tag:
        raise XmlValidateError(
            f(_("Invalid XML. Expected tag {tag}, got tag {ele.tag}."))
        )


def validate_xml_attribs(ele: Element, attribs: list[str]):
    for attrib in attribs:
        if attrib not in ele.attrib:
            raise XmlValidateError(
                f(_("Invalid XML. Expected attribute {attrib} for XML tag {ele.tag}."))
            )


def prettify(elem):
    rough_string = ElementTree.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
