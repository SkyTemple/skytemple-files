import os
import shutil
from pathlib import Path

from skytemple_files_test.case import load_rom_path

ASSET_PROJECT_PATH = Path("skytemple_files_test", "common", "fixtures", "asset_project")
TEMP_ASSET_PROJECT_PATH = Path("skytemple_files_test", "common", "fixtures", "temp_asset_project")
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
    if os.path.exists(ROM_COPY_PATH):
        os.remove(ROM_COPY_PATH)


def delete_temp_asset_project():
    if os.path.exists(TEMP_ASSET_PROJECT_PATH):
        shutil.rmtree(TEMP_ASSET_PROJECT_PATH)
