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

        project.save_file(data_handler, file_path, file_data, skip_save_to_rom=True, rom_project=project)


def save_project_to_rom(rom_path: Path, asset_dir: Path, extracted_rom_dir: Path):
    project = RomProject.new(rom_path, asset_dir)
    rom_files = project.list_files(search_rom=False)

    for file_path, data_handler in rom_files.items():
        assets = project.load_assets(data_handler, file_path)
        file_data = project.open_file(data_handler, file_path, assets=assets, force=True)

        project.save_file(
            data_handler, file_path, file_data, skip_save_to_project_dir=True, extracted_rom_dir=extracted_rom_dir
        )


def main():
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(description="Transfer data between a ROM and an asset project.")
    parser.add_argument("operation", help="'rom_to_project' or 'project_to_rom")
    parser.add_argument("-r", "--rom_path", metavar="ROM_PATH", help="Path to the ROM file.")
    parser.add_argument("-a", "--asset_dir", metavar="ASSET_DIR", help="Directory to create the asset project in.")
    parser.add_argument(
        "-e",
        "--extracted_rom_dir",
        metavar="EXTRACTED_ROM_PATH",
        required=False,
        help="Path to the extracted ROM files.",
    )

    args = parser.parse_args()

    if args.operation == "rom_to_project":
        extract_rom_files_to_project(Path(args.rom_path), Path(args.asset_dir))
    elif args.operation == "project_to_rom":
        save_project_to_rom(Path(args.rom_path), Path(args.asset_dir), Path(args.extracted_rom_dir))
    else:
        raise ValueError(f"Invalid operation: {args.operation}")


if __name__ == "__main__":
    main()
