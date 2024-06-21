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
from __future__ import annotations

from typing import Type

from parameterized import parameterized

from skytemple_files.common.impl_cfg import env_use_native
from skytemple_files.compression_container._prviate.bpc_tilemap.handler import (
    BpcTilemapHandler,
)
from skytemple_files.compression_container.protocol import CompressionContainerProtocol
from skytemple_files_test.compression_container.util import (
    dataset_name_func,
    load_dataset,
)
from skytemple_files_test.case import SkyTempleFilesTestCase

FIX = (
    b"Hello World. I am testing compression. 11111111111111111111111111111111111111111111111111111"
    b"111111111111111111. 232323232323232323232323232323232323232323232323. 123456789. 11223344. 12121213."
)


class BpcTilemapTestCase(SkyTempleFilesTestCase[BpcTilemapHandler, CompressionContainerProtocol]):
    @classmethod
    def handler(cls) -> Type[BpcTilemapHandler]:
        return BpcTilemapHandler

    def test_cross_native_implementation_compress(self):
        """Tests the native implementation against the Python implementation (assuming this one works)"""
        if not env_use_native():
            self.skipTest("This test is only enabled when the native implementations are tested.")
        py_cls = self.handler().load_python_model()
        rs_cls = self.handler().load_native_model()
        result_rs = rs_cls.compress(FIX).to_bytes()
        self.assertEqual(
            FIX,
            bytes(py_cls(result_rs).decompress()),
            "The rust implementation mus compress correctly, so the Python implementation "
            "can correctly decompress it again.",
        )

    def test_cross_native_implementation_decompress(self):
        """Tests the native implementation against the Python implementation (assuming this one works)"""
        if not env_use_native():
            self.skipTest("This test is only enabled when the native implementations are tested.")
        py_cls = self.handler().load_python_model()
        rs_cls = self.handler().load_native_model()
        result_py = py_cls.compress(FIX).to_bytes()
        self.assertEqual(
            FIX,
            rs_cls(result_py).decompress(),
            "The rust implementation mus decompress correctly.",
        )

    @parameterized.expand(load_dataset(), name_func=dataset_name_func)
    def test_container(self, _, in_bytes):
        model = self.handler().compress(in_bytes)
        self.assertEqual(len(model.to_bytes()), model.cont_size(model.to_bytes()))
        self.assertTrue(model.to_bytes().startswith(b"BPCTLM"))
        self.assertEqual(
            model.to_bytes(),
            self.handler().serialize(self.handler().deserialize(model.to_bytes())),
        )
        self.assertEqual(in_bytes, model.decompress())
