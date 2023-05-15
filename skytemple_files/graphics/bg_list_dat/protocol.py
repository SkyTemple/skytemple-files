#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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

from abc import abstractmethod
from typing import List, Optional, Protocol, Sequence, TypeVar, Union

from skytemple_files.common.protocol import RomFileProviderProtocol
from skytemple_files.graphics.bma.protocol import BmaProtocol
from skytemple_files.graphics.bpa.protocol import BpaProtocol
from skytemple_files.graphics.bpc.protocol import BpcProtocol
from skytemple_files.graphics.bpl.protocol import BplProtocol

M = TypeVar("M", bound=BmaProtocol, covariant=True)
P = TypeVar("P", bound=BpaProtocol)
C = TypeVar("C", bound=BpcProtocol, covariant=True)
L = TypeVar("L", bound=BplProtocol, covariant=True)


class BgListEntryProtocol(Protocol[M, P, C, L]):
    bpl_name: str
    bpc_name: str
    bma_name: str
    bpa_names: Sequence[Optional[str]]

    @abstractmethod
    def __init__(
        self,
        bpl_name: str,
        bpc_name: str,
        bma_name: str,
        bpa_names: List[Optional[str]],
    ):
        ...

    @abstractmethod
    def get_bpl(self, rom_or_directory_root: Union[str, RomFileProviderProtocol]) -> L:
        ...

    @abstractmethod
    def get_bpc(
        self,
        rom_or_directory_root: Union[str, RomFileProviderProtocol],
        bpc_tiling_width: int = 3,
        bpc_tiling_height: int = 3,
    ) -> C:
        ...

    @abstractmethod
    def get_bma(self, rom_or_directory_root: Union[str, RomFileProviderProtocol]) -> M:
        ...

    @abstractmethod
    def get_bpas(
        self, rom_or_directory_root: Union[str, RomFileProviderProtocol]
    ) -> List[Optional[P]]:
        ...


T = TypeVar("T", bound=BgListEntryProtocol)


class BgListProtocol(Protocol[T]):
    level: Sequence[T]

    @abstractmethod
    def __init__(self, data: bytes):
        ...

    @abstractmethod
    def find_bma(self, name: str) -> int:
        """Count all occurrences of this BMA in the list."""
        ...

    @abstractmethod
    def find_bpl(self, name: str) -> int:
        """Count all occurrences of this BPL in the list."""
        ...

    @abstractmethod
    def find_bpc(self, name: str) -> int:
        """Count all occurrences of this BPL in the list."""
        ...

    @abstractmethod
    def find_bpa(self, name: str) -> int:
        """Count all occurrences of this BPA in the list."""
        ...

    @abstractmethod
    def add_level(self, level: T):
        """Adds a level to the level list."""
        ...

    @abstractmethod
    def set_level(self, level_id: int, level: T):
        """Overwrites a level in the level list."""
        ...

    @abstractmethod
    def set_level_bpa(self, level_id: int, bpa_id: int, bpa_name: Optional[str]):
        """Overwrites an entry in a level's BPA list."""
        ...
