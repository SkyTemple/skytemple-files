"""SpriteCollab client tests that use a local schema to mock the data."""

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

import os
import tempfile
from filecmp import dircmp
from typing import Optional
from unittest import IsolatedAsyncioTestCase

from gql.dsl import DSLQuery
from PIL import Image
from xmldiff import main

from skytemple_files.common.ppmdu_config.data import Pmd2Sprite
from skytemple_files.common.spritecollab.client import SpriteCollabClient
from skytemple_files_test.common.spritecollab.requests_mock import (
    FIXTURES_DIR,
    AioRequestAdapterMock,
)
from skytemple_files_test.common.spritecollab.sc_offline_fixtures import (
    CONFIG_FIX,
    LIST_MONSTER_FORMS_NO_PORTRAITS_FIX,
    LIST_MONSTER_FORMS_WITH_PORTRAITS_FIX,
    MONSTER_FORM_DETAILS_FIX,
    MONSTER_FORM_DETAILS_FIX_MULTI_MON,
    QUERY_API_VERSION_FIX,
)
from skytemple_files.common.types.file_types import FileType
from skytemple_files.graphics.chara_wan.model import WanFile
from skytemple_files.graphics.kao.sprite_bot_sheet import SpriteBotSheet
from skytemple_files_test.image import ImageTestCaseAbc

EXPECTED_DIR = os.path.join(os.path.dirname(__file__), "expected")


class SpriteCollabOfflineTestCase(IsolatedAsyncioTestCase, ImageTestCaseAbc):
    client: SpriteCollabClient

    def setUp(self) -> None:
        self.client = SpriteCollabClient(request_adapter=AioRequestAdapterMock())

    async def test_fetch_config(self):
        async with self.client as session:
            result = await session.fetch_config()
            self.assertEqual(result, CONFIG_FIX)

    async def test_list_monster_forms_no_portraits(self):
        async with self.client as session:
            result = await session.list_monster_forms(False)
            self.assertEqual(result, LIST_MONSTER_FORMS_NO_PORTRAITS_FIX)

    async def test_list_monster_forms_with_portraits(self):
        async with self.client as session:
            result = await session.list_monster_forms(True)
            self.assertEqual(result, LIST_MONSTER_FORMS_WITH_PORTRAITS_FIX)

    async def test_monster_form_details_multi_mon(self):
        async with self.client as session:
            result = await session.monster_form_details([(9998, ""), (9999, ""), (9999, "9999/9999")])
            self.assertEqual(result, MONSTER_FORM_DETAILS_FIX_MULTI_MON)

    async def test_monster_form_details_single_mon(self):
        async with self.client as session:
            result = await session.monster_form_details([(9999, ""), (9999, "9999/9999")])
            self.assertEqual(result, MONSTER_FORM_DETAILS_FIX)

    async def test_fetch_portraits(self):
        async with self.client as session:
            result = await session.fetch_portraits([(9999, ""), (9999, "9999/9999")])

            expected_sheets = [
                Image.open(os.path.join(FIXTURES_DIR, "portrait", "sheet1.png")),
                Image.open(os.path.join(FIXTURES_DIR, "portrait", "sheet2.png")),
            ]

            self.assertEqual(len(expected_sheets), len(result))

            for result_portraits, expected_sheet in zip(result, expected_sheets):
                kao = FileType.KAO.new(1)

                for i, p in enumerate(result_portraits):
                    if p is not None:
                        kao.set(0, i, p)

                result_sheet = SpriteBotSheet.create(kao, 0)
                resized_result_sheet = Image.new("RGBA", (200, 320))
                resized_result_sheet.paste(result_sheet, (0, 0, result_sheet.width, result_sheet.height))

                self.assertImagesEqual(expected_sheet, resized_result_sheet)

    async def test_fetch_sprites_unfiltered(self):
        async with self.client as session:
            result = await session.fetch_sprites([(9999, ""), (9999, "9999/9999")], [None, None])

            self.assertEqual(2, len(result))
            assert result[0] is not None  # we do it like this for mypy
            assert result[1] is not None  # we do it like this for mypy
            self.assertSpritesEqual(os.path.join(FIXTURES_DIR, "sprite", "1"), *result[0])
            self.assertSpritesEqual(os.path.join(FIXTURES_DIR, "sprite", "2"), *result[1])

    async def test_fetch_sprites_filtered(self):
        async with self.client as session:
            result = await session.fetch_sprites(
                [(9999, ""), (9999, "9999/9999")],
                [["Idle", "Walk", "Pose", "wdjasjda"], None],
            )

            self.assertEqual(2, len(result))
            assert result[0] is not None  # we do it like this for mypy
            assert result[1] is not None  # we do it like this for mypy
            self.assertSpritesEqual(os.path.join(EXPECTED_DIR, "sprite", "filtered1"), *result[0])
            self.assertSpritesEqual(os.path.join(FIXTURES_DIR, "sprite", "2"), *result[1])

    async def test_fetch_sprites_copy_event_sleep_no_target(self):
        async with self.client as session:
            result = await session.fetch_sprites([(9999, "")], [["Idle", "Walk"]], copy_to_event_sleep_if_missing=True)

            self.assertEqual(1, len(result))
            assert result[0] is not None  # we do it like this for mypy
            self.assertSpritesEqual(os.path.join(EXPECTED_DIR, "sprite", "event_sleep1"), *result[0])

    async def test_fetch_sprites_copy_event_sleep(self):
        async with self.client as session:
            result = await session.fetch_sprites([(9999, "")], [None], copy_to_event_sleep_if_missing=True)

            self.assertEqual(1, len(result))
            assert result[0] is not None  # we do it like this for mypy
            self.assertSpritesEqual(os.path.join(EXPECTED_DIR, "sprite", "event_sleep2"), *result[0])

    async def test_fetch_sprites_copy_event_sleep_partial(self):
        async with self.client as session:
            result = await session.fetch_sprites(
                [(9999, "")],
                [["Sleep", "EventSleep", "Laying"]],  # notice we don't request wake
                copy_to_event_sleep_if_missing=True,
            )

            self.assertEqual(1, len(result))
            assert result[0] is not None  # we do it like this for mypy
            self.assertSpritesEqual(os.path.join(EXPECTED_DIR, "sprite", "event_sleep4"), *result[0])

    async def test_fetch_sprites_copy_event_sleep_no_effect(self):
        """Kinda like above, but this time the sprite already has EventSleep, so the flag has no effect for that."""
        async with self.client as session:
            result = await session.fetch_sprites(
                [(9999, "9999/9999")],
                [["Sleep", "EventSleep", "Wake", "Laying"]],
                copy_to_event_sleep_if_missing=True,
            )

            self.assertEqual(1, len(result))
            assert result[0] is not None  # we do it like this for mypy
            self.assertSpritesEqual(os.path.join(EXPECTED_DIR, "sprite", "event_sleep3"), *result[0])

    async def test_execute_query(self):
        async with self.client as session:
            result = await session.execute_query(DSLQuery(session.ds.Query.meta.select(session.ds.Meta.apiVersion)))
            self.assertEqual(result, QUERY_API_VERSION_FIX)

    def assertSpritesEqual(
        self,
        expected_dir: str,
        sprite: Optional[WanFile],
        sprite_names: Pmd2Sprite,
        _shadow_size: int,
    ):
        self.assertIsNotNone(sprite)
        with tempfile.TemporaryDirectory() as tempdir:
            FileType.WAN.CHARA.export_sheets(
                tempdir,
                sprite,
                sprite_names,  # type: ignore
            )

            cmp = dircmp(tempdir, expected_dir)

            diff_files = []
            xml_diffs = {}
            for f in cmp.diff_files:
                if f.endswith(".png"):
                    self.assertImagesEqual(
                        Image.open(os.path.join(expected_dir, f)),
                        Image.open(os.path.join(tempdir, f)),
                    )
                elif f.endswith(".xml"):
                    diff = main.diff_files(
                        os.path.join(expected_dir, f),
                        os.path.join(tempdir, f),
                        diff_options={"F": 0.5, "ratio_mode": "fast"},
                    )
                    if diff:
                        diff_files.append(f)
                        xml_diffs[f] = diff
                else:
                    diff_files.append(f)

            the_same = (
                len(diff_files) == 0
                and len(cmp.funny_files) == 0
                and len(cmp.left_only) == 0
                and len(cmp.right_only) == 0
            )

            if not the_same:
                print("")
                print("====================================")
                print("DIR DIFF (see below):")
                cmp.diff_files = diff_files
                cmp.report()
                print()
                print("XML diffs:")
                for k, v in xml_diffs.items():
                    print(f">> {k}:")
                    print(f"{v}")
                print("====================================")
                print("")
            self.assertTrue(
                the_same,
                "The exported sprite directories must be the same. Comparison report see above.",
            )
