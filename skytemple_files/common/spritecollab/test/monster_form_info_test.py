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
from __future__ import annotations

from unittest import IsolatedAsyncioTestCase

from PIL import Image

from skytemple_files.common.spritecollab.client import MonsterFormInfoWithPortrait
from skytemple_files.common.spritecollab.schema import PHASE_UNKNOWN
from skytemple_files.common.spritecollab.test.requests_mock import (
    FIX_TEST_FILES_WITH_NONE,
    AioRequestAdapterMock,
)


class MonsterFormInfoTestCase(IsolatedAsyncioTestCase):
    def setUp(self):
        self.obj = MonsterFormInfoWithPortrait(
            _request_adapter=AioRequestAdapterMock(),
            monster_id=0,
            form_path="",
            monster_name="",
            full_form_name="",
            shiny=False,
            female=False,
            canon=False,
            portraits_phase=PHASE_UNKNOWN,
            sprites_phase=PHASE_UNKNOWN,
            portraits_modified_date=None,
            sprites_modified_date=None,
            preview_portrait="",
        )

    async def test_fetch_preview_portrait(self):
        for (url, fpath) in FIX_TEST_FILES_WITH_NONE:
            self.obj.preview_portrait = url

            if fpath is None:
                self.assertEqual(None, await self.obj.fetch_preview_portrait())

            else:
                data = Image.open(fpath)

                self.assertEqual(data, await self.obj.fetch_preview_portrait())
