#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
from typing import Protocol, Optional, Tuple, TypeVar, Iterable, Union, Iterator

from PIL.Image import Image


class KaoImageProtocol(Protocol):
    @classmethod
    def create_from_raw(cls, cimg: bytes, pal: bytes) -> 'KaoImageProtocol':
        """Create from raw compressed image and palette data"""
        ...

    def get(self) -> Image:
        """Returns the portrait as a PIL image with a 16-color color palette"""
        ...

    def size(self) -> int:
        ...

    def set(self, pil: Image) -> 'KaoImageProtocol':
        """Sets the portrait using a PIL image with 16-bit color palette as input"""
        ...

    def raw(self) -> Tuple[bytes, bytes]:
        """Returns raw image data and palettes"""
        ...


T = TypeVar('T', bound=KaoImageProtocol, covariant=True)


class KaoProtocol(Protocol[T]):
    def __init__(self, data: bytes):
        ...

    def expand(self, new_size: int):
        ...

    def get(self, index: int, subindex: int) -> Optional[T]:
        ...

    def set(self, index: int, subindex: int, pil: 'KaoImageProtocol'):
        """Set the KaoImage at the specified location."""
        ...

    def set_from_img(self, index: int, subindex: int, pil: Image):
        """Set the KaoImage at the specified location."""
        ...

    def delete(self, index: int, subindex: int):
        """Removes a KaoImage, if it exists."""
        ...

    def __iter__(self) -> Iterator[Tuple[int, int, Optional[KaoImageProtocol]]]:
        """
        Iterates over all KaoImages.
        Tuple: index, subindex, KaoImage or None
        """
        ...
