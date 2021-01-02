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
from typing import List, Tuple, Optional

from skytemple_files.common.ppmdu_config.data import Pmd2Data


class Sir0Serializable(ABC):
    @abstractmethod
    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        """
        Prepares this object to be wrapped in Sir0.
        Returns:
        - The binary content data for this type
        - A list of pointers in the binary content (offsets)
        - Optionally a pointer to the start of the data, if None, the beginning of the data is used.
        """
        pass

    @classmethod
    @abstractmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int, static_data: Optional[Pmd2Data] = None) -> 'Sir0Serializable':
        """
        Builds the model from the unwrapped Sir0.
        static_data may be omitted if not needed for this type.
        """
        pass
