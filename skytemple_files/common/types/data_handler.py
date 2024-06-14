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

import abc
from pathlib import Path
from typing import Generic, TypeVar, Sequence, cast

from skytemple_files.common.types.file_storage import (
    FileStorage,
    AssetHashMismatchError,
    Asset,
    AssetSpec,
)
from skytemple_files.common.util import OptionalKwargs

T = TypeVar("T")


class DataHandler(Generic[T], abc.ABC):
    """
    Handler base class for a file or data type.
    Can convert its binary data into high-level representations and back.
    Can also convert the high-level representation into human and machine-readable asset files (and back).
    """

    ###
    ### PUBLIC INTERFACE TO BE IMPLEMENTED - Binary Serialization
    ###

    @classmethod
    @abc.abstractmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> T:
        """Loads the internal high-level representation for this data type"""
        pass

    @classmethod
    @abc.abstractmethod
    def serialize(cls, data: T, **kwargs: OptionalKwargs) -> bytes:
        """Converts the internal high-level representation back into bytes."""
        pass

    ###
    ### PRIVATE INTERFACE TO BE IMPLEMENTED - Asset Serialization
    ###

    @classmethod
    @abc.abstractmethod
    def _assets(cls, rom_path: Path) -> Sequence[AssetSpec]:
        """The specifications for the assets that make up this model given a file at `rom_path`."""
        pass

    @classmethod
    @abc.abstractmethod
    def _serialize_asset(cls, spec: AssetSpec, rom_path: Path, data: T, **kwargs: OptionalKwargs) -> Asset:
        """Serialize a single asset. `spec` is guaranteed to be an asset spec defined via `_assets`."""
        pass

    @classmethod
    @abc.abstractmethod
    def _deserialize_from_assets(
        cls,
        assets: Sequence[Asset],
        **kwargs: OptionalKwargs,
    ):
        """Create a model from all loaded assets. `assets` is guaranteed to contain all assets defined via `_assets`."""
        pass

    ###
    ### PUBLIC PROVIDED INTERFACE - Asset Serialization
    ###

    @classmethod
    def deserialize_from_files(
        cls,
        files: FileStorage,
        rom_path: Path,
        force: Sequence[Path] | None = None,
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
        """
        if force is None:
            force = []
        assets = cls.__try_load_assets(rom_path, files)
        first_missing_asset = cls.__first_missing_asset(assets)
        if first_missing_asset is not None:
            # If all are missing, fall back to ROM
            if cls.__all_assets_missing(assets):
                return cls.deserialize(files.get_from_rom(rom_path), **kwargs)
            else:
                raise AssetHashMismatchError(
                    "XXX",
                    first_missing_asset.path,
                    first_missing_asset.rom_path,
                    None,
                    None,
                    True,
                )
        # otherwise all assets exist:
        assets = cast(Sequence[Asset], assets)
        for asset in assets:
            if not asset.do_hashes_match() and asset.spec.path not in force:
                raise AssetHashMismatchError(
                    "XXX",
                    asset.spec.path,
                    asset.spec.rom_path,
                    asset.expected_rom_obj_hash,
                    asset.actual_rom_obj_hash,
                    False,
                )
        return cls._deserialize_from_assets(assets, **kwargs)

    @classmethod
    def serialize_to_files(cls, files: FileStorage, rom_path: Path, data: T, **kwargs: OptionalKwargs):
        """
        Stores the asset-representation of this model into asset storage and ROM.
        """
        slf_bytes = cls.serialize(data, **kwargs)
        assets = cls.__serialize_to_assets(rom_path, data, **kwargs)
        for asset in assets:
            files.store_asset(asset.spec.path, asset.spec.rom_path, asset.data)
        files.store_in_rom(rom_path, slf_bytes)

    ###
    ### PRIVATE PROVIDED METHODS - Asset Serialization
    ###

    @classmethod
    def __try_load_assets(cls, rom_path: Path, files: FileStorage) -> Sequence[Asset | AssetSpec]:
        """Returns loaded bytes of assets or just a string for an asset (it's supposed spec) if it's missing."""
        assets: list[Asset | AssetSpec] = []
        for spec in cls._assets(rom_path):
            try:
                assets.append(files.get_asset(spec.path, spec.rom_path))
            except FileNotFoundError:
                assets.append(spec)
        return assets

    @classmethod
    def __serialize_to_assets(cls, rom_path: Path, data: T, **kwargs: OptionalKwargs) -> Sequence[Asset]:
        """Serialize a model to assets."""
        assets = []
        for spec in cls._assets(rom_path):
            assets.append(cls._serialize_asset(spec, rom_path, data, **kwargs))
        return assets

    @staticmethod
    def __first_missing_asset(assets: Sequence[Asset | AssetSpec]) -> AssetSpec | None:
        for x in assets:
            if isinstance(x, AssetSpec):
                return x
        return None

    @staticmethod
    def __all_assets_missing(assets: Sequence[Asset | AssetSpec]) -> bool:
        return all(isinstance(x, AssetSpec) for x in assets)
