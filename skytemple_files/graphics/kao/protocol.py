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
from typing import Iterator, Optional, Protocol, Tuple, TypeVar

from PIL.Image import Image


class KaoImageProtocol(Protocol):
    @classmethod
    @abstractmethod
    def create_from_raw(cls, cimg: bytes, pal: bytes) -> "KaoImageProtocol":
        """Create from raw compressed image and palette data"""
        ...

    @abstractmethod
    def get(self) -> Image:
        """Returns the portrait as a PIL image with a 16-color color palette"""
        ...

    @abstractmethod
    def clone(self) -> "KaoImageProtocol":
        ...

    @abstractmethod
    def size(self) -> int:
        ...

    @abstractmethod
    def set(self, pil: Image) -> "KaoImageProtocol":
        """Sets the portrait using a PIL image with 16-bit color palette as input"""
        ...

    @abstractmethod
    def raw(self) -> Tuple[bytes, bytes]:
        """Returns raw image data and palettes"""
        ...


T = TypeVar("T", bound=KaoImageProtocol)


class KaoProtocol(Protocol[T]):
    @abstractmethod
    def __init__(self, data: bytes):
        ...

    @classmethod
    @abstractmethod
    def create_new(cls, number_entries: int):
        """Creates a new empty KAO with the specified number of entries."""
        ...

    @abstractmethod
    def n_entries(self) -> int:
        """Returns the number of entries."""
        ...

    @abstractmethod
    def expand(self, new_size: int) -> None:
        ...

    @abstractmethod
    def get(self, index: int, subindex: int) -> Optional[T]:
        ...

    @abstractmethod
    def set(self, index: int, subindex: int, img: T) -> None:
        """Set the KaoImage at the specified location."""
        ...

    @abstractmethod
    def set_from_img(self, index: int, subindex: int, pil: Image) -> None:
        """Set the KaoImage at the specified location."""
        ...

    @abstractmethod
    def delete(self, index: int, subindex: int) -> None:
        """Removes a KaoImage, if it exists."""
        ...

    @abstractmethod
    def __iter__(self) -> Iterator[Tuple[int, int, Optional[T]]]:
        """
        Iterates over all KaoImages.
        Tuple: index, subindex, KaoImage or None
        """
        ...
