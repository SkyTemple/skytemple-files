#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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
from range_typed_integers import u32_checked, u16_checked

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_US,
    GAME_REGION_JP,
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

PATCH_CHECK_ADDR_APPLIED_US = 0x53664
PATCH_CHECK_INSTR_APPLIED_US = 0xE3A01001
PATCH_CHECK_ADDR_APPLIED_EU = 0x53764
PATCH_CHECK_INSTR_APPLIED_EU = 0xE3A01001
PATCH_CHECK_ADDR_APPLIED_JP = 0x533B8
PATCH_CHECK_INSTR_APPLIED_JP = 0xE3A01001

START_OV29_US = 0x022DC240
START_TABLE_US = 0x0232F8AC
START_M_FUNC_US = 0x02330134
END_M_FUNC_US = 0x023326CC
START_METRONOME_DATA_US = 0x935C

START_OV29_EU = 0x022DCB80
START_TABLE_EU = 0x023302EC
START_M_FUNC_EU = 0x02330B74
END_M_FUNC_EU = 0x0233310C
START_METRONOME_DATA_EU = 0x9374

START_OV29_JP = 0x022DD8E0
START_TABLE_JP = 0x02330CA0
START_M_FUNC_JP = 0x02331528
END_M_FUNC_JP = 0x02333AC0
START_METRONOME_DATA_JP = 0x92A4

METRONOME_DATA_LENGTH = 0x540

MOVE_CODE_PATH = "BALANCE/waza_cd.bin"
METRONOME_DATA_PATH = "BALANCE/metrono.bin"


class ExtractMoveCodePatchHandler(AbstractPatchHandler):
    @property
    def name(self) -> str:
        return "ExtractMoveCode"

    @property
    def description(self) -> str:
        return _("Extracts move effects code and put it in files.")

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
                    read_u32(rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_US)
                    != PATCH_CHECK_INSTR_APPLIED_US
                )
            if config.game_region == GAME_REGION_EU:
                return (
                    read_u32(rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_EU)
                    != PATCH_CHECK_INSTR_APPLIED_EU
                )
            if config.game_region == GAME_REGION_JP:
                return (
                    read_u32(rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_JP)
                    != PATCH_CHECK_INSTR_APPLIED_JP
                )
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data) -> None:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                start_ov29 = START_OV29_US
                start_table = START_TABLE_US
                start_m_functions = START_M_FUNC_US
                end_m_functions = END_M_FUNC_US
                start_metronome_data = START_METRONOME_DATA_US
            if config.game_region == GAME_REGION_EU:
                start_ov29 = START_OV29_EU
                start_table = START_TABLE_EU
                start_m_functions = START_M_FUNC_EU
                end_m_functions = END_M_FUNC_EU
                start_metronome_data = START_METRONOME_DATA_EU
            if config.game_region == GAME_REGION_JP:
                start_ov29 = START_OV29_JP
                start_table = START_TABLE_JP
                start_m_functions = START_M_FUNC_JP
                end_m_functions = END_M_FUNC_JP
                start_metronome_data = START_METRONOME_DATA_JP

        if MOVE_CODE_PATH not in rom.filenames:
            main_func = dict()

            data = rom.loadArm9Overlays([29])[29].data

            switch = AsmFunction(
                data[start_table - start_ov29 : start_m_functions - start_ov29],
                start_table,
            )
            switch.process()
            main_calls = switch.process_switch(6, (0, 559), {0: 542})

            unique_main_calls = list(sorted(set(main_calls)))
            unique_main_calls.append(end_m_functions)

            last_call = None
            for i in range(len(unique_main_calls) - 1):
                start = unique_main_calls[i]
                end = unique_main_calls[i + 1]
                func_data = data[start - start_ov29 : end - start_ov29]
                main_func[start] = AsmFunction(func_data, start)
                main_func[start].process()
                last_call = start

            nb_moves = len(main_calls)
            header = bytearray(4 + 2 * nb_moves + len(main_func) * 8)
            write_u32(header, u32_checked(4 + 2 * nb_moves), 0)
            code_data = bytearray(0)
            current_ptr = len(header)
            id_codes = dict()
            for i, t in enumerate(main_func.items()):
                k = t[0]
                x = t[1]
                id_codes[k] = i
                fdata = bytearray(x.compile(start_m_functions))
                if k == last_call:
                    # Add a branch to the end for the last case since it doesn't have one
                    fdata += bytearray([0x63, 0x09, 0x00, 0xEA])
                write_u32(header, u32_checked(current_ptr), 4 + 2 * nb_moves + i * 8)
                write_u32(header, u32_checked(len(fdata)), 4 + 2 * nb_moves + i * 8 + 4)
                code_data += fdata

                current_ptr += len(fdata)
            for i, y in enumerate(main_calls):
                write_u16(header, u16_checked(id_codes[y]), 4 + 2 * i)
            file_data = header + code_data
            create_file_in_rom(rom, MOVE_CODE_PATH, file_data)

        if METRONOME_DATA_PATH not in rom.filenames:
            # Metronome
            data = rom.loadArm9Overlays([10])[10].data
            file_data = bytearray(METRONOME_DATA_LENGTH // 2)
            for z in range(start_metronome_data, start_metronome_data + METRONOME_DATA_LENGTH, 8):
                write_u32(file_data, read_u32(data, z), (z - start_metronome_data) // 2)
            create_file_in_rom(rom, METRONOME_DATA_PATH, file_data)
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data) -> None:
        raise NotImplementedError()
