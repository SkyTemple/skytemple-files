import os
from pathlib import Path
from unittest import TestCase, SkipTest

from common.file_api_v2 import RomProject, ALLOW_EXTRA_SKYPATCHES
from common.types.file_types import FileType
from skytemple_files.data.waza_p.handler import WazaPHandler

SKYTEMPLE_TEST_ROM_ENV = "SKYTEMPLE_TEST_ROM"


class FileApiV2TestCase(TestCase):

    asset_project_path = Path("skytemple_files_test", "common", "fixtures", "asset_project")

    def test_list_files_rom(self):
        project = RomProject.new(self.load_rom_path(), self.asset_project_path)

        file_list = project.list_files(search_project_dir=False)

        expected_path = Path("BALANCE", "waza_p.bin")
        self.assertTrue(expected_path in file_list)
        self.assertEqual(FileType.WAZA_P, file_list[expected_path])

    def test_list_files_project(self):
        project = RomProject.new(self.load_rom_path(), self.asset_project_path)

        file_list = project.list_files(search_rom=False)

        expected_path = Path("BALANCE", "waza_p.bin")
        self.assertTrue(expected_path in file_list)
        self.assertEqual(FileType.WAZA_P, file_list[expected_path])

    def test_load_allow_extra_skypatches(self):
        project = RomProject.new(self.load_rom_path(), self.asset_project_path)

        self.assertTrue(project.does_allow_extra_skypatches())

    def test_set_allow_extra_skypatches_no_remember(self):
        project = RomProject.new(self.load_rom_path(), self.asset_project_path)

        project.set_allow_extra_skypatches(False)

        self.assertFalse(project.does_allow_extra_skypatches())
        # Assert that the config file has not changed.
        asset_config = project._load_asset_config()
        self.assertTrue(asset_config[ALLOW_EXTRA_SKYPATCHES])

    def test_set_allow_extra_skypatches_remember(self):
        project = RomProject.new(self.load_rom_path(), self.asset_project_path)

        try:
            project.set_allow_extra_skypatches(False, True)

            self.assertFalse(project.does_allow_extra_skypatches())
            asset_config = project._load_asset_config()
            self.assertFalse(asset_config[ALLOW_EXTRA_SKYPATCHES])
        finally:
            project.set_allow_extra_skypatches(True, True)

    def load_rom_path(self):
        if SKYTEMPLE_TEST_ROM_ENV in os.environ and os.environ[SKYTEMPLE_TEST_ROM_ENV] != "":
            return Path(os.environ[SKYTEMPLE_TEST_ROM_ENV])
        else:
            raise SkipTest("No ROM file provided or ROM not found.")
