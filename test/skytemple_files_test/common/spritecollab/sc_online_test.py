"""SpriteCollab client tests that require the main server to be online and functioning."""

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

import sys
from typing import Any, get_args, get_origin, get_type_hints
from unittest import IsolatedAsyncioTestCase, skipIf

from gql.dsl import DSLQuery

from skytemple_files.common.spritecollab.client import (
    MonsterFormDetails,
    MonsterFormInfo,
    MonsterFormInfoWithPortrait,
    SpriteCollabClient,
)
from skytemple_files.common.spritecollab.schema import Config


class SpriteCollabOnlineTestCase(IsolatedAsyncioTestCase):
    client: SpriteCollabClient

    def setUp(self) -> None:
        self.client = SpriteCollabClient()

    def check_type(self, v: Any, ftype: type):
        args = get_args(ftype)
        origin = get_origin(ftype)
        if args is not None and origin == list:
            self.assertIsInstance(v, list)
            t = args[0]
            for vv in v:
                self.check_type(vv, t)
        elif args is not None and origin == dict:
            self.assertIsInstance(v, dict)
            t = args[1]
            for vv in v.values():
                self.check_type(vv, t)
        elif hasattr(ftype, "__required_keys__"):
            self.assertIsInstance(v, dict)
            type_hints = get_type_hints(ftype)
            for field, ftype in type_hints.items():
                self.assertIn(field, v)
                self.check_type(v[field], ftype)
        else:
            self.assertIsInstance(v, ftype)

    async def test_fetch_config(self):
        async with self.client as session:
            result = await session.fetch_config()
            self.assertIsInstance(result, dict)
            self.check_type(result, Config)

    async def test_list_monster_forms_no_portraits(self):
        async with self.client as session:
            result = await session.list_monster_forms(False)
            self.assertIsInstance(result, list)
            # Sanity check
            self.assertTrue(len(result) > 10)
            for form in result:
                self.check_type(form, MonsterFormInfo)

    async def test_list_monster_forms_with_portraits(self):
        async with self.client as session:
            result = await session.list_monster_forms(True)
            self.assertIsInstance(result, list)
            # Sanity check
            self.assertTrue(len(result) > 10)
            for form in result:
                self.check_type(form, MonsterFormInfoWithPortrait)

    async def test_monster_form_details(self):
        async with self.client as session:
            result = await session.monster_form_details([(0, ""), (0, "0002/0001")])
            self.assertIsInstance(result, list)
            self.assertEqual(2, len(result))
            self.assertEqual(0, result[0].monster_id)
            self.assertEqual("", result[0].form_path)
            self.assertEqual(0, result[1].monster_id)
            self.assertEqual("0002/0001", result[1].form_path)
            for form in result:
                self.check_type(form, MonsterFormDetails)

    async def test_execute_query(self):
        async with self.client as session:
            result = await session.execute_query(DSLQuery(session.ds.Query.apiVersion))
            self.assertIsInstance(result, dict)
            self.assertIn("apiVersion", result)
            self.assertIsInstance(result["apiVersion"], str)
