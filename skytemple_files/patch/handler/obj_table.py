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
    read_u8,
    read_u32,
    write_u8,
)
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler

START_OV11_US = 0x022DC240
START_TABLE_US = 0x0231EE54
TABLE_ENTRIES_US = 555

START_OV11_EU = 0x022DCB80
START_TABLE_EU = 0x0231F8DC
TABLE_ENTRIES_EU = 569

START_OV11_JP = 0x022DD8E0
START_TABLE_JP = 0
TABLE_ENTRIES_JP = 0

PATCH_CHECK_ADDR_APPLIED_US = 0x1FEC8
PATCH_CHECK_ADDR_APPLIED_EU = 0x1FF28
PATCH_CHECK_INSTR_APPLIED = 0xE5D50008

OBJECT_TABLE_PATH = "BALANCE/objects.bin"


class ExtractObjectTablePatchHandler(AbstractPatchHandler):
    @property
    def name(self) -> str:
        return "ExtractObjectTable"

    @property
    def description(self) -> str:
        return _("Extracts the object table to a separate file in the ROM.")

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
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        if not self.is_applied(rom, config):
            if OBJECT_TABLE_PATH not in rom.filenames:
                if config.game_version == GAME_VERSION_EOS:
                    if config.game_region == GAME_REGION_US:
                        start_ov11 = START_OV11_US
                        start_table = START_TABLE_US
                        table_entries = TABLE_ENTRIES_US
                    if config.game_region == GAME_REGION_EU:
                        start_ov11 = START_OV11_EU
                        start_table = START_TABLE_EU
                        table_entries = TABLE_ENTRIES_EU
                    if config.game_region == GAME_REGION_JP:
                        start_ov11 = START_OV11_JP
                        start_table = START_TABLE_JP
                        table_entries = TABLE_ENTRIES_JP

                data = rom.loadArm9Overlays([11])[11].data

                table = []

                for i in range(table_entries):
                    offset = start_table - start_ov11 + i * 0xC
                    array = bytearray(0x10)
                    attr = read_u32(data, offset)
                    write_u32(array, attr, 0)
                    attr2 = read_u8(data, offset + 8)
                    write_u8(array, attr2, 4)
                    addr: int = read_u32(data, offset + 4)
                    if addr != 0:
                        addr -= start_ov11
                        count = 0
                        while data[addr + count] != 0:
                            if count >= 10:
                                raise ValueError(
                                    "Invalid string length (more than 10 characters)"
                                )
                            array[5 + count] = data[addr + count]
                            count += 1
                    if sum(array) == 0:
                        print("Found blank entry, stopping at", i)
                        break
                    table.append(array)
                file_data = b"".join(table)
                create_file_in_rom(rom, OBJECT_TABLE_PATH, file_data)
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
