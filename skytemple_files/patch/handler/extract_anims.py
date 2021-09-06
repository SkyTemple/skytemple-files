#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch
from skytemple_files.common.i18n_util import _

PATCH_CHECK_ADDR_APPLIED_US = 0x3420
PATCH_CHECK_ADDR_APPLIED_EU = 0x3420
PATCH_CHECK_INSTR_APPLIED = 0xE59F2008

START_TABLE_US = 0xAFD0
START_TABLE_EU = 0xAFE8

ANIM_PATH = "BALANCE/anim.bin"


class ExtractAnimDataPatchHandler(AbstractPatchHandler, DependantPatch):

    @property
    def name(self) -> str:
        return 'ExtractAnimData'

    @property
    def description(self) -> str:
        return _('Extracts animation data and put it in files. \nNeeds ActorAndLevelLoader patch to free some space. ')

    @property
    def author(self) -> str:
        return 'irdkwia'

    @property
    def version(self) -> str:
        return '0.0.1'

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.UTILITY
    
    def depends_on(self) -> List[str]:
        return ['ActorAndLevelLoader']
    
    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_uintle(rom.loadArm9Overlays([10])[10].data, PATCH_CHECK_ADDR_APPLIED_US, 4)!=PATCH_CHECK_INSTR_APPLIED
            if config.game_region == GAME_REGION_EU:
                return read_uintle(rom.loadArm9Overlays([10])[10].data, PATCH_CHECK_ADDR_APPLIED_EU, 4)!=PATCH_CHECK_INSTR_APPLIED
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        if not self.is_applied(rom, config):
            if config.game_version == GAME_VERSION_EOS:
                if config.game_region == GAME_REGION_US:
                    start_table = START_TABLE_US
                if config.game_region == GAME_REGION_EU:
                    start_table = START_TABLE_EU
        if ANIM_PATH not in rom.filenames:

            data = rom.loadArm9Overlays([10])[10].data

            header = bytearray(5*4)
            write_uintle(header, 5*4, 0, 4)
            write_uintle(header, 5*4+52, 4, 4)
            write_uintle(header, 5*4+52+5600, 8, 4)
            write_uintle(header, 5*4+52+5600+13512, 12, 4)
            write_uintle(header, 5*4+52+5600+13512+19600, 16, 4)
            file_data = bytes(header) + bytes(data[start_table:start_table+0x14560])
            create_file_in_rom(rom, ANIM_PATH, file_data)
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    
    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
