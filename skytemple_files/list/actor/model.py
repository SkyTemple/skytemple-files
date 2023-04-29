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

from typing import List, Tuple, Optional

from range_typed_integers import u16_checked, u32_checked, u32

from skytemple_files.common import string_codec
from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptEntity
from skytemple_files.common.util import (
    write_u32,
    read_var_length_string,
    read_u16,
    write_u16,
    read_u32,
)
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable

LEN_ACTOR_ENTRY = 12


class ActorListBin(Sir0Serializable):
    """Wrapper around a List[Pmd2ScriptEntity] that is read and written as/to a binary stream."""

    def __init__(self, data: bytes, header_start: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.list: List[Pmd2ScriptEntity] = []

        pointer_start = read_u32(data, header_start)
        number_entries = read_u32(data, header_start + 4)
        for i in range(0, number_entries):
            start = pointer_start + (i * LEN_ACTOR_ENTRY)
            self.list.append(
                Pmd2ScriptEntity(
                    id=u16_checked(i),
                    type=read_u16(data, start + 0),
                    entid=read_u16(data, start + 2),
                    name=self._read_string(data, read_u32(data, start + 4)),
                    unk3=read_u16(data, start + 8),
                    unk4=read_u16(data, start + 10),
                )
            )

    def serialize(self) -> bytes:
        return self.sir0_serialize_parts()[0]

    def sir0_serialize_parts(self) -> Tuple[bytes, List[u32], Optional[u32]]:
        string_codec.init()

        out_data = bytearray()
        # 1. Write strings
        pointer_offsets: List[u32] = []
        for entry in self.list:
            pointer_offsets.append(u32_checked(len(out_data)))
            out_data += bytes(entry.name, string_codec.PMD2_STR_ENCODER) + b"\0"

        # Padding
        self._pad(out_data)

        # Write table
        sir0_pointer_offsets = []
        pointer_data_block = len(out_data)
        for i, entry in enumerate(self.list):
            entry_buffer = bytearray(LEN_ACTOR_ENTRY)
            write_u16(entry_buffer, entry.type, 0)
            write_u16(entry_buffer, entry.entid, 2)
            sir0_pointer_offsets.append(u32(len(out_data) + 4))
            write_u32(entry_buffer, pointer_offsets[i], 4)
            write_u16(entry_buffer, entry.unk3, 8)
            write_u16(entry_buffer, entry.unk4, 10)
            out_data += entry_buffer

        # Padding
        self._pad(out_data)

        # 4. Write sub-header
        data_pointer = u32(len(out_data))
        sir0_pointer_offsets.append(u32(len(out_data)))
        out_data += pointer_data_block.to_bytes(4, byteorder="little", signed=False)
        out_data += len(self.list).to_bytes(4, byteorder="little", signed=False)

        return out_data, sir0_pointer_offsets, data_pointer

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: u32,
    ) -> "ActorListBin":
        return cls(content_data, data_pointer)

    def _read_string(self, data: bytes, string_offset: int) -> str:
        return read_var_length_string(data, string_offset)[1]

    def _pad(self, out_data):
        if len(out_data) % 16 != 0:
            out_data += bytes(0xAA for _ in range(0, 16 - (len(out_data) % 16)))
