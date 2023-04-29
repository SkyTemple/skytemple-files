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

from typing import Callable

from ndspy.rom import NintendoDSRom
from range_typed_integers import u32_checked, u16

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_US,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.util import (
    create_file_in_rom,
    write_u32,
    write_u16,
    read_u32,
)
from skytemple_files.patch.asm_tools import AsmFunction
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler

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
        return "ExtractItemCode"

    @property
    def description(self) -> str:
        return _("Extracts item effects code and put it in files.")

    @property
    def author(self) -> str:
        return "Anonymous"

    @property
    def version(self) -> str:
        return "0.0.1"

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.UTILITY

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return (
                    read_u32(
                        rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_US
                    )
                    != PATCH_CHECK_INSTR_APPLIED_US
                )
            if config.game_region == GAME_REGION_EU:
                return (
                    read_u32(
                        rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_EU
                    )
                    != PATCH_CHECK_INSTR_APPLIED_EU
                )
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
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

            switch = AsmFunction(
                data[start_table - start_ov29 : start_m_functions - start_ov29],
                start_table,
            )
            ext_data = switch.process()[1]
            lst_data = {}
            data_processed = set()
            for offset in ext_data:
                code = 0
                for xx in range(4):
                    code += data[offset - start_ov29 + xx] * (256**xx)
                lst_data[offset] = code
                data_processed.add(offset)
            switch.provide_data(lst_data)
            main_calls = switch.process_switch(0, (0, 1400), {})

            unique_main_calls_p = set(main_calls)
            unique_main_calls_p.add(data_seg)
            unique_main_calls = list(sorted(unique_main_calls_p))
            unique_main_calls.append(end_m_functions)

            for i in range(len(unique_main_calls) - 1):
                if unique_main_calls[i] != data_seg:
                    start = unique_main_calls[i]
                    end = unique_main_calls[i + 1]
                    func_data = data[start - start_ov29 : end - start_ov29]
                    main_func[start] = AsmFunction(func_data, start)
                    ext_data = main_func[start].process()[1]
                    if i >= len(unique_main_calls) - 3:
                        new_baddr = (
                            end_m_functions - len(func_data) - start_m_functions - 0x8
                        ) // 0x4
                        if new_baddr < 0:
                            new_baddr += 2 * 0x800000
                        main_func[start].add_instructions(
                            bytes(
                                [
                                    new_baddr % 256,
                                    (new_baddr // 256) % 256,
                                    (new_baddr // 65536) % 256,
                                    0xEA,
                                ]
                            )
                        )
                    lst_data = {}
                    for offset in ext_data:
                        code = 0
                        for x in range(4):
                            code += data[offset - start_ov29 + x] * (256**x)
                        lst_data[offset] = code
                        data_processed.add(offset)
                    main_func[start].provide_data(lst_data)

            nb_items = len(main_calls)
            header = bytearray(4 + 2 * nb_items + len(main_func) * 8)
            write_u32(header, u32_checked(4 + 2 * nb_items), 0)
            code_data = bytearray(0)
            current_ptr = len(header)
            id_codes = dict()
            for i, t in enumerate(main_func.items()):
                k = t[0]
                xfn = t[1]
                id_codes[k] = i
                fdata = bytearray(xfn.compile(start_m_functions))
                write_u32(header, u32_checked(current_ptr), 4 + 2 * nb_items + i * 8)
                write_u32(header, u32_checked(len(fdata)), 4 + 2 * nb_items + i * 8 + 4)
                code_data += fdata

                current_ptr += len(fdata)
            for i, xy in enumerate(main_calls):
                write_u16(header, u16(id_codes[xy]), 4 + 2 * i)
            file_data = header + code_data
            if ITEM_CODE_PATH not in rom.filenames:
                create_file_in_rom(rom, ITEM_CODE_PATH, file_data)
            else:
                rom.setFileByName(ITEM_CODE_PATH, file_data)
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
