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

from typing import TYPE_CHECKING, Dict, List, Union

from range_typed_integers import u16, u8

from skytemple_files.common.util import AutoString, read_u16, write_u16
from skytemple_files.dungeon_data.mappa_bin.protocol import (
    MappaTrapListProtocol,
    _MappaTrapType,
)

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin._python_impl.model import (
        MappaBinReadContainer,
    )


class MappaTrapList(MappaTrapListProtocol, AutoString):
    weights: Dict[_MappaTrapType, u16]

    def __init__(self, weights: Union[List[u16], Dict[_MappaTrapType, u16]]):
        if isinstance(weights, list):
            if len(weights) != 25:
                raise ValueError(
                    "MappaTrapList constructor needs a weight value for all of the 25 traps."
                )
            self.weights = {}
            for i, value in enumerate(weights):
                self.weights[u8(i)] = value
        elif isinstance(weights, dict):
            self.weights = weights
            if set(self.weights.keys()) != set(range(0, 25)):
                raise ValueError(
                    "MappaTrapList constructor needs a weight value for all of the 25 traps."
                )
        else:
            raise ValueError(f"Invalid type for MappaTrapList {type(weights)}")

    @classmethod
    def from_mappa(cls, read: "MappaBinReadContainer", pointer: int) -> "MappaTrapList":
        weights = []
        for i in range(pointer, pointer + 50, 2):
            weights.append(read_u16(read.data, i))
        return MappaTrapList(weights)

    def to_mappa(self):
        data = bytearray(50)
        for i in range(0, 25):
            write_u16(data, self.weights[u8(i)], i * 2)
        return data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MappaTrapList):
            return False
        return self.weights == other.weights
