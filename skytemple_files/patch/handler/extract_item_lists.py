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

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data, GAME_VERSION_EOS, GAME_REGION_US, GAME_REGION_EU
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler
from skytemple_files.common.i18n_util import f, _

PATCH_CHECK_ADDR_APPLIED_US = 0xE1E0
PATCH_CHECK_INSTR_APPLIED_US = 0xE1A00008
PATCH_CHECK_ADDR_APPLIED_EU = 0xE268
PATCH_CHECK_INSTR_APPLIED_EU = 0xE1A00008

ITEM_LISTS_TABLE_US = 0xB0948
ITEM_LISTS_TABLE_EU = 0xB1264
ITEM_LISTS_SIZE = 0x2F8
ITEM_LISTS_NB = 26
LIST_PATH = "TABLEDAT/list_%02d.bin"
ARM9_START = 0x02000000

class ExtractItemListsPatchHandler(AbstractPatchHandler):

    @property
    def name(self) -> str:
        return 'ExtractHardcodedItemLists'

    @property
    def description(self) -> str:
        return _('Extracts the hardcoded item lists, used for mission rewards/treasure boxes content as well as Kecleon shop items, and put them in files. Provides support for reading them from the rom file system.')

    @property
    def author(self) -> str:
        return 'irdkwia'

    @property
    def version(self) -> str:
        return '0.0.2'

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
            path_len = len(LIST_PATH%0)+1
            if path_len%4!=0:
                path_len += 4-(path_len%4)
            if config.game_version == GAME_VERSION_EOS:
                if config.game_region == GAME_REGION_US:
                    table = ITEM_LISTS_TABLE_US
                if config.game_region == GAME_REGION_EU:
                    table = ITEM_LISTS_TABLE_EU

            ranges = []
            for i in range(ITEM_LISTS_NB):
                start = read_uintle(rom.arm9, table+i*4, 4)-ARM9_START
                end = start
                size = 0
                while size<ITEM_LISTS_SIZE:
                    val = read_uintle(rom.arm9, end, 2)
                    if val>=30000:
                        size += (val-30000)*2
                    else:
                        size += 2
                    end += 2
                data = rom.arm9[start:end]
                if end%4!=0:
                    end += 4-(end%4)
                path = LIST_PATH%i
                if path not in rom.filenames:
                    create_file_in_rom(rom, path, data)
                else:
                    rom.setFileByName(path, data)
                rom.arm9 = rom.arm9[:start]+bytes([0xCC]*(end-start))+rom.arm9[end:]
                ranges.append([start, end])
            ranges.sort()
            i = 0
            while i<len(ranges)-1:
                if ranges[i][1]==ranges[i+1][0]:
                    ranges[i][1] = ranges[i+1][1]
                    del ranges[i+1]
                    i-=1
                i+=1
            buffer = bytearray(4*ITEM_LISTS_NB)
            for i in range(ITEM_LISTS_NB):
                path = LIST_PATH%i
                while ranges[0][1]-ranges[0][0]<path_len:
                    del ranges[0]
                    if len(ranges)==0:
                        raise RuntimeError(_("Don't have enough space to put filenames! "))
                
                rom.arm9 = rom.arm9[:ranges[0][0]]+path.encode(encoding="ascii")+bytes(path_len-len(path))+rom.arm9[ranges[0][0]+path_len:]
                write_uintle(buffer, ARM9_START+ranges[0][0], i*4, 4)
                ranges[0][0] += path_len
            rom.arm9 = rom.arm9[:table]+buffer+rom.arm9[table+len(buffer):]
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
