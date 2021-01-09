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

from abc import ABC, abstractmethod
from skytemple_files.common.util import *



class CommonAt(ABC):

    @abstractmethod
    def decompress(self) -> bytes:
        """Returns the uncompressed data stored in the container"""

    @abstractmethod
    def to_bytes(self) -> bytes:
        """Converts the container back into a bit (compressed) representation"""

    @classmethod
    def cont_size(cls, data: bytes, byte_offset=0):
        """Returns the container size"""

    @classmethod
    def compress(cls, data: bytes) -> 'CommonAt':
        """Create a new AT container from originally uncompressed data."""
