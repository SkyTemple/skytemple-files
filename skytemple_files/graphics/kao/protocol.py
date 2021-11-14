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
from typing import Protocol, Optional, Tuple, TypeVar

from PIL.Image import Image


class KaoImageProtocol(Protocol):
    def get(self) -> Image:
        """Returns the portrait as a PIL image with a 16-bit color palette"""
        ...

    def size(self) -> int:
        ...

    #def get_internal(self) -> bytes:
    #    """Returns the portrait as 16 color palette followed by AT compressed image data"""
    #    return bytes(self.pal_data) + bytes(self.compressed_img_data)

    def set(self, pil: Image) -> 'KaoImageProtocol':
        """Sets the portrait using a PIL image with 16-bit color palette as input"""
        ...

    @classmethod
    def new(cls, pil: Image) -> 'KaoImageProtocol':
        """Creates a new KaoImage from a PIL image with 16-bit color palette as input"""
        ...


T = TypeVar('T', bound=KaoImageProtocol)
U = TypeVar('U', bound='KaoIteratorProtocol', covariant=True)


class KaoProtocol(Protocol[T, U]):
    def __init__(self, data: bytes):
        ...

    def expand(self, new_size: int):
        ...

    def get(self, index: int, subindex: int) -> Optional[T]:
        ...

    def set(self, index: int, subindex: int, img: T):
        """
        Set the KaoImage at the specified location. This fails,
        if there is already an image there. Use get instead.
        """
        ...

    def delete(self, index: int, subindex: int):
        """Removes a KaoImage, if it exists."""
        ...

    def has_loaded(self, index: int, subindex: int) -> bool:
        """Returns whether or not a kao image at the specified index was loaded"""
        ...

    def __iter__(self) -> U:
        """
        Iterates over all KaoImages.
        """
        ...


class KaoIteratorProtocol(Protocol):
    def __next__(self) -> Tuple[int, int, Optional[KaoImageProtocol]]:
        """Tuple: index, subindex, KaoImage or None"""
        ...
