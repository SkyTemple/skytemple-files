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
from typing import Callable

from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data, GAME_VERSION_EOS, GAME_REGION_US, GAME_REGION_EU
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler
from skytemple_files.hardcoded.dungeons import HardcodedDungeons
from skytemple_files.common.util import _
PATCH_CHECK_ADDR_APPLIED_US = 0x4F7F8
PATCH_CHECK_INSTR_APPLIED_US = 0x359F1010
PATCH_CHECK_ADDR_APPLIED_EU = 0x4FB30
PATCH_CHECK_INSTR_APPLIED_EU = 0x359F1010

FLOOR_FORBID_TABLE_US = 0x9F714
ITEM_AVAILABLE_TABLE_US = 0x94D34
FLOOR_RANKS_TABLE_US = 0xA0AD4
FLOOR_FORBID_TABLE_EU = 0x9FC98
ITEM_AVAILABLE_TABLE_EU = 0x95130
FLOOR_RANKS_TABLE_EU = 0xA1058
NB_ITEMS_TABLE = 100
AVAILABLE_ITEMS_NB = 1024
ARM9_START = 0x02000000

FLOOR_FORBID_PATH = "BALANCE/fforbid.bin"
FLOOR_RANKS_PATH = "BALANCE/f_ranks.bin"
AVAILABLE_ITEMS_PATH = "BALANCE/a_items.bin"
# TODO: move this somewhere else
FLOORS_NB = [3, 5, 6, 10, 8, 12, 9, 5, 14, 5, 11, 5, 16, 20, 15, 21, 11, 14, 8, 15, 15, 8, 12, 20, 15, 24, 24, 14, 25, 25, 20, 18, 50, 20, 23, 30, 18, 30, 20, 8, 13, 20, 10, 15, 20, 20, 30, 6, 5, 10, 5, 50, 20, 99, 30, 19, 19, 17, 25, 75, 40, 40, 99, 1, 50, 99, 10, 5, 15, 20, 25, 30, 40, 17, 7, 10, 15, 11, 16, 20, 8, 10, 15, 10, 18, 10, 11, 5, 5, 11, 19, 16, 5, 6, 7, 6, 5, 5, 5, 5]

class ExtractDungeonDataPatchHandler(AbstractPatchHandler):

    @property
    def name(self) -> str:
        return 'ExtractDungeonData'

    @property
    def description(self) -> str:
        return _('Extracts the floor ranks, forbidden mission floors, items available in dungeon tables and put them in files. Provides support for reading them from the rom file system.')

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
                return read_uintle(rom.arm9, PATCH_CHECK_ADDR_APPLIED_US, 4)!=PATCH_CHECK_INSTR_APPLIED_US
            if config.game_region == GAME_REGION_EU:
                return read_uintle(rom.arm9, PATCH_CHECK_ADDR_APPLIED_EU, 4)!=PATCH_CHECK_INSTR_APPLIED_EU
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        if not self.is_applied(rom, config):
            if config.game_version == GAME_VERSION_EOS:
                if config.game_region == GAME_REGION_US:
                    rank_table = FLOOR_RANKS_TABLE_US
                    item_table = ITEM_AVAILABLE_TABLE_US
                    forbid_table = FLOOR_FORBID_TABLE_US
                if config.game_region == GAME_REGION_EU:
                    rank_table = FLOOR_RANKS_TABLE_EU
                    item_table = ITEM_AVAILABLE_TABLE_EU
                    forbid_table = FLOOR_FORBID_TABLE_EU

            header = bytearray(NB_ITEMS_TABLE*4)
            rank_data = bytearray(0)
            forbid_data = bytearray(0)
            current_ptr = len(header)
            for i in range(NB_ITEMS_TABLE):
                start = read_uintle(rom.arm9, rank_table+i*4, 4)-ARM9_START
                end = start+1+FLOORS_NB[i]
                if end%4!=0:
                    end += 4-(end%4)
                rdata = rom.arm9[start:end]
                fdata = bytearray(len(rdata))
                x = forbid_table
                while rom.arm9[x]!=0x64:
                    if rom.arm9[x]==i:
                        fdata[rom.arm9[x+1]] = 1
                    x += 2
                rom.arm9 = rom.arm9[:start]+bytes([0xCC]*(end-start))+rom.arm9[end:]
                write_uintle(header, current_ptr, i*4, 4)
                rank_data += bytearray(rdata)
                forbid_data += bytearray(fdata)
                
                current_ptr += end-start
            file_data = header + rank_data
            if FLOOR_RANKS_PATH not in rom.filenames:
                create_file_in_rom(rom, FLOOR_RANKS_PATH, file_data)
            else:
                rom.setFileByName(FLOOR_RANKS_PATH, file_data)
            file_data = header + forbid_data
            if FLOOR_FORBID_PATH not in rom.filenames:
                create_file_in_rom(rom, FLOOR_FORBID_PATH, file_data)
            else:
                rom.setFileByName(FLOOR_FORBID_PATH, file_data)

            dungeon_list = HardcodedDungeons.get_dungeon_list(rom.arm9, config)
            groups = [d.mappa_index for d in dungeon_list]
            print(hex(len(groups)))
            list_available = []
            for x in range(AVAILABLE_ITEMS_NB):
                list_available.append(bytearray(0x100//8))
                for i, g in enumerate(groups):
                    off = item_table + g * (AVAILABLE_ITEMS_NB//8) + (x//8)
                    if rom.arm9[off]&(1<<(x%8)):
                        list_available[-1][i//8] |= 1<<(i%8)
            file_data = bytearray().join(list_available)
            if AVAILABLE_ITEMS_PATH not in rom.filenames:
                create_file_in_rom(rom, AVAILABLE_ITEMS_PATH, file_data)
            else:
                rom.setFileByName(AVAILABLE_ITEMS_PATH, file_data)
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
