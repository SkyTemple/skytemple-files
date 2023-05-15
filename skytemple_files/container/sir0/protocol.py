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
from typing import Optional, Protocol, List

from range_typed_integers import u32


class Sir0Protocol(Protocol):
    data_pointer: u32
    content: bytes
    content_pointer_offsets: List[u32]

    @abstractmethod
    def __init__(
        self,
        content: bytes,
        pointer_offsets: List[u32],
        data_pointer: Optional[int] = None,
    ):
        ...

    @classmethod
    @abstractmethod
    def from_bin(cls, data: bytes) -> Sir0Protocol:
        ...
