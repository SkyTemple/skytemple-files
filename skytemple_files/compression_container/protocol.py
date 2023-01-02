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
from typing import Protocol


class CompressionContainerProtocol(Protocol):
    @abstractmethod
    def __init__(self, data: bytes):
        """Initialises container for binary representation"""

    @abstractmethod
    def decompress(self) -> bytes:
        """Returns the uncompressed data stored in the container"""

    @abstractmethod
    def to_bytes(self) -> bytes:
        """Converts the container back into a bit (compressed) representation"""

    @classmethod
    @abstractmethod
    def cont_size(cls, data: bytes, byte_offset: int = 0) -> bool:
        """Returns the container size"""

    @classmethod
    @abstractmethod
    def compress(cls, data: bytes) -> "CompressionContainerProtocol":
        """Create a new compressed container from originally uncompressed data."""


class NewableCompressionContainerProtocol(CompressionContainerProtocol):
    # noinspection PyProtocol
    @abstractmethod
    def __init__(self, data: bytes, new=False):
        """
        Initialises container for binary representation.
        If new is true, a new container is created, with data being the content.
        """
