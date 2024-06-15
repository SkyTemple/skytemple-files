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

from skytemple_files.common.types.data_handler import DataHandler

from skytemple_files.common.util import OptionalKwargs

from skytemple_files.common.types.file_storage import (
    FileStorage,
    Asset,
    AssetSpec,
    AssetHashMismatchError,
)

T = TypeVar("T")


def _load_assets(
    handler: type[DataHandler[T]], path_to_rom_obj: Path, files: FileStorage
) -> Sequence[Asset | AssetSpec]:
    """Returns loaded bytes of assets or just the spec if it's missing."""
    assets: list[Asset | AssetSpec] = []
    for spec in handler.asset_specs(path_to_rom_obj):
        try:
            assets.append(files.get_asset(spec.path, spec.rom_path))
        except FileNotFoundError:
            assets.append(spec)
    return assets


def _deserialize_from_files(
    handler: type[DataHandler[T]],
    files: FileStorage,
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
    """
    if assets is None:
        assets = _extract_assets(_load_assets(handler, path_to_rom_obj, files))

    if len(assets) < 1:
        # Force ROM deserialization if no assets exist.
        return handler.deserialize(files.get_from_rom(path_to_rom_obj), **kwargs)

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


def _extract_assets(assets: Sequence[Asset | AssetSpec]) -> Sequence[Asset]:
    """
    Given a list of assets and non-existent assets (AssetSpecs), see `load_assets`
    - returns either a list of assets if all assets exists
    - returns the empty list of no assets exist at all
    - throws a `AssetHashMismatchError` for the first missing asset if any asset exists, but at least one is missing.
    """
    first_missing_asset = __first_missing_asset(assets)
    if first_missing_asset is not None:
        # If all are missing, return an empty list
        if __all_assets_missing(assets):
            return []
        else:
            raise AssetHashMismatchError(
                "TODO!!",  # TODO
                first_missing_asset.path,
                first_missing_asset.rom_path,
                None,
            )
    return cast(Sequence[Asset], assets)


def _serialize_to_files(
    handler: type[DataHandler[T]],
    files: FileStorage,
    rom_path: Path,
    data: T,
    **kwargs: OptionalKwargs,
):
    """
    Stores the asset-representation of this model into asset storage and ROM.
    """
    slf_bytes = handler.serialize(data, **kwargs)
    assets = __serialize_to_assets(handler, rom_path, data, **kwargs)
    for asset in assets:
        files.store_asset(asset.spec.path, asset.spec.rom_path, asset.data)
    files.store_in_rom(rom_path, slf_bytes)


def __serialize_to_assets(
    handler: type[DataHandler[T]], rom_path: Path, data: T, **kwargs: OptionalKwargs
) -> Sequence[Asset]:
    """Serialize a model to assets."""
    assets = []
    for spec in handler.asset_specs(rom_path):
        assets.append(handler.serialize_asset(spec, rom_path, data, **kwargs))
    return assets


def __first_missing_asset(assets: Sequence[Asset | AssetSpec]) -> AssetSpec | None:
    for x in assets:
        if isinstance(x, AssetSpec):
            return x
    return None


def __all_assets_missing(assets: Sequence[Asset | AssetSpec]) -> bool:
    return all(isinstance(x, AssetSpec) for x in assets)
