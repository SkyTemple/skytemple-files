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

from skytemple_files.graphics.bpl.handler import BplHandler
from skytemple_files.graphics.bpl.protocol import BplProtocol, BplAnimationSpecProtocol
from skytemple_files.test.case import SkyTempleFilesTestCase, fixpath


class BplTestCase(SkyTempleFilesTestCase[BplHandler, BplProtocol[BplAnimationSpecProtocol]]):
    handler = BplHandler

    def setUp(self) -> None:
        self.one = self._load_main_fixture(self._fix_path1())
        self.assertIsNotNone(self.one)
        self.two = self._load_main_fixture(self._fix_path2())
        self.assertIsNotNone(self.two)

    def test_animation_specs(self) -> None:
        self.fail("Not implemented")

    def test_import_palettes(self) -> None:
        self.fail("Not implemented")

    def test_apply_palette_animations(self) -> None:
        self.fail("Not implemented")

    def test_is_palette_affected_by_animation(self) -> None:
        self.fail("Not implemented")

    def test_get_real_palettes(self) -> None:
        self.fail("Not implemented")

    def test_set_palettes(self) -> None:
        self.fail("Not implemented")

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path1(cls):
        return '..', '..', 'test', 'fixtures', 'coco.bpl'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path2(cls):
        return 'fixtures', 'two.bpl'
