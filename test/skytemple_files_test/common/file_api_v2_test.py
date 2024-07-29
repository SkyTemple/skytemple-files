import os
import shutil
from pathlib import Path
from unittest import TestCase, SkipTest

from skytemple_files.common.types.file_storage import Asset, AssetSpec
from skytemple_files.common.file_api_v2 import RomProject, SkyTempleProjectFileStorage, ALLOW_EXTRA_SKYPATCHES
from skytemple_files.common.types.file_types import FileType
from skytemple_files_test.case import load_rom_path

ASSET_PROJECT_PATH = Path("skytemple_files_test", "common", "fixtures", "asset_project")
ROM_COPY_PATH = Path("skytemple_files_test", "common", "fixtures", "rom_copy.nds")


def copy_rom_to_temp_file() -> Path:
    """
    Copies the provided ROM to a temporary file for testing.
    This allows testing writes to the ROM without changing the ROM supplied by the user.
    """
    rom_path = load_rom_path()
    shutil.copy(rom_path, ROM_COPY_PATH)
    return ROM_COPY_PATH


def delete_temp_rom():
    os.remove(ROM_COPY_PATH)


class RomProjectTestCase(TestCase):
    def test_load_assets(self):
        project = RomProject.new(load_rom_path(), ASSET_PROJECT_PATH)

        assets = project.load_assets(FileType.WAZA_P, Path("BALANCE", "waza_p.bin"))
        self.assertEqual(2, len(assets))

        self.assertEqual(Asset, assets[0].__class__)
        self.assertEqual(Path("pokemon", "moves.json"), assets[0].spec.path)

        self.assertEqual(AssetSpec, assets[1].__class__)
        self.assertEqual(Path("pokemon", "learnsets.json"), assets[1].path)

    def test_list_files_rom(self):
        project = RomProject.new(load_rom_path(), ASSET_PROJECT_PATH)

        file_list = project.list_files(search_project_dir=False)

        expected_path = Path("BALANCE", "waza_p.bin")
        self.assertTrue(expected_path in file_list)
        self.assertEqual(FileType.WAZA_P, file_list[expected_path])

    def test_list_files_project(self):
        project = RomProject.new(load_rom_path(), ASSET_PROJECT_PATH)

        file_list = project.list_files(search_rom=False)

        expected_path = Path("BALANCE", "waza_p.bin")
        self.assertTrue(expected_path in file_list)
        self.assertEqual(FileType.WAZA_P, file_list[expected_path])

    def test_save_file_extracted_rom_dir(self):
        project = RomProject.new(load_rom_path(), ASSET_PROJECT_PATH)
        rom_path = Path("BALANCE", "waza_p.bin")
        assets = project.load_assets(FileType.WAZA_P, rom_path)
        assets = [asset for asset in assets if isinstance(asset, Asset)]
        file_data = project.open_file(FileType.WAZA_P, rom_path, assets=assets, force=True)

        extracted_rom_dir = Path(ASSET_PROJECT_PATH, "extracted_rom")
        expected_file_path = Path(extracted_rom_dir, rom_path)
        try:
            project.save_file(
                FileType.WAZA_P,
                rom_path,
                file_data,
                skip_save_to_rom=True,
                skip_save_to_project_dir=True,
                extracted_rom_dir=extracted_rom_dir,
            )

            self.assertTrue(expected_file_path.exists())
        finally:
            if expected_file_path.exists():
                os.remove(str(expected_file_path))

    def test_load_allow_extra_skypatches(self):
        project = RomProject.new(load_rom_path(), ASSET_PROJECT_PATH)

        self.assertTrue(project.does_allow_extra_skypatches())

    def test_set_allow_extra_skypatches_no_remember(self):
        project = RomProject.new(load_rom_path(), ASSET_PROJECT_PATH)

        project.set_allow_extra_skypatches(False)

        self.assertFalse(project.does_allow_extra_skypatches())
        # Assert that the config file has not changed.
        asset_config = project._load_asset_config()
        self.assertTrue(asset_config[ALLOW_EXTRA_SKYPATCHES])

    def test_set_allow_extra_skypatches_remember(self):
        project = RomProject.new(load_rom_path(), ASSET_PROJECT_PATH)

        try:
            project.set_allow_extra_skypatches(False, True)

            self.assertFalse(project.does_allow_extra_skypatches())
            asset_config = project._load_asset_config()
            self.assertFalse(asset_config[ALLOW_EXTRA_SKYPATCHES])
        finally:
            project.set_allow_extra_skypatches(True, True)


class SkyTempleProjectFileStorageTestCase(TestCase):
    def test_get_from_rom(self):
        storage = SkyTempleProjectFileStorage(load_rom_path(), ASSET_PROJECT_PATH)

        file_bytes = storage.get_from_rom(Path("BALANCE", "waza_p.bin"))

        self.assertEqual(80432, len(file_bytes))

    def test_get_from_rom_invalid_file(self):
        storage = SkyTempleProjectFileStorage(load_rom_path(), ASSET_PROJECT_PATH)

        self.assertRaises(FileNotFoundError, storage.get_from_rom, Path("BALANCE", "missing.bin"))

    def test_store_in_rom_existing_file(self):
        try:
            rom_path = copy_rom_to_temp_file()
            storage = SkyTempleProjectFileStorage(rom_path, ASSET_PROJECT_PATH)

            test_data: bytes = bytes(300)
            storage.store_in_rom(Path("BALANCE", "waza_p.bin"), test_data)

            storage = SkyTempleProjectFileStorage(rom_path, ASSET_PROJECT_PATH)
            file_bytes = storage.get_from_rom(Path("BALANCE", "waza_p.bin"))
            self.assertEqual(test_data, file_bytes)
        finally:
            delete_temp_rom()

    def test_store_in_rom_new_file(self):
        try:
            rom_path = copy_rom_to_temp_file()
            storage = SkyTempleProjectFileStorage(rom_path, ASSET_PROJECT_PATH)

            test_data: bytes = bytes(300)
            storage.store_in_rom(Path("BALANCE", "new.bin"), test_data)

            storage = SkyTempleProjectFileStorage(rom_path, ASSET_PROJECT_PATH)
            file_bytes = storage.get_from_rom(Path("BALANCE", "new.bin"))
            self.assertEqual(test_data, file_bytes)
        finally:
            delete_temp_rom()

    def test_get_asset(self):
        storage = SkyTempleProjectFileStorage(load_rom_path(), ASSET_PROJECT_PATH)

        asset = storage.get_asset(Path("pokemon", "moves.json"), Path("BALANCE", "waza_p.bin"))

        self.assertEqual(Path("pokemon", "moves.json"), asset.spec.path)
        self.assertEqual(Path("BALANCE", "waza_p.bin"), asset.spec.rom_path)
        self.assertIsNone(asset.expected_rom_obj_hash)
        self.assertEqual(b"f85089b1c47c9392c93f76f5d1baf9b28677454c", asset.actual_rom_obj_hash)
        self.assertIsNone(asset.expected_asset_hash)
        self.assertEqual(b"bf21a9e8fbc5a3846fb05b4fa0859e0917b2202f", asset.actual_asset_hash)
        self.assertEqual(b"{}", asset.data)

    def test_get_asset_invalid_project_file(self):
        storage = SkyTempleProjectFileStorage(load_rom_path(), ASSET_PROJECT_PATH)

        self.assertRaises(
            FileNotFoundError, storage.get_asset, Path("BALANCE", "missing.json"), Path("BALANCE", "waza_p.bin")
        )

    def test_get_asset_invalid_rom_file(self):
        storage = SkyTempleProjectFileStorage(load_rom_path(), ASSET_PROJECT_PATH)

        self.assertRaises(
            FileNotFoundError, storage.get_asset, Path("pokemon", "moves.json"), Path("BALANCE", "missing.bin")
        )

    def test_store_asset(self):
        storage = SkyTempleProjectFileStorage(load_rom_path(), ASSET_PROJECT_PATH)
        test_data = b'{"test": "test"}'

        asset = storage.get_asset(Path("pokemon", "moves.json"), Path("BALANCE", "waza_p.bin"))
        before_data = asset.data

        try:
            data = storage.store_asset(Path("pokemon", "moves.json"), Path("BALANCE", "waza_p.bin"), test_data)

            self.assertEqual(test_data, data)
            asset = storage.get_asset(Path("pokemon", "moves.json"), Path("BALANCE", "waza_p.bin"))
            self.assertEqual(test_data, asset.data)
        finally:
            storage.store_asset(Path("pokemon", "moves.json"), Path("BALANCE", "waza_p.bin"), before_data)

    def test_store_asset_invalid_project_file(self):
        storage = SkyTempleProjectFileStorage(load_rom_path(), ASSET_PROJECT_PATH)

        self.assertRaises(
            FileNotFoundError, storage.get_asset, Path("BALANCE", "missing.json"), Path("BALANCE", "waza_p.bin")
        )

    def test_hash_of_rom_object(self):
        storage = SkyTempleProjectFileStorage(load_rom_path(), ASSET_PROJECT_PATH)

        sha1_hash = storage.hash_of_rom_object(Path("BALANCE", "waza_p.bin"))

        self.assertEqual("f85089b1c47c9392c93f76f5d1baf9b28677454c", sha1_hash)

    def test_hash_of_asset(self):
        storage = SkyTempleProjectFileStorage(load_rom_path(), ASSET_PROJECT_PATH)

        sha1_hash = storage.hash_of_asset(Path("pokemon", "moves.json"))

        self.assertEqual("bf21a9e8fbc5a3846fb05b4fa0859e0917b2202f", sha1_hash)
