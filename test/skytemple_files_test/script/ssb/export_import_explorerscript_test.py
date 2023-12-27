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

import unittest

from skytemple_files.common.impl_cfg import env_use_native
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.script.ssb.flow import SsbFlow
from skytemple_files.script.ssb.handler import SsbHandler
from skytemple_files.script.ssb.script_compiler import ScriptCompiler
from skytemple_files_test.case import romtest


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

        ssb_before = SsbHandler.deserialize(file, pmd2_data)
        explorer_script, source_map_before = ssb_before.to_explorerscript()

        # Test the compiling and writing, by compiling the model, writing it to binary, and then loading it again,
        # and checking the generated ssb script.
        compiler = ScriptCompiler(pmd2_data)

        ssb_after, source_map_after = compiler.compile_explorerscript(
            explorer_script, path.split("/")[-1]
        )

        file_after = SsbHandler.serialize(ssb_after, pmd2_data)
        ssb_after = SsbHandler.deserialize(file_after, pmd2_data)

        # Run flow check
        ssb_flow_before = SsbFlow(ssb_before, pmd2_data)
        ssb_flow_after = SsbFlow(ssb_after, pmd2_data)

        ssb_flow_before.assert_equal(ssb_flow_after)
