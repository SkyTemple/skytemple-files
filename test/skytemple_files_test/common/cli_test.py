import os.path
import shutil
from pathlib import Path
from unittest import TestCase

import skytemple_files.common.cli as cli
from skytemple_files.common.file_api_v2 import ROM_HASHES_FILE, ASSET_HASHES_FILE
from skytemple_files_test.common.temp_rom import (
    copy_rom_to_temp_file,
    delete_temp_asset_project,
    TEMP_ASSET_PROJECT_PATH,
    ASSET_PROJECT_PATH,
)


class CliTestCase(TestCase):
    def test_extract_rom_files_to_project(self):
        try:
            rom_path = copy_rom_to_temp_file()
            cli.extract_rom_files_to_project(rom_path, TEMP_ASSET_PROJECT_PATH, None)

            self.assertTrue(os.path.exists(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json")))

            rom_hashes_path = Path(TEMP_ASSET_PROJECT_PATH, ROM_HASHES_FILE)
            self.assertTrue(os.path.exists(rom_hashes_path))
            with open(rom_hashes_path, "r") as rom_hashes_file:
                self.assertTrue("f85089b1c47c9392c93f76f5d1baf9b28677454c BALANCE/waza_p.bin" in rom_hashes_file.read())
        finally:
            delete_temp_asset_project()

    def test_extract_rom_files_to_project_with_file_type(self):
        try:
            rom_path = copy_rom_to_temp_file()
            cli.extract_rom_files_to_project(rom_path, TEMP_ASSET_PROJECT_PATH, ["WAZA_P"])

            self.assertTrue(os.path.exists(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json")))
        finally:
            delete_temp_asset_project()

    def test_extract_rom_files_to_project_with_unimplemented_file_type(self):
        try:
            rom_path = copy_rom_to_temp_file()
            cli.extract_rom_files_to_project(rom_path, TEMP_ASSET_PROJECT_PATH, ["KAO"])

            self.assertFalse(os.path.exists(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json")))
        finally:
            delete_temp_asset_project()

    def test_save_project_to_rom(self):
        try:
            rom_path = copy_rom_to_temp_file()
            Path(TEMP_ASSET_PROJECT_PATH, "pokemon").mkdir(parents=True, exist_ok=True)
            shutil.copyfile(
                Path(ASSET_PROJECT_PATH, "pokemon", "moves.json"),
                Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json"),
            )
            cli.save_project_to_rom(rom_path, TEMP_ASSET_PROJECT_PATH, None, None)

            rom_hashes_path = Path(TEMP_ASSET_PROJECT_PATH, ROM_HASHES_FILE)
            self.assertTrue(os.path.exists(rom_hashes_path))
            with open(rom_hashes_path, "r") as rom_hashes_file:
                self.assertTrue("a7ed113f8b4f542ffc927a2fd5e4509327bef7d8 BALANCE/waza_p.bin" in rom_hashes_file.read())

            asset_hashes_path = Path(TEMP_ASSET_PROJECT_PATH, ASSET_HASHES_FILE)
            self.assertTrue(os.path.exists(asset_hashes_path))
            with open(asset_hashes_path, "r") as asset_hashes_file:
                self.assertTrue(
                    "bf21a9e8fbc5a3846fb05b4fa0859e0917b2202f pokemon/moves.json" in asset_hashes_file.read()
                )
        finally:
            delete_temp_asset_project()

    def test_save_project_to_rom_with_file_type(self):
        try:
            rom_path = copy_rom_to_temp_file()
            Path(TEMP_ASSET_PROJECT_PATH, "pokemon").mkdir(parents=True, exist_ok=True)
            shutil.copyfile(
                Path(ASSET_PROJECT_PATH, "pokemon", "moves.json"),
                Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json"),
            )
            cli.save_project_to_rom(rom_path, TEMP_ASSET_PROJECT_PATH, None, ["WAZA_P"])

            rom_hashes_path = Path(TEMP_ASSET_PROJECT_PATH, ROM_HASHES_FILE)
            self.assertTrue(os.path.exists(rom_hashes_path))
            with open(rom_hashes_path, "r") as rom_hashes_file:
                self.assertTrue("a7ed113f8b4f542ffc927a2fd5e4509327bef7d8 BALANCE/waza_p.bin" in rom_hashes_file.read())
        finally:
            delete_temp_asset_project()

    def test_save_project_to_rom_with_unimplemented_file_type(self):
        try:
            rom_path = copy_rom_to_temp_file()
            Path(TEMP_ASSET_PROJECT_PATH, "pokemon").mkdir(parents=True, exist_ok=True)
            shutil.copyfile(
                Path(ASSET_PROJECT_PATH, "pokemon", "moves.json"),
                Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json"),
            )
            cli.save_project_to_rom(rom_path, TEMP_ASSET_PROJECT_PATH, None, ["KAO"])

            self.assertFalse(os.path.exists(Path(TEMP_ASSET_PROJECT_PATH, "rom_hashes.sha1")))
        finally:
            delete_temp_asset_project()

    def test_save_project_to_rom_with_extracted_rom_dir(self):
        try:
            rom_path = copy_rom_to_temp_file()
            Path(TEMP_ASSET_PROJECT_PATH, "pokemon").mkdir(parents=True, exist_ok=True)
            shutil.copyfile(
                Path(ASSET_PROJECT_PATH, "pokemon", "moves.json"),
                Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json"),
            )
            cli.save_project_to_rom(rom_path, TEMP_ASSET_PROJECT_PATH, TEMP_ASSET_PROJECT_PATH, None)

            self.assertTrue(os.path.exists(Path(TEMP_ASSET_PROJECT_PATH, "BALANCE", "waza_p.bin")))
        finally:
            delete_temp_asset_project()

    def test_sync_project_and_rom_with_no_asset_project(self):
        try:
            rom_path = copy_rom_to_temp_file()
            cli.sync_project_and_rom(rom_path, TEMP_ASSET_PROJECT_PATH, None, ["WAZA_P"])

            # If there are no assets, assets should be created.
            self.assertTrue(os.path.exists(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json")))
            self.assertTrue(os.path.exists(Path(TEMP_ASSET_PROJECT_PATH, ROM_HASHES_FILE)))
            self.assertTrue(os.path.exists(Path(TEMP_ASSET_PROJECT_PATH, ASSET_HASHES_FILE)))
        finally:
            delete_temp_asset_project()

    def test_sync_project_and_rom_with_rom_hashes_mismatch(self):
        try:
            rom_path = copy_rom_to_temp_file()
            Path(TEMP_ASSET_PROJECT_PATH, "pokemon").mkdir(parents=True, exist_ok=True)
            with open(Path(TEMP_ASSET_PROJECT_PATH, ROM_HASHES_FILE), "w+") as rom_hashes_file:
                rom_hashes_file.write("0000000000000000000000000000000000000000 BALANCE/waza_p.bin\n")
            with open(Path(TEMP_ASSET_PROJECT_PATH, ASSET_HASHES_FILE), "w+") as asset_hashes_file:
                asset_hashes_file.writelines(
                    [
                        "bf21a9e8fbc5a3846fb05b4fa0859e0917b2202f pokemon/learnsets.json\n",
                        "bf21a9e8fbc5a3846fb05b4fa0859e0917b2202f pokemon/moves.json\n",
                    ]
                )
            with open(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "learnsets.json"), "w+") as learnsets_file:
                learnsets_file.write("{}")
            with open(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json"), "w+") as moves_files:
                moves_files.write("{}")

            cli.sync_project_and_rom(rom_path, TEMP_ASSET_PROJECT_PATH, None, ["WAZA_P"])

            # If ROM hashes don't match and asset hashes do, extract ROM files to assets.
            self.assertTrue(os.path.getsize(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json")) > 2)
        finally:
            delete_temp_asset_project()

    def test_sync_project_and_rom_with_both_hashes_match(self):
        try:
            rom_path = copy_rom_to_temp_file()
            Path(TEMP_ASSET_PROJECT_PATH, "pokemon").mkdir(parents=True, exist_ok=True)
            with open(Path(TEMP_ASSET_PROJECT_PATH, ROM_HASHES_FILE), "w+") as rom_hashes_file:
                rom_hashes_file.write("f85089b1c47c9392c93f76f5d1baf9b28677454c BALANCE/waza_p.bin\n")
            with open(Path(TEMP_ASSET_PROJECT_PATH, ASSET_HASHES_FILE), "w+") as asset_hashes_file:
                asset_hashes_file.writelines(
                    [
                        "bf21a9e8fbc5a3846fb05b4fa0859e0917b2202f pokemon/learnsets.json\n",
                        "bf21a9e8fbc5a3846fb05b4fa0859e0917b2202f pokemon/moves.json\n",
                    ]
                )
            with open(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "learnsets.json"), "w+") as learnsets_file:
                learnsets_file.write("{}")
            with open(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json"), "w+") as moves_files:
                moves_files.write("{}")

            cli.sync_project_and_rom(rom_path, TEMP_ASSET_PROJECT_PATH, None, ["WAZA_P"])

            # If asset and ROM hashes match, nothing should happen.
            self.assertEqual(2, os.path.getsize(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json")))
        finally:
            delete_temp_asset_project()

    def test_sync_project_and_rom_with_asset_hashes_mismatch(self):
        try:
            rom_path = copy_rom_to_temp_file()
            cli.extract_rom_files_to_project(rom_path, TEMP_ASSET_PROJECT_PATH, ["WAZA_P"])

            Path(TEMP_ASSET_PROJECT_PATH, "pokemon").mkdir(parents=True, exist_ok=True)
            with open(Path(TEMP_ASSET_PROJECT_PATH, ROM_HASHES_FILE), "w+") as rom_hashes_file:
                rom_hashes_file.write("f85089b1c47c9392c93f76f5d1baf9b28677454c BALANCE/waza_p.bin\n")
            with open(Path(TEMP_ASSET_PROJECT_PATH, ASSET_HASHES_FILE), "w+") as asset_hashes_file:
                asset_hashes_file.writelines(
                    [
                        "0000000000000000000000000000000000000000 pokemon/learnsets.json\n",
                        "0000000000000000000000000000000000000000 pokemon/moves.json\n",
                    ]
                )
            with open(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "learnsets.json"), "w+") as learnsets_file:
                learnsets_file.write("{}")
            with open(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json"), "w+") as moves_files:
                moves_files.write("{}")

            cli.sync_project_and_rom(rom_path, TEMP_ASSET_PROJECT_PATH, None, ["WAZA_P"])

            # If ROM hashes match and asset hashes don't, save assets to ROM.
            with open(Path(TEMP_ASSET_PROJECT_PATH, ROM_HASHES_FILE), "r") as rom_hashes_file:
                self.assertTrue("a7ed113f8b4f542ffc927a2fd5e4509327bef7d8 BALANCE/waza_p.bin" in rom_hashes_file.read())
        finally:
            delete_temp_asset_project()

    def test_sync_project_and_rom_with_both_hashes_mismatch(self):
        try:
            rom_path = copy_rom_to_temp_file()
            cli.extract_rom_files_to_project(rom_path, TEMP_ASSET_PROJECT_PATH, ["WAZA_P"])

            Path(TEMP_ASSET_PROJECT_PATH, "pokemon").mkdir(parents=True, exist_ok=True)
            with open(Path(TEMP_ASSET_PROJECT_PATH, ROM_HASHES_FILE), "w+") as rom_hashes_file:
                rom_hashes_file.write("0000000000000000000000000000000000000000 BALANCE/waza_p.bin\n")
            with open(Path(TEMP_ASSET_PROJECT_PATH, ASSET_HASHES_FILE), "w+") as asset_hashes_file:
                asset_hashes_file.writelines(
                    [
                        "0000000000000000000000000000000000000000 pokemon/learnsets.json\n",
                        "0000000000000000000000000000000000000000 pokemon/moves.json\n",
                    ]
                )
            with open(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "learnsets.json"), "w+") as learnsets_file:
                learnsets_file.write("{}")
            with open(Path(TEMP_ASSET_PROJECT_PATH, "pokemon", "moves.json"), "w+") as moves_files:
                moves_files.write("{}")

                # If both hashes mismatch, the user is prompted to select which side to use.
                # pytest can't input to stdin and throws an OSError, but that still indicates the user was prompted.
                self.assertRaises(
                    OSError, cli.sync_project_and_rom, rom_path, TEMP_ASSET_PROJECT_PATH, None, ["WAZA_P"]
                )
        finally:
            delete_temp_asset_project()
