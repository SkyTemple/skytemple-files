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
from skytemple_files.common.util import get_binary_from_rom
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler


class DisarmOneRoomMHPatchHandler(AbstractPatchHandler):
    @property
    def name(self) -> str:
        return "DisarmOneRoomMonsterHouses"

    @property
    def description(self) -> str:
        return _(
            "Disarms one-room Monster House floors, which can appear in cases like a layout generation failure. These floors will still be one giant room, but will no longer be Monster Houses."
        )

    @property
    def author(self) -> str:
        return "UsernameFodder"

    @property
    def version(self) -> str:
        return "0.1.0"

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.IMPROVEMENT_TWEAK

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            ORIGINAL_BYTES = bytes([0xD8, 0x0D, 0x00, 0xEB])
            OFFSETS = {
                GAME_REGION_US: 0x605F4,
                GAME_REGION_EU: 0x60898,
            }
            offset = OFFSETS.get(config.game_region)
            if offset is not None:
                overlay29 = get_binary_from_rom(rom, config.bin_sections.overlay29)
                return (
                    overlay29[offset : offset + len(ORIGINAL_BYTES)] != ORIGINAL_BYTES
                )
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        apply()

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
