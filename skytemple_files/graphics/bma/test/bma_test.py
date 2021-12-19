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

from skytemple_files.graphics.bma.handler import BmaHandler
from skytemple_files.graphics.bma.protocol import BmaProtocol
from skytemple_files.graphics.test.stubs.bpa_stub import BpaStub
from skytemple_files.graphics.test.stubs.bpc_stub import BpcStub
from skytemple_files.graphics.test.stubs.bpl_stub import BplStub
from skytemple_files.test.case import SkyTempleFilesTestCase, fixpath


class BmaTestCase(SkyTempleFilesTestCase[BmaHandler, BmaProtocol[BpaStub, BpcStub, BplStub]]):
    handler = BmaHandler

    def setUp(self) -> None:
        self.single_layer = self._load_main_fixture(self._fix_path_single_layer())
        self.assertIsNotNone(self.single_layer)
        self.two_layers = self._load_main_fixture(self._fix_path_two_layers())
        self.assertIsNotNone(self.two_layers)
        self.single_layer_one_col = self._load_main_fixture(self._fix_path_single_layer_one_col())
        self.assertIsNotNone(self.single_layer_one_col)
        self.two_layers_one_col = self._load_main_fixture(self._fix_path_two_layers_one_col())
        self.assertIsNotNone(self.two_layers_one_col)
        self.two_layers_two_col = self._load_main_fixture(self._fix_path_two_layers_two_col())
        self.assertIsNotNone(self.two_layers_two_col)
        self.two_layers_two_col_data = self._load_main_fixture(self._fix_path_two_layers_two_col_data())
        self.assertIsNotNone(self.two_layers_two_col_data)
        self.two_layers_data = self._load_main_fixture(self._fix_path_two_layers_data())
        self.assertIsNotNone(self.two_layers_data)
        self.one_layer_two_col = self._load_main_fixture(self._fix_path_one_layer_two_col())
        self.assertIsNotNone(self.one_layer_two_col)

    def test_to_pil_single_layer(self) -> None:
        self.fail("Not implemented")

    def test_to_pil(self) -> None:
        self.fail("Not implemented")

    def test_from_pil(self) -> None:
        self.fail("Not implemented")

    def test_remove_upper_layer(self) -> None:
        self.fail("Not implemented")

    def test_add_upper_layer(self) -> None:
        self.fail("Not implemented")

    def test_resize(self) -> None:
        self.fail("Not implemented")

    def test_place_chunk(self) -> None:
        self.fail("Not implemented")

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_single_layer(cls):
        return 'fixtures', 'single_layer.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_two_layers(cls):
        return 'fixtures', 'two_layers.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_single_layer_one_col(cls):
        return 'fixtures', 'single_layer_one_col.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_two_layers_one_col(cls):
        return 'fixtures', 'two_layers_one_col.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_two_layers_two_col(cls):
        return 'fixtures', 'two_layers_two_col.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_two_layers_two_col_data(cls):
        return 'fixtures', 'two_layers_two_col_data.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_two_layers_data(cls):
        return 'fixtures', 'two_layers_data.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_one_layer_two_col(cls):
        return 'fixtures', 'one_layer_two_col.bma'
