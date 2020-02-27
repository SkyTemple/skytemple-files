#  Copyright 2020 Parakoopa
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
from enum import Enum

from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptData, Pmd2ScriptOpCode
from skytemple_files.common.util import *
from skytemple_files.script.ssb.header import AbstractSsbHeader


class SsbRoutineType(Enum):
    GENERIC = 1
    UNK2 = 2
    ACTOR = 3
    OBJECT = 4
    PERFORMER = 5
    UNK6 = 6
    UNK7 = 7
    UNK8 = 8
    COROUTINE = 9


class SsbOperation(AutoString):
    def __init__(self, offset: int, op_code: Pmd2ScriptOpCode, params: List[int]):
        self.offset = offset
        self.op_code = op_code
        self.params = params


class SsbRoutineInfo(AutoString):
    def __init__(self, offset_start: int, type: SsbRoutineType, linked_to: int):
        # ONLY used for reading in the data. THIS IS NOT UPDATED. Stored in bytes.
        self.offset_start = offset_start
        self.type = type
        self.linked_to = linked_to


class Ssb:
    def __init__(self, data: bytes, header: AbstractSsbHeader, begin_data_offset: int, scriptdata: Pmd2ScriptData):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        self._scriptdata = scriptdata

        start_of_const_table = begin_data_offset + (read_uintle(data, begin_data_offset + 0x00, 2) * 2)
        number_of_routines = read_uintle(data, begin_data_offset + 0x02, 2)

        self.header = header
        self.routine_info = []
        self.routine_ops = []

        cursor = begin_data_offset + 0x04
        cursor = self._read_routine_info(data, number_of_routines, cursor)

        for i, rtn in enumerate(self.routine_info):
            if i == number_of_routines - 1:
                end_offset = start_of_const_table
            else:
                end_offset = begin_data_offset + self.routine_info[i + 1].offset_start
            read_ops, cursor = self._read_routine_op_codes(data, begin_data_offset + rtn.offset_start, end_offset, begin_data_offset)
            self.routine_ops.append(read_ops)

        # We read all the routines, the cursor should be at the beginning of the const_table
        assert cursor == start_of_const_table

        # ### CONSTANT OFFSETS AND CONSTANT STRINGS
        # Read const offset table
        start_of_constants = begin_data_offset + header.constant_strings_start
        const_offset_table = []
        for i in range(start_of_const_table, start_of_constants, 2):
            const_offset_table.append(
                # Actual offset is start_of_const_table + X - header.number_of_strings
                start_of_const_table + read_uintle(data, i, 2) - (header.number_of_strings * 2)
            )
        self.constants = []
        cursor = start_of_constants
        # Read constants
        for const_string_offset in const_offset_table:
            assert cursor == const_string_offset
            bytes_read, string = read_var_length_string(data, const_string_offset)
            self.constants.append(string)
            cursor += bytes_read
        # Padding if not even
        if cursor % 2 != 0:
            cursor += 1
        # The end of the script block must also match the data from the header
        assert start_of_const_table + header.number_of_constants * 2 == start_of_constants

        # ### STRING OFFSETS AND STRING STRINGS
        # Read strings
        string_offset_table = {}
        self.strings = {}
        # The offsets of other languages DON'T count the size of the previuos langs, so we have to add them
        previous_languages_block_sizes = 0
        for language, len_of_lang in header.string_table_lengths.items():
            cursor_before_strings = cursor
            string_offset_table_lang = []
            strings_lang = []
            # Read string offset table
            for i in range(cursor, cursor + header.number_of_strings * 2, 2):
                string_offset_table_lang.append(
                    start_of_const_table + read_uintle(data, i, 2) + previous_languages_block_sizes
                )
            cursor += header.number_of_strings * 2
            # Read strings
            for string_offset in string_offset_table_lang:
                assert cursor == string_offset
                bytes_read, string = read_var_length_string(data, string_offset)
                strings_lang.append(string)
                cursor += bytes_read
            string_offset_table[language] = string_offset_table_lang
            self.strings[language] = strings_lang
            # Padding if not even
            if cursor % 2 != 0:
                cursor += 1
            previous_languages_block_sizes += len_of_lang
            assert cursor_before_strings + len_of_lang == cursor

    def _read_routine_info(self, data, number_of_routines, cursor):
        for i in range(0, number_of_routines):
            self.routine_info.append(SsbRoutineInfo(
                offset_start=read_uintle(data, cursor, 2) * 2,
                type=SsbRoutineType(read_uintle(data, cursor + 2, 2)),
                linked_to=read_uintle(data, cursor + 4, 2),
            ))
            cursor += 6
        return cursor

    def _read_routine_op_codes(self, data, start_offset, end_offset, len_header):
        ops = []
        cursor = start_offset
        while cursor < end_offset:
            read_op, cursor = self._read_single_op_code(data, cursor, len_header)
            ops.append(read_op)
        return ops, cursor

    def _read_single_op_code(self, data, cursor, len_header):
        opcode_offset = int((cursor - len_header) / 2)
        op_code = self._scriptdata.op_codes__by_id[read_uintle(data, cursor, 2)]
        cursor += 2
        arguments = []
        cnt_params = op_code.params
        if cnt_params == -1:
            # Variable length opcode
            cnt_params = read_uintle(data, cursor, 2)
            cursor += 2
        for i in range(0, cnt_params):
            arguments.append(read_uintle(data, cursor, 2))
            cursor += 2

        return SsbOperation(opcode_offset, op_code, arguments), cursor
