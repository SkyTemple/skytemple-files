import os
from pathlib import Path
from unittest import TestCase

from skytemple_files.common.types.file_storage import Asset, AssetSpec
from skytemple_files.common.file_api_v2 import (
    RomProject,
    SkyTempleProjectFileStorage,
    ALLOW_EXTRA_SKYPATCHES,
    ASSET_HASHES_FILE,
    ROM_HASHES_FILE,
    FILE_CONFIG_FILE_NAME,
)
from skytemple_files.common.types.file_types import FileType
from skytemple_files_test.case import load_rom_path
from skytemple_files_test.common.temp_rom import ASSET_PROJECT_PATH, copy_rom_to_temp_file, delete_temp_rom


class RomProjectTestCase(TestCase):
    def test_load_assets(self):
        project = RomProject.new(load_rom_path(), ASSET_PROJECT_PATH)

        assets = project.load_assets(FileType.WAZA_P, Path("BALANCE", "waza_p.bin"))
        self.assertEqual(2, len(assets))

        self.assertEqual(Asset, assets[0].__class__)
        self.assertEqual(Path("pokemon", "moves.json"), assets[0].spec.path)

        self.assertEqual(AssetSpec, assets[1].__class__)
        self.assertEqual(Path("pokemon", "learnsets.json"), assets[1].path)

    def test_list_files_default_config(self):
        try:
            project = RomProject.new(load_rom_path(), ASSET_PROJECT_PATH)

            file_list = project.list_files()

            expected_path = Path("BALANCE", "waza_p.bin")
            self.assertTrue(expected_path in file_list)
            self.assertEqual(FileType.WAZA_P, file_list[expected_path])
        finally:
            delete_file_config()

    def test_list_files_custom_config(self):
        try:
            project = RomProject.new(load_rom_path(), ASSET_PROJECT_PATH)
            create_file_config("BALANCE/waza_p2.bin: FileType.WAZA_P")

            file_list = project.list_files()

            expected_path = Path("BALANCE", "waza_p2.bin")
            self.assertTrue(expected_path in file_list)
            self.assertEqual(FileType.WAZA_P, file_list[expected_path])
        finally:
            delete_file_config()

    def test_list_files_custom_config_glob(self):
        try:
            project = RomProject.new(load_rom_path(), ASSET_PROJECT_PATH)
            create_file_config("BALANCE/waza_p*.bin: FileType.WAZA_P")

            file_list = project.list_files()

            self.assertEqual(2, len(file_list))
            for file_name in ["waza_p.bin", "waza_p2.bin"]:
                expected_path = Path("BALANCE", file_name)
                self.assertTrue(expected_path in file_list)
                self.assertEqual(FileType.WAZA_P, file_list[expected_path])
        finally:
            delete_file_config()

    def test_list_files_custom_config_ignore_invalid_file_type(self):
        try:
            project = RomProject.new(load_rom_path(), ASSET_PROJECT_PATH)
            create_file_config("BALANCE/waza_p.bin: FileType.BLAH")

            file_list = project.list_files()

            self.assertEqual(0, len(file_list))
        finally:
            delete_file_config()

    def test_list_files_custom_config_ignore_invalid_file_type_value(self):
        try:
            project = RomProject.new(load_rom_path(), ASSET_PROJECT_PATH)
            create_file_config("BALANCE/waza_p.bin: BLAH")

            file_list = project.list_files()

            self.assertEqual(0, len(file_list))
        finally:
            delete_file_config()

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
            self.assertEqual(
                "b23b62bbd22a602b113038a07217c6abcb156f06", storage.rom_hashes[Path("BALANCE", "waza_p.bin")]
            )
        finally:
            delete_temp_rom()
            revert_hash_files()

    def test_store_in_rom_new_file(self):
        try:
            rom_path = copy_rom_to_temp_file()
            storage = SkyTempleProjectFileStorage(rom_path, ASSET_PROJECT_PATH)

            test_data: bytes = bytes(300)
            storage.store_in_rom(Path("BALANCE", "new.bin"), test_data)

            storage = SkyTempleProjectFileStorage(rom_path, ASSET_PROJECT_PATH)
            file_bytes = storage.get_from_rom(Path("BALANCE", "new.bin"))
            self.assertEqual(test_data, file_bytes)
            self.assertEqual(
                "f85089b1c47c9392c93f76f5d1baf9b28677454c", storage.rom_hashes[Path("BALANCE", "waza_p.bin")]
            )
            self.assertEqual("b23b62bbd22a602b113038a07217c6abcb156f06", storage.rom_hashes[Path("BALANCE", "new.bin")])
        finally:
            delete_temp_rom()
            revert_hash_files()

    def test_get_asset(self):
        storage = SkyTempleProjectFileStorage(load_rom_path(), ASSET_PROJECT_PATH)

        asset = storage.get_asset(Path("pokemon", "moves.json"), Path("BALANCE", "waza_p.bin"))

        self.assertEqual(Path("pokemon", "moves.json"), asset.spec.path)
        self.assertEqual(Path("BALANCE", "waza_p.bin"), asset.spec.rom_path)
        self.assertEqual("f85089b1c47c9392c93f76f5d1baf9b28677454c", asset.expected_rom_obj_hash)
        self.assertEqual("f85089b1c47c9392c93f76f5d1baf9b28677454c", asset.actual_rom_obj_hash)
        self.assertEqual("bf21a9e8fbc5a3846fb05b4fa0859e0917b2202f", asset.expected_asset_hash)
        self.assertEqual("bf21a9e8fbc5a3846fb05b4fa0859e0917b2202f", asset.actual_asset_hash)
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
            self.assertEqual(
                "31ead60c9066eefb8011f3f68aed25d004d60957", storage.asset_hashes[Path("pokemon", "moves.json")]
            )
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


def revert_hash_files():
    with open(Path(ASSET_PROJECT_PATH, ASSET_HASHES_FILE), "w") as asset_hashes_file:
        asset_hashes_file.write("bf21a9e8fbc5a3846fb05b4fa0859e0917b2202f pokemon/moves.json\n")
    with open(Path(ASSET_PROJECT_PATH, ROM_HASHES_FILE), "w") as rom_hashes_file:
        rom_hashes_file.write("f85089b1c47c9392c93f76f5d1baf9b28677454c BALANCE/waza_p.bin\n")


def create_file_config(contents: str):
    with open(Path(ASSET_PROJECT_PATH, FILE_CONFIG_FILE_NAME), "w") as file_config_file:
        file_config_file.write(contents)


def delete_file_config():
    file_config_path = Path(ASSET_PROJECT_PATH, FILE_CONFIG_FILE_NAME)
    if os.path.exists(file_config_path):
        os.remove(file_config_path)
