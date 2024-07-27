#!/usr/bin/env python3
"""
This is a sample script to create an asset project with the v2 file API.
For all implemented file handlers, asset files will be created using data from the provided ROM.
"""
import argparse
from pathlib import Path

from skytemple_files.common.file_api_v2 import RomProject


def extract_rom_files_to_project(rom_path: Path, asset_dir: Path):
    project = RomProject.new(rom_path, asset_dir)
    rom_files = project.list_files(search_project_dir=False)

    for file_path, data_handler in rom_files.items():
        file_data = project.open_file(data_handler, file_path, force=True, load_from_rom=True)

        project.save_file(data_handler, file_path, file_data, skip_save_to_rom=True)


def main():
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(description="Creates an asset project from the files in a ROM.")
    parser.add_argument("rom_path", metavar="ROM_PATH", help="Path to the ROM file.")
    parser.add_argument("asset_dir", metavar="ASSET_DIR", help="Directory to create the asset project in.")

    args = parser.parse_args()

    extract_rom_files_to_project(Path(args.rom_path), Path(args.asset_dir))


if __name__ == "__main__":
    main()
