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
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.util import get_binary_from_rom, set_binary_in_rom, read_u32
from skytemple_files.hardcoded.iq import IqGroupsSkills
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler

ORIGINAL_INSTRUCTION = 0xE92D4010
OFFSET_EU = 0x591E4
OFFSET_US = 0x58E68


class CompressIQDataPatchHandler(AbstractPatchHandler):
    @property
    def name(self) -> str:
        return "CompressIQData"

    @property
    def description(self) -> str:
        return _(
            "Optimizes the way the list of IQ skills learnt by each IQ group is stored, removing the limit of "
            "max 25 skills per group."
        )

    @property
    def author(self) -> str:
        return "End45"

    @property
    def version(self) -> str:
        return "0.1.0"

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.UTILITY

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_u32(rom.arm9, OFFSET_US) != ORIGINAL_INSTRUCTION
            if config.game_region == GAME_REGION_EU:
                return read_u32(rom.arm9, OFFSET_EU) != ORIGINAL_INSTRUCTION
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        # Copy the list of skills per group and rewrite it after applying the patch to avoid overwriting
        # it with the default data included in the patch
        if self.is_applied(rom, config):
            group_data = IqGroupsSkills.read_compressed(rom.arm9, config)
        else:
            group_data = IqGroupsSkills.read_uncompressed(rom.arm9, config)
        apply()
        arm9 = bytearray(get_binary_from_rom(rom, config.bin_sections.arm9))
        IqGroupsSkills.write_compressed(arm9, group_data, config)
        set_binary_in_rom(rom, config.bin_sections.arm9, arm9)

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
