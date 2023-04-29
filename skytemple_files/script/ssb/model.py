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

import logging
from typing import Dict, Optional, List, Tuple

from explorerscript.source_map import SourceMap
from explorerscript.ssb_converting.ssb_data_types import (
    SsbOperation,
    SsbOpParam,
    SsbOpParamConstString,
    SsbOpParamLanguageString,
    SsbOpParamPositionMarker,
    SsbRoutineInfo,
    SsbRoutineType,
)
from explorerscript.ssb_converting.ssb_decompiler import ExplorerScriptSsbDecompiler
from explorerscript.ssb_script.ssb_converting.ssb_decompiler import (
    SsbScriptSsbDecompiler,
)

from skytemple_files.common import string_codec
from skytemple_files.common.ppmdu_config.script_data import (
    Pmd2ScriptData,
    Pmd2ScriptOpCode,
)
from skytemple_files.common.util import read_var_length_string, read_u16
from skytemple_files.script.ssb.constants import SsbConstant
from skytemple_files.script.ssb.header import AbstractSsbHeader

logger = logging.getLogger(__name__)


SSB_LEN_ROUTINE_INFO_ENTRY = 6
SSB_PADDING_BEFORE_ROUTINE_INFO = 4
ENUM_ARGUMENTS = {
    "Entity": "level_entities__by_id",
    "Object": "objects__by_id",
    "Routine": "common_routine_info__by_id",
    "Face": "face_names__by_id",
    "FaceMode": "face_position_modes__by_id",
    "GameVar": "game_variables__by_id",
    "Level": "level_list__by_id",
    "Menu": "menus__by_id",
    "ProcessSpecial": "process_specials__by_id",
    "Direction": "directions__by_ssb_id",
    "Bgm": "bgms__by_id",
    "Effect": "sprite_effects__by_id",
}


class SkyTempleSsbOperation(SsbOperation):
    def __init__(
        self, offset: int, op_code: Pmd2ScriptOpCode, params: List[SsbOpParam]
    ):
        super().__init__(offset, op_code, params)


class Ssb:
    @classmethod
    def create_empty(cls, scriptdata: Pmd2ScriptData, supported_langs=None):
        return cls(
            None, None, None, scriptdata, if_empty_supported_langs=supported_langs
        )

    def __init__(
        self,
        data: Optional[bytes],
        header: Optional[AbstractSsbHeader],
        begin_data_offset: Optional[int],
        scriptdata: Pmd2ScriptData,
        if_empty_supported_langs=None,
        string_codec=string_codec.PMD2_STR_ENCODER,
    ):
        self._scriptdata = scriptdata
        self._string_codec = string_codec

        if data is None:
            # Empty model mode, for the ScriptCompiler.
            if if_empty_supported_langs is None:
                if_empty_supported_langs = []
            self.original_binary_data = bytes()
            self.routine_info: List[Tuple[int, SsbRoutineInfo]] = []
            self.routine_ops: List[List[SkyTempleSsbOperation]] = []
            self.constants: List[str] = []
            self.strings: Dict[str, List[str]] = {
                lang_name: [] for lang_name in if_empty_supported_langs
            }
            return
        assert begin_data_offset is not None
        assert header is not None

        logger.debug("Deserializing SSB model (size: %d)...", len(data))

        if not isinstance(data, memoryview):
            data = memoryview(data)

        # WARNING: This is NOT updated by this model. Only the writer can update it.
        self.original_binary_data = bytes(data)

        start_of_const_table = begin_data_offset + (
            read_u16(data, begin_data_offset + 0x00) * 2
        )
        number_of_routines = read_u16(data, begin_data_offset + 0x02)

        self._header = header
        self.routine_info = []  # Offset, RoutineInfo
        self.routine_ops = []

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
                        if alias_i == len(self.routine_info):
                            end_offset = start_of_const_table
                            break
                        end_offset = begin_data_offset + self.routine_info[alias_i][0]
                read_ops, cursor = self._read_routine_op_codes(
                    data,
                    begin_data_offset + rtn_start_offset,
                    end_offset,
                    begin_data_offset,
                )
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
                start_of_const_table
                + read_u16(data, i)
                - (header.number_of_strings * 2)
            )
        self.constants = []
        cursor = start_of_constants
        # Read constants
        for const_string_offset in const_offset_table:
            assert cursor == const_string_offset
            bytes_read, string = read_var_length_string(
                data, const_string_offset, self._string_codec
            )
            self.constants.append(string)
            cursor += bytes_read
        # Padding if not even
        if cursor % 2 != 0:
            cursor += 1
        # The end of the script block must also match the data from the header
        assert (
            start_of_const_table + header.number_of_constants * 2 == start_of_constants
        )

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
                    start_of_const_table
                    + read_u16(data, i)
                    + previous_languages_block_sizes
                )
            cursor += header.number_of_strings * 2
            # Read strings
            for string_offset in string_offset_table_lang:
                assert cursor == string_offset
                bytes_read, string = read_var_length_string(
                    data, string_offset, self._string_codec
                )
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
            self.routine_info.append(
                (
                    read_u16(data, cursor) * 2,
                    SsbRoutineInfo(
                        type=SsbRoutineType(read_u16(data, cursor + 2)),
                        linked_to=read_u16(data, cursor + 4),
                    ),
                )
            )
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
        op_code = self._scriptdata.op_codes__by_id[read_u16(data, cursor)]
        cursor += 2
        arguments = []
        cnt_params = op_code.params
        if cnt_params == -1:
            # Variable length opcode
            cnt_params = read_u16(data, cursor)
            cursor += 2
        for i in range(0, cnt_params):
            arguments.append(read_u16(data, cursor))
            cursor += 2

        return SkyTempleSsbOperation(opcode_offset, op_code, arguments), cursor

    def to_explorerscript(self) -> Tuple[str, SourceMap]:
        self.add_linked_to_names_to_routine_ops()
        return ExplorerScriptSsbDecompiler(
            [x[1] for x in self.routine_info],
            self.get_filled_routine_ops(),
            self._scriptdata.common_routine_info,
            SsbConstant.create_for(
                self._scriptdata.game_variables__by_name["PERFORMANCE_PROGRESS_LIST"]
            ).name,
            SsbConstant.get_dungeon_mode_constants(),
        ).convert()

    def to_ssb_script(self) -> Tuple[str, SourceMap]:
        self.add_linked_to_names_to_routine_ops()
        return SsbScriptSsbDecompiler(
            [x[1] for x in self.routine_info],
            self.get_filled_routine_ops(),
            self._scriptdata.common_routine_info,
        ).convert()

    def add_linked_to_names_to_routine_ops(self):
        for _, r in self.routine_info:
            try:
                if r.type == SsbRoutineType.ACTOR:
                    r.linked_to_name = SsbConstant.create_for(
                        self._scriptdata.level_entities__by_id[r.linked_to]
                    ).name
                elif r.type == SsbRoutineType.OBJECT:
                    r.linked_to_name = SsbConstant.create_for(
                        self._scriptdata.objects__by_id[r.linked_to]
                    ).name
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
                        if argument_spec.type == "uint":
                            # TODO: Do unsigned parameters actually exist? If so are they also 14bit?
                            new_params.append(param)
                        elif argument_spec.type == "sint":
                            # 14 bit signed int.
                            if param >= 0x8000:
                                # ??? This is bigger than 14bit.
                                pass
                            elif param & 0x4000:
                                param = -0x8000 + param
                            new_params.append(param)
                        elif argument_spec.type == "sint16":
                            # 16bit signed
                            if param & 0x8000:
                                param = -0x10000 + param
                            new_params.append(param)
                        elif argument_spec.type in ENUM_ARGUMENTS:
                            const_data = getattr(
                                self._scriptdata, ENUM_ARGUMENTS[argument_spec.type]
                            )
                            if param in const_data:
                                new_params.append(
                                    SsbConstant.create_for(const_data[param])
                                )
                            else:
                                logger.warning(
                                    f"Unknown {argument_spec.type} id: {param}"
                                )
                                new_params.append(param)
                        elif (
                            argument_spec.type == "String"
                            or argument_spec.type == "ConstString"
                        ):
                            if param >= len(self.constants):
                                new_params.append(
                                    SsbOpParamLanguageString(
                                        self.get_single_string(
                                            param - len(self.constants)
                                        )
                                    )
                                )
                            else:
                                new_params.append(
                                    SsbOpParamConstString(self.constants[param])
                                )
                        elif argument_spec.type == "PositionMark":
                            x_offset = y_offset = x_relative = y_relative = 0
                            try:
                                x_offset = param
                                y_offset = op.params[i + 1]
                                x_relative = op.params[i + 2]
                                y_relative = op.params[i + 3]
                            except IndexError:
                                logger.warning(
                                    "SSB had wrong number of arguments for building a position marker."
                                )
                            new_params.append(
                                SsbOpParamPositionMarker(
                                    f"m{pos_marker_increment}",
                                    x_offset,
                                    y_offset,
                                    x_relative,
                                    y_relative,
                                )
                            )
                            pos_marker_increment += 1
                            skip_arguments = 3
                        else:
                            raise RuntimeError(
                                f"Unknown argument type '{argument_spec.type}'"
                            )
                    else:
                        raise RuntimeError(
                            f"Missing argument spec for argument #{i} for OpCode {op.op_code.name}"
                        )
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
        if (
            op_code.repeating_argument_group is not None
            and op_code.repeating_argument_group.id <= i
        ):
            # Use repeating args
            repeat_i = i - op_code.repeating_argument_group.id
            index = repeat_i % len(op_code.repeating_argument_group.arguments)
            return op_code.repeating_argument_group.arguments[index]
        elif i in op_code.arguments__by_id:
            return op_code.arguments__by_id[i]
        return None

    @classmethod
    def internal__get_all_raw_strings_from(
        cls, data: bytes, region: str
    ) -> List[bytes]:
        """Returns all strings in this file, undecoded."""

        def _read_var_length_string_raw(stdata: bytes, start: int = 0):
            bytes_of_string = bytearray()
            current_byte = -1
            stcursor = start
            while current_byte != 0:
                current_byte = stdata[stcursor]
                stcursor += 1
                if current_byte != 0:
                    bytes_of_string.append(current_byte)

            return stcursor - start, bytes_of_string

        from skytemple_files.common.ppmdu_config.data import (
            GAME_REGION_EU,
            GAME_REGION_JP,
            GAME_REGION_US,
        )
        from skytemple_files.script.ssb.header import (
            SsbHeaderEu,
            SsbHeaderJp,
            SsbHeaderUs,
        )

        if not isinstance(data, memoryview):
            data = memoryview(data)

        header: AbstractSsbHeader
        if region == GAME_REGION_EU:
            header = SsbHeaderEu(data)
        elif region == GAME_REGION_US:
            header = SsbHeaderUs(data)
        elif region == GAME_REGION_JP:
            header = SsbHeaderJp(data)
        else:
            raise ValueError(f"Unsupported game edition: {region}")

        start_of_const_table = header.data_offset + (
            read_u16(data, header.data_offset + 0x00) * 2
        )

        # ### CONSTANT OFFSETS AND CONSTANT STRINGS
        # Read const offset table
        start_of_constants = header.data_offset + header.constant_strings_start
        const_offset_table = []
        for i in range(start_of_const_table, start_of_constants, 2):
            const_offset_table.append(
                # Actual offset is start_of_constble + X - header.number_of_strings_ta
                start_of_const_table
                + read_u16(data, i)
                - (header.number_of_strings * 2)
            )
        constants = []
        cursor = start_of_constants
        # Read constants
        for const_string_offset in const_offset_table:
            assert cursor == const_string_offset
            bytes_read, string = _read_var_length_string_raw(data, const_string_offset)
            constants.append(string)
            cursor += bytes_read
        # Padding if not even
        if cursor % 2 != 0:
            cursor += 1
        # The end of the script block must also match the data from the header
        assert (
            start_of_const_table + header.number_of_constants * 2 == start_of_constants
        )

        # ### STRING OFFSETS AND STRING STRINGS
        # Read strings
        strings = []
        # The offsets of other languages DON'T count the size of the previuos langs, so we have to add them
        previous_languages_block_sizes = 0
        for language, len_of_lang in header.string_table_lengths.items():
            cursor_before_strings = cursor
            string_offset_table_lang = []
            strings_lang = []
            # Read string offset table
            for i in range(cursor, cursor + header.number_of_strings * 2, 2):
                string_offset_table_lang.append(
                    start_of_const_table
                    + read_u16(data, i)
                    + previous_languages_block_sizes
                )
            cursor += header.number_of_strings * 2
            # Read strings
            for string_offset in string_offset_table_lang:
                assert cursor == string_offset
                bytes_read, string = _read_var_length_string_raw(data, string_offset)
                strings_lang.append(string)
                cursor += bytes_read
            strings += strings_lang
            # Padding if not even
            if cursor % 2 != 0:
                cursor += 1
            previous_languages_block_sizes += len_of_lang
            assert cursor_before_strings + len_of_lang == cursor
        return constants + strings
