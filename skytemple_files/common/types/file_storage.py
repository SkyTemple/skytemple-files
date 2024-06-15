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
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass
class AssetSpec:
    path: Path
    rom_path: Path

    # handler internal category name, to know which kind of asset to generate
    category: str
    # handler internal identifier, to know which kind of asset to generate
    id: str


@dataclass
class Asset:
    spec: AssetSpec
    expected_rom_obj_hash: bytes | None  # may be None if no hash info was stored yet.
    actual_rom_obj_hash: bytes | None  # may be None if the file does not exist in ROM.
    expected_asset_hash: bytes | None  # may be None if no hash info was stored yet.
    actual_asset_hash: bytes | None  # may be None if no hash info was stored yet.
    data: bytes

    def do_rom_hashes_match(self):
        """
        Check if the expected hash of the binary object file matches the hash of the binary file built using this asset.

        If they mismatch but `self.do_asset_hashes_match` returns True for this and all other assets used to build this
        object, then the file in the ROM was changed externally. Otherwise, if for any asset
        `self.do_asset_hashes_match` returns False, then there were changes in both the ROM and the assets.
        """
        return self.expected_rom_obj_hash == self.actual_rom_obj_hash

    def do_asset_hashes_match(self):
        """
        Check if the asset is unchanged since it was last used to build the ROM. If this returns True, then this
        asset file was not changed since the ROM object was last built, otherwise this asset file was changed, and
        the ROM object should be re-built.
        """
        return self.expected_asset_hash == self.actual_asset_hash

    def do_hashes_match(self):
        return self.do_rom_hashes_match() and self.do_asset_hashes_match()


class FileStorage(Protocol):
    def get_from_rom(self, path: Path) -> bytes:
        """
        Get the bytes of a file from ROM.
        Raises `FileNotFound` if the file under `path` was not found.
        """
        ...

    def store_in_rom(self, path: Path, data: bytes) -> bytes:
        """Store a file in the ROM."""
        ...

    def get_asset(self, path: Path, for_rom_path: Path) -> Asset:
        """
        Returns the bytes of an asset file and its corresponding hash (if any).
        Raises `FileNotFound` if the asset under `path` was not found.
        """
        ...

    def store_asset(self, path: Path, for_rom_path: Path, data: bytes) -> bytes:
        """Store an asset file."""
        ...


class AssetHashMismatchError(Exception):
    """
    An exception that signals that loading an asset has been aborted because the hash of the
    ROM model corresponding to an asset mismatch.
    """

    def __init__(
        self,
        message,
        path_asset: Path,
        path_rom_file: Path,
        asset: Asset | None,  # If None, the asset was missing
    ):
        super().__init__(message)
        self.path_asset = path_asset
        self.path_rom_file = path_rom_file
        self.asset = asset
