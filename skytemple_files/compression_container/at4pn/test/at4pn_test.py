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
# mypy: ignore-errors
from typing import Type

from parameterized import parameterized

from skytemple_files.compression_container.at4pn.handler import At4pnHandler
from skytemple_files.compression_container.protocol import CompressionContainerProtocol
from skytemple_files.compression_container.test.util import load_dataset, dataset_name_func

from skytemple_files.test.case import SkyTempleFilesTestCase


class At4pnTestCase(SkyTempleFilesTestCase[At4pnHandler, CompressionContainerProtocol]):
    @classmethod
    def handler(cls) -> Type[At4pnHandler]:
        return At4pnHandler

    @parameterized.expand(load_dataset(), name_func=dataset_name_func)
    def test_container(self, _, in_bytes):
        model = self.handler().compress(in_bytes)
        self.assertEqual(len(model.to_bytes()) - 7, model.cont_size(model.to_bytes()))
        self.assertTrue(model.to_bytes().startswith(b'AT4PN'))
        self.assertEqual(model.to_bytes(), self.handler().serialize(self.handler().deserialize(model.to_bytes())))
        self.assertEqual(in_bytes, model.decompress())
