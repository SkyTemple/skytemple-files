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
from typing import Generic, TypeVar, Sequence

from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_storage import (
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
    ### Binary Serialization
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
    ### Asset Serialization
    ###

    @classmethod
    @abc.abstractmethod
    def asset_specs(cls, path_to_rom_obj: Path) -> Sequence[AssetSpec]:
        """The specifications for the assets that make up this model given a file at `rom_path`."""
        return []

    @classmethod
    @abc.abstractmethod
    def serialize_asset(cls, spec: AssetSpec, path_to_rom_obj: Path, data: T, **kwargs: OptionalKwargs) -> Asset:
        """Serialize a single asset. `spec` must be an asset spec defined via `cls.assets`."""
        pass

    @classmethod
    @abc.abstractmethod
    def deserialize_from_assets(
        cls,
        assets: Sequence[Asset],
        **kwargs: OptionalKwargs,
    ):
        """Create a model from all loaded assets. `assets` must contain all assets defined via `cls.assets`."""
        pass
