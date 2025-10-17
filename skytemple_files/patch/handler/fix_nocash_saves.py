#  Copyright 2020-2025 SkyTemple Contributors
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

from collections.abc import Callable

from ndspy.rom import NintendoDSRom

from skytemple_files.common.exceptions.outdated_patch_dependency import OutdatedPatchDependencyError
from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_US,
    GAME_REGION_JP,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.util import read_u32
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch

ORIGINAL_INSTRUCTION = 0xE3A00008
OFFSET_EU = 0x4ADD0
OFFSET_US = 0x4AA98
OFFSET_JP = 0x4AE00

EXTRA_SPACE_OFFSET = 0xC6C + 0x34
EXTRA_SPACE_ORIGINAL_INSTRUCTION = 0xE3A00000


class FixNocashSavesPatchHandler(AbstractPatchHandler, DependantPatch):
    @property
    def name(self) -> str:
        return "FixNo$GbaSaves"

    @property
    def description(self) -> str:
        return _("Fixes an issue that causes saving to fail on the No$GBA emulator.")

    @property
    def author(self) -> str:
        return "Frostbyte, Chesyon"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.BUGFIXES

    def depends_on(self) -> list[str]:
        return ["ExtraSpace"]

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_u32(rom.arm9, OFFSET_US) != ORIGINAL_INSTRUCTION
            if config.game_region == GAME_REGION_EU:
                return read_u32(rom.arm9, OFFSET_EU) != ORIGINAL_INSTRUCTION
            if config.game_region == GAME_REGION_JP:
                return read_u32(rom.arm9, OFFSET_JP) != ORIGINAL_INSTRUCTION
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data) -> None:
        if (
            36 in rom.loadArm9Overlays([36])
            and read_u32(rom.arm9, EXTRA_SPACE_OFFSET) == EXTRA_SPACE_ORIGINAL_INSTRUCTION
        ):  # if overlay36 exists, but the NitroMain hook to load it does not, we're on the old version of ExtraSpace
            raise OutdatedPatchDependencyError(self.name, ["ExtraSpace"])
        else:
            # Apply the patch
            apply()

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data) -> None:
        raise NotImplementedError()
