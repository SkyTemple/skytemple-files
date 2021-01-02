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
from typing import Tuple, List, Optional

from skytemple_files.common import string_codec
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptEntity
from skytemple_files.common.util import read_uintle, read_var_length_string, write_uintle
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable


LEN_ACTOR_ENTRY = 12


class ActorListBin(Sir0Serializable):
    """Wrapper around a List[Pmd2ScriptEntity] that is read and written as/to a binary stream."""

    def __init__(self, data: bytes, header_start: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.list: List[Pmd2ScriptEntity] = []

        pointer_start = read_uintle(data, header_start, 4)
        number_entries = read_uintle(data, header_start + 4, 4)
        for i in range(0, number_entries):
            start = pointer_start + (i * LEN_ACTOR_ENTRY)
            self.list.append(Pmd2ScriptEntity(
                id=i,
                type=read_uintle(data, start + 0, 2),
                entid=read_uintle(data, start + 2, 2),
                name=self._read_string(data, read_uintle(data, start + 4, 4)),
                unk3=read_uintle(data, start + 8, 2),
                unk4=read_uintle(data, start + 10, 2)
            ))

    def serialize(self) -> bytes:
        return self.sir0_serialize_parts()[0]

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        string_codec.init()

        out_data = bytearray()
        # 1. Write strings
        pointer_offsets: List[int] = []
        for entry in self.list:
            pointer_offsets.append(len(out_data))
            out_data += bytes(entry.name, string_codec.PMD2_STR_ENCODER) + b'\0'

        # Padding
        self._pad(out_data)

        # Write table
        sir0_pointer_offsets = []
        pointer_data_block = len(out_data)
        for i, entry in enumerate(self.list):
            entry_buffer = bytearray(LEN_ACTOR_ENTRY)
            write_uintle(entry_buffer, entry.type, 0, 2)
            write_uintle(entry_buffer, entry.entid, 2, 2)
            sir0_pointer_offsets.append(len(out_data) + 4)
            write_uintle(entry_buffer, pointer_offsets[i], 4, 4)
            write_uintle(entry_buffer, entry.unk3, 8, 2)
            write_uintle(entry_buffer, entry.unk4, 10, 2)
            out_data += entry_buffer

        # Padding
        self._pad(out_data)

        # 4. Write sub-header
        data_pointer = len(out_data)
        sir0_pointer_offsets.append(len(out_data))
        out_data += pointer_data_block.to_bytes(4, byteorder='little', signed=False)
        out_data += len(self.list).to_bytes(4, byteorder='little', signed=False)

        return out_data, sir0_pointer_offsets, data_pointer

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int, static_data: Optional[Pmd2Data] = None) -> 'ActorListBin':
        return cls(content_data, data_pointer)

    def _read_string(self, data: bytes, string_offset: int) -> str:
        return read_var_length_string(data, string_offset)[1]

    def _pad(self, out_data):
        if len(out_data) % 16 != 0:
            out_data += bytes(0xAA for _ in range(0, 16 - (len(out_data) % 16)))
