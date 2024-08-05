#!/usr/bin/env python3

import argparse
from pathlib import Path

import skytemple_files.common.cli as cli


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
        cli.extract_rom_files_to_project(Path(args.rom_path), Path(args.asset_dir))
    elif args.operation == "project_to_rom":
        cli.save_project_to_rom(Path(args.rom_path), Path(args.asset_dir), Path(args.extracted_rom_dir))
    else:
        raise ValueError(f"Invalid operation: {args.operation}")


if __name__ == "__main__":
    main()
