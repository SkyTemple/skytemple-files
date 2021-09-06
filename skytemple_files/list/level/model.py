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
from typing import Tuple, List, Optional

from skytemple_files.common import string_codec
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptLevel
from skytemple_files.common.util import read_uintle, read_var_length_string, write_uintle, read_sintle, write_sintle
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable


LEN_LEVEL_ENTRY = 12
PADDING_END = b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'


class LevelListBin(Sir0Serializable):
    """Wrapper around a List[Pmd2ScriptLevel] that is read and written as/to a binary stream."""

    def __init__(self, data: bytes, header_start: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.list: List[Pmd2ScriptLevel] = []

        #pointer_start = read_uintle(data, header_start, 4)
        #number_entries = read_uintle(data, header_start + 4, 4)
        for i in range(0, len(data) - header_start):
            start = header_start + (i * LEN_LEVEL_ENTRY)
            if data[start:start + 12] == b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa':
                break
            self.list.append(Pmd2ScriptLevel(
                id=i,
                mapty=read_uintle(data, start + 0, 2),
                nameid=read_uintle(data, start + 2, 2),
                mapid=read_uintle(data, start + 4, 2),
                weather=read_sintle(data, start + 6, 2),
                name=self._read_string(data, read_uintle(data, start + 8, 4))
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
            entry_buffer = bytearray(LEN_LEVEL_ENTRY)
            write_uintle(entry_buffer, entry.mapty, 0, 2)
            write_uintle(entry_buffer, entry.nameid, 2, 2)
            write_uintle(entry_buffer, entry.mapid, 4, 2)
            write_sintle(entry_buffer, entry.weather, 6, 2)
            sir0_pointer_offsets.append(len(out_data) + 8)
            write_uintle(entry_buffer, pointer_offsets[i], 8, 4)
            out_data += entry_buffer
        out_data += PADDING_END

        # Padding
        self._pad(out_data)

        # 4. Write sub-header
        #sir0_pointer_offsets.append(len(out_data))
        #out_data += pointer_data_block.to_bytes(4, byteorder='little', signed=False)
        #out_data += len(self.list).to_bytes(4, byteorder='little', signed=False)

        return out_data, sir0_pointer_offsets, pointer_data_block

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int, static_data: Optional[Pmd2Data] = None) -> 'ActorListBin':
        return cls(content_data, data_pointer)

    def _read_string(self, data: bytes, string_offset: int) -> str:
        return read_var_length_string(data, string_offset)[1]

    def _pad(self, out_data):
        if len(out_data) % 16 != 0:
            out_data += bytes(0xAA for _ in range(0, 16 - (len(out_data) % 16)))
