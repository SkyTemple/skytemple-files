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

from skytemple_files.graphics.bgp.handler import BgpHandler
from skytemple_files.graphics.bgp.protocol import BgpProtocol
from skytemple_files.test.case import SkyTempleFilesTestCase, fixpath, romtest


class BgpTestCase(SkyTempleFilesTestCase[BgpHandler, BgpProtocol]):
    handler = BgpHandler

    def setUp(self) -> None:
        self.bgp1 = self._load_main_fixture(self._fix_path("1.bgp"))
        self.bgp2 = self._load_main_fixture(self._fix_path("2.bgp"))

    def test_get(self):
        self.assertImagesEqual(
            self._fix_path("1.png"),
            self.bgp1.to_pil()
        )
        self.assertImagesEqual(
            self._fix_path("2.png"),
            self.bgp2.to_pil()
        )
        self.assertImagesNotEqual(
            self._fix_path("2.png"),
            self.bgp1.to_pil()
        )
        self.assertImagesNotEqual(
            self._fix_path("1.png"),
            self.bgp2.to_pil()
        )

    def test_set(self):
        self.bgp1.from_pil(self._load_image(self._fix_path("2.png")))
        bgp = self._save_and_reload_main_fixture(self.bgp1)
        self.assertImagesEqual(
            self._fix_path("2.png"),
            bgp.to_pil()
        )

    @romtest(file_ext='bgp', path='')
    def test_using_rom(self, _, file):
        bgp_before = self.handler.deserialize(file)
        bgp_after = self._save_and_reload_main_fixture(bgp_before)
        self.assertImagesEqual(
            bgp_before.to_pil(),
            bgp_after.to_pil()
        )

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path(cls, file: str) -> str:
        return 'fixtures', file
