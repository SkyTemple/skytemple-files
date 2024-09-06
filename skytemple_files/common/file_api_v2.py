"""
API to read/write files from ROMs and file storage.

Using this API files and hardcoded in a game ROM can be manipulated
while also storing machine and human-readable versions of those files
out-of-ROM (so-called "assets"; e.g. as YAML or PNG).
Requesting to read a file from the ROM will first try to load it from assets,
and fall back to the ROM if no assets have been saved yet for that file.
Writing a model back to ROM will also write the model to the asset files.

The API implements mechanisms for dealing with conflicts between the state of
assets and actual files in ROM.

This API also supports handling patches and exposes the static ROM data (Pmd2Data).

The entrypoint is `RomProject`.
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
from __future__ import annotations

import fnmatch
import shutil
from pathlib import Path, PurePosixPath
from typing import Sequence, TypeVar, cast
from collections import defaultdict
from hashlib import sha1
import json

from ruamel.yaml import YAML

from ndspy.fnt import Folder
from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.rom_data.loader import RomDataLoader
from skytemple_files.common.types.file_types import FileType
from skytemple_files.patch.patches import Patcher
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.util import OptionalKwargs, get_ppmdu_config_for_rom, create_file_in_rom, get_resources_dir

from skytemple_files.common.types.file_storage import (
    FileStorage,
    Asset,
    AssetSpec,
    AssetHashMismatchError,
    AssetHash,
)

T = TypeVar("T")

ASSET_CONFIG_FILE = "asset_config.json"
ROM_HASHES_FILE = "rom_hashes.sha1"
ASSET_HASHES_FILE = "asset_hashes.sha1"
DEFAULT_FILE_CONFIG_FILE = Path("file_api_v2", "default_file_config.yml")
FILE_CONFIG_FILE_NAME = "file_config.yml"

SKYPATCHES_DIR = "skypatches"
ALLOW_EXTRA_SKYPATCHES = "allow_extra_skypatches"


def _first_missing_asset(assets: Sequence[Asset | AssetSpec]) -> AssetSpec | None:
    for x in assets:
        if isinstance(x, AssetSpec):
            return x
    return None


def _all_assets_missing(assets: Sequence[Asset | AssetSpec]) -> bool:
    return all(isinstance(x, AssetSpec) for x in assets)


def extract_assets(assets: Sequence[Asset | AssetSpec]) -> Sequence[Asset]:
    """
    Given a list of assets and non-existent assets (AssetSpecs), see `RomProject.load_assets`
    - returns either a list of assets if all assets exists
    - returns the empty list of no assets exist at all
    - throws a `AssetHashMismatchError` for the first missing asset if any asset exists, but at least one is missing.
    """
    first_missing_asset = _first_missing_asset(assets)
    if first_missing_asset is not None:
        # If all are missing, return an empty list
        if _all_assets_missing(assets):
            return []
        else:
            raise AssetHashMismatchError(
                "TODO!!",  # TODO
                first_missing_asset.path,
                first_missing_asset.rom_path,
                None,
            )
    return cast(Sequence[Asset], assets)


class RomProject:
    """
    A SkyTemple Files ROM project.

    A new eos-asset-spec standard compliant project can be created with `RomProject.new`. Otherwise,
    a custom project can be created using `RomProject.__init__`. Custom projects can also work without
    actual ROM files, in which case all operations which would usually get/set data from/to the ROM may fail.
    """

    _file_storage: FileStorage
    _rom: NintendoDSRom | None
    _static_data: Pmd2Data
    _allow_extra_skypatches: bool | None
    _patcher: Patcher | None
    _asset_config: dict

    @property
    def rom(self) -> NintendoDSRom | None:
        """
        The underlying ROM. May return None for ROM-less projects.
        Projects created via `self.new` will always have a ROM.
        """
        return self._rom

    @property
    def file_storage(self) -> FileStorage:
        """
        The underlying file storage for interacting with the ROM and asset project file systems.
        """
        return self._file_storage

    @property
    def static_data(self) -> Pmd2Data:
        """
        PPMDU static data for this ROM project.
        """
        return self._static_data

    @property
    def patcher(self):
        """
        Returns a patcher. May load arbitrary code from SkyPatches, see `self.does_allow_extra_skypatches`.
        This may be cached until `self.set_allow_extra_skypatches` was called.
        """
        if self.rom is None:
            raise ValueError("No ROM available to patch")
        if not self._patcher:
            self._patcher = Patcher(self.rom, self.static_data)
            if self.does_allow_extra_skypatches():
                self._load_extra_skypatches()
        return self._patcher

    def __init__(
        self,
        file_storage: FileStorage,
        rom: NintendoDSRom | None,
        static_data: Pmd2Data | None = None,
    ):
        """
        Initialize a ROM project with a custom file storage backend.
        If no ROM is supplied, `static_data` must be supplied.
        """
        self._file_storage = file_storage
        self._rom = rom
        if static_data is None:
            if rom is None:
                raise ValueError("A RomProject must be provided static data if no ROM is provided.")
            self._static_data = get_ppmdu_config_for_rom(rom, init_from_rom=False)
            self._enrich_static_data()
        else:
            self._static_data = static_data

        self._patcher = None
        self._asset_config = self._load_asset_config()
        self._allow_extra_skypatches = self._load_allow_extra_skypatches()

    @classmethod
    def new(cls, rom_path: Path, project_dir: Path):
        """
        Create or open an eos-asset-spec compatible standard SkyTemple ROM project.

        `rom_path` is the path to the ROM to save to and to read from when assets in `project_dir`
        do not exist yet (or reading from ROM is otherwise forced). The ROM must already exist.
        """
        proj = SkyTempleProjectFileStorage(rom_path, project_dir)
        return cls(proj, proj.rom)

    def does_allow_extra_skypatches(self) -> bool | None:
        """
        None (effectively False) by default.

        If None this means the user has not set this value yet and should
        potentially be asked.

        If True, getting `self.patcher` will return a patcher with extra SkyPatches stored
        in the project directory. Otherwise, the patcher will only return builtin patches.
        """
        return self._allow_extra_skypatches

    def set_allow_extra_skypatches(self, value: bool, remember: bool = False):
        """
        Set whether extra SkyPatches can be loaded, see `self.does_allow_extra_skypatches`.
        If `remember` is set to True and the `value` is True, the next time this project is loaded,
        SkyPatches will be automatically allowed unless the list of hashes SkyPatches (by name) changes
        (see `self.list_extra_skypatches`). If `value` is False and `remember` is True, the next time
        the project is loaded,

        If `remember` is False, the next time the project is opened the value will be None again (default).
        """
        self._patcher = None
        self._allow_extra_skypatches = value
        if remember:
            self._asset_config[ALLOW_EXTRA_SKYPATCHES] = value
            self._save_asset_config()

    def load_assets(self, handler: type[DataHandler[T]], path_to_rom_obj: Path) -> Sequence[Asset | AssetSpec]:
        """Returns loaded bytes of assets or just the spec if it's missing."""
        assets: list[Asset | AssetSpec] = []
        for spec in handler.asset_specs(path_to_rom_obj):
            try:
                assets.append(self._file_storage.get_asset_from_spec(spec))
            except FileNotFoundError:
                assets.append(spec)
        return assets

    def list_files(self) -> dict[Path, type[DataHandler[T]]]:
        """
        Returns a dictionary of all files in the project and their corresponding handlers.

        The dictionary is built from information in the file config within the asset project.
        A default file config is created if one doesn't exist.
        """
        file_config_path = Path(self.file_storage.get_project_dir(), FILE_CONFIG_FILE_NAME)
        if not file_config_path.exists():
            default_file_config_path = Path(get_resources_dir(), DEFAULT_FILE_CONFIG_FILE)
            if not file_config_path.parent.exists():
                file_config_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(default_file_config_path, file_config_path)
            print(f"Initialized default file config at {file_config_path}")

        with open(file_config_path, "r") as file_config_file:
            yaml = YAML(typ="safe")
            file_config_yaml: dict[str, str] = yaml.load(file_config_file.read())

        def get_files_in_folder(folder_path, folder: Folder) -> list[PurePosixPath]:
            # Since the file config supports globs, return Posix paths regardless of OS.
            folder_files = [PurePosixPath(folder_path, folder_file) for folder_file in folder.files]
            for subfolder in folder.folders:
                folder_files.extend(get_files_in_folder(Path(folder_path, subfolder[0]), subfolder[1]))
            return folder_files

        if self.rom is None:
            rom_files = []
        else:
            rom_files = get_files_in_folder(Path(), self.rom.filenames)

        files: dict[Path, type[DataHandler]] = {}
        for file_key, handler_name in file_config_yaml.items():
            handler_class = None
            try:
                if isinstance(handler_name, str) and handler_name.startswith("FileType."):
                    handler_class = getattr(FileType, handler_name[len("FileType.") :])
            except AttributeError:
                pass

            if handler_class is None:
                print(f"Skipping invalid file handler {handler_name} for file {file_key}.")
                continue

            if "*" in file_key:
                # Evaluate the file key as a glob.
                file_matches = [Path(file) for file in rom_files if fnmatch.fnmatch(str(file), file_key)]
                for file in file_matches:
                    files[file] = handler_class
            else:
                files[Path(file_key)] = handler_class

        return files

    def open_file(
        self,
        handler: type[DataHandler[T]],
        path_to_rom_obj: Path,
        *,
        force: bool = False,
        load_from_rom=False,
        assets: Sequence[Asset] | None = None,
        **kwargs: OptionalKwargs,
    ) -> T:
        """
        Loads this model from assets from the asset storage or ROM.

        Reads from assets if they exist, otherwise falls back to ROM if all assets are missing.
        Raises `AssetHashMismatchError` if the hash of any asset mismatches and `force` is not True.
        If only some but not all assets are missing, raises a `AssetHashMismatchError` with no hashes
        but `missing_asset` set to `True`.
        May raise any other exception if an asset exists but is not loadable.

        If `assets` is provided, the given assets are used (they must match the asset specification
        of this handler) otherwise, the assets are loaded using `cls.load_assets`. If `assets` is
        an empty list or `load_from_rom` is `True`, the model is always loaded from ROM.

        Calling this repeatedly will always deserialize again, there is no caching.
        """
        if assets is None and not load_from_rom:
            assets = extract_assets(self.load_assets(handler, path_to_rom_obj))

        if load_from_rom or assets is None or len(assets) < 1:
            # Force ROM deserialization if no assets exist.
            return handler.deserialize(self._file_storage.get_from_rom(path_to_rom_obj), **kwargs)

        # otherwise all assets exist:
        for asset in assets:
            if not asset.do_hashes_match() and not force:
                raise AssetHashMismatchError(
                    "TODO!!",  # TODO
                    asset.spec.path,
                    asset.spec.rom_path,
                    asset,
                )
        return handler.deserialize_from_assets(assets, **kwargs)

    def save_file(
        self,
        handler: type[DataHandler[T]],
        rom_path: Path,
        data: T,
        *,
        skip_save_to_rom: bool = False,
        skip_save_to_project_dir: bool = False,
        extracted_rom_dir: Path | None = None,
        **kwargs: OptionalKwargs,
    ):
        """
        Stores the asset-representation of this model into asset storage and ROM.
        If extracted_rom_dir is defined, also saves the raw ROM files to the specified path.
        """
        if not skip_save_to_project_dir:
            assets = self._serialize_to_assets(handler, rom_path, data, **kwargs)
            for asset in assets:
                self._file_storage.store_asset(asset.spec.path, asset.spec.rom_path, asset.data)

        slf_bytes = None
        if not skip_save_to_rom:
            slf_bytes = handler.serialize(data, **kwargs)
            self._file_storage.store_in_rom(rom_path, slf_bytes)

        if extracted_rom_dir is not None:
            if slf_bytes is None:
                # Skip serializing again if data was already saved to the ROM.
                slf_bytes = handler.serialize(data, **kwargs)

            self._file_storage.store_asset(rom_path, rom_path, slf_bytes, custom_project_dir=extracted_rom_dir)

    # TODO: signature
    def symbol_info_asset(self):
        """
        Returns the asset providing information about the requested state of symbols in the ROM, or None
        if it doesn't exist. This can be applied to the ROM with `self.apply_symbol_info_asset`.
        """
        raise NotImplementedError()

    # TODO: signature
    def apply_symbol_info_asset(self, symbol_info_asset=None, apply_rules=None):
        """
        Applies symbol changes to the ROM. How symbols are applied can be customized using `apply_rules`.
        The asset info file is also saved to asset storage, replacing the currently stored one.
        """
        raise NotImplementedError()

    # TODO: signature
    def patch_info_asset(self):
        """
        Returns the asset providing information about the requested state of patches applied to the ROM, or None
        if it doesn't exist. This can be applied to the ROM with `self.apply_patch_info_asset`.
        """
        raise NotImplementedError()

    # TODO: signature
    def apply_patch_info_asset(self, patch_info_asset=None, apply_rules=None):
        """
        Applies patch state changes to the ROM. How patches are applied can be customized using `apply_rules`.

        By default, this will not re-apply all patches but rather only patches that for which this is deemed necessary.
        The asset info file is also saved to asset storage, replacing the currently stored one.
        """
        raise NotImplementedError()

    def list_extra_skypatches(self) -> list[tuple[str, AssetHash]]:
        """List the file names and hashes of extra skypatches names, without loading them."""
        raise NotImplementedError()

    @staticmethod
    def _serialize_to_assets(
        handler: type[DataHandler[T]], rom_path: Path, data: T, **kwargs: OptionalKwargs
    ) -> Sequence[Asset]:
        """Serialize a model to assets."""
        assets = []
        for spec in handler.asset_specs(rom_path):
            assets.append(handler.serialize_asset(spec, rom_path, data, **kwargs))
        return assets

    @staticmethod
    def _load_data_handlers() -> list[type[DataHandler[T]]]:
        return [
            handler
            for handler in vars(FileType).values()
            if isinstance(handler, type) and issubclass(handler, DataHandler)
        ]

    def _enrich_static_data(self):
        if self.rom is not None:
            RomDataLoader(self.rom).load_into(self.static_data)

    def _load_extra_skypatches(self):
        raise NotImplementedError()

    def _load_asset_config(self) -> dict:
        asset_config_path = Path(self._file_storage.get_project_dir(), ASSET_CONFIG_FILE)
        if asset_config_path.exists():
            with open(asset_config_path, "r") as asset_file:
                return defaultdict(lambda: None, json.load(asset_file))
        return defaultdict(lambda: None)

    def _save_asset_config(self):
        asset_config_path = Path(self._file_storage.get_project_dir(), ASSET_CONFIG_FILE)
        with open(asset_config_path, "w") as asset_file:
            asset_file.write(json.dumps(self._asset_config, sort_keys=True, indent=4))

    def _load_allow_extra_skypatches(self) -> bool:
        return self._asset_config[ALLOW_EXTRA_SKYPATCHES] or False


class SkyTempleProjectFileStorage(FileStorage):
    rom_path: Path
    project_dir: Path
    rom: NintendoDSRom
    rom_hashes: dict[Path, AssetHash | None]
    asset_hashes: dict[Path, AssetHash | None]

    def __init__(self, rom_path: Path, project_dir: Path):
        self.rom_path = rom_path
        self.project_dir = project_dir
        self.rom = NintendoDSRom.fromFile(str(rom_path))
        self.rom_hashes = self._read_hash_file(ROM_HASHES_FILE)
        self.asset_hashes = self._read_hash_file(ASSET_HASHES_FILE)

    def get_project_dir(self) -> Path:
        return self.project_dir

    def get_from_rom(self, path: Path) -> bytes:
        try:
            return bytes(self.rom.getFileByName(str(path)))
        except ValueError:
            raise FileNotFoundError(f"Cannot find ROM file at {path}")

    def store_in_rom(self, path: Path, data: bytes) -> bytes:
        try:
            self.rom.setFileByName(str(path), data)
        except ValueError:
            create_file_in_rom(self.rom, str(path), data)
        self.rom.saveToFile(str(self.rom_path))
        self._save_rom_object_hash(path, data)
        return data

    def get_asset(self, path: Path, for_rom_path: Path) -> Asset:
        full_path = Path(self.project_dir, path)
        if not full_path.exists():
            raise FileNotFoundError(f"Cannot find project file at {full_path}")

        with open(Path(self.project_dir, path), "rb") as project_file:
            project_file_bytes = project_file.read()

        return Asset(
            AssetSpec(path, for_rom_path),
            self.rom_hashes[for_rom_path],
            self.hash_of_rom_object(for_rom_path),
            self.asset_hashes[path],
            self.hash_of_asset(path),
            project_file_bytes,
        )

    def store_asset(self, path: Path, for_rom_path: Path, data: bytes, custom_project_dir: Path | None = None) -> bytes:
        if custom_project_dir is None:
            full_path = Path(self.project_dir, path)
            self._save_asset_hash(path, data)
        else:
            full_path = Path(custom_project_dir, path)
        if not full_path.parent.exists():
            full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "wb+") as project_file:
            project_file.write(data)

        return data

    def hash_of_rom_object(self, path: Path) -> AssetHash:
        return self.hash_from_bytes(self.get_from_rom(path))

    def hash_of_asset(self, path: Path) -> AssetHash:
        with open(Path(self.project_dir, path), "rb") as project_file:
            return self.hash_from_bytes(project_file.read())

    def _save_rom_object_hash(self, path: Path, data: bytes):
        self.save_rom_object_hash(path, self.hash_from_bytes(data))

    def save_rom_object_hash(self, path: Path, asset_hash: AssetHash):
        self.rom_hashes[path] = asset_hash
        self._save_hash_file(ROM_HASHES_FILE, self.rom_hashes)

    def _save_asset_hash(self, path: Path, data: bytes):
        self.save_asset_hash(path, self.hash_from_bytes(data))

    def save_asset_hash(self, path: Path, asset_hash: AssetHash):
        self.asset_hashes[path] = asset_hash
        self._save_hash_file(ASSET_HASHES_FILE, self.asset_hashes)

    def _read_hash_file(self, hash_file_name: str) -> dict[Path, AssetHash | None]:
        hashes: dict[Path, AssetHash | None] = defaultdict(lambda: None)
        hash_file_path = Path(self.project_dir, hash_file_name)
        if hash_file_path.exists():
            with open(hash_file_path, "r") as hash_file:
                for line in hash_file.readlines():
                    split_line = line.split(" ")
                    if len(split_line) == 2:
                        hashes[Path(split_line[1][:-1])] = AssetHash(split_line[0])
                    elif len(split_line) != 0:
                        print(f"Malformed hash file {hash_file_name} detected. Skipping line: {line}")
        return hashes

    def _save_hash_file(self, hash_file_name: str, hashes: dict[Path, AssetHash | None]):
        lines = []
        for file_name in sorted(hashes.keys()):
            lines.append(f"{hashes[file_name]} {file_name}\n")
        if not self.project_dir.exists():
            self.project_dir.mkdir(parents=True, exist_ok=True)
        with open(Path(self.project_dir, hash_file_name), "w+") as hash_file:
            hash_file.writelines(lines)

    @staticmethod
    def hash_from_bytes(data: bytes) -> AssetHash:
        return AssetHash(str(sha1(data).hexdigest()))
