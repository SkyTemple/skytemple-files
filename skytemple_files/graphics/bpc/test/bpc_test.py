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

from skytemple_files.graphics.bpc.handler import BpcHandler
from skytemple_files.graphics.bpc.protocol import BpcProtocol, BpcLayerProtocol
from skytemple_files.graphics.test.stubs.bpa_stub import BpaStub
from skytemple_files.test.case import SkyTempleFilesTestCase, fixpath


class BpcTestCase(SkyTempleFilesTestCase[BpcHandler, BpcProtocol[BpcLayerProtocol, BpaStub]]):
    handler = BpcHandler

    def setUp(self) -> None:
        self.single_layer1 = self._load_main_fixture(self._fix_path_single_layer1())
        self.assertIsNotNone(self.single_layer1)
        self.single_layer2 = self._load_main_fixture(self._fix_path_single_layer2())
        self.assertIsNotNone(self.single_layer2)
        self.two_layers1 = self._load_main_fixture(self._fix_path_two_layers1())
        self.assertIsNotNone(self.two_layers1)
        self.two_layers2 = self._load_main_fixture(self._fix_path_two_layers2())
        self.assertIsNotNone(self.two_layers2)

    def test_layer_info(self) -> None:
        self.fail("Not implemented")

    def test_chunks_to_pil(self) -> None:
        self.fail("Not implemented")

    def test_single_chunk_to_pil(self) -> None:
        self.fail("Not implemented")

    def test_tiles_to_pil(self) -> None:
        self.fail("Not implemented")

    def test_chunks_animated_to_pil(self) -> None:
        self.fail("Not implemented")

    def test_single_chunk_animated_to_pil(self) -> None:
        self.fail("Not implemented")

    def test_pil_to_tiles(self) -> None:
        self.fail("Not implemented")

    def test_pil_to_chunks(self) -> None:
        self.fail("Not implemented")

    def test_get_tile(self) -> None:
        self.fail("Not implemented")

    def test_set_tile(self) -> None:
        self.fail("Not implemented")

    def test_get_chunk(self) -> None:
        self.fail("Not implemented")

    def test_set_chunk(self) -> None:
        self.fail("Not implemented")

    def test_import_tiles(self) -> None:
        self.fail("Not implemented")

    def test_import_tile_mappings(self) -> None:
        self.fail("Not implemented")

    def test_get_bpas_for_layer(self) -> None:
        self.fail("Not implemented")

    def test_remove_upper_layer(self) -> None:
        self.fail("Not implemented")

    def test_add_upper_layer(self) -> None:
        self.fail("Not implemented")

    def test_process_bpa_change(self) -> None:
        self.fail("Not implemented")

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_single_layer1(cls):
        return 'fixtures', 'single_layer1.bpc'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_single_layer2(cls):
        return 'fixtures', 'single_layer2.bpc'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_two_layers1(cls):
        return 'fixtures', 'two_layers1.bpc'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_two_layers2(cls):
        return 'fixtures', 'two_layers2.bpc'
