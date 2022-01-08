#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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

from skytemple_files.graphics.bpa.handler import BpaHandler
from skytemple_files.graphics.bpa.protocol import BpaProtocol, BpaFrameInfoProtocol
from skytemple_files.test.case import SkyTempleFilesTestCase, fixpath


class BpaTestCase(SkyTempleFilesTestCase[BpaHandler, BpaProtocol[BpaFrameInfoProtocol]]):
    handler = BpaHandler

    def setUp(self) -> None:
        self.one = self._load_main_fixture(self._fix_path1())
        self.assertIsNotNone(self.one)
        self.two = self._load_main_fixture(self._fix_path2())
        self.assertIsNotNone(self.two)

    def test_frame_info(self) -> None:
        self.fail("Not implemented")

    def test_get_tile(self) -> None:
        self.fail("Not implemented")

    def test_tiles_to_pil_separate(self) -> None:
        self.fail("Not implemented")

    def test_pil_to_tiles(self) -> None:
        self.fail("Not implemented")

    def test_pil_to_tiles_separate(self) -> None:
        self.fail("Not implemented")

    def test_tiles_for_frame(self) -> None:
        self.fail("Not implemented")

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path1(cls):
        return '..', '..', 'test', 'fixtures', 'coco1.bpa'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path2(cls):
        return '..', '..', 'test', 'fixtures', 'coco2.bpa'
