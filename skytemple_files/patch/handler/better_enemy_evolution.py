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

from typing import Callable, List

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import get_binary_from_rom, read_u32
from skytemple_files.common.ppmdu_config.data import (
    Pmd2Data,
    GAME_VERSION_EOS,
    GAME_REGION_US,
    GAME_REGION_EU,
)
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch

ORIGINAL_INSTRUCTION = 0xEB0004C5
OFFSET_EU = 0x2680C
OFFSET_US = 0x26720


class BetterEnemyEvolutionPatchHandler(AbstractPatchHandler, DependantPatch):
    @property
    def name(self) -> str:
        return "BetterEnemyEvolution"

    @property
    def description(self) -> str:
        return "Allows changing how enemy evolution works. In particular, it allows you to choose if the evolved enemy will get the stats and/or moves from its new species, add extra stats after evolving, heal the enemy after evolving or choosing if the evolution will take place even if the target is revived."

    @property
    def author(self) -> str:
        return "End45"

    @property
    def version(self) -> str:
        return "0.1.0"

    def depends_on(self) -> List[str]:
        return ["ExtraSpace"]

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.NEW_MECHANIC

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        overlay29 = get_binary_from_rom(rom, config.bin_sections.overlay29)
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_u32(overlay29, OFFSET_US) != ORIGINAL_INSTRUCTION
            if config.game_region == GAME_REGION_EU:
                return read_u32(overlay29, OFFSET_EU) != ORIGINAL_INSTRUCTION
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        # Apply the patch
        apply()

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ):
        raise NotImplementedError()
