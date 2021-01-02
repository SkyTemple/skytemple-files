#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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

import abc
from typing import TypeVar, Generic

T = TypeVar('T')


class DataHandler(Generic[T], abc.ABC):
    """
    Handler base class for a file or data type.
    Can convert it's type into high-level representations and back.
    """

    @classmethod
    @abc.abstractmethod
    def deserialize(cls, data: bytes, **kwargs) -> T:
        """Loads the internal high-level representation for this data type"""
        pass

    @classmethod
    @abc.abstractmethod
    def serialize(cls, data: T, **kwargs) -> bytes:
        """Converts the internal high-level representation back into bytes."""
        pass
