import os
from pathlib import Path
from unittest import TestCase, SkipTest

from common.file_api_v2 import RomProject
from skytemple_files.data.waza_p.handler import WazaPHandler


class FileApiV2TestCase(TestCase):

    asset_project_path = Path("skytemple_files_test", "common", "fixtures", "asset_project")

    def test_list_files_rom(self):
        project = RomProject.new(self.load_rom_path(), self.asset_project_path)
        file_list = project.list_files(search_project_dir=False)

        expected_path = Path("BALANCE", "waza_p.bin")
        self.assertTrue(expected_path in file_list)
        self.assertEqual(WazaPHandler, file_list[expected_path])

    def test_list_files_project(self):
        project = RomProject.new(self.load_rom_path(), self.asset_project_path)
        file_list = project.list_files(search_rom=False)

        expected_path = Path("BALANCE", "waza_p.bin")
        self.assertTrue(expected_path in file_list)
        self.assertEqual(WazaPHandler, file_list[expected_path])


    def load_rom_path(self):
        if "SKYTEMPLE_TEST_ROM" in os.environ and os.environ["SKYTEMPLE_TEST_ROM"] != "":
            return Path(os.environ["SKYTEMPLE_TEST_ROM"])
        else:
            raise SkipTest("No ROM file provided or ROM not found.")
