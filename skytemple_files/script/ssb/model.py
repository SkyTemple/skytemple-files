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
from typing import Dict

from explorerscript.source_map import SourceMap
from explorerscript.ssb_converting.ssb_decompiler import ExplorerScriptSsbDecompiler
from explorerscript.ssb_converting.ssb_data_types import SsbRoutineType, SsbWarning, SsbRoutineInfo, SsbOpParamConstant, \
    SsbOpParamConstString, SsbOpParamLanguageString, ListOfSsbOpParam, SsbOperation
from explorerscript.ssb_script.ssb_converting.ssb_decompiler import SsbScriptSsbDecompiler
from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptData, Pmd2ScriptOpCode
from skytemple_files.common.util import *
from skytemple_files.script.ssb.constants import SsbConstant
from skytemple_files.script.ssb.header import AbstractSsbHeader


class SkyTempleSsbOperation(SsbOperation):
    def __init__(self, offset: int, op_code: Pmd2ScriptOpCode, params: ListOfSsbOpParam):
        super().__init__(offset, op_code, params)


class Ssb:
    def __init__(self, data: bytes, header: AbstractSsbHeader, begin_data_offset: int, scriptdata: Pmd2ScriptData):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        # WARNING: This is NOT updated by this model. Only the writer can update it.
        self.original_binary_data = bytes(data)

        self._scriptdata = scriptdata

        start_of_const_table = begin_data_offset + (read_uintle(data, begin_data_offset + 0x00, 2) * 2)
        number_of_routines = read_uintle(data, begin_data_offset + 0x02, 2)

        self.header = header
        self.routine_info: List[Tuple[int, SsbRoutineInfo]] = []  # Offset, RoutineInfo
        self.routine_ops: List[List[SkyTempleSsbOperation]] = []

        cursor = begin_data_offset + 0x04
        cursor = self._read_routine_info(data, number_of_routines, cursor)

        for i, (rtn_start_offset, _) in enumerate(self.routine_info):
            if i == number_of_routines - 1:
                end_offset = start_of_const_table
            else:
                end_offset = begin_data_offset + self.routine_info[i + 1][0]
            read_ops, cursor = self._read_routine_op_codes(data, begin_data_offset + rtn_start_offset, end_offset, begin_data_offset)
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
            self.routine_info.append((read_uintle(data, cursor, 2) * 2, SsbRoutineInfo(
                type=SsbRoutineType(read_uintle(data, cursor + 2, 2)),
                linked_to=read_uintle(data, cursor + 4, 2),
            )))
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

        return SkyTempleSsbOperation(opcode_offset, op_code, arguments), cursor

    def to_explorerscript(self) -> Tuple[str, SourceMap]:
        self.add_linked_to_names_to_routine_ops()
        return ExplorerScriptSsbDecompiler(
            [x[1] for x in self.routine_info],
            self.get_filled_routine_ops(),
            self._scriptdata.common_routine_info__by_id
        ).convert()

    def to_ssb_script(self) -> Tuple[str, SourceMap]:
        self.add_linked_to_names_to_routine_ops()
        return SsbScriptSsbDecompiler(
            [x[1] for x in self.routine_info],
            self.get_filled_routine_ops(),
            self._scriptdata.common_routine_info__by_id
        ).convert()

    def add_linked_to_names_to_routine_ops(self):
        for _, r in self.routine_info:
            if r.type == SsbRoutineType.ACTOR:
                r.linked_to_name = SsbConstant.create_for(self._scriptdata.level_entities__by_id[r.linked_to]).name
            elif r.type == SsbRoutineType.PERFORMER:
                r.linked_to_name = SsbConstant.create_for(self._scriptdata.objects__by_id[r.linked_to]).name

    def get_filled_routine_ops(self):
        """Returns self.routine_ops, but with constant strings, strings and constants from scriptdata filled out"""
        rtns: List[List[SkyTempleSsbOperation]] = []
        for rtn in self.routine_ops:
            rtn_ops = []
            for op in rtn:
                # If there is at least one argument name / type defined for this operation's opcode,
                # then we turn the list of params into a named argument list (dict)
                use_named_arguments = len(op.op_code.arguments) > 0
                if use_named_arguments:
                    new_params = {}
                    for i, param in enumerate(op.params):
                        if i in op.op_code.arguments__by_id:
                            argument_spec = op.op_code.arguments__by_id[i]
                            if argument_spec.type == 'int':
                                new_params[argument_spec.name] = param
                            elif argument_spec.type == 'Entity':
                                new_params[argument_spec.name] = SsbConstant.create_for(self._scriptdata.level_entities__by_id[param])
                            elif argument_spec.type == 'Object':
                                new_params[argument_spec.name] = SsbConstant.create_for(self._scriptdata.objects__by_id[param])
                            elif argument_spec.type == 'Routine':
                                new_params[argument_spec.name] = SsbConstant.create_for(self._scriptdata.common_routine_info__by_id[param])
                            elif argument_spec.type == 'Face':
                                if param in self._scriptdata.face_names__by_id:
                                    new_params[argument_spec.name] = SsbConstant.create_for(self._scriptdata.face_names__by_id[param])
                                else:
                                    warnings.warn(f"Unknown face id: {param}", SsbWarning)
                                    new_params[argument_spec.name] = param
                            elif argument_spec.type == 'FaceMode':
                                new_params[argument_spec.name] = SsbConstant.create_for(self._scriptdata.face_position_modes__by_id[param])
                            elif argument_spec.type == 'GameVar':
                                new_params[argument_spec.name] = SsbConstant.create_for(self._scriptdata.game_variables__by_id[param])
                            elif argument_spec.type == 'Level':
                                if param in self._scriptdata.level_list__by_id:
                                    new_params[argument_spec.name] = SsbConstant.create_for(self._scriptdata.level_list__by_id[param])
                                else:
                                    warnings.warn(f"Unknown level id: {param}", SsbWarning)
                            elif argument_spec.type == 'Menu':
                                if param in self._scriptdata.menus__by_id:
                                    new_params[argument_spec.name] = SsbConstant.create_for(self._scriptdata.menus__by_id[param])
                                else:
                                    warnings.warn(f"Unknown menu id: {param}", SsbWarning)
                                    new_params[argument_spec.name] = param
                            elif argument_spec.type == 'ProcessSpecial':
                                if param in self._scriptdata.process_specials__by_id:
                                    new_params[argument_spec.name] = SsbConstant.create_for(self._scriptdata.process_specials__by_id[param])
                                else:
                                    new_params[argument_spec.name] = param
                                    warnings.warn(f"Unknown special process id: {param}", SsbWarning)
                            elif argument_spec.type == 'Direction':
                                if param in self._scriptdata.directions__by_id:
                                    new_params[argument_spec.name] = SsbConstant.create_for(self._scriptdata.directions__by_id[param])
                                else:
                                    new_params[argument_spec.name] = param
                                    warnings.warn(f"Unknown direction id: {param}", SsbWarning)
                            elif argument_spec.type == 'String':
                                new_params[argument_spec.name] = SsbOpParamLanguageString(self.get_single_string(param - self.header.number_of_constants))
                            elif argument_spec.type == 'ConstString':
                                new_params[argument_spec.name] = SsbOpParamConstString(self.constants[param])
                            else:
                                raise RuntimeError(f"Unknown argument type '{argument_spec.type}'")
                        else:
                            raise RuntimeError(f"Missing argument spec for argument #{i} for OpCode {op.op_code.name}")
                else:
                    new_params = op.params
                new_op = SkyTempleSsbOperation(op.offset, op.op_code, new_params)
                rtn_ops.append(new_op)
            rtns.append(rtn_ops)
        return rtns

    def get_single_string(self, id: int) -> Dict[str, str]:
        """Return a single string in all languages"""
        res = {}
        for key, strs in self.strings.items():
            res[key] = strs[id]
        return res
