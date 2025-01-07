#  Copyright 2020-2025 Capypara and the SkyTemple Contributors
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
from __future__ import (
    annotations,
)
from typing import Callable

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import read_u32, get_binary_from_rom
from skytemple_files.common.ppmdu_config.data import (
    Pmd2Data,
    GAME_VERSION_EOS,
    GAME_REGION_US,
    GAME_REGION_EU,
    GAME_REGION_JP,
)
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch
from skytemple_files.common.i18n_util import f, _

MODIFIED_INSTRUCTION = 0xE8BD83F8  # ldmia all the shit
OFFSET_EU = (
    0x231F358 - 1084 - 0x22DCB80
)  # location of the next function minus the number of saved bytes minus 4 minus starting point of overlay 29
OFFSET_US = 0x231E8F0 - 1084 - 0x22DC240  # same but US HeHeHaHa


class AiItemOptimizationsHandler(AbstractPatchHandler, DependantPatch):
    @property
    def name(self) -> str:
        return "AiItemOptimizations"

    @property
    def description(self) -> str:
        return _(
            "Reduces the size of GetAiUseItemProbability without changing anything else, creating 1080 bytes of free space in overlay29."
        )

    @property
    def author(self) -> str:
        return "happylappy"

    @property
    def version(self) -> str:
        return "1.0.0"

    def depends_on(self) -> list[str]:
        return []

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.UTILITY

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        patch_area = get_binary_from_rom(rom, config.bin_sections.overlay29)
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_u32(patch_area, OFFSET_US) == MODIFIED_INSTRUCTION
            if config.game_region == GAME_REGION_EU:
                return read_u32(patch_area, OFFSET_EU) == MODIFIED_INSTRUCTION
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data) -> None:
        # Apply the patch
        apply()

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
