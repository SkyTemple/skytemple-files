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

from typing import List, Optional, Tuple

from range_typed_integers import u32_checked, u32

from skytemple_files.common import string_codec
from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptLevel
from skytemple_files.common.util import (
    read_i16,
    read_u16,
    read_u32,
    read_var_length_string,
    write_i16,
    write_u16,
    write_u32,
)
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable

LEN_LEVEL_ENTRY = 12
PADDING_END = b"\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa"


class LevelListBin(Sir0Serializable):
    """Wrapper around a List[Pmd2ScriptLevel] that is read and written as/to a binary stream."""

    def __init__(self, data: bytes, header_start: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.list: List[Pmd2ScriptLevel] = []

        # pointer_start = read_uintle(data, header_start, 4)
        # number_entries = read_uintle(data, header_start + 4, 4)
        for i in range(0, len(data) - header_start):
            start = header_start + (i * LEN_LEVEL_ENTRY)
            if (
                data[start : start + 12]
                == b"\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa"
            ):
                break
            self.list.append(
                Pmd2ScriptLevel(
                    id=i,
                    mapty=read_u16(data, start + 0),
                    nameid=read_u16(data, start + 2),
                    mapid=read_u16(data, start + 4),
                    weather=read_i16(data, start + 6),
                    name=self._read_string(data, read_u32(data, start + 8)),
                )
            )

    def serialize(self) -> bytes:
        return self.sir0_serialize_parts()[0]

    def sir0_serialize_parts(self) -> Tuple[bytes, List[u32], Optional[u32]]:
        string_codec.init()

        out_data = bytearray()
        # 1. Write strings
        pointer_offsets = []
        for entry in self.list:
            pointer_offsets.append(u32_checked(len(out_data)))
            out_data += bytes(entry.name, string_codec.PMD2_STR_ENCODER) + b"\0"

        # Padding
        self._pad(out_data)

        # Write table
        sir0_pointer_offsets = []
        pointer_data_block = u32(len(out_data))
        for i, entry in enumerate(self.list):
            entry_buffer = bytearray(LEN_LEVEL_ENTRY)
            write_u16(entry_buffer, entry.mapty, 0)
            write_u16(entry_buffer, entry.nameid, 2)
            write_u16(entry_buffer, entry.mapid, 4)
            write_i16(entry_buffer, entry.weather, 6)
            sir0_pointer_offsets.append(u32(len(out_data) + 8))
            write_u32(entry_buffer, pointer_offsets[i], 8)
            out_data += entry_buffer
        out_data += PADDING_END

        # Padding
        self._pad(out_data)

        # 4. Write sub-header
        # sir0_pointer_offsets.append(len(out_data))
        # out_data += pointer_data_block.to_bytes(4, byteorder='little', signed=False)
        # out_data += len(self.list).to_bytes(4, byteorder='little', signed=False)

        return out_data, sir0_pointer_offsets, pointer_data_block

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: u32,
    ) -> "LevelListBin":
        return cls(content_data, data_pointer)

    def _read_string(self, data: bytes, string_offset: int) -> str:
        return read_var_length_string(data, string_offset)[1]

    def _pad(self, out_data):
        if len(out_data) % 16 != 0:
            out_data += bytes(0xAA for _ in range(0, 16 - (len(out_data) % 16)))
