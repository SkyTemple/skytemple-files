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

from skytemple_files.common.i18n_util import _, get_locales
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_US,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.util import read_u32
from skytemple_files.data.str.handler import StrHandler
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch

PATCH_CHECK_ADDR_APPLIED_US = 0x16440
PATCH_CHECK_ADDR_APPLIED_EU = 0x164B4
PATCH_CHECK_INSTR_APPLIED = 0xE59D0014

PUSH_DIALOGUE = "[string:0] pushed [string:1]!"

# For xgettext scanning:
_("[string:0] pushed [string:1]!")  # TRANSLATORS: Push allies dialogue


class PushAlliesPatchHandler(AbstractPatchHandler, DependantPatch):
    @property
    def name(self) -> str:
        return "PushAllies"

    @property
    def description(self) -> str:
        return _(
            """Implements pushing allies in dungeons.
Uses the same command style as PSMD"""
        )

    @property
    def author(self) -> str:
        return "Anonymous"

    @property
    def version(self) -> str:
        return "0.0.1"

    def depends_on(self) -> List[str]:
        return ["ExtraSpace"]

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.NEW_MECHANIC

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
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        try:
            param = self.get_parameters()
            if param["ReplaceStrings"] == "1":
                # Change dialogue
                for lang in config.string_index_data.languages:
                    filename = "MESSAGE/" + lang.filename
                    bin_before = rom.getFileByName(filename)
                    strings = StrHandler.deserialize(
                        bin_before, string_encoding=config.string_encoding
                    )
                    strings.strings[
                        int(param["PushStringID"]) - 1
                    ] = get_locales().translate(
                        PUSH_DIALOGUE, lang.locale.replace("-", "_")
                    )
                    bin_after = StrHandler.serialize(strings)
                    rom.setFileByName(filename, bin_after)
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
