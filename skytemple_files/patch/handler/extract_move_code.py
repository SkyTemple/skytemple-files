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
from skytemple_files.patch.handler.abstract import AbstractPatchHandler

BRANCH_MASK = 0x0E000000
BRANCH_CODE = 0x0A000000
BRANCH_ADDR = 0x00FFFFFF
BRANCH_NEG = 0x00800000
LDR_MASK = 0x0F7F0000
LDR_CODE = 0x051F0000
LDR_OFFSET = 0x00000FFF
LDR_NEG = 0x00800000

class AsmFunction:
    def __init__(self, data: bytes, old_start_address: int):
        self.data = data
        self.old_start_address = old_start_address
        self.external_calls = {}
    def _read_instr(self, i):
        code = 0
        for x in range(4):
            code += self.data[i*4+x]*(256**x)
        return code
    def process(self) -> Set[int]:
        r12_loc = 0
        calls = set()
        for x in range(len(self.data)//4):
            offset = self.old_start_address+x*4
            code = self._read_instr(x)
            if code&BRANCH_MASK==BRANCH_CODE:
                baddr = code&BRANCH_ADDR
                if baddr>=BRANCH_NEG:
                    baddr -= 2*BRANCH_NEG
                baddr = baddr*0x4+offset+0x8
                if not (self.old_start_address<=baddr<self.old_start_address+len(self.data)):
                    self.external_calls[x] = (False, baddr, 'b')
                    calls.add(baddr)
            elif code&LDR_MASK==LDR_CODE:
                offset = code&LDR_OFFSET
                if code&LDR_NEG:
                    offset = -offset
                offset += 0x8
                datapos = x+offset//4
                self.external_calls[datapos] = (False, self._read_instr(datapos), 'ldr')
        return calls
    def link_to_others(self, func_list: Dict[int, 'AsmFunction']) -> bool:
        has_links = False
        for c in self.external_calls.keys():
            v = self.external_calls[c]
            baddr = v[1]
            if baddr in func_list:
                self.external_calls[c] = (True, func_list[baddr], v[2])
                has_links = True
        return has_links
    def compile(self, new_start_address: int) -> bytes:
        new_data = bytearray(self.data)
        
        for c, v in self.external_calls.items():
            if v[0]:
                if self==v[1]:
                    new_baddr = new_start_address
                else:
                    new_baddr = new_start_address+len(new_data)
                    new_data += bytearray(v[1].compile(new_baddr))
            else:
                new_baddr = v[1]
            if v[2]=='b':
                offset = new_start_address+c*4
                new_baddr = (new_baddr-offset-0x8)//4
                if new_baddr<0:
                    new_baddr += 2*BRANCH_NEG
                new_data[c*4:c*4+3] = bytearray([new_baddr%256, (new_baddr//256)%256, (new_baddr//65536)%256])
            elif v[2]=='ldr':
                new_data[c*4:c*4+4] = bytearray([new_baddr%256, (new_baddr//256)%256, (new_baddr//65536)%256, (new_baddr//65536//256)%256])
        return bytes(new_data)

PATCH_CHECK_ADDR_APPLIED_US = 0x53664
PATCH_CHECK_INSTR_APPLIED_US = 0xE3A01001
PATCH_CHECK_ADDR_APPLIED_EU = 0x53764
PATCH_CHECK_INSTR_APPLIED_EU = 0xE3A01001


START_OV29_US = 0x022DC240
START_TABLE_US = 0x0232F8B8
START_M_FUNC_US = 0x02330134
END_M_FUNC_US = 0x023326CC

START_OV29_EU = 0x022DCB80
START_TABLE_EU = 0x023302F8
START_M_FUNC_EU = 0x02330B74
END_M_FUNC_EU = 0x0233310C

MOVE_CODE_PATH = "BALANCE/waza_cd.bin"

class ExtractMoveCodePatchHandler(AbstractPatchHandler):

    @property
    def name(self) -> str:
        return 'ExtractMoveCode'

    @property
    def description(self) -> str:
        return 'Extracts move effects code and put it in files. '

    @property
    def author(self) -> str:
        return 'irdkwia'

    @property
    def version(self) -> str:
        return '0.0.1'

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
                if config.game_region == GAME_REGION_EU:
                    start_ov29 = START_OV29_EU
                    start_table = START_TABLE_EU
                    start_m_functions = START_M_FUNC_EU
                    end_m_functions = END_M_FUNC_EU

            main_calls = []
            main_func = dict()

            data = rom.loadArm9Overlays([29])[29].data
                
            for offset in range(start_table, start_m_functions, 4):
                code = 0
                for x in range(4):
                    code += data[offset-start_ov29+x]*(256**x)
                baddr = code&BRANCH_ADDR
                if baddr>=BRANCH_NEG:
                    baddr -= 2*BRANCH_NEG
                baddr = baddr*0x4+offset+0x8
                main_calls.append(baddr)

            unique_main_calls = list(sorted(set(main_calls)))
            unique_main_calls.append(end_m_functions)

            for i in range(len(unique_main_calls)-1):
                start = unique_main_calls[i]
                end = unique_main_calls[i+1]
                func_data = data[start-start_ov29:end-start_ov29]
                main_func[start] = AsmFunction(func_data, start)
                main_func[start].process()

            nb_moves = len(main_calls)
            header = bytearray(4+2*nb_moves+len(main_func)*8)
            write_uintle(header, 4+2*nb_moves, 0, 4)
            code_data = bytearray(0)
            current_ptr = len(header)
            id_codes = dict()
            for i, t in enumerate(main_func.items()):
                k = t[0]
                x = t[1]
                id_codes[k] = i
                fdata = bytearray(x.compile(start_m_functions))
                write_uintle(header, current_ptr, 4+2*nb_moves+i*8, 4)
                write_uintle(header, len(fdata), 4+2*nb_moves+i*8+4, 4)
                code_data += fdata
                
                current_ptr += len(fdata)
            for i, x in enumerate(main_calls):
                write_uintle(header, id_codes[x], 4+2*i, 2)
            file_data = header + code_data
            if MOVE_CODE_PATH not in rom.filenames:
                create_file_in_rom(rom, MOVE_CODE_PATH, file_data)
            else:
                rom.setFileByName(MOVE_CODE_PATH, file_data)
        try:
            apply()
        except RuntimeError as ex:
            raise ex
    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
