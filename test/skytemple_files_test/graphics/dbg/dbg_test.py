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
from skytemple_files.graphics.dbg import DBG_WIDTH_AND_HEIGHT
from skytemple_files.graphics.dbg.handler import DbgHandler
from skytemple_files.graphics.dbg.protocol import DbgProtocol
from skytemple_files_test.case import SkyTempleFilesTestCase, romtest, fixpath
from skytemple_files_test.graphics.mocks.dpc_mock import DpcMock
from skytemple_files_test.graphics.mocks.dpci_mock import DpciMock
from skytemple_files_test.graphics.mocks.dpl_mock import DplMock


class DbgTestCase(SkyTempleFilesTestCase[DbgHandler, DbgProtocol]):
    handler = DbgHandler

    def setUp(self) -> None:
        self.one: DbgProtocol = self._load_main_fixture(self._fix_path1())
        self.assertIsNotNone(self.one)

    def test_get_mappings(self):
        # fmt: off
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 9, 20, 21, 22, 23, 24, 24, 24, 24, 24, 24, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 24, 24, 24, 24, 24, 24, 24, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 60, 68, 69, 70, 56, 71, 72, 24, 24, 24, 24, 24, 24, 24, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 83, 84, 91, 92, 93, 94, 95, 24, 24, 24, 24, 24, 24, 24, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 107, 115, 116, 117, 118, 119, 24, 24, 24, 24, 24, 24, 24, 120, 121, 122, 123, 120, 121, 124, 125, 120, 121, 122, 123, 126, 127, 128, 129, 130, 131, 132, 123, 120, 121, 133, 134, 135, 24, 24, 24, 24, 24, 24, 24, 136, 137, 138, 139, 140, 141, 138, 139, 142, 143, 138, 139, 140, 141, 138, 139, 142, 143, 138, 139, 140, 141, 138, 139, 144, 24, 24, 24, 24, 24, 24, 24, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 147, 148, 149, 150, 151, 152, 153, 154, 147, 148, 149, 150, 151, 152, 155, 24, 24, 24, 24, 24, 24, 24, 156, 157, 158, 159, 160, 161, 7, 22, 162, 163, 18, 159, 164, 161, 7, 22, 162, 163, 18, 159, 160, 161, 7, 22, 23, 24, 24, 24, 24, 24, 24, 24, 165, 166, 31, 167, 168, 169, 31, 167, 170, 171, 172, 167, 168, 169, 31, 167, 173, 174, 175, 176, 177, 169, 31, 167, 178, 24, 24, 24, 24, 24, 24, 24, 179, 70, 56, 180, 179, 70, 56, 180, 179, 181, 182, 180, 179, 70, 56, 180, 179, 183, 184, 185, 186, 70, 56, 180, 187, 24, 24, 24, 24, 24, 24, 24, 188, 189, 190, 94, 188, 191, 192, 94, 188, 92, 193, 94, 188, 92, 194, 195, 188, 92, 193, 94, 188, 92, 196, 94, 95, 24, 24, 24, 24, 24, 24, 24, 197, 198, 199, 200, 197, 201, 202, 200, 197, 203, 204, 200, 197, 203, 204, 200, 197, 203, 204, 200, 205, 203, 206, 200, 207, 24, 24, 24, 24, 24, 24, 24, 168, 174, 31, 167, 168, 174, 31, 167, 168, 174, 31, 167, 168, 174, 31, 167, 168, 174, 31, 167, 168, 174, 31, 167, 178, 24, 24, 24, 24, 24, 24, 24, 179, 70, 56, 208, 179, 209, 56, 180, 179, 70, 56, 180, 179, 70, 56, 180, 179, 70, 56, 180, 179, 70, 210, 211, 187, 24, 24, 24, 24, 24, 24, 24, 188, 92, 193, 212, 213, 92, 193, 94, 188, 92, 193, 94, 188, 92, 193, 94, 188, 92, 193, 94, 188, 92, 214, 215, 95, 24, 24, 24, 24, 24, 24, 24, 216, 203, 204, 217, 218, 203, 204, 200, 197, 203, 204, 200, 197, 203, 204, 200, 197, 203, 204, 200, 197, 203, 204, 200, 207, 24, 24, 24, 24, 24, 24, 24, 168, 174, 31, 167, 168, 174, 31, 219, 168, 174, 31, 167, 168, 220, 31, 167, 168, 174, 31, 167, 168, 174, 31, 167, 178, 24, 24, 24, 24, 24, 24, 24, 179, 70, 56, 221, 179, 70, 56, 180, 179, 70, 56, 180, 179, 70, 56, 180, 179, 70, 56, 180, 179, 70, 222, 180, 187, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24], self.one.mappings)
        # fmt: on

    def test_set_mappings(self):
        new_mappings = list(x % 255 for x in range(0, 1024))
        self.one.mappings = new_mappings
        self.assertEqual(self.one.mappings, new_mappings)
        saved = self._save_and_reload_main_fixture(self.one)
        self.assertEqual(saved.mappings, new_mappings)

    def test_place_chunk(self):
        self.assertEqual(99, self.one.mappings[4 * DBG_WIDTH_AND_HEIGHT + 3])
        self.one.place_chunk(3, 4, 10)
        self.assertEqual(10, self.one.mappings[4 * DBG_WIDTH_AND_HEIGHT + 3])
        saved = self._save_and_reload_main_fixture(self.one)
        self.assertEqual(10, saved.mappings[4 * DBG_WIDTH_AND_HEIGHT + 3])

    def test_to_pil(self):
        self.assertImagesEqual(
            self._fix_path_expected(["to_pil.png"]),
            self.one.to_pil(
                DpcMock.make_for_dungeon_bg_one(),
                DpciMock.make_for_dungeon_bg_one(),
                DplMock.make_for_dungeon_bg_one().palettes,
            ),
        )

    def test_from_pil(self):
        pil = self._load_image(self._fix_path_from_pil())
        dpc_mock = DpcMock.make_empty_importable()
        dpci_mock = DpciMock.make_empty_importable()
        dpl_mock = DplMock.make_empty_importable()
        self.one.from_pil(dpc_mock, dpci_mock, dpl_mock, pil)
        self.assertImagesEqual(
            pil,
            self.one.to_pil(
                dpc_mock,
                dpci_mock,
                dpl_mock.palettes,
            ),
        )

    @romtest(file_names=["dungeon.bin"], path="DUNGEON/")
    def test_using_rom(self, _, file, pmd2_data):
        dbin_model = FileType.DUNGEON_BIN.deserialize(file, pmd2_data)
        for fn in dbin_model.get_files_with_ext("dbg"):
            try:
                model = self.handler.deserialize(dbin_model.get_raw(fn))
                model_reloaded = self._save_and_reload_main_fixture(model)
                self.assertEqual(model.mappings, model_reloaded.mappings)
            except Exception as e:
                raise AssertionError(f"failed processing file {fn}") from e

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path1(cls):
        return "fixtures", "bgone.dbg"

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_expected(cls, subpath):
        return "fixtures", "expected", *subpath

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_from_pil(cls):
        return "fixtures", "from_pil.png"
