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
)  # i have no clue what this does but every other patch i looked at had it (i looked at 2 patches)

from typing import Callable

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import read_u32, get_binary_from_rom
from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import (
    Pmd2Data,
    GAME_VERSION_EOS,
    GAME_REGION_US,
    GAME_REGION_EU,
    GAME_REGION_JP,
)
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch

ORIGINAL_INSTRUCTION = 0xE5D00007
OFFSET_EU = 0x2305E64 - 0x22DCB80
OFFSET_US = 0x2305438 - 0x22DC240
OFFSET_JP = 0x2306988 - 0x22DD8E0


class PartyUpdatesMapPatchHandler(AbstractPatchHandler, DependantPatch):
    @property
    def name(self) -> str:
        return "PartyUpdatesMap"

    @property
    def description(self) -> str:
        return "Causes all party members to update the dungeon minimap, as they do in Super."

    @property
    def author(self) -> str:
        return "Chesyon"

    @property
    def version(self) -> str:
        return "0.1.0"

    def depends_on(self) -> list[str]:
        return ["ExtraSpace"]

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.IMPROVEMENT_TWEAK

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        overlay29 = get_binary_from_rom(rom, config.bin_sections.overlay29)
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_u32(overlay29, OFFSET_US) != ORIGINAL_INSTRUCTION
            if config.game_region == GAME_REGION_EU:
                return read_u32(overlay29, OFFSET_EU) != ORIGINAL_INSTRUCTION
            if config.game_region == GAME_REGION_JP:
                return read_u32(overlay29, OFFSET_JP) != ORIGINAL_INSTRUCTION
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data) -> None:
        # Apply the patch
        apply()

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
