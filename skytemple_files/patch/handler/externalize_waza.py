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
from skytemple_files.common.ppmdu_config.data import Pmd2Data, GAME_VERSION_EOS, GAME_REGION_US, GAME_REGION_EU, GAME_REGION_JP
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch
from skytemple_files.common.i18n_util import _, get_locales
from skytemple_files.data.str.handler import StrHandler

PATCH_CHECK_ADDR_APPLIED_US = 0x13414
PATCH_CHECK_ADDR_APPLIED_EU = 0x134BC
PATCH_CHECK_ADDR_APPLIED_JP = 0x133E4
PATCH_CHECK_INSTR_APPLIED = 0xE92D4010

class ExternalizeWazaPatchHandler(AbstractPatchHandler, DependantPatch):

    @property
    def name(self) -> str:
        return 'ExternalizeWazaFile'

    @property
    def description(self) -> str:
        return _("""Use filestreams to access waza_p/waza_p2 data instead of loading them entirely.
This patch is useless on its own.
Depends on the ActorAndLevelLoader patch, as it needs some space provided by this one.""")

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
                return read_uintle(rom.arm9, PATCH_CHECK_ADDR_APPLIED_US, 4)!=PATCH_CHECK_INSTR_APPLIED
            if config.game_region == GAME_REGION_EU:
                return read_uintle(rom.arm9, PATCH_CHECK_ADDR_APPLIED_EU, 4)!=PATCH_CHECK_INSTR_APPLIED
            if config.game_region == GAME_REGION_JP:
                return read_uintle(rom.arm9, PATCH_CHECK_ADDR_APPLIED_JP, 4)!=PATCH_CHECK_INSTR_APPLIED
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    
    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
