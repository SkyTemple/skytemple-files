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
import typing

from skytemple_files.common.types.file_types import FileType
from skytemple_files.graphics.dma.handler import DmaHandler
from skytemple_files.graphics.dma.protocol import DmaProtocol, DmaType, DmaExtraType
from skytemple_files.graphics.dma.util import get_tile_neighbors
from skytemple_files_test.case import SkyTempleFilesTestCase, romtest, fixpath


class DmaTestCase(SkyTempleFilesTestCase[DmaHandler, DmaProtocol]):
    handler = DmaHandler

    def setUp(self) -> None:
        self.one: DmaProtocol = self._load_main_fixture(self._fix_path1())
        self.assertIsNotNone(self.one)
        self.two: DmaProtocol = self._load_main_fixture(self._fix_path2())
        self.assertIsNotNone(self.two)

    def test_get_chunk_mappings(self):
        # fmt: off
        self.assertEqual([12, 12, 12, 18, 18, 18, 12, 12, 12, 31, 31, 31, 23, 23, 23, 5, 5, 5, 31, 31, 31, 2, 2, 2, 12, 12, 12, 18, 18, 18, 12, 12, 12, 31, 31, 31, 31, 31, 31, 5, 5, 5, 31, 31, 31, 2, 2, 2, 30, 30, 30, 11, 11, 11, 30, 30, 30, 30, 30, 30, 17, 17, 17, 29, 29, 29, 17, 17, 17, 40, 40, 40, 31, 31, 31, 18, 18, 18, 31, 31, 31, 31, 31, 31, 14, 14, 14, 34, 34, 34, 14, 14, 14, 8, 147, 157, 12, 12, 12, 18, 18, 18, 12, 12, 12, 31, 31, 31, 23, 23, 23, 5, 5, 5, 31, 31, 31, 2, 2, 2, 12, 12, 12, 18, 18, 18, 12, 12, 12, 31, 31, 31, 31, 31, 31, 5, 5, 5, 31, 31, 31, 2, 2, 2, 31, 31, 31, 18, 18, 18, 31, 31, 31, 31, 31, 31, 17, 17, 17, 29, 29, 29, 17, 17, 17, 40, 40, 40, 31, 31, 31, 18, 18, 18, 31, 31, 31, 31, 31, 31, 14, 14, 14, 34, 34, 34, 14, 14, 14, 8, 147, 157, 25, 25, 25, 7, 7, 7, 25, 25, 25, 7, 7, 7, 6, 6, 6, 22, 22, 22, 25, 25, 25, 37, 37, 37, 25, 25, 25, 7, 7, 7, 25, 25, 25, 7, 7, 7, 25, 25, 25, 22, 22, 22, 25, 25, 25, 37, 37, 37, 13, 13, 13, 31, 31, 31, 13, 13, 13, 31, 31, 31, 28, 28, 28, 24, 24, 24, 28, 28, 28, 44, 44, 44, 13, 13, 13, 31, 31, 31, 13, 13, 13, 31, 31, 31, 43, 43, 43, 46, 46, 46, 43, 43, 43, 21, 152, 162, 31, 31, 31, 7, 7, 7, 31, 31, 31, 7, 7, 7, 23, 23, 23, 22, 22, 22, 31, 31, 31, 37, 37, 37, 31, 31, 31, 7, 7, 7, 31, 31, 31, 7, 7, 7, 31, 31, 31, 22, 22, 22, 31, 31, 31, 37, 37, 37, 16, 16, 16, 35, 35, 35, 16, 16, 16, 35, 35, 35, 42, 42, 42, 47, 47, 47, 42, 42, 42, 49, 49, 49, 16, 16, 16, 35, 35, 35, 16, 16, 16, 35, 35, 35, 15, 150, 160, 27, 154, 164, 15, 150, 160, 33, 33, 33, 12, 12, 12, 31, 31, 31, 12, 12, 12, 31, 31, 31, 23, 23, 23, 5, 5, 5, 31, 31, 31, 2, 2, 2, 12, 12, 12, 31, 31, 31, 12, 12, 12, 31, 31, 31, 31, 31, 31, 5, 5, 5, 31, 31, 31, 2, 2, 2, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 17, 17, 17, 29, 29, 29, 17, 17, 17, 40, 40, 40, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 14, 14, 14, 34, 34, 34, 14, 14, 14, 8, 147, 157, 12, 12, 12, 31, 31, 31, 12, 12, 12, 31, 31, 31, 23, 23, 23, 5, 5, 5, 31, 31, 31, 2, 2, 2, 12, 12, 12, 31, 31, 31, 12, 12, 12, 31, 31, 31, 31, 31, 31, 5, 5, 5, 31, 31, 31, 2, 2, 2, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 17, 17, 17, 29, 29, 29, 17, 17, 17, 40, 40, 40, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 14, 14, 14, 34, 34, 34, 14, 14, 14, 8, 147, 157, 31, 31, 31, 4, 4, 4, 31, 31, 31, 4, 4, 4, 23, 23, 23, 36, 36, 36, 31, 31, 31, 3, 146, 156, 31, 31, 31, 4, 4, 4, 31, 31, 31, 4, 4, 4, 31, 31, 31, 36, 36, 36, 31, 31, 31, 3, 146, 156, 13, 13, 13, 41, 41, 41, 13, 13, 13, 41, 41, 41, 28, 28, 28, 45, 45, 45, 28, 28, 28, 26, 153, 163, 13, 13, 13, 41, 41, 41, 13, 13, 13, 41, 41, 41, 43, 43, 43, 48, 48, 48, 43, 43, 43, 39, 39, 39, 31, 31, 31, 4, 4, 4, 31, 31, 31, 4, 4, 4, 23, 23, 23, 36, 36, 36, 31, 31, 31, 3, 146, 156, 31, 31, 31, 4, 4, 4, 31, 31, 31, 4, 4, 4, 31, 31, 31, 36, 36, 36, 31, 31, 31, 3, 146, 156, 16, 16, 16, 10, 149, 159, 16, 16, 16, 10, 149, 159, 42, 42, 42, 20, 151, 161, 42, 42, 42, 38, 38, 38, 16, 16, 16, 10, 149, 159, 16, 16, 16, 10, 149, 159, 15, 150, 160, 32, 32, 32, 15, 150, 160, 9, 148, 158, 60, 60, 60, 66, 66, 66, 60, 60, 60, 66, 66, 66, 71, 71, 71, 53, 53, 53, 71, 71, 71, 50, 50, 50, 60, 60, 60, 66, 66, 66, 60, 60, 60, 66, 66, 66, 71, 71, 71, 53, 53, 53, 71, 71, 71, 50, 50, 50, 78, 78, 78, 59, 59, 59, 78, 78, 78, 59, 59, 59, 65, 65, 65, 77, 77, 77, 65, 65, 65, 88, 88, 88, 78, 78, 78, 59, 59, 59, 78, 78, 78, 59, 59, 59, 62, 62, 62, 82, 82, 82, 62, 62, 62, 56, 56, 56, 60, 60, 60, 66, 66, 66, 60, 60, 60, 66, 66, 66, 71, 71, 71, 53, 53, 53, 71, 71, 71, 50, 50, 50, 60, 60, 60, 66, 66, 66, 60, 60, 60, 66, 66, 66, 71, 71, 71, 53, 53, 53, 71, 71, 71, 50, 50, 50, 78, 78, 78, 59, 59, 59, 78, 78, 78, 59, 59, 59, 65, 65, 65, 77, 77, 77, 65, 65, 65, 88, 88, 88, 78, 78, 78, 59, 59, 59, 78, 78, 78, 59, 59, 59, 62, 62, 62, 82, 82, 82, 62, 62, 62, 56, 56, 56, 73, 73, 73, 55, 55, 55, 73, 73, 73, 55, 55, 55, 54, 54, 54, 70, 70, 70, 54, 54, 54, 85, 85, 85, 73, 73, 73, 55, 55, 55, 73, 73, 73, 55, 55, 55, 54, 54, 54, 70, 70, 70, 54, 54, 54, 85, 85, 85, 61, 61, 61, 79, 79, 79, 61, 61, 61, 79, 79, 79, 76, 76, 76, 72, 72, 72, 76, 76, 76, 92, 92, 92, 61, 61, 61, 79, 79, 79, 61, 61, 61, 79, 79, 79, 91, 91, 91, 94, 94, 94, 91, 91, 91, 69, 69, 69, 73, 73, 73, 55, 55, 55, 73, 73, 73, 55, 55, 55, 54, 54, 54, 70, 70, 70, 54, 54, 54, 85, 85, 85, 73, 73, 73, 55, 55, 55, 73, 73, 73, 55, 55, 55, 54, 54, 54, 70, 70, 70, 54, 54, 54, 85, 85, 85, 64, 64, 64, 83, 83, 83, 64, 64, 64, 83, 83, 83, 90, 90, 90, 95, 95, 95, 90, 90, 90, 97, 97, 97, 64, 64, 64, 83, 83, 83, 64, 64, 64, 83, 83, 83, 63, 63, 63, 75, 75, 75, 63, 63, 63, 81, 81, 81, 60, 60, 60, 66, 66, 66, 60, 60, 60, 66, 66, 66, 71, 71, 71, 53, 53, 53, 71, 71, 71, 50, 50, 50, 60, 60, 60, 66, 66, 66, 60, 60, 60, 66, 66, 66, 71, 71, 71, 53, 53, 53, 71, 71, 71, 50, 50, 50, 78, 78, 78, 59, 59, 59, 78, 78, 78, 59, 59, 59, 65, 65, 65, 77, 77, 77, 65, 65, 65, 88, 88, 88, 78, 78, 78, 59, 59, 59, 78, 78, 78, 59, 59, 59, 62, 62, 62, 82, 82, 82, 62, 62, 62, 56, 56, 56, 60, 60, 60, 66, 66, 66, 60, 60, 60, 66, 66, 66, 71, 71, 71, 53, 53, 53, 71, 71, 71, 50, 50, 50, 60, 60, 60, 66, 66, 66, 60, 60, 60, 66, 66, 66, 71, 71, 71, 53, 53, 53, 71, 71, 71, 50, 50, 50, 78, 78, 78, 59, 59, 59, 78, 78, 78, 59, 59, 59, 65, 65, 65, 77, 77, 77, 65, 65, 65, 88, 88, 88, 78, 78, 78, 59, 59, 59, 78, 78, 78, 59, 59, 59, 62, 62, 62, 82, 82, 82, 62, 62, 62, 56, 56, 56, 73, 73, 73, 52, 52, 52, 73, 73, 73, 52, 52, 52, 54, 54, 54, 84, 84, 84, 54, 54, 54, 51, 51, 51, 73, 73, 73, 52, 52, 52, 73, 73, 73, 52, 52, 52, 54, 54, 54, 84, 84, 84, 54, 54, 54, 51, 51, 51, 61, 61, 61, 89, 89, 89, 61, 61, 61, 89, 89, 89, 76, 76, 76, 93, 93, 93, 76, 76, 76, 74, 74, 74, 61, 61, 61, 89, 89, 89, 61, 61, 61, 89, 89, 89, 91, 91, 91, 96, 96, 96, 91, 91, 91, 87, 87, 87, 73, 73, 73, 52, 52, 52, 73, 73, 73, 52, 52, 52, 54, 54, 54, 84, 84, 84, 54, 54, 54, 51, 51, 51, 73, 73, 73, 52, 52, 52, 73, 73, 73, 52, 52, 52, 54, 54, 54, 84, 84, 84, 54, 54, 54, 51, 51, 51, 64, 64, 64, 58, 58, 58, 64, 64, 64, 58, 58, 58, 90, 90, 90, 68, 68, 68, 90, 90, 90, 86, 86, 86, 64, 64, 64, 58, 58, 58, 64, 64, 64, 58, 58, 58, 63, 63, 63, 80, 80, 80, 63, 63, 63, 57, 57, 57, 108, 108, 108, 114, 114, 114, 108, 108, 108, 114, 114, 114, 119, 119, 119, 101, 101, 101, 119, 119, 119, 98, 98, 98, 108, 108, 108, 114, 114, 114, 108, 108, 108, 114, 114, 114, 119, 119, 119, 101, 101, 101, 119, 119, 119, 98, 98, 98, 126, 126, 126, 107, 107, 107, 126, 126, 126, 107, 107, 107, 113, 113, 113, 125, 125, 125, 113, 113, 113, 136, 136, 136, 126, 126, 126, 107, 107, 107, 126, 126, 126, 107, 107, 107, 110, 110, 110, 130, 130, 130, 110, 110, 110, 104, 104, 104, 108, 108, 108, 114, 114, 114, 108, 108, 108, 114, 114, 114, 119, 119, 119, 101, 101, 101, 119, 119, 119, 98, 98, 98, 108, 108, 108, 114, 114, 114, 108, 108, 108, 114, 114, 114, 119, 119, 119, 101, 101, 101, 119, 119, 119, 98, 98, 98, 126, 126, 126, 107, 107, 107, 126, 126, 126, 107, 107, 107, 113, 113, 113, 125, 125, 125, 113, 113, 113, 136, 136, 136, 126, 126, 126, 107, 107, 107, 126, 126, 126, 107, 107, 107, 110, 110, 110, 130, 130, 130, 110, 110, 110, 104, 104, 104, 121, 121, 121, 103, 103, 103, 121, 121, 121, 103, 103, 103, 102, 102, 102, 118, 118, 118, 102, 102, 102, 133, 133, 133, 121, 121, 121, 103, 103, 103, 121, 121, 121, 103, 103, 103, 102, 102, 102, 118, 118, 118, 102, 102, 102, 133, 133, 133, 109, 109, 109, 127, 127, 127, 109, 109, 109, 127, 127, 127, 124, 124, 124, 120, 120, 120, 124, 124, 124, 140, 140, 140, 109, 109, 109, 127, 127, 127, 109, 109, 109, 127, 127, 127, 139, 139, 139, 142, 142, 142, 139, 139, 139, 117, 117, 117, 121, 121, 121, 103, 103, 103, 121, 121, 121, 103, 103, 103, 102, 102, 102, 118, 118, 118, 102, 102, 102, 133, 133, 133, 121, 121, 121, 103, 103, 103, 121, 121, 121, 103, 103, 103, 102, 102, 102, 118, 118, 118, 102, 102, 102, 133, 133, 133, 112, 112, 112, 131, 131, 131, 112, 112, 112, 131, 131, 131, 138, 138, 138, 143, 143, 143, 138, 138, 138, 145, 145, 145, 112, 112, 112, 131, 131, 131, 112, 112, 112, 131, 131, 131, 111, 111, 111, 123, 123, 123, 111, 111, 111, 129, 129, 129, 108, 108, 108, 114, 114, 114, 108, 108, 108, 114, 114, 114, 119, 119, 119, 101, 101, 101, 119, 119, 119, 98, 98, 98, 108, 108, 108, 114, 114, 114, 108, 108, 108, 114, 114, 114, 119, 119, 119, 101, 101, 101, 119, 119, 119, 98, 98, 98, 126, 126, 126, 107, 107, 107, 126, 126, 126, 107, 107, 107, 113, 113, 113, 125, 125, 125, 113, 113, 113, 136, 136, 136, 126, 126, 126, 107, 107, 107, 126, 126, 126, 107, 107, 107, 110, 110, 110, 130, 130, 130, 110, 110, 110, 104, 104, 104, 108, 108, 108, 114, 114, 114, 108, 108, 108, 114, 114, 114, 119, 119, 119, 101, 101, 101, 119, 119, 119, 98, 98, 98, 108, 108, 108, 114, 114, 114, 108, 108, 108, 114, 114, 114, 119, 119, 119, 101, 101, 101, 119, 119, 119, 98, 98, 98, 126, 126, 126, 107, 107, 107, 126, 126, 126, 107, 107, 107, 113, 113, 113, 125, 125, 125, 113, 113, 113, 136, 136, 136, 126, 126, 126, 107, 107, 107, 126, 126, 126, 107, 107, 107, 110, 110, 110, 130, 130, 130, 110, 110, 110, 104, 104, 104, 121, 121, 121, 100, 100, 100, 121, 121, 121, 100, 100, 100, 102, 102, 102, 132, 132, 132, 102, 102, 102, 99, 99, 99, 121, 121, 121, 100, 100, 100, 121, 121, 121, 100, 100, 100, 102, 102, 102, 132, 132, 132, 102, 102, 102, 99, 99, 99, 109, 109, 109, 137, 137, 137, 109, 109, 109, 137, 137, 137, 124, 124, 124, 141, 141, 141, 124, 124, 124, 122, 122, 122, 109, 109, 109, 137, 137, 137, 109, 109, 109, 137, 137, 137, 139, 139, 139, 144, 144, 144, 139, 139, 139, 135, 135, 135, 121, 121, 121, 100, 100, 100, 121, 121, 121, 100, 100, 100, 102, 102, 102, 132, 132, 132, 102, 102, 102, 99, 99, 99, 121, 121, 121, 100, 100, 100, 121, 121, 121, 100, 100, 100, 102, 102, 102, 132, 132, 132, 102, 102, 102, 99, 99, 99, 112, 112, 112, 106, 106, 106, 112, 112, 112, 106, 106, 106, 138, 138, 138, 116, 116, 116, 138, 138, 138, 134, 134, 134, 112, 112, 112, 106, 106, 106, 112, 112, 112, 106, 106, 106, 111, 111, 111, 128, 128, 128, 111, 111, 111, 105, 155, 165, 155, 9, 165, 105, 21, 105, 105, 162, 105, 105, 21, 105, 105, 152, 105, 105, 162, 105, 105, 21, 105, 105, 21, 105, 105, 152, 105, 105, 162, 105, 105, 21, 105, 105, 21, 105, 105, 152, 105, 105, 152, 105, 105, 162, 105, 105, 21, 105], self.one.chunk_mappings)
        # fmt: on

    def test_set_chunk_mappings(self):
        new_mappings = list(x % 255 for x in range(0, 2352))
        self.one.chunk_mappings = new_mappings
        self.assertEqual(self.one.chunk_mappings, new_mappings)
        saved = self._save_and_reload_main_fixture(self.one)
        self.assertEqual(saved.chunk_mappings, new_mappings)

    def test_get(self):
        neighbor_config1 = get_tile_neighbors(
            [[True, True, True], [False, False, False], [True, True, True]],
            1,
            1,
            True,
            True,
        )
        neighbor_config2 = get_tile_neighbors(
            [[True, False, True], [True, False, False], [True, False, False]],
            2,
            2,
            False,
            True,
        )
        neighbor_config3 = get_tile_neighbors(
            [[True, True, True], [True, True, True], [True, True, True]],
            1,
            2,
            True,
            True,
        )

        self.assertEqual([59, 59, 59], self.one.get(DmaType.WATER, neighbor_config1))
        self.assertEqual([64, 64, 64], self.one.get(DmaType.WATER, neighbor_config2))
        self.assertEqual([57, 57, 57], self.one.get(DmaType.WATER, neighbor_config3))
        self.assertEqual([31, 31, 31], self.one.get(DmaType.WALL, neighbor_config1))
        self.assertEqual([16, 16, 16], self.one.get(DmaType.WALL, neighbor_config2))
        self.assertEqual([9, 148, 158], self.one.get(DmaType.WALL, neighbor_config3))
        self.assertEqual([107, 107, 107], self.one.get(DmaType.FLOOR, neighbor_config1))
        self.assertEqual([112, 112, 112], self.one.get(DmaType.FLOOR, neighbor_config2))
        self.assertEqual([105, 155, 165], self.one.get(DmaType.FLOOR, neighbor_config3))

        self.assertEqual([57, 57, 57], self.two.get(DmaType.WATER, neighbor_config1))
        self.assertEqual([74, 74, 74], self.two.get(DmaType.WATER, neighbor_config2))
        self.assertEqual([95, 95, 95], self.two.get(DmaType.WATER, neighbor_config3))
        self.assertEqual([18, 18, 18], self.two.get(DmaType.WALL, neighbor_config1))
        self.assertEqual([4, 4, 4], self.two.get(DmaType.WALL, neighbor_config2))
        self.assertEqual([1, 13, 10], self.two.get(DmaType.WALL, neighbor_config3))
        self.assertEqual([94, 94, 94], self.two.get(DmaType.FLOOR, neighbor_config1))
        self.assertEqual([93, 93, 93], self.two.get(DmaType.FLOOR, neighbor_config2))
        self.assertEqual([23, 12, 12], self.two.get(DmaType.FLOOR, neighbor_config3))

    def test_get_extra(self):
        self.assertEqual(
            [
                155,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
            ],
            self.one.get_extra(DmaExtraType.FLOOR1),
        )
        self.assertEqual(
            [
                165,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
                105,
            ],
            self.one.get_extra(DmaExtraType.FLOOR2),
        )
        self.assertEqual(
            [9, 21, 162, 21, 152, 162, 21, 21, 152, 162, 21, 21, 152, 152, 162, 21],
            self.one.get_extra(DmaExtraType.WALL_OR_VOID),
        )
        self.assertEqual(
            [9, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23],
            self.two.get_extra(DmaExtraType.FLOOR1),
        )
        self.assertEqual(
            [12, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23],
            self.two.get_extra(DmaExtraType.FLOOR2),
        )
        self.assertEqual(
            [1, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
            self.two.get_extra(DmaExtraType.WALL_OR_VOID),
        )

    def test_set(self):
        neighbor_config1 = get_tile_neighbors(
            [[True, True, True], [False, False, False], [True, True, True]],
            1,
            1,
            True,
            True,
        )
        neighbor_config2 = get_tile_neighbors(
            [[True, False, True], [True, False, False], [True, False, False]],
            2,
            2,
            False,
            True,
        )

        self.one.set(DmaType.WATER, neighbor_config1, 0, 1)
        self.one.set(DmaType.WATER, neighbor_config1, 1, 2)
        self.one.set(DmaType.WATER, neighbor_config1, 2, 3)
        self.one.set(DmaType.WATER, neighbor_config2, 0, 4)
        self.one.set(DmaType.WATER, neighbor_config2, 1, 5)
        self.one.set(DmaType.WATER, neighbor_config2, 2, 6)
        self.one.set(DmaType.WALL, neighbor_config1, 0, 7)
        self.one.set(DmaType.WALL, neighbor_config1, 1, 8)
        self.one.set(DmaType.WALL, neighbor_config1, 2, 9)
        self.one.set(DmaType.WALL, neighbor_config2, 0, 10)
        self.one.set(DmaType.WALL, neighbor_config2, 1, 11)
        self.one.set(DmaType.WALL, neighbor_config2, 2, 12)
        self.one.set(DmaType.FLOOR, neighbor_config1, 0, 13)
        self.one.set(DmaType.FLOOR, neighbor_config1, 1, 14)
        self.one.set(DmaType.FLOOR, neighbor_config1, 2, 15)
        self.one.set(DmaType.FLOOR, neighbor_config2, 0, 16)
        self.one.set(DmaType.FLOOR, neighbor_config2, 1, 17)
        self.one.set(DmaType.FLOOR, neighbor_config2, 2, 18)

        self.assertEqual([1, 2, 3], self.one.get(DmaType.WATER, neighbor_config1))
        self.assertEqual([4, 5, 6], self.one.get(DmaType.WATER, neighbor_config2))
        self.assertEqual([7, 8, 9], self.one.get(DmaType.WALL, neighbor_config1))
        self.assertEqual([10, 11, 12], self.one.get(DmaType.WALL, neighbor_config2))
        self.assertEqual([13, 14, 15], self.one.get(DmaType.FLOOR, neighbor_config1))
        self.assertEqual([16, 17, 18], self.one.get(DmaType.FLOOR, neighbor_config2))

        saved = self._save_and_reload_main_fixture(self.one)

        self.assertEqual([1, 2, 3], saved.get(DmaType.WATER, neighbor_config1))
        self.assertEqual([4, 5, 6], saved.get(DmaType.WATER, neighbor_config2))
        self.assertEqual([7, 8, 9], saved.get(DmaType.WALL, neighbor_config1))
        self.assertEqual([10, 11, 12], saved.get(DmaType.WALL, neighbor_config2))
        self.assertEqual([13, 14, 15], saved.get(DmaType.FLOOR, neighbor_config1))
        self.assertEqual([16, 17, 18], saved.get(DmaType.FLOOR, neighbor_config2))

    def test_set_extra(self):
        self.one.set_extra(DmaExtraType.FLOOR1, 2, 123)
        self.one.set_extra(DmaExtraType.FLOOR1, 5, 92)
        self.one.set_extra(DmaExtraType.FLOOR2, 3, 124)
        self.one.set_extra(DmaExtraType.FLOOR2, 6, 93)
        self.one.set_extra(DmaExtraType.WALL_OR_VOID, 0, 222)
        self.one.set_extra(DmaExtraType.WALL_OR_VOID, 1, 222)

        one_floor1 = self.one.get_extra(DmaExtraType.FLOOR1)
        one_floor2 = self.one.get_extra(DmaExtraType.FLOOR2)
        one_wall_or_void = self.one.get_extra(DmaExtraType.WALL_OR_VOID)
        self.assertEqual(123, one_floor1[2])
        self.assertEqual(92, one_floor1[5])
        self.assertEqual(124, one_floor2[3])
        self.assertEqual(93, one_floor2[6])
        self.assertEqual(222, one_wall_or_void[0])
        self.assertEqual(222, one_wall_or_void[1])

        saved = self._save_and_reload_main_fixture(self.one)

        saved_floor1 = saved.get_extra(DmaExtraType.FLOOR1)
        saved_floor2 = saved.get_extra(DmaExtraType.FLOOR2)
        saved_wall_or_void = saved.get_extra(DmaExtraType.WALL_OR_VOID)
        self.assertEqual(123, saved_floor1[2])
        self.assertEqual(92, saved_floor1[5])
        self.assertEqual(124, saved_floor2[3])
        self.assertEqual(93, saved_floor2[6])
        self.assertEqual(222, saved_wall_or_void[0])
        self.assertEqual(222, saved_wall_or_void[1])

    @romtest(file_names=["dungeon.bin"], path="DUNGEON/")
    def test_using_rom(self, _, file, pmd2_data):
        dbin_model = FileType.DUNGEON_BIN.deserialize(file, pmd2_data)
        for fn in dbin_model.get_files_with_ext("dma"):
            try:
                model = self.handler.deserialize(dbin_model.get_raw(fn))
                model_reloaded = self._save_and_reload_main_fixture(model)
                self.assertEqual(model.chunk_mappings, model_reloaded.chunk_mappings)
            except Exception as e:
                raise AssertionError(f"failed processing file {fn}") from e

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path1(cls):
        return "fixtures", "one.dma"

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path2(cls):
        return "fixtures", "two.dma"
