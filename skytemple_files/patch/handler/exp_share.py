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
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch
from skytemple_files.common.util import _

PATCH_CODE_START_US = 0x97DDC
PATCH_CODE_END_US = 0x97EB8
PATCH_CHECK_ADDR_APPLIED_US = 0x5A588
PATCH_CHECK_INSTR_APPLIED_US = 0xE0410000

PATCH_CODE_START_EU = 0x981D8
PATCH_CODE_END_EU = 0x982B4
PATCH_CHECK_ADDR_APPLIED_EU = 0x5A904
PATCH_CHECK_INSTR_APPLIED_EU = 0xE0410000


class ExpSharePatchHandler(AbstractPatchHandler, DependantPatch):

    @property
    def name(self) -> str:
        return 'AddExperienceShare'

    @property
    def description(self) -> str:
        return _('Implements shared experience points between all members (GtI style). \n'
                 'This is disabled during Special Episodes and dungeons with level 1 or no exp. restrictions. \n'
                 'Needs the ExtractDungeonData patch to be applied to free some space used by this.')

    @property
    def author(self) -> str:
        return 'irdkwia'

    @property
    def version(self) -> str:
        return '0.0.2'

    def depends_on(self) -> List[str]:
        return ['ExtractDungeonData']

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.NEW_MECHANIC

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_uintle(rom.arm9, PATCH_CHECK_ADDR_APPLIED_US, 4) != PATCH_CHECK_INSTR_APPLIED_US
            if config.game_region == GAME_REGION_EU:
                return read_uintle(rom.arm9, PATCH_CHECK_ADDR_APPLIED_EU, 4) != PATCH_CHECK_INSTR_APPLIED_EU
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
