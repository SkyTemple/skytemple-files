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

from ndspy.code import loadOverlayTable
from ndspy.rom import NintendoDSRom
from range_typed_integers import u8

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_JP,
    GAME_REGION_US,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.util import read_u32
from skytemple_files.hardcoded.fixed_floor import HardcodedFixedFloorTables
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler

PATCH_CHECK_ADDR_APPLIED_US = 0x67E6C
PATCH_CHECK_ADDR_APPLIED_EU = 0x68110
PATCH_CHECK_ADDR_APPLIED_JP = 0x67B90
PATCH_CHECK_INSTR_APPLIED = 0xE3500000


class ChangeFixedFloorPropertiesPatchHandler(AbstractPatchHandler):
    @property
    def name(self) -> str:
        return "ChangeFixedFloorProperties"

    @property
    def description(self) -> str:
        return _(
            """Changes and adds some properties for fixed floors.
Removes restrictions. """
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
                    read_u32(
                        rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_US
                    )
                    != PATCH_CHECK_INSTR_APPLIED
                )
            if config.game_region == GAME_REGION_EU:
                return (
                    read_u32(
                        rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_EU
                    )
                    != PATCH_CHECK_INSTR_APPLIED
                )
            if config.game_region == GAME_REGION_JP:
                return (
                    read_u32(
                        rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_JP
                    )
                    != PATCH_CHECK_INSTR_APPLIED
                )
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        if not self.is_applied(rom, config):
            table = loadOverlayTable(rom.arm9OverlayTable, lambda x, y: bytes())
            ov = table[10]
            ov10 = bytearray(rom.files[ov.fileID])
            props = HardcodedFixedFloorTables.get_fixed_floor_properties(ov10, config)
            for i, p in enumerate(props):
                p.null = u8(0)
                if i == 0 or i >= 0xA5:
                    p.orbs_enabled = True
                    p.unk8 = True
                    p.unk9 = True
                else:
                    p.null |= 0x1  # type: ignore

                if 0 < i < 0x51:
                    p.null |= 0x2  # type: ignore

                if 0 < i <= 0x6E:
                    p.null |= 0x4  # type: ignore
            HardcodedFixedFloorTables.set_fixed_floor_properties(ov10, props, config)
            rom.files[ov.fileID] = bytes(ov10)
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
