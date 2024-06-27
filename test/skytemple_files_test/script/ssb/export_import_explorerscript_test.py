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

import os.path
import unittest

from skytemple_files.common.impl_cfg import env_use_native
from skytemple_files.common.ppmdu_config.data import (
    Pmd2Data,
    GAME_REGION_US,
    GAME_REGION_EU,
    GAME_REGION_JP,
    GAME_VERSION_EOS,
)
from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.script.ssb.flow import SsbFlow
from skytemple_files.script.ssb.handler import SsbHandler
from skytemple_files.script.ssb.script_compiler import ScriptCompiler
from skytemple_files_test.case import romtest, with_fixtures


def _collect_for_path(path):
    abspath = os.path.abspath(path)
    dirpath = os.path.dirname(abspath)
    ssb_fn = os.path.basename(abspath)
    basename, region, _ext = ssb_fn.split(".")
    expspath = os.path.join(dirpath, f"{basename}.exps")
    if region == "us":
        version = f"{GAME_VERSION_EOS}_{GAME_REGION_US}"
    elif region == "eu":
        version = f"{GAME_VERSION_EOS}_{GAME_REGION_EU}"
    elif region == "jp":
        version = f"{GAME_VERSION_EOS}_{GAME_REGION_JP}"
    else:
        assert False, "wrong region code in fixture"
    with open(abspath, "rb") as f:
        ssb = f.read()
    with open(expspath, "r") as f:
        exps = f.read()
    pmd2_data = Pmd2XmlReader.load_default(for_version=version)
    return exps, ssb, pmd2_data


class ExportImportExplorerScriptTest(unittest.TestCase):
    @romtest(file_ext="ssb", path="SCRIPT/")
    def test_using_rom_ssb(self, path, file, *, pmd2_data: Pmd2Data):
        if env_use_native():
            self.skipTest(
                "This test is not enabled when the native implementations are tested, since there is no native implementation."
            )
        # Those scripts fail for JP because they are invalid leftovers.
        if path in [
            "SCRIPT/D42P21A/enter23.ssb",
            "SCRIPT/D73P11A/us0303.ssb",
            "SCRIPT/D73P11A/us0305.ssb",
            "SCRIPT/D73P11A/us2003.ssb",
            "SCRIPT/D73P11A/us2005.ssb",
            "SCRIPT/D73P11A/us2103.ssb",
            "SCRIPT/D73P11A/us2105.ssb",
            "SCRIPT/D73P11A/us2203.ssb",
            "SCRIPT/D73P11A/us2205.ssb",
            "SCRIPT/D73P11A/us2303.ssb",
            "SCRIPT/D73P11A/us2305.ssb",
        ]:
            self.skipTest("Test not supported for this ssb.")

        self._run_test(path, None, file, pmd2_data)

    @with_fixtures(file_ext="ssb", path=os.path.join(os.path.dirname(__file__), "fixtures/"))
    def test_using_custom_ssb(self, path: str):
        if env_use_native():
            self.skipTest(
                "This test is not enabled when the native implementations are tested, since there is no native implementation."
            )

        exps, ssb, pmd2_data = _collect_for_path(path)

        self._run_test(path, exps, ssb, pmd2_data)

    @with_fixtures(file_ext="ssb", path=os.path.join(os.path.dirname(__file__), "fixtures/"))
    def test_using_custom_ssb_decompile(self, path: str):
        """
        Like test_using_custom_ssb, but tries to decompile instead of working with the ExplorerScript source code.
        """
        if env_use_native():
            self.skipTest(
                "This test is not enabled when the native implementations are tested, since there is no native implementation."
            )

        _exps, ssb, pmd2_data = _collect_for_path(path)

        self._run_test(path, None, ssb, pmd2_data, expect_ssb_script="UTOPIA13_final2" in path)

    def _run_test(
        self,
        path: str,
        exps_before: str | None,
        ssb_file: bytes,
        pmd2_data: Pmd2Data,
        *,
        expect_ssb_script=False,
        _skip_flow_check=False,
    ):
        ssb_before = SsbHandler.deserialize(ssb_file, pmd2_data)
        if not exps_before:
            # Test the compiling and writing, by compiling the model, writing it to binary,
            # and then loading it again, and checking the generated ssb script.
            exps_before, _source_map_before = ssb_before.to_explorerscript()
            if not expect_ssb_script:
                self.assertNotIn(
                    "is-ssb-script", exps_before, "Was not expecting the decompiler to fall back to SsbScript"
                )
            else:
                self.assertIn("is-ssb-script", exps_before, "Was expecting the decompiler to fall back to SsbScript")

        compiler = ScriptCompiler(pmd2_data)

        ssb_after, source_map_after = compiler.compile_explorerscript(exps_before, path.split("/")[-1])

        file_after = SsbHandler.serialize(ssb_after, pmd2_data)
        ssb_after = SsbHandler.deserialize(file_after, pmd2_data)

        if not _skip_flow_check:
            # Run flow check
            ssb_flow_before = SsbFlow(ssb_before, pmd2_data)
            ssb_flow_after = SsbFlow(ssb_after, pmd2_data)

            ssb_flow_before.assert_equal(ssb_flow_after)

        return file_after
