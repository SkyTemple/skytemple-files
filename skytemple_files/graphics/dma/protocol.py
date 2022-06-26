#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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
from typing import Protocol, Sequence

_DmaType = int
_DmaExtraType = int


class DmaType:
    WALL = 0
    WATER = 1
    FLOOR = 2


class DmaExtraType:
    FLOOR1 = 0
    WALL_OR_VOID = 1
    FLOOR2 = 2


class DmaNeighbor:
    SOUTH = 0x01
    SOUTH_EAST = 0x02
    EAST = 0x04
    NORTH_EAST = 0x08
    NORTH = 0x10
    NORTH_WEST = 0x20
    WEST = 0x40
    SOUTH_WEST = 0x80


class DmaProtocol(Protocol):
    chunk_mappings: Sequence[int]

    @abstractmethod
    def __init__(self, data: bytes):
        ...

    @abstractmethod
    def get(self, get_type: _DmaType, neighbors_same: int) -> Sequence[int]:
        """
        Returns all three variations (chunk ids) set for this dungeon tile configuration.
        neighbors_same is a bitfield with the bits for the directions set to 1 if the neighbor at this
        position has the same type as the tile at this position.
        TIP: For neighbors_same, use the bit flags in DmaNeighbor.
        """
        ...

    @abstractmethod
    def get_extra(self, extra_type: _DmaExtraType) -> Sequence[int]:
        """
        Returns a few extra chunk variations for the given type.
        How they are used exactly by the game is currently not know,
        this interface could change if we find out.
        """
        ...

    @abstractmethod
    def set(
        self, get_type: _DmaType, neighbors_same: int, variation_index: int, value: int
    ):
        """
        Sets the mapping for the given configuration and the given variation of it.
        """
        ...

    @abstractmethod
    def set_extra(self, extra_type: _DmaExtraType, index: int, value: int):
        """
        Sets and extra tile entry.
        """
        ...
