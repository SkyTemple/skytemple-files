"""
Requires extra: cli

CLI API modules for skytemple-files. See documentation of commands.
"""
#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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

import argparse
from pathlib import Path

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.file_api_v2 import RomProject


def extract_rom_files_to_project(rom_path: Path, asset_dir: Path, file_types: list[str] | None):
    accepted_file_types: set[type[DataHandler]] | None = load_accepted_file_types(file_types)
    project = RomProject.new(rom_path, asset_dir)
    rom_files = project.list_files(search_project_dir=False)

    for file_path, data_handler in rom_files.items():
        if accepted_file_types is None or data_handler in accepted_file_types:
            file_data = project.open_file(data_handler, file_path, force=True, load_from_rom=True)

            project.save_file(data_handler, file_path, file_data, skip_save_to_rom=True, rom_project=project)


def save_project_to_rom(rom_path: Path, asset_dir: Path, extracted_rom_dir: Path, file_types: list[str] | None):
    accepted_file_types: set[type[DataHandler]] | None = load_accepted_file_types(file_types)
    project = RomProject.new(rom_path, asset_dir)
    rom_files = project.list_files(search_rom=False)

    for file_path, data_handler in rom_files.items():
        if accepted_file_types is None or data_handler in accepted_file_types:
            assets = project.load_assets(data_handler, file_path)
            file_data = project.open_file(data_handler, file_path, assets=assets, force=True)

            project.save_file(
                data_handler, file_path, file_data, skip_save_to_project_dir=True, extracted_rom_dir=extracted_rom_dir
            )


def load_accepted_file_types(file_types: list[str] | None) -> set[type[DataHandler]] | None:
    if file_types is None:
        return None
    return set([getattr(FileType, file_type) for file_type in file_types])


def main():
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(description="Transfer data between a ROM and an asset project.")
    parser.add_argument("assets")
    parser.add_argument("-o", "--operation", help="'rom_to_project' or 'project_to_rom")
    parser.add_argument("-r", "--rom_path", metavar="ROM_PATH", help="Path to the ROM file.")
    parser.add_argument("-a", "--asset_dir", metavar="ASSET_DIR", help="Directory to create the asset project in.")
    parser.add_argument(
        "-f", "--file_types", nargs="*", metavar="FILE_TYPES", help="File types to include when transferring."
    )
    parser.add_argument(
        "-e",
        "--extracted_rom_dir",
        metavar="EXTRACTED_ROM_PATH",
        required=False,
        help="Path to the extracted ROM files.",
    )

    args = parser.parse_args()

    if args.assets:
        if args.operation == "rom_to_project":
            extract_rom_files_to_project(Path(args.rom_path), Path(args.asset_dir), args.file_types)
        elif args.operation == "project_to_rom":
            save_project_to_rom(
                Path(args.rom_path), Path(args.asset_dir), Path(args.extracted_rom_dir), args.file_types
            )
        else:
            raise ValueError(f"Invalid operation: {args.operation}")


if __name__ == "__main__":
    main()
