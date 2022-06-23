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
import unittest

from PIL import Image

from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.hardcoded.cart_removed import HardcodedCartRemoved
from skytemple_files.test.case import fixpath


class CartRemovedTestCase(unittest.TestCase):
    def test_compression(self) -> None:
        """
        This effectively tests the performance of the compression algorithms available (only AT3PX by default) to see
        if they can compress the standard cart removed image.
        """
        HardcodedCartRemoved.set_cart_removed_data(
            Image.open(self._fix_path()),
            bytearray(0xFFFFFFF),
            Pmd2XmlReader.load_default()
        )

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path(cls):
        return 'fixtures', 'default.png'
