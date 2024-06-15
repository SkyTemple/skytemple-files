"""
API to read/write files from ROMS and file storage.

Using this API files and hardcoded in a game ROM can be manipulated
while also storing machine and human-readable versions of those files
out-of-ROM (so-called "assets"; eg. as YAML or PNG).
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

from pathlib import Path
from typing import Sequence, TypeVar, cast

from ndspy.rom import NintendoDSRom
from skytemple_files.patch.patches import Patcher

from skytemple_files.common.ppmdu_config.data import Pmd2Data

from skytemple_files.common.types.data_handler import DataHandler

from skytemple_files.common.util import OptionalKwargs, get_ppmdu_config_for_rom

from skytemple_files.common.types.file_storage import (
    FileStorage,
    Asset,
    AssetSpec,
    AssetHashMismatchError,
    AssetHash,
)

T = TypeVar("T")


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

    A new eos-asset-sepc standard compliant project can be created with `RomProject.new`. Otherwise,
    a custom project can be created using `RomProject.__init__`. Custom projects can also work without
    actual ROM files, in which case all operations which would usually get/set data from/to the ROM may fail.
    """

    _file_storage: FileStorage
    _rom: NintendoDSRom | None
    _static_data: Pmd2Data
    _allow_extra_skypatches: bool | None
    _patcher: Patcher | None

    @property
    def rom(self) -> NintendoDSRom | None:
        """
        The underlying ROM. May return None for ROM-less projects.
        Projects created via `self.new` will always have a ROM.
        """
        return self._rom

    @property
    def static_data(self) -> Pmd2Data:
        """
        PPMDU static data for this ROM project.
        """
        return self._static_data

    @property
    def patcher(self):
        """
        Returns a patcher. May load aribitrary code from SkyPatches, see `self.does_allow_extra_skypatches`.
        This may be cached until `self.set_allow_extra_skypatches` was called.
        """
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
            if self._rom is None:
                raise ValueError(
                    "A RomProject must be provided static data if no ROM is provided."
                )
            self._static_data = get_ppmdu_config_for_rom(rom, init_from_rom=False)
            self._enrich_static_data()
        else:
            self._static_data = static_data

        self._patcher = None
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
        raise NotImplementedError()

    def load_assets(
        self, handler: type[DataHandler[T]], path_to_rom_obj: Path
    ) -> Sequence[Asset | AssetSpec]:
        """Returns loaded bytes of assets or just the spec if it's missing."""
        assets: list[Asset | AssetSpec] = []
        for spec in handler.asset_specs(path_to_rom_obj):
            try:
                assets.append(self._file_storage.get_asset(spec.path, spec.rom_path))
            except FileNotFoundError:
                assets.append(spec)
        return assets

    def list_files(
        self, search_project_dir: bool = True, search_rom: bool = True
    ) -> list[Path]:
        """
        Returns a list of all assets in the project.

        The list is built from information in the project directory and ROM by default.
        """
        raise NotImplementedError()

    def open_file(
        self,
        handler: type[DataHandler[T]],
        path_to_rom_obj: Path,
        *,
        force: bool = False,
        assets: Sequence[Asset] | None = None,
        **kwargs: OptionalKwargs,
    ) -> T:
        """
        Loads this model from assets from the asset storage or ROM.

        Reads from assets if they exist, otherwise falls back to ROM if all assets are missing.
        Raises `AssetHashMismatchError` if the hash of any asset mismatches and that asset path
        is not in `force`.
        If only some but not all assets are missing, raises a `AssetHashMismatchError` with no hashes
        but `missing_asset` set to `True`.
        May raise any other exception if an asset exists but is not loadable.

        If `assets` is provided, the given assets are used (they must match the asset specification
        of this handler) otherwise, the assets are loaded using `cls.load_assets`. If `assets` is
        an empty list, the model is always loaded from ROM.

        Calling this repeatedly will always deserialize again, there is no caching.
        """
        if assets is None:
            assets = extract_assets(self.load_assets(handler, path_to_rom_obj))

        if len(assets) < 1:
            # Force ROM deserialization if no assets exist.
            return handler.deserialize(
                self._file_storage.get_from_rom(path_to_rom_obj), **kwargs
            )

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
        **kwargs: OptionalKwargs,
    ):
        """
        Stores the asset-representation of this model into asset storage and ROM.
        """
        slf_bytes = handler.serialize(data, **kwargs)
        if not skip_save_to_project_dir:
            assets = self._serialize_to_assets(handler, rom_path, data, **kwargs)
            for asset in assets:
                self._file_storage.store_asset(
                    asset.spec.path, asset.spec.rom_path, asset.data
                )
        if not skip_save_to_rom:
            self._file_storage.store_in_rom(rom_path, slf_bytes)

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
        if it doesn't exist. This can be applied to the ROM with `self.apply_symbol_info_asset`.
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

    def _enrich_static_data(self):
        # RomDataLoader(rom).load_into(config)
        raise NotImplementedError()

    def _load_extra_skypatches(self):
        raise NotImplementedError()

    def _load_allow_extra_skypatches(self) -> bool | None:
        raise NotImplementedError()


class SkyTempleProjectFileStorage(FileStorage):
    rom_path: Path
    project_dir: Path
    rom: NintendoDSRom

    def __init__(self, rom_path: Path, project_dir: Path):
        self.rom_path = rom_path
        self.project_dir = project_dir
        self.rom = NintendoDSRom.fromFile(rom_path)

    def get_from_rom(self, path: Path) -> bytes:
        raise NotImplementedError()

    def store_in_rom(self, path: Path, data: bytes) -> bytes:
        # todo: also support creating new files!
        # todo: also record hash in hash file.
        raise NotImplementedError()

    def get_asset(self, path: Path, for_rom_path: Path) -> Asset:
        # todo: also throw hash mismatch errors
        raise NotImplementedError()

    def store_asset(self, path: Path, for_rom_path: Path, data: bytes) -> bytes:
        # todo: also record hash in hash file.
        raise NotImplementedError()

    def hash_of_rom_object(self, path: Path) -> AssetHash | None:
        raise NotImplementedError()

    def hash_of_asset(self, path: Path) -> AssetHash | None:
        raise NotImplementedError()
