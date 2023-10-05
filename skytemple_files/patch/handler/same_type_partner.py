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

from typing import Callable

from ndspy.rom import NintendoDSRom

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_US,
    GAME_REGION_JP,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.util import get_binary_from_rom
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler

ORIGINAL_BYTESEQ = b"\x07\x00\x00\x1a"
OFFSET_US = 0x180C
OFFSET_EU = 0x180C
OFFSET_JP = 0x1810


class SameTypePartnerPatch(AbstractPatchHandler):
    @property
    def name(self) -> str:
        return "SameTypePartner"

    @property
    def description(self) -> str:
        return _(
            "Allows the partner to be of the same type as the player in the personality test."
        )

    @property
    def author(self) -> str:
        return "End45"

    @property
    def version(self) -> str:
        return "0.1.0"

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.IMPROVEMENT_TWEAK

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        overlay13 = get_binary_from_rom(rom, config.bin_sections.overlay13)
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return overlay13[OFFSET_US : OFFSET_US + 4] != ORIGINAL_BYTESEQ
            if config.game_region == GAME_REGION_EU:
                return overlay13[OFFSET_EU : OFFSET_EU + 4] != ORIGINAL_BYTESEQ
            if config.game_region == GAME_REGION_JP:
                return overlay13[OFFSET_JP : OFFSET_JP + 4] != ORIGINAL_BYTESEQ
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        # Apply the patch
        apply()

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
