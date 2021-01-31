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
from typing import Tuple, Dict, Callable

from explorerscript.error import SsbCompilerError
from explorerscript.macro import ExplorerScriptMacro
from explorerscript.source_map import SourceMap, SourceMapBuilder
from explorerscript.ssb_converting.ssb_data_types import SsbRoutineInfo, SsbOperation, SsbRoutineType, \
    SsbOpParam, SsbOpParamConstString, SsbOpParamConstant, SsbOpParamLanguageString, SsbOpParamPositionMarker
from explorerscript.ssb_converting.ssb_special_ops import OPS_WITH_JUMP_TO_MEM_OFFSET
from explorerscript.ssb_script.ssb_converting.ssb_compiler import SsbScriptSsbCompiler
from explorerscript.ssb_converting.ssb_compiler import ExplorerScriptSsbCompiler
from skytemple_files.common.ppmdu_config.data import Pmd2Data, GAME_REGION_EU
from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptOpCode
from skytemple_files.script.ssb.constants import SsbConstant
from skytemple_files.script.ssb.header import SsbHeaderEu, SsbHeaderUs
from skytemple_files.script.ssb.model import Ssb, List, SkyTempleSsbOperation, SSB_LEN_ROUTINE_INFO_ENTRY, \
    SSB_PADDING_BEFORE_ROUTINE_INFO
from skytemple_files.common.i18n_util import f, _
logger = logging.getLogger(__name__)


class ScriptCompiler:
    """Compiles SSBScript or ExplorerScript into a SSB model"""
    def __init__(self, rom_data: Pmd2Data):
        self.rom_data = rom_data

    def compile_ssbscript(self, ssb_script_src: str, callback_after_parsing: Callable = None) -> Tuple[Ssb, SourceMap]:
        """
        Compile SSBScript into a SSB model

        :raises: ParseError: On parsing errors
        :raises: SsbCompilerError: On logical compiling errors (eg. unknown opcodes)
        :raises: ValueError: On misc. logical compiling errors (eg. unknown constants)
        """
        logger.debug("Compiling SSBScript (size: %d)...", len(ssb_script_src))

        base_compiler = SsbScriptSsbCompiler()
        base_compiler.compile(ssb_script_src)

        # Profiling callback
        if callback_after_parsing:
            callback_after_parsing()

        return self.compile_structured(
            base_compiler.routine_infos, base_compiler.routine_ops, base_compiler.named_coroutines,
            base_compiler.source_map
        )

    def compile_explorerscript(self, es_src: str, exps_absolue_path: str,
                               callback_after_parsing: Callable = None,
                               lookup_paths: List[str] = None) -> Tuple[Ssb, SourceMap]:
        """
        Compile ExplorerScript into a SSB model. Returns the Ssb model, the source map, and a list of macros
        that were used in the ExplorerScript file.

        lookup_paths is the list of include lookup paths.

        :raises: ParseError: On parsing errors
        :raises: SsbCompilerError: On logical compiling errors (eg. unknown opcodes)
        :raises: ValueError: On misc. logical compiling errors (eg. unknown constants)
        """
        logger.debug("Compiling ExplorerScript (size: %d, path: %s)...", len(es_src), exps_absolue_path)

        base_compiler = ExplorerScriptSsbCompiler(
            SsbConstant.create_for(self.rom_data.script_data.game_variables__by_name['PERFORMANCE_PROGRESS_LIST']).name,
            lookup_paths
        )
        base_compiler.compile(es_src, exps_absolue_path)

        # Profiling callback
        if callback_after_parsing:
            callback_after_parsing()

        return self.compile_structured(
            base_compiler.routine_infos, base_compiler.routine_ops, base_compiler.named_coroutines,
            base_compiler.source_map
        )

    def compile_structured(
            self,
            routine_infos: List[SsbRoutineInfo],
            routine_ops: List[List[SsbOperation]],
            named_coroutines: List[str],
            original_source_map: SourceMap
    ) -> Tuple[Ssb, SourceMap]:
        """Compile the structured data from a base compiler for SsbScript or ExplorerScript into an SSB model."""
        logger.debug("Assembling SSB model...")

        model = Ssb.create_empty(self.rom_data.script_data)
        if len(routine_ops) != len(routine_ops) != len(named_coroutines):
            raise SsbCompilerError(_("The routine data lists for the decompiler must have the same lengths."))

        # Build routines and opcodes.
        if len(routine_ops) > 0:
            header_class = SsbHeaderUs
            if self.rom_data.game_region == GAME_REGION_EU:
                header_class = SsbHeaderEu

            built_strings: Dict[str, List[str]] = {lang: [] for lang in header_class.supported_langs()}
            built_constants: List[str] = []

            for i, r in enumerate(routine_infos):
                if r is None:
                    raise SsbCompilerError(f(_("Routine {i} not found.")))

            input_routine_structure: List[
                Tuple[SsbRoutineInfo, str, List[SsbOperation]]
            ] = list(zip(routine_infos, named_coroutines, routine_ops))

            # The cursor position of the written routine opcodes.
            # The opcodes start after the routine info, which has a fixed length, based on the number of routines.
            opcode_cursor = SSB_LEN_ROUTINE_INFO_ENTRY * len(input_routine_structure) + SSB_PADDING_BEFORE_ROUTINE_INFO
            # If it has any coroutines, they all have to be.
            has_coroutines = routine_infos[0].type == SsbRoutineType.COROUTINE

            # Run coroutine checks and sortings.
            if has_coroutines:
                # Assert, that the data contains all coroutines from the ROM schema and sort all three lists by this
                if len(input_routine_structure) != len(self.rom_data.script_data.common_routine_info):
                    raise SsbCompilerError(
                        f(_("The script must contain exactly {len(self.rom_data.script_data.common_routine_info)} coroutines."))
                    )
                if len(routine_infos) != len(set(named_coroutines)):
                    raise SsbCompilerError(f(_("The script must not contain any duplicate coroutines.")))
                try:
                    input_routine_structure = sorted(
                        input_routine_structure, key=lambda k: self.rom_data.script_data.common_routine_info__by_name[k[1]].id
                    )
                except KeyError as err:
                    raise SsbCompilerError(f(_("Unknown coroutine {err}"))) from err

            # Build Routine Infos
            built_routine_info_with_offset: List[Tuple[int, SsbRoutineInfo]] = []
            built_routine_ops: List[List[SsbOperation]] = []
            # A list of lists for ALL opcodes that maps all opcode indices to their memory address.
            opcode_index_mem_offset_mapping: Dict[int, int] = {}
            bytes_written_last_rtn = 0

            for i, (input_info, __, input_ops) in enumerate(input_routine_structure):
                if (
                        has_coroutines and input_info.type != SsbRoutineType.COROUTINE
                ) or (
                        not has_coroutines and input_info.type == SsbRoutineType.COROUTINE
                ):
                    raise SsbCompilerError(f(_("Coroutines and regular routines can not be mixed in a script file.")))

                routine_start_cursor = opcode_cursor
                # Build OPs
                built_ops: List[SkyTempleSsbOperation] = []
                if len(input_ops) == 0:
                    # ALIAS ROUTINE. This alias the PREVIOUS routine
                    routine_start_cursor = opcode_cursor - bytes_written_last_rtn
                else:
                    bytes_written_last_rtn = 0
                    for in_op in input_ops:
                        if in_op.op_code.name not in self.rom_data.script_data.op_codes__by_name:
                            raise SsbCompilerError(f(_("Unknown operation {in_op.op_code.name}.")))
                        op_codes: List[Pmd2ScriptOpCode] = self.rom_data.script_data.op_codes__by_name[in_op.op_code.name]
                        if len(op_codes) > 1:
                            # Can be either a variable length opcode or the "normal" variant.
                            var_len_op_code = next(o for o in op_codes if o.params == -1)
                            normal_op_code = next(o for o in op_codes if o.params != -1)
                            if self._correct_param_list_len(in_op.params) == normal_op_code.params:
                                op_code = normal_op_code
                            elif self._correct_param_list_len(in_op.params) > normal_op_code.params:
                                op_code = var_len_op_code
                            else:
                                raise SsbCompilerError(f(_("The number of parameters for {normal_op_code.name} "
                                                          "must be at least {normal_op_code.params}, is {self._correct_param_list_len(in_op.params)}.")))
                        else:
                            op_code = op_codes[0]
                        new_params: List[int] = []
                        op_len = 2
                        if op_code.params == -1:
                            # Handle variable length opcode by inserting the number of opcodes as the first argument.
                            # ... nothing to do here! Writing the first "meta-argument" for the number of arguments
                            # is the job of the writer later!
                            op_len += 2
                            pass
                        elif self._correct_param_list_len(in_op.params) != op_code.params:
                            # TODO: This might be a confusing count for end users in the case of position markers.
                            raise SsbCompilerError(f(_("The number of parameters for {op_code.name} "
                                                       "must be {op_code.params}, is {self._correct_param_list_len(in_op.params)}.")))
                        for param in in_op.params:
                            if isinstance(param, SsbOpParamPositionMarker):
                                # Handle multi-argument case position markers
                                new_params.append(param.x_offset)
                                new_params.append(param.y_offset)
                                new_params.append(param.x_relative)
                                new_params.append(param.y_relative)
                                op_len += 8
                            else:
                                # Handle the rest
                                new_params.append(self._parse_param(param, built_strings, built_constants))
                                op_len += 2
                        built_ops.append(SkyTempleSsbOperation(opcode_cursor, op_code, new_params))

                        # Create actual offset mapping for this opcode and update source map
                        opcode_index_mem_offset_mapping[in_op.offset] = int(opcode_cursor / 2)

                        bytes_written_last_rtn += op_len
                        opcode_cursor += op_len

                # Find out the target for this routine if it's specified by name
                if input_info.linked_to == -1:
                    input_info.linked_to = SsbConstant(input_info.linked_to_name, self.rom_data.script_data).value.id

                built_routine_info_with_offset.append((routine_start_cursor, input_info))
                built_routine_ops.append(built_ops)

            # Second pass: Update all jumps to their correct place and update string index positions
            for built_routine in built_routine_ops:
                for op in built_routine:
                    if op.op_code.name in OPS_WITH_JUMP_TO_MEM_OFFSET:
                        param_id = OPS_WITH_JUMP_TO_MEM_OFFSET[op.op_code.name]
                        index_to_jump_to = op.params[param_id]
                        op.params[param_id] = opcode_index_mem_offset_mapping[index_to_jump_to]
                    for i, param in enumerate(op.params):
                        if isinstance(param, StringIndexPlaceholder):
                            # If the parameter is a reference to a language string, the length of the constants
                            # has to be added, because the language strings are after the const strings.
                            op.params[i] = len(built_constants) + int(param)

            # Fill the model
            model.routine_info = built_routine_info_with_offset
            model.routine_ops = built_routine_ops
            model.constants = built_constants
            model.strings = built_strings

            # Update the source map
            original_source_map.rewrite_offsets(opcode_index_mem_offset_mapping)

        return model, original_source_map

    def _parse_param(self, param: SsbOpParam, built_strings: Dict[str, List[str]], built_constants: List[str]) -> int:
        if isinstance(param, int):
            return param

        if isinstance(param, SsbOpParamConstant):
            try:
                return SsbConstant(param.name, self.rom_data.script_data).value.id
            except ValueError as err:
                raise SsbCompilerError(str(err)) from err

        if isinstance(param, SsbOpParamConstString):
            i = len(built_constants)
            built_constants.append(param.name)
            return i

        if isinstance(param, SsbOpParamLanguageString):
            i = len(built_strings[next(iter(built_strings.keys()))])
            if len(param.strings.keys()) == 1:
                # Single language convenience mode, apply this to all languages.
                only_value = param.strings[next(iter(param.strings.keys()))]
                for lang in built_strings.keys():
                    built_strings[lang].append(only_value)
            else:
                # Multi language regular case. All languages must be known.
                for lang, string in param.strings.items():
                    if lang not in built_strings:
                        raise SsbCompilerError(f(_("Unknown language for string: {lang}")))
                    built_strings[lang].append(string)
            return StringIndexPlaceholder(i)

        raise SsbCompilerError(f(_("Invalid parameter supplied for an operation: {param}")))

    @staticmethod
    def _correct_param_list_len(params: List[SsbOpParam]):
        """Returns the correct length of a parameter list (positon markers count as 4"""
        len = 0
        for p in params:
            if isinstance(p, SsbOpParamPositionMarker):
                len += 4
            else:
                len += 1
        return len


class StringIndexPlaceholder(int):
    pass
