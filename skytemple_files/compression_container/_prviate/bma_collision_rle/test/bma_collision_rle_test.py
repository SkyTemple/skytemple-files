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

import pytest
from parameterized import parameterized

from skytemple_files.common.impl_cfg import env_use_native
from skytemple_files.compression_container._prviate.bma_collision_rle.handler import BmaCollisionRleHandler
from skytemple_files.compression_container.protocol import CompressionContainerProtocol
from skytemple_files.compression_container.test.util import load_dataset, dataset_name_func

from skytemple_files.test.case import SkyTempleFilesTestCase


def rle_dataset():
    return [
        ('00', bytes()),
        ('01', bytes((0,))),
        ('02', bytes((1,))),
        ('03', bytes((0, 0,))),
        ('04', bytes((1, 1,))),
        ('05', bytes((0, 0, 1, 1))),
        ('06', bytes((0, 1, 1, 1))),
        ('07', bytes((1, 1))),
        ('08', bytes((0,) * 10)),
        ('09', bytes((1,) * 20)),
        ('10', bytes((0, 1) * 20 + (0,) * 40 + (1,) * 30 + (0, 1, 1, 0, 0) + (0,) * 31)),
        ('11', bytes((0, 1, 0, 1) * 13 + (0, 1, 1, 0, 0) * 20 + (1,) * 200 + (0, 1, 0, 0, 0) + (0, 1, 1, 1, 1) * 30))
    ]


class BmaCollisionRleTestCase(SkyTempleFilesTestCase[BmaCollisionRleHandler, CompressionContainerProtocol]):
    @classmethod
    def handler(cls) -> Type[BmaCollisionRleHandler]:
        return BmaCollisionRleHandler

    @parameterized.expand(rle_dataset(), name_func=dataset_name_func)
    def test_container(self, _, in_bytes):
        model = self.handler().compress(in_bytes)
        self.assertEqual(len(model.to_bytes()), model.cont_size(model.to_bytes()))
        self.assertTrue(model.to_bytes().startswith(b'BMARLE'))
        self.assertEqual(model.to_bytes(), self.handler().serialize(self.handler().deserialize(model.to_bytes())))
        self.assertEqual(in_bytes, model.decompress())

    @parameterized.expand(rle_dataset(), name_func=dataset_name_func)
    def test_cross_native_implementation_compress(self, _, in_bytes):
        """Tests the native implementation against the Python implementation (assuming this one works) -- Using the main dataset."""
        if not env_use_native():
            self.skipTest("This test is only enabled when the native implementations are tested.")
        py_cls = self.handler().load_python_model()
        rs_cls = self.handler().load_native_model()
        result_rs = rs_cls.compress(in_bytes).to_bytes()
        self.assertEqual(
            in_bytes, bytes(py_cls(result_rs).decompress()),
            "The rust implementation mus compress correctly, so the Python implementation "
            "can correctly decompress it again."
        )

    @parameterized.expand(rle_dataset(), name_func=dataset_name_func)
    def test_cross_native_implementation_decompress(self, _, in_bytes):
        """Tests the native implementation against the Python implementation -- Using the main dataset."""
        if not env_use_native():
            self.skipTest("This test is only enabled when the native implementations are tested.")
        py_cls = self.handler().load_python_model()
        rs_cls = self.handler().load_native_model()
        result_py = py_cls.compress(in_bytes).to_bytes()
        self.assertEqual(
            in_bytes, rs_cls(result_py).decompress(),
            "The rust implementation mus decompress correctly."
        )
