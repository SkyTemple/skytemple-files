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

from ndspy.code import loadOverlayTable
from ndspy.rom import NintendoDSRom

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_JP,
    GAME_REGION_US,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.util import read_u32
from skytemple_files.patch.asm_tools import AsmFunction
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler

START_OV11_US = 0x022DC240
START_TABLE_US = 0x022F5D50
LST_FUNC_US = [0x022F6E18, 0x022F6E20, 0x022F6E28, 0x022F6E44]

START_OV11_EU = 0x022DCB80
START_TABLE_EU = 0x022F66F0
LST_FUNC_EU = [0x022F77B8, 0x022F77C0, 0x022F77C8, 0x022F77E4]

START_OV11_JP = 0x022DD8E0
START_TABLE_JP = 0x022F73D4
LST_FUNC_JP = [0x022F849C, 0x022F84A4, 0x022F84AC, 0x022F84C8]

PATCH_CHECK_ADDR_APPLIED_US = 0x19B10
PATCH_CHECK_ADDR_APPLIED_EU = 0x19B70
PATCH_CHECK_ADDR_APPLIED_JP = 0x19AF4
PATCH_CHECK_INSTR_APPLIED = 0xE59F2F9C


class PkmnGroundAnimPatchHandler(AbstractPatchHandler):
    @property
    def name(self) -> str:
        return "ChangePokemonGroundAnim"

    @property
    def description(self) -> str:
        return _("Changes implementation of idle animation to an editable table.")

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
                        rom.loadArm9Overlays([11])[11].data, PATCH_CHECK_ADDR_APPLIED_US
                    )
                    != PATCH_CHECK_INSTR_APPLIED
                )
            if config.game_region == GAME_REGION_EU:
                return (
                    read_u32(
                        rom.loadArm9Overlays([11])[11].data, PATCH_CHECK_ADDR_APPLIED_EU
                    )
                    != PATCH_CHECK_INSTR_APPLIED
                )
            if config.game_region == GAME_REGION_JP:
                return (
                    read_u32(
                        rom.loadArm9Overlays([11])[11].data, PATCH_CHECK_ADDR_APPLIED_JP
                    )
                    != PATCH_CHECK_INSTR_APPLIED
                )
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        if not self.is_applied(rom, config):
            if config.game_version == GAME_VERSION_EOS:
                if config.game_region == GAME_REGION_US:
                    start_ov11 = START_OV11_US
                    start_table = START_TABLE_US
                    lst_func = LST_FUNC_US
                if config.game_region == GAME_REGION_EU:
                    start_ov11 = START_OV11_EU
                    start_table = START_TABLE_EU
                    lst_func = LST_FUNC_EU
                if config.game_region == GAME_REGION_JP:
                    start_ov11 = START_OV11_JP
                    start_table = START_TABLE_JP
                    lst_func = LST_FUNC_JP

            table = loadOverlayTable(rom.arm9OverlayTable, lambda x, y: bytes())
            ov = table[11]
            ov11 = bytearray(rom.files[ov.fileID])

            switch = AsmFunction(
                ov11[start_table - start_ov11 : lst_func[0] - start_ov11], start_table
            )
            ext_data = switch.process()[1]
            lst_data = {}
            data_processed = set()
            for offset in ext_data:
                code = 0
                for x in range(4):
                    code += ov11[offset - start_ov11 + x] * (256**x)
                lst_data[offset] = code
                data_processed.add(offset)
            switch.provide_data(lst_data)
            main_calls = switch.process_switch(0, (0, 2048), {})
            lst_calls = []
            for x in main_calls:
                lst_calls.append(lst_func.index(x))
            ov11[
                start_table - start_ov11 + 4 : start_table - start_ov11 + 2052
            ] = bytes(lst_calls)
            rom.files[ov.fileID] = bytes(ov11)

        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
