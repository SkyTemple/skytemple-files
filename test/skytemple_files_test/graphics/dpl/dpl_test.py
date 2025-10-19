#  Copyright 2020-2025 SkyTemple Contributors
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

from skytemple_files.common.types.file_types import FileType
from skytemple_files.graphics.dpl.handler import DplHandler
from skytemple_files.graphics.dpl.protocol import DplProtocol
from skytemple_files_test.case import SkyTempleFilesTestCase, romtest, fixpath


class DplTestCase(SkyTempleFilesTestCase[DplHandler, DplProtocol]):
    handler = DplHandler

    def setUp(self) -> None:
        self.one: DplProtocol = self._load_main_fixture(self._fix_path1())
        self.assertIsNotNone(self.one)

    def test_get_palettes(self) -> None:
        # fmt: off
        self.assertEqual(
            [[111, 0, 0, 223, 103, 0, 223, 151, 7, 199, 0, 71, 183, 15, 79, 207, 71, 119, 223, 135, 159, 0, 87, 47, 7, 119, 63, 47, 159, 87, 87, 191, 103, 63, 127, 0, 79, 151, 0, 103, 167, 0, 127, 183, 0, 151, 207, 0], [111, 0, 0, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 167, 95, 0, 199, 119, 15, 215, 135, 39, 223, 159, 55, 175, 127, 15, 111, 119, 0, 63, 127, 0, 79, 151, 0, 103, 167, 0, 127, 183, 0, 151, 207, 0], [0, 255, 0, 159, 55, 0, 231, 111, 0, 255, 159, 15, 143, 111, 191, 207, 175, 239, 247, 215, 255, 223, 135, 0, 247, 215, 0, 255, 255, 0, 0, 111, 0, 0, 167, 0, 39, 183, 0, 71, 207, 0, 111, 231, 0, 143, 255, 0], [111, 0, 0, 31, 103, 47, 47, 127, 47, 63, 159, 47, 79, 183, 47, 103, 215, 47, 119, 239, 47, 135, 255, 47, 95, 23, 0, 119, 47, 0, 143, 71, 0, 63, 127, 0, 79, 151, 0, 103, 167, 0, 127, 183, 0, 151, 207, 0], [111, 0, 0, 31, 103, 47, 47, 127, 47, 63, 159, 47, 79, 183, 47, 103, 215, 47, 183, 15, 79, 207, 71, 119, 223, 135, 159, 95, 23, 0, 119, 47, 0, 143, 71, 0, 63, 127, 0, 79, 151, 0, 103, 167, 0, 127, 183, 0], [101, 101, 255, 31, 103, 47, 47, 127, 47, 63, 159, 47, 79, 183, 47, 103, 215, 47, 119, 239, 47, 135, 255, 47, 95, 23, 0, 119, 47, 0, 143, 71, 0, 0, 167, 0, 39, 183, 0, 71, 207, 0, 111, 231, 0, 143, 255, 0], [111, 0, 0, 31, 103, 47, 47, 127, 47, 63, 159, 47, 79, 183, 47, 103, 215, 47, 119, 239, 47, 135, 255, 47, 95, 23, 0, 119, 47, 0, 143, 71, 0, 207, 71, 0, 215, 111, 0, 223, 151, 7, 223, 47, 223, 223, 47, 223], [111, 0, 0, 31, 103, 47, 47, 127, 47, 63, 159, 47, 79, 183, 47, 103, 215, 47, 119, 239, 47, 135, 255, 47, 95, 23, 0, 119, 47, 0, 143, 71, 0, 183, 15, 79, 207, 71, 119, 223, 135, 159, 0, 167, 223, 0, 167, 223], [223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223], [223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223, 223, 47, 223], [255, 243, 0, 0, 7, 167, 0, 47, 175, 0, 79, 175, 0, 119, 183, 0, 151, 191, 31, 31, 95, 79, 47, 0, 111, 63, 15, 135, 95, 15, 127, 151, 207, 135, 167, 215, 143, 183, 223, 39, 183, 0, 71, 207, 0, 111, 231, 0], [255, 243, 0, 87, 111, 119, 127, 143, 151, 159, 175, 175, 199, 207, 207, 215, 223, 223, 239, 239, 239, 47, 95, 175, 79, 127, 215, 127, 175, 239, 183, 223, 255, 199, 238, 255, 23, 63, 135, 39, 183, 0, 71, 207, 0, 111, 231, 0]],
            self.one.palettes,
        )
        # fmt: on

    def test_set_palettes(self) -> None:
        new_pal = [
            [0] * 16 * 3,
            [0, 0, 0] + [1] * 15 * 3,
            [0, 0, 0] + [2] * 15 * 3,
            [0, 0, 0] + [3] * 15 * 3,
        ]
        self.one.palettes = new_pal * 3

        self.assertEqual(new_pal * 3, self.one.palettes)
        saved = self._save_and_reload_main_fixture(self.one)
        self.assertEqual(new_pal * 3, saved.palettes)

        self.one.palettes = list(new_pal)

        self.assertEqual(new_pal, self.one.palettes)
        saved = self._save_and_reload_main_fixture(self.one)
        self.assertEqual(new_pal, saved.palettes)

    @romtest(file_names=["dungeon.bin"], path="DUNGEON/")
    def test_using_rom(self, _, file, pmd2_data):
        dbin_model = FileType.DUNGEON_BIN.deserialize(file, pmd2_data)
        new_pal = [
            [0] * 16 * 3,
            [0, 0, 0] + [1] * 15 * 3,
            [0, 0, 0] + [2] * 15 * 3,
            [0, 0, 0] + [3] * 15 * 3,
        ]
        for fn in dbin_model.get_files_with_ext("dpl"):
            try:
                model = self.handler.deserialize(dbin_model.get_raw(fn))
                model_reloaded = self._save_and_reload_main_fixture(model)
                self.assertEqual(model.palettes, model_reloaded.palettes)
                model_reloaded.palettes = new_pal
                model_reloaded2 = self._save_and_reload_main_fixture(model_reloaded)
                self.assertNotEqual(model.palettes, model_reloaded2.palettes)
                self.assertEqual(model_reloaded.palettes, model_reloaded2.palettes)
            except Exception as e:
                raise AssertionError(f"failed processing file {fn}") from e

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path1(cls):
        return "fixtures", "one.dpl"
