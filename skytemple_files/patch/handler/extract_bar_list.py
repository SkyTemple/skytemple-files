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
from range_typed_integers import u16_checked, u32

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_JP,
    GAME_REGION_US,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.util import (
    create_file_in_rom,
    write_u32,
    read_u16,
    write_u16,
    read_u32,
)
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler

PATCH_CHECK_ADDR_APPLIED_US = 0x0
PATCH_CHECK_ADDR_APPLIED_EU = 0x0
PATCH_CHECK_ADDR_APPLIED_JP = 0x0
PATCH_CHECK_INSTR_APPLIED = 0xE92D4008

BAR_LIST_US = 0x3A8C
BAR_LIST_EU = 0x3A80
BAR_LIST_JP = 0x3A84

BAR_LIST_ENTRY_SIZE = 0x16
BAR_LIST_SIZE = 0x5AC

NB_ITEMS = 1400

ITEM_LIST_PATH = "BALANCE/itembar.bin"


class ExtractBarItemListPatchHandler(AbstractPatchHandler):
    @property
    def name(self) -> str:
        return "ExtractBarItemList"

    @property
    def description(self) -> str:
        return _("Extracts Spinda bar's item list.")

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
                        rom.loadArm9Overlays([19])[19].data, PATCH_CHECK_ADDR_APPLIED_US
                    )
                    != PATCH_CHECK_INSTR_APPLIED
                )
            if config.game_region == GAME_REGION_EU:
                return (
                    read_u32(
                        rom.loadArm9Overlays([19])[19].data, PATCH_CHECK_ADDR_APPLIED_EU
                    )
                    != PATCH_CHECK_INSTR_APPLIED
                )
            if config.game_region == GAME_REGION_JP:
                return (
                    read_u32(
                        rom.loadArm9Overlays([19])[19].data, PATCH_CHECK_ADDR_APPLIED_JP
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
                    bar_list = BAR_LIST_US
                if config.game_region == GAME_REGION_EU:
                    bar_list = BAR_LIST_EU
                if config.game_region == GAME_REGION_JP:
                    bar_list = BAR_LIST_JP

            data = rom.loadArm9Overlays([19])[19].data

            header = bytearray([0xFF] * (4 + 2 * NB_ITEMS))
            write_u32(header, u32(4 + 2 * NB_ITEMS), 0)
            list_data: list[bytes] = []
            for x in range(bar_list, bar_list + BAR_LIST_SIZE, BAR_LIST_ENTRY_SIZE):
                item_id = read_u16(data, x)
                cdata = bytes(data[x + 2 : x + BAR_LIST_ENTRY_SIZE])
                if cdata in list_data:
                    index = list_data.index(cdata)
                else:
                    index = len(list_data)
                    list_data.append(cdata)
                write_u16(header, u16_checked(index), 4 + 2 * item_id)
            file_data = header + b"".join(list_data)
            if ITEM_LIST_PATH not in rom.filenames:
                create_file_in_rom(rom, ITEM_LIST_PATH, file_data)
            else:
                rom.setFileByName(ITEM_LIST_PATH, file_data)
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
