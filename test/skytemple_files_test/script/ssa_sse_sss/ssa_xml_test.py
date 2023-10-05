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

import typing
from xml.etree import ElementTree

from range_typed_integers import IntegerBoundError

from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.common.xml_util import XmlValidateError
from skytemple_files.script.ssa_sse_sss.handler import SsaHandler
from skytemple_files.script.ssa_sse_sss.ssa_xml import ssa_to_xml, ssa_from_xml

from skytemple_files_test.case import fixpath, SkyTempleFilesTestCase, T
from skytemple_files_test.xml import XmlTestCaseAbc


class SsaXmlTestCase(SkyTempleFilesTestCase, XmlTestCaseAbc):
    handler = SsaHandler

    def test_export_valid_enter(self) -> None:
        self.do_test_export_valid(
            self._fix_path_xml("enter"), self._fix_path_model("enter")
        )

    def test_import_valid_enter(self) -> None:
        self.do_test_import_valid(
            self._fix_path_xml("enter"), self._fix_path_model("enter")
        )

    def test_export_valid_sub(self) -> None:
        self.do_test_export_valid(
            self._fix_path_xml("sub"), self._fix_path_model("sub")
        )

    def test_import_valid_sub(self) -> None:
        self.do_test_import_valid(
            self._fix_path_xml("sub"), self._fix_path_model("sub")
        )

    def test_export_valid_acting(self) -> None:
        self.do_test_export_valid(
            self._fix_path_xml("acting"), self._fix_path_model("acting")
        )

    def test_import_valid_acting(self) -> None:
        self.do_test_import_valid(
            self._fix_path_xml("acting"), self._fix_path_model("acting")
        )

    def do_test_export_valid(self, xml_path: str, ssx_path: str):
        self.assertXmlEqual(xml_path, ssa_to_xml(self._load_main_fixture(ssx_path)))

    def do_test_import_valid(self, xml_path: str, ssx_path: str):
        self.assertEqual(
            self._load_main_fixture(ssx_path),
            ssa_from_xml(
                ElementTree.parse(xml_path).getroot(),
                Pmd2XmlReader.load_default().script_data,
            ),
        )

    def test_import_invalid_integer(self) -> None:
        with self.assertRaises(ValueError):
            ssa_from_xml(
                ElementTree.parse(self._fix_path_xml("invalid_integer")).getroot(),
                Pmd2XmlReader.load_default().script_data,
            )

    def test_import_invalid_direction(self) -> None:
        with self.assertRaises(XmlValidateError):
            ssa_from_xml(
                ElementTree.parse(self._fix_path_xml("invalid_direction")).getroot(),
                Pmd2XmlReader.load_default().script_data,
            )

    def test_import_invalid_integer_range(self) -> None:
        with self.assertRaises(IntegerBoundError):
            ssa_from_xml(
                ElementTree.parse(
                    self._fix_path_xml("invalid_integer_range")
                ).getroot(),
                Pmd2XmlReader.load_default().script_data,
            )

    def test_import_invalid_integer_range2(self) -> None:
        with self.assertRaises(IntegerBoundError):
            ssa_from_xml(
                ElementTree.parse(
                    self._fix_path_xml("invalid_integer_range2")
                ).getroot(),
                Pmd2XmlReader.load_default().script_data,
            )

    def test_import_invalid_trigger_event(self) -> None:
        with self.assertRaises(XmlValidateError):
            ssa_from_xml(
                ElementTree.parse(
                    self._fix_path_xml("invalid_trigger_event")
                ).getroot(),
                Pmd2XmlReader.load_default().script_data,
            )

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_model(cls, name: str):
        return "fixtures", f"{name}.ssx"

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_xml(cls, name: str):
        return "fixtures", f"{name}.xml"
