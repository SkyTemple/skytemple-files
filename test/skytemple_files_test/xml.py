#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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

import unittest
from abc import ABC
from xml.etree.ElementTree import Element

from skytemple_files.common.xml_util import prettify


class XmlTestCaseAbc(unittest.TestCase, ABC):
    def assertXmlEqual(self, xml1: str | Element, xml2: str | Element):
        from xmldiff import main

        xml1_text: str
        xml2_text: str
        if isinstance(xml1, str):
            with open(xml1, "r") as f:
                xml1_text = f.read()
        else:
            xml1_text = prettify(xml1)
        if isinstance(xml2, str):
            with open(xml2, "r") as f:
                xml2_text = f.read()
        else:
            xml2_text = prettify(xml2)
        diff = main.diff_texts(
            xml1_text,
            xml2_text,
            diff_options={"F": 0.5, "ratio_mode": "fast"},
        )
        if len(diff) < 1:
            return
        s = "\n".join((str(x) for x in diff))
        raise AssertionError(f"Expected XMLs to be equal. Differences from xml1 to xml2:\n{s}")
