#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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

from skytemple_files.graphics.bg_list_dat.handler import BgListDatHandler
from skytemple_files.graphics.bg_list_dat.protocol import BgListProtocol, BgListEntryProtocol
from skytemple_files.test.case import SkyTempleFilesTestCase, fixpath


class BgListDatTestCase(SkyTempleFilesTestCase[BgListDatHandler, BgListProtocol[BgListEntryProtocol]]):
    handler = BgListDatHandler

    def setUp(self) -> None:
        self.bg_list = self._load_main_fixture(self._fix_path_bg_list())
        self.assertIsNotNone(self.bg_list)

    def test_read(self) -> None:
        self.fail("Not implemented")

    def test_write(self) -> None:
        self.fail("Not implemented")

    def test_get_bpl(self) -> None:
        self.fail("Not implemented")

    def test_get_bpc(self) -> None:
        self.fail("Not implemented")

    def test_get_bma(self) -> None:
        self.fail("Not implemented")

    def test_get_bpas(self) -> None:
        self.fail("Not implemented")

    def test_find_bma(self) -> None:
        self.fail("Not implemented")

    def test_find_bpl(self) -> None:
        self.fail("Not implemented")

    def test_find_bpc(self) -> None:
        self.fail("Not implemented")

    def test_find_bpa(self) -> None:
        self.fail("Not implemented")

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_bg_list(cls) -> str:
        return 'fixtures', 'bg_list.dat'
