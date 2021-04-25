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
from skytemple_files.common.i18n_util import f, _

NUM_PREVIOUS_ENTRIES = 600


PATCH_CODE_START_US = 0xA48F8
PATCH_CODE_END_US = 0x0A4ED8
PATCH_CHECK_ADDR_APPLIED_US = 0x1F6B0
PATCH_CHECK_INSTR_APPLIED_US = 0xEA0000D4
PATCH_CODE_START_EU = 0xA4EF8
PATCH_CODE_END_EU = 0xA54D8
PATCH_CHECK_ADDR_APPLIED_EU = 0x1F74C
PATCH_CHECK_INSTR_APPLIED_EU = 0xEA0000D4


class AtupxSupportPatchHandler(AbstractPatchHandler, DependantPatch):

    @property
    def name(self) -> str:
        return 'ProvideATUPXSupport'

    @property
    def description(self) -> str:
        return _('Provide support for ATUPX containers, which use a different algorithm than PX compression.\nRequires the ActorAndLevelLoader, as it frees the space needed to implement this.')

    @property
    def author(self) -> str:
        return 'irdkwia'

    @property
    def version(self) -> str:
        return '0.0.1'

    def depends_on(self) -> List[str]:
        return ['ActorAndLevelLoader']

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.UTILITY

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
