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
from typing import Callable, Dict, List, Set

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data, GAME_VERSION_EOS, GAME_REGION_US, GAME_REGION_EU
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler
from skytemple_files.patch.asm_tools import AsmFunction
from skytemple_files.common.i18n_util import _

PATCH_CHECK_ADDR_APPLIED_US = 0x3F76C
PATCH_CHECK_INSTR_APPLIED_US = 0xE3500F67
PATCH_CHECK_ADDR_APPLIED_EU = 0x3F88C
PATCH_CHECK_INSTR_APPLIED_EU = 0xE3500F67


START_OV29_US = 0x022DC240
START_TABLE_US = 0x0231B9AC
START_M_FUNC_US = 0x0231BE50
END_M_FUNC_US = 0x0231CB14
DATA_SEG_US = 0x0231C6C0

START_OV29_EU = 0x022DCB80
START_TABLE_EU = 0x0231C40C
START_M_FUNC_EU = 0x0231C8B0
END_M_FUNC_EU = 0x0231D574
DATA_SEG_EU = 0x0231D120

ITEM_CODE_PATH = "BALANCE/item_cd.bin"


class ExtractItemCodePatchHandler(AbstractPatchHandler):

    @property
    def name(self) -> str:
        return 'ExtractItemCode'

    @property
    def description(self) -> str:
        return _('Extracts item effects code and put it in files.')

    @property
    def author(self) -> str:
        return 'irdkwia'

    @property
    def version(self) -> str:
        return '0.0.1'

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.UTILITY

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_uintle(rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_US, 4)!=PATCH_CHECK_INSTR_APPLIED_US
            if config.game_region == GAME_REGION_EU:
                return read_uintle(rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_EU, 4)!=PATCH_CHECK_INSTR_APPLIED_EU
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        if not self.is_applied(rom, config):
            if config.game_version == GAME_VERSION_EOS:
                if config.game_region == GAME_REGION_US:
                    start_ov29 = START_OV29_US
                    start_table = START_TABLE_US
                    start_m_functions = START_M_FUNC_US
                    end_m_functions = END_M_FUNC_US
                    data_seg = DATA_SEG_US
                if config.game_region == GAME_REGION_EU:
                    start_ov29 = START_OV29_EU
                    start_table = START_TABLE_EU
                    start_m_functions = START_M_FUNC_EU
                    end_m_functions = END_M_FUNC_EU
                    data_seg = DATA_SEG_EU
            
            main_func = dict()

            data = rom.loadArm9Overlays([29])[29].data
            
            switch = AsmFunction(data[start_table-start_ov29:start_m_functions-start_ov29], start_table)
            ext_data = switch.process()[1]
            lst_data = {}
            data_processed = set()
            for offset in ext_data:
                code = 0
                for x in range(4):
                    code += data[offset-start_ov29+x]*(256**x)
                lst_data[offset] = code
                data_processed.add(offset)
            switch.provide_data(lst_data)
            main_calls = switch.process_switch(0, (0,1400), {})
            
            unique_main_calls = set(main_calls)
            unique_main_calls.add(data_seg)
            unique_main_calls = list(sorted(unique_main_calls))
            unique_main_calls.append(end_m_functions)

            for i in range(len(unique_main_calls)-1):
                if unique_main_calls[i]!=data_seg:
                    start = unique_main_calls[i]
                    end = unique_main_calls[i+1]
                    func_data = data[start-start_ov29:end-start_ov29]
                    main_func[start] = AsmFunction(func_data, start)
                    ext_data = main_func[start].process()[1]
                    if i>=len(unique_main_calls)-3:
                        new_baddr = (end_m_functions-len(func_data)-start_m_functions-0x8)//0x4
                        if new_baddr<0:
                            new_baddr += 2*0x800000
                        main_func[start].add_instructions(bytes([new_baddr%256, (new_baddr//256)%256, (new_baddr//65536)%256, 0xEA]))
                    lst_data = {}
                    for offset in ext_data:
                        code = 0
                        for x in range(4):
                            code += data[offset-start_ov29+x]*(256**x)
                        lst_data[offset] = code
                        data_processed.add(offset)
                    main_func[start].provide_data(lst_data)

            nb_items = len(main_calls)
            header = bytearray(4+2*nb_items+len(main_func)*8)
            write_uintle(header, 4+2*nb_items, 0, 4)
            code_data = bytearray(0)
            current_ptr = len(header)
            id_codes = dict()
            for i, t in enumerate(main_func.items()):
                k = t[0]
                x = t[1]
                id_codes[k] = i
                fdata = bytearray(x.compile(start_m_functions))
                write_uintle(header, current_ptr, 4+2*nb_items+i*8, 4)
                write_uintle(header, len(fdata), 4+2*nb_items+i*8+4, 4)
                code_data += fdata
                
                current_ptr += len(fdata)
            for i, x in enumerate(main_calls):
                write_uintle(header, id_codes[x], 4+2*i, 2)
            file_data = header + code_data
            if ITEM_CODE_PATH not in rom.filenames:
                create_file_in_rom(rom, ITEM_CODE_PATH, file_data)
            else:
                rom.setFileByName(ITEM_CODE_PATH, file_data)
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    
    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
