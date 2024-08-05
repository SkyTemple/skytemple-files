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
