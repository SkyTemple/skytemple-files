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
from skytemple_files.common.util import *
from skytemple_files.container.sir0 import HEADER_LEN
from skytemple_files.container.sir0.sir0_util import decode_sir0_pointer_offsets


class Sir0:
    def __init__(self, content: bytes, pointer_offsets: List[int], data_pointer: int = None):
        self.content = content
        self.content_pointer_offsets = pointer_offsets
        if data_pointer is None:
            data_pointer = 0
        self.data_pointer = data_pointer

    @classmethod
    def from_bin(cls, data: bytes):
        data = memoryview(bytearray(data))
        data_pointer = read_uintle(data, 0x04, 4)
        pointer_offset_list_pointer = read_uintle(data, 0x08, 4)

        pointer_offsets = cls._decode_pointer_offsets(data, pointer_offset_list_pointer)

        # Correct pointers by subtracting the header
        for pnt_off in pointer_offsets:
            write_uintle(data, read_uintle(data, pnt_off, 4) - HEADER_LEN, pnt_off, 4)

        # The first two are for the pointers in the header, we remove them now, they are not
        # part of the content pointers
        content_pointer_offsets = [pnt - HEADER_LEN for pnt in pointer_offsets][2:]

        return cls(
            bytes(data[HEADER_LEN:pointer_offset_list_pointer]),
            content_pointer_offsets,
            data_pointer - HEADER_LEN
        )

    # Based on C++ algorithm by psy_commando from
    # https://projectpokemon.org/docs/mystery-dungeon-nds/sir0siro-format-r46/
    @classmethod
    def _decode_pointer_offsets(cls, data: bytes, pointer_offset_list_pointer: int) -> List[int]:
        return decode_sir0_pointer_offsets(data, pointer_offset_list_pointer)
