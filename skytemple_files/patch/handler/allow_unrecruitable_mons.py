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

ORIGINAL_INSTRUCTION = 0xE59F1060
OFFSET_EU = 0x31A58
OFFSET_US = 0x31924


class AllowUnrecruitableMonsPatchHandler(AbstractPatchHandler):

    @property
    def name(self) -> str:
        return 'AllowUnrecruitableMons'

    @property
    def description(self) -> str:
        return _("Allows recruiting the other Deoxys forms and the regis inside dungeons.")

    @property
    def author(self) -> str:
        return 'End45'

    @property
    def version(self) -> str:
        return '0.1.0'

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.IMPROVEMENT_TWEAK

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_uintle(rom.loadArm9Overlays([29])[29].data, OFFSET_US, 4) != ORIGINAL_INSTRUCTION
            if config.game_region == GAME_REGION_EU:
                return read_uintle(rom.loadArm9Overlays([29])[29].data, OFFSET_EU, 4) != ORIGINAL_INSTRUCTION
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        # Apply the patch
        apply()

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
