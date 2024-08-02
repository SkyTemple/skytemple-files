#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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
import typing
from xml.etree import ElementTree
from tempfile import TemporaryDirectory

from skytemple_files.common.impl_cfg import env_use_native
from skytemple_files.common.ppmdu_config.data import Pmd2Sprite, Pmd2Index
from skytemple_files.graphics.chara_wan.handler import CharaWanHandler
from skytemple_files.graphics.chara_wan.model import WanFile
from skytemple_files_test.case import SkyTempleFilesTestCase, fixpath


class CharaWanoTestCase(SkyTempleFilesTestCase[CharaWanHandler, WanFile]):
    handler = CharaWanHandler

    # Simple tests that just make sure the sprites' SpriteCollab representation still matches
    # after export / import and splitting / merging.

    def test_duskako(self):
        self._test_import_export(self._fix_path_sheets("duskako"))

    def test_ghost(self):
        self._test_import_export(self._fix_path_sheets("ghost"))

    def test_missingno_(self):
        self._test_import_export(self._fix_path_sheets("missingno_"))

    def test_missingno_glaceon_colored(self):
        # Tests the "Glaceon transparency bug"
        self._test_import_export(self._fix_path_sheets("missingno_glaceon_colored"))

    def test_smiley(self):
        # RearUp is not imported since it has no ID in the XML
        self._test_import_export(self._fix_path_sheets("smiley"), not_imported_anims=["RearUp"])

    def test_type_null(self):
        # Dance is not imported since it has no ID in the XML
        self._test_import_export(self._fix_path_sheets("type_null"), not_imported_anims=["Dance"])

    def _test_import_export(self, fix_path: str, *, not_imported_anims: list[str] | None = None):
        if env_use_native():
            self.skipTest(
                "This test is not enabled when the native implementations are tested, since no native chara_wan implementation exists."
            )
        not_imported_anims = not_imported_anims or []
        sprite_def = self._get_sprite_def(fix_path)
        wan_after_import = self.handler.import_sheets(fix_path, strict=True)
        with TemporaryDirectory() as tmp_dir:
            self.handler.export_sheets(tmp_dir, wan_after_import, sprite_def)
            self.assert_sheet_dirs_equal(
                fix_path, tmp_dir, "Exported WAN sheet must match Input WAN sheet", not_imported_anims
            )

        # Try again after splitting and merging
        split = self.handler.split_wan(wan_after_import)
        combined = self.handler.merge_wan(*split)

        with TemporaryDirectory() as tmp_dir:
            self.handler.export_sheets(tmp_dir, combined, sprite_def)
            self.assert_sheet_dirs_equal(
                fix_path,
                tmp_dir,
                "Exported WAN sheet must match Input WAN sheet after splitting and merging",
                not_imported_anims,
            )

    def assert_sheet_dirs_equal(self, dir1: str, dir2: str, msg: str, not_imported_anims: list[str]):
        self.assertDirsEqual(dir1, dir2, msg, ignore_contents=["AnimData.xml"])
        # We diff the AnimData.xml as well, but if "not_imported_anims" is set, we don't expect
        # these animations in the output: so we load the AnimData.xml from the first directory and remove
        # those animations before diffing.
        loaded_anim_data1 = ElementTree.parse(os.path.join(dir1, "AnimData.xml")).getroot()
        anims = loaded_anim_data1.find("Anims")
        to_remove = []
        assert anims is not None
        for action in anims:
            find_result = action.find("Name")
            assert find_result is not None
            name_normal = find_result.text
            assert name_normal is not None
            if name_normal in not_imported_anims:
                to_remove.append(action)
        for rem in to_remove:
            anims.remove(rem)
        self.assertXmlEqual(
            loaded_anim_data1,
            os.path.join(dir2, "AnimData.xml"),
            f"{msg}: AnimData.xml not expected format",
        )

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_sheets(cls, testset: str) -> str:
        return "fixtures", testset, "sheets"

    def _get_sprite_def(self, fn: str) -> Pmd2Sprite:
        # TODO: This is from SkyTemple. It should probably be ported to the chara_wan handler itself.
        tree = ElementTree.parse(os.path.join(fn, "AnimData.xml")).getroot()
        anims = tree.find("Anims")
        assert anims is not None
        action_indices = {}
        for action in anims:
            find_result = action.find("Name")
            assert find_result is not None
            name_normal = find_result.text
            assert name_normal is not None
            action_index = action.find("Index")
            if action_index is not None:
                action_text = action_index.text
                assert action_text is not None
                idx = int(action_text)
                action_indices[idx] = Pmd2Index(idx, [name_normal])
        return Pmd2Sprite(-1, action_indices)
