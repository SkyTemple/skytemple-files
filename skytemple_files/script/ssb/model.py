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
import logging
from typing import Dict, Optional

from explorerscript.source_map import SourceMap
from explorerscript.ssb_converting.ssb_decompiler import ExplorerScriptSsbDecompiler
from explorerscript.ssb_converting.ssb_data_types import SsbRoutineType, SsbRoutineInfo, \
    SsbOpParamConstString, SsbOpParamLanguageString, SsbOperation, SsbOpParam, SsbOpParamPositionMarker
from explorerscript.ssb_script.ssb_converting.ssb_decompiler import SsbScriptSsbDecompiler
from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptData, Pmd2ScriptOpCode
from skytemple_files.common.util import *
from skytemple_files.script.ssb.constants import SsbConstant
from skytemple_files.script.ssb.header import AbstractSsbHeader

logger = logging.getLogger(__name__)


SSB_LEN_ROUTINE_INFO_ENTRY = 6
SSB_PADDING_BEFORE_ROUTINE_INFO = 4


class SkyTempleSsbOperation(SsbOperation):
    def __init__(self, offset: int, op_code: Pmd2ScriptOpCode, params: List[SsbOpParam]):
        super().__init__(offset, op_code, params)


class Ssb:
    @classmethod
    def create_empty(cls, scriptdata: Pmd2ScriptData, supported_langs=None):
        return cls(None, None, None, scriptdata, if_empty_supported_langs=supported_langs)

    def __init__(
            self, data: Optional[bytes], header: Optional[AbstractSsbHeader],
            begin_data_offset: Optional[int], scriptdata: Pmd2ScriptData, if_empty_supported_langs=None,
            string_codec=string_codec.PMD2_STR_ENCODER
    ):

        self._scriptdata = scriptdata
        self._string_codec = string_codec

        if data is None:
            # Empty model mode, for the ScriptCompiler.
            if if_empty_supported_langs is None:
                if_empty_supported_langs = []
            self.original_binary_data = bytes()
            self.routine_info = []
            self.routine_ops = []
            self.constants = []
            self.strings = {lang_name: [] for lang_name in if_empty_supported_langs}
            return

        logger.debug("Deserializing SSB model (size: %d)...", len(data))

        if not isinstance(data, memoryview):
            data = memoryview(data)

        # WARNING: This is NOT updated by this model. Only the writer can update it.
        self.original_binary_data = bytes(data)

        start_of_const_table = begin_data_offset + (read_uintle(data, begin_data_offset + 0x00, 2) * 2)
        number_of_routines = read_uintle(data, begin_data_offset + 0x02, 2)

        self._header = header
        self.routine_info: List[Tuple[int, SsbRoutineInfo]] = []  # Offset, RoutineInfo
        self.routine_ops: List[List[SkyTempleSsbOperation]] = []

        cursor = begin_data_offset + SSB_PADDING_BEFORE_ROUTINE_INFO
        cursor = self._read_routine_info(data, number_of_routines, cursor)

        alias_counter = 0
        for i, (rtn_start_offset, _) in enumerate(self.routine_info):
            if alias_counter > 0:
                # process an alias of the previous routine
                alias_counter -= 1
                read_ops = []
            else:
                if i == number_of_routines - 1:
                    end_offset = start_of_const_table
                else:
                    alias_i = i + 1
                    end_offset = begin_data_offset + self.routine_info[alias_i][0]
                    while begin_data_offset + rtn_start_offset == end_offset:
                        # This is a set of aliases!
                        alias_counter += 1
                        alias_i += 1
                        end_offset = begin_data_offset + self.routine_info[alias_i][0]
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
                # Actual offset is start_of_constble + X - header.number_of_strings_ta
                start_of_const_table + read_uintle(data, i, 2) - (header.number_of_strings * 2)
            )
        self.constants = []
        cursor = start_of_constants
        # Read constants
        for const_string_offset in const_offset_table:
            assert cursor == const_string_offset
            bytes_read, string = read_var_length_string(data, const_string_offset, self._string_codec)
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
                bytes_read, string = read_var_length_string(data, string_offset, self._string_codec)
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
            cursor += SSB_LEN_ROUTINE_INFO_ENTRY
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
            self._scriptdata.common_routine_info__by_id,
            SsbConstant.create_for(self._scriptdata.game_variables__by_name['PERFORMANCE_PROGRESS_LIST']).name,
            SsbConstant.get_dungeon_mode_constants()
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
            try:
                if r.type == SsbRoutineType.ACTOR:
                    r.linked_to_name = SsbConstant.create_for(self._scriptdata.level_entities__by_id[r.linked_to]).name
                elif r.type == SsbRoutineType.OBJECT:
                    r.linked_to_name = SsbConstant.create_for(self._scriptdata.objects__by_id[r.linked_to]).name
            except KeyError:
                pass

    def get_filled_routine_ops(self):
        """Returns self.routine_ops, but with constant strings, strings and constants from scriptdata filled out"""
        logger.debug("Disassembling SSB model data...")
        rtns: List[List[SkyTempleSsbOperation]] = []
        pos_marker_increment = 0
        for rtn in self.routine_ops:
            rtn_ops = []
            for op in rtn:
                new_params = []
                skip_arguments = 0
                for i, param in enumerate(op.params):
                    if skip_arguments > 0:
                        skip_arguments -= 1
                        continue
                    argument_spec = self._get_argument_spec(op.op_code, i)
                    if argument_spec is not None:
                        if argument_spec.type == 'uint':
                            # TODO: Do unsigned parameters actually exist? If so are they also 14bit?
                            new_params.append(param)
                        elif argument_spec.type == 'sint':
                            # 14 bit signed int.
                            if param >= 0x8000:
                                # ??? This is bigger than 14bit.
                                pass
                            elif param & 0x4000:
                                param = -0x8000 + param
                            new_params.append(param)
                        elif argument_spec.type == 'sint16':
                            # 16bit signed
                            if param & 0x8000:
                                param = -0x10000 + param
                            new_params.append(param)
                        elif argument_spec.type == 'Entity':
                            new_params.append(SsbConstant.create_for(self._scriptdata.level_entities__by_id[param]))
                        elif argument_spec.type == 'Object':
                            new_params.append(SsbConstant.create_for(self._scriptdata.objects__by_id[param]))
                        elif argument_spec.type == 'Routine':
                            new_params.append(SsbConstant.create_for(self._scriptdata.common_routine_info__by_id[param]))
                        elif argument_spec.type == 'Face':
                            if param in self._scriptdata.face_names__by_id:
                                new_params.append(SsbConstant.create_for(self._scriptdata.face_names__by_id[param]))
                            else:
                                logger.warning(f"Unknown face id: {param}")
                                new_params.append(param)
                        elif argument_spec.type == 'FaceMode':
                            new_params.append(SsbConstant.create_for(self._scriptdata.face_position_modes__by_id[param]))
                        elif argument_spec.type == 'GameVar':
                            new_params.append(SsbConstant.create_for(self._scriptdata.game_variables__by_id[param]))
                        elif argument_spec.type == 'Level':
                            if param in self._scriptdata.level_list__by_id:
                                new_params.append(SsbConstant.create_for(self._scriptdata.level_list__by_id[param]))
                            else:
                                logger.warning(f"Unknown level id: {param}")
                                new_params.append(param)
                        elif argument_spec.type == 'Menu':
                            if param in self._scriptdata.menus__by_id:
                                new_params.append(SsbConstant.create_for(self._scriptdata.menus__by_id[param]))
                            else:
                                logger.warning(f"Unknown menu id: {param}")
                                new_params.append(param)
                        elif argument_spec.type == 'ProcessSpecial':
                            if param in self._scriptdata.process_specials__by_id:
                                new_params.append(SsbConstant.create_for(self._scriptdata.process_specials__by_id[param]))
                            else:
                                new_params.append(param)
                                logger.warning(f"Unknown special process id: {param}")
                        elif argument_spec.type == 'Direction':
                            if param in self._scriptdata.directions__by_ssb_id:
                                new_params.append(SsbConstant.create_for(self._scriptdata.directions__by_ssb_id[param]))
                            else:
                                new_params.append(param)
                                logger.warning(f"Unknown direction id: {param}")
                        elif argument_spec.type == 'Bgm':
                            if param in self._scriptdata.bgms__by_id:
                                new_params.append(SsbConstant.create_for(self._scriptdata.bgms__by_id[param]))
                            else:
                                logger.warning(f"Unknown BGM id: {param}")
                                new_params.append(param)
                        elif argument_spec.type == 'Effect':
                            if param in self._scriptdata.sprite_effects__by_id:
                                new_params.append(SsbConstant.create_for(self._scriptdata.sprite_effects__by_id[param]))
                            else:
                                logger.warning(f"Unknown effect id: {param}")
                                new_params.append(param)
                        elif argument_spec.type == 'String':
                            try:
                                new_params.append(SsbOpParamLanguageString(self.get_single_string(param - len(self.constants))))
                            except IndexError:
                                # Fall back to const table
                                new_params.append(SsbOpParamConstString(self.constants[param]))
                        elif argument_spec.type == 'ConstString':
                            try:
                                new_params.append(SsbOpParamConstString(self.constants[param]))
                            except IndexError:
                                # Fall back to lang string
                                new_params.append(SsbOpParamLanguageString(self.get_single_string(param - len(self.constants))))
                        elif argument_spec.type == 'PositionMark':
                            x_offset = y_offset = x_relative = y_relative = 0
                            try:
                                x_offset = param
                                y_offset = op.params[i + 1]
                                x_relative = op.params[i + 2]
                                y_relative = op.params[i + 3]
                            except IndexError:
                                logger.warning("SSB had wrong number of arguments for building a position marker.")
                            new_params.append(SsbOpParamPositionMarker(
                                f'm{pos_marker_increment}', x_offset, y_offset, x_relative, y_relative
                            ))
                            pos_marker_increment += 1
                            skip_arguments = 3
                        else:
                            raise RuntimeError(f"Unknown argument type '{argument_spec.type}'")
                    else:
                        raise RuntimeError(f"Missing argument spec for argument #{i} for OpCode {op.op_code.name}")
                new_op = SkyTempleSsbOperation(op.offset, op.op_code, new_params)
                rtn_ops.append(new_op)
            rtns.append(rtn_ops)
        return rtns

    def get_single_string(self, id: int) -> Dict[str, str]:
        """Return a single string in all languages"""
        res = {}
        if len(self.strings) < 1:
            raise IndexError(f"No strings exist.")
        for key, strs in self.strings.items():
            res[key] = strs[id]
        return res

    @staticmethod
    def _get_argument_spec(op_code: Pmd2ScriptOpCode, i):
        """Returns the spec for an argument at a given index, if defined. Also checks repeating arguments."""
        # Maybe it's a repeating argument?
        if op_code.repeating_argument_group is not None and op_code.repeating_argument_group.id <= i:
            # Use repeating args
            repeat_i = i - op_code.repeating_argument_group.id
            index = repeat_i % len(op_code.repeating_argument_group.arguments)
            return op_code.repeating_argument_group.arguments[index]
        elif i in op_code.arguments__by_id:
            return op_code.arguments__by_id[i]
        return None
