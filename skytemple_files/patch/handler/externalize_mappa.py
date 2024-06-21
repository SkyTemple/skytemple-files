#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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
    GAME_REGION_JP,
    GAME_REGION_US,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.util import read_u32
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler

PATCH_CHECK_ADDR_APPLIED_US = 0xAD80
PATCH_CHECK_ADDR_APPLIED_EU = 0xADF0
PATCH_CHECK_ADDR_APPLIED_JP = 0xAD50
PATCH_CHECK_INSTR_APPLIED = 0xE24DD050


class ExternalizeMappaPatchHandler(AbstractPatchHandler):
    @property
    def name(self) -> str:
        return "ExternalizeMappaFile"

    @property
    def description(self) -> str:
        return _(
            """Use filestreams to access mappa_t/mappa_y/mappa_s data instead of loading them entirely.
This patch is useless on its own, unless you have a too big mappa file."""
        )

    @property
    def author(self) -> str:
        return "Anonymous"

    @property
    def version(self) -> str:
        return "0.0.1"

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.UTILITY

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return (
                    read_u32(rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_US)
                    != PATCH_CHECK_INSTR_APPLIED
                )
            if config.game_region == GAME_REGION_EU:
                return (
                    read_u32(rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_EU)
                    != PATCH_CHECK_INSTR_APPLIED
                )
            if config.game_region == GAME_REGION_JP:
                raise NotImplementedError()  # TODO EXTERNALIZE_MAPPA: Works fine for the most part, but some attributes are read incorrectly (trying to add Pitfall Traps to a dungeon resulted in Chestnut Traps).
                return (
                    read_u32(rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_JP)
                    != PATCH_CHECK_INSTR_APPLIED
                )
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data) -> None:
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data) -> None:
        raise NotImplementedError()
