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
from typing import List, Type, TypeVar, Optional

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.util import read_bytes
from skytemple_files.container.sir0.model import Sir0
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.container.sir0.writer import Sir0Writer


T = TypeVar('T', bound=Sir0Serializable)


class Sir0Handler(DataHandler[Sir0]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Sir0:
        if not cls.matches(data):
            raise ValueError("This is not valid Sir0.")
        return Sir0.from_bin(data)

    @classmethod
    def serialize(cls, data: Sir0, **kwargs) -> bytes:
        return Sir0Writer(data).write()

    @classmethod
    def matches(cls, data: bytes, byte_offset=0):
        """Check if the given data stream is a Sir0 container"""
        return read_bytes(data, byte_offset, 4) == b'SIR0'

    @classmethod
    def wrap(cls, content: bytes, pointer_offsets: List[int], data_pointer: int = None) -> Sir0:
        """Wraps existing data in Sir0."""
        return Sir0(content, pointer_offsets, data_pointer)

    @classmethod
    def wrap_obj(cls, obj: Sir0Serializable) -> Sir0:
        return cls.wrap(*obj.sir0_serialize_parts())

    @classmethod
    def unwrap_obj(cls, data: Sir0, spec: Type[T], static_data: Optional[Pmd2Data] = None) -> T:
        return spec.sir0_unwrap(data.content, data.data_pointer, static_data)
