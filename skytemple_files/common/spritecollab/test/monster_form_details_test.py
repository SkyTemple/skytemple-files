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

from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptFaceName
from skytemple_files.common.spritecollab.client import (MonsterFormDetails,
                                                        SpriteUrls)
from skytemple_files.common.spritecollab.schema import PHASE_UNKNOWN
from skytemple_files.common.spritecollab.test.requests_mock import (
    FIX_TEST_FILES, FIX_TEST_FILES_WITH_NONE, AioRequestAdapterMock)


class MonsterFormDetailsTestCase(IsolatedAsyncioTestCase):
    def setUp(self):
        self.fixtures_emotions = [
            ("Normal", FIX_TEST_FILES_WITH_NONE[0]),
            ("Happy", FIX_TEST_FILES_WITH_NONE[1]),
            ("Foobar", FIX_TEST_FILES_WITH_NONE[2]),
            ("Crying", FIX_TEST_FILES_WITH_NONE[-1]),  # None, None
        ]

        self.fixtures_actions = [
            ("Idle", {
                "anim": FIX_TEST_FILES_WITH_NONE[0],
                "offsets": FIX_TEST_FILES_WITH_NONE[1],
                "shadows": FIX_TEST_FILES_WITH_NONE[2],
            }),
            ("Happy", {
                "anim": FIX_TEST_FILES_WITH_NONE[1],
                "offsets": FIX_TEST_FILES_WITH_NONE[1],
                "shadows": FIX_TEST_FILES_WITH_NONE[1],
            }),
            ("Foobar", {
                "anim": FIX_TEST_FILES_WITH_NONE[1],
                "offsets": FIX_TEST_FILES_WITH_NONE[2],
                "shadows": FIX_TEST_FILES_WITH_NONE[0],
            }),
            ("Crying", {
                "anim": FIX_TEST_FILES_WITH_NONE[-1],    # None, None
                "offsets": FIX_TEST_FILES_WITH_NONE[-1], # None, None
                "shadows": FIX_TEST_FILES_WITH_NONE[-1], # None, None
            }),
        ]

        self.obj = MonsterFormDetails(
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
            portraits={
                "Normal": FIX_TEST_FILES_WITH_NONE[0][0],
                "Happy": FIX_TEST_FILES_WITH_NONE[1][0],
                "Foobar": FIX_TEST_FILES_WITH_NONE[2][0],
            },
            portrait_sheet="",
            sprites={
                "Idle": SpriteUrls(
                    anim=FIX_TEST_FILES_WITH_NONE[0][0],
                    offsets=FIX_TEST_FILES_WITH_NONE[1][0],
                    shadows=FIX_TEST_FILES_WITH_NONE[2][0],
                ),
                "Happy": SpriteUrls(
                    anim=FIX_TEST_FILES_WITH_NONE[1][0],
                    offsets=FIX_TEST_FILES_WITH_NONE[1][0],
                    shadows=FIX_TEST_FILES_WITH_NONE[1][0],
                ),
                "Foobar": SpriteUrls(
                    anim=FIX_TEST_FILES_WITH_NONE[1][0],
                    offsets=FIX_TEST_FILES_WITH_NONE[2][0],
                    shadows=FIX_TEST_FILES_WITH_NONE[0][0],
                ),
            },
            sprite_zip="",
            sprites_copy_of={},
            portrait_credits=[],
            sprite_credits=[],
        )

    async def test_fetch_portrait(self):
        for (emotion, (_, fpath)) in self.fixtures_emotions:
            if fpath is None:
                self.assertEqual(
                    None,
                    await self.obj.fetch_portrait(emotion)
                )

            else:
                data = Image.open(fpath)

                self.assertEqual(
                    data,
                    await self.obj.fetch_portrait(emotion)
                )

    async def test_fetch_portrait_via_face_name(self):
        emotion_map = {
            "Normal": "NORMAL",
            "Happy": "happy",
            "Pain": "pAiN",
            "Angry": "anGRY",
            "Worried": "Worried",
            "Sad": "Sad",
            "Crying": "Crying",
            "Shouting": "Shouting",
            "Teary-Eyed": "Teary-Eyed",
            "Determined": "Determined",
            "Joyous": "Joyous",
            "Inspired": "Inspired",
            "Surprised": "Surprised",
            "Dizzy": "Dizzy",
            "Special0": "Special0",
            "Special1": "Special1",
            "Sigh": "Sigh",
            "Stunned": "Stunned",
            "Special2": "Special2",
            "Special3": "Special3",
            "Foo": "Foo"
        }
        fixtures_emotions = [
            ("Normal", FIX_TEST_FILES_WITH_NONE[0]),
            ("Happy", FIX_TEST_FILES_WITH_NONE[1]),
            ("Pain", FIX_TEST_FILES_WITH_NONE[2]),
            ("Angry", FIX_TEST_FILES_WITH_NONE[0]),
            ("Worried", FIX_TEST_FILES_WITH_NONE[1]),
            ("Sad", FIX_TEST_FILES_WITH_NONE[2]),
            ("Crying", FIX_TEST_FILES_WITH_NONE[0]),
            ("Shouting", FIX_TEST_FILES_WITH_NONE[1]),
            ("Teary-Eyed", FIX_TEST_FILES_WITH_NONE[2]),
            ("Determined", FIX_TEST_FILES_WITH_NONE[0]),
            ("Joyous", FIX_TEST_FILES_WITH_NONE[1]),
            ("Inspired", FIX_TEST_FILES_WITH_NONE[2]),
            ("Surprised", FIX_TEST_FILES_WITH_NONE[0]),
            ("Dizzy", FIX_TEST_FILES_WITH_NONE[1]),
            ("Special0", FIX_TEST_FILES_WITH_NONE[2]),
            ("Special1", FIX_TEST_FILES_WITH_NONE[0]),
            ("Sigh", FIX_TEST_FILES_WITH_NONE[1]),
            ("Stunned", FIX_TEST_FILES_WITH_NONE[2]),
            ("Special2", FIX_TEST_FILES_WITH_NONE[0]),
            ("Special3", FIX_TEST_FILES_WITH_NONE[1]),
            ("Foo", FIX_TEST_FILES_WITH_NONE[-1]),  # None, None
        ]
        urls = {}
        for (emotion, (url, _)) in fixtures_emotions:
            if url is not None:
                urls[emotion] = url
        self.obj.portraits = urls

        for (emotion, (_, fpath)) in fixtures_emotions:
            renamed_emotion = emotion_map[emotion]
            face_name = Pmd2ScriptFaceName(-1, renamed_emotion)
            if fpath is None:
                self.assertEqual(
                    None,
                    await self.obj.fetch_portrait_via_face_name(face_name)
                )

            else:
                data = Image.open(fpath)

                self.assertEqual(
                    data,
                    await self.obj.fetch_portrait_via_face_name(face_name)
                )

    async def test_fetch_sprite_anim(self):
        for (action, fpaths) in self.fixtures_actions:
            fpath = fpaths["anim"][1]
            if fpath is None:
                self.assertEqual(
                    None,
                    await self.obj.fetch_sprite_anim(action)
                )

            else:
                data = Image.open(fpath)

                self.assertEqual(
                    data,
                    await self.obj.fetch_sprite_anim(action)
                )

    async def test_fetch_sprite_shadows(self):
        for (action, fpaths) in self.fixtures_actions:
            fpath = fpaths["shadows"][1]
            if fpath is None:
                self.assertEqual(
                    None,
                    await self.obj.fetch_sprite_shadows(action)
                )

            else:
                data = Image.open(fpath)

                self.assertEqual(
                    data,
                    await self.obj.fetch_sprite_shadows(action)
                )

    async def test_fetch_sprite_offsets(self):
        for (action, fpaths) in self.fixtures_actions:
            fpath = fpaths["offsets"][1]
            if fpath is None:
                self.assertEqual(
                    None,
                    await self.obj.fetch_sprite_offsets(action)
                )

            else:
                data = Image.open(fpath)

                self.assertEqual(
                    data,
                    await self.obj.fetch_sprite_offsets(action)
                )

    async def test_fetch_portrait_sheet(self):
        for (url, fpath) in FIX_TEST_FILES:
            self.obj.portrait_sheet = url

            if fpath is None:
                self.assertEqual(
                    None,
                    await self.obj.fetch_portrait_sheet()
                )

            else:
                data = Image.open(fpath)

                self.assertEqual(
                    data,
                    await self.obj.fetch_portrait_sheet()
                )

    async def test_fetch_sprite_zip(self):
        for (url, fpath) in FIX_TEST_FILES_WITH_NONE:
            self.obj.sprite_zip = url

            if fpath is None:
                self.assertEqual(
                    None,
                    await self.obj.fetch_sprite_zip()
                )

            else:
                with open(fpath, 'rb') as f:
                    data = f.read()

                self.assertEqual(
                    data,
                    await self.obj.fetch_sprite_zip()
                )
