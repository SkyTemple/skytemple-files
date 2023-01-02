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
from typing import Protocol, runtime_checkable

from range_typed_integers import u16


@runtime_checkable
class RomFileProviderProtocol(Protocol):
    @abstractmethod
    def getFileByName(self, filename: str) -> bytes:
        ...


class TilemapEntryProtocol(Protocol):
    idx: int
    flip_x: bool
    flip_y: bool
    pal_idx: int

    @abstractmethod
    def __init__(
        self,
        idx: int,
        flip_x: bool,
        flip_y: bool,
        pal_idx: int,
        ignore_too_large: bool = False,
    ):
        ...

    @abstractmethod
    def to_int(self) -> u16:
        ...

    @classmethod
    @abstractmethod
    def from_int(cls, entry: u16) -> "TilemapEntryProtocol":
        ...
