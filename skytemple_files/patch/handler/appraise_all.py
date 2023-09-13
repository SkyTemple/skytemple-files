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

from ndspy.code import loadOverlayTable, saveOverlayTable
from ndspy.rom import NintendoDSRom

from skytemple_files.common.i18n_util import _, get_locales
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_JP,
    GAME_REGION_US,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.util import read_u32
from skytemple_files.data.str.handler import StrHandler
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler

PATCH_CHECK_ADDR_APPLIED_US = 0x18
PATCH_CHECK_ADDR_APPLIED_EU = 0x18
PATCH_CHECK_ADDR_APPLIED_JP = 0x18
PATCH_CHECK_INSTR_APPLIED = 0xEA000137

OVERLAY25_INITAL_SIZE_US = 0x14C0
OVERLAY25_INITAL_SIZE_EU = 0x14C0
OVERLAY25_INITAL_SIZE_JP = 0x14C0

OVERLAY25_ADD_SIZE = 0x1000

MENU_OPTION = "Appraise all"
APPRAISE_ALL_CONFIRM = """ And to appraise all your items, 
you will pay [CS:G][gold_left:0][CR][M:S0]?"""
APPRAISE_REVEAL_BEFORE = """ And so...[K]it is revealed...[C] Within the boxes...[K]
were..."""
APPRAISE_REVEAL_ITEM = " ...a [me_play:1][string0]!"

# For xgettext scanning:
_("Appraise all")  # TRANSLATORS: Appraise All Menu Option
_(
    """ And to appraise all your items, 
you will pay [CS:G][gold_left:0][CR][M:S0]?"""
)  # TRANSLATORS: Appraise All Confirm
_(
    """ And so...[K]it is revealed...[C] Within the boxes...[K]
were..."""
)  # TRANSLATORS: Appraise All Reveal Before
_(" ...a [me_play:1][string0]!")  # TRANSLATORS: Appraise All Reveal Item


class AppraiseAllPatchHandler(AbstractPatchHandler):
    @property
    def name(self) -> str:
        return "AppraiseAll"

    @property
    def description(self) -> str:
        return _(
            """Adds an extra menu in box appraisal to appraise all boxes at once. """
        )

    @property
    def author(self) -> str:
        return "Anonymous"

    @property
    def version(self) -> str:
        return "0.0.1"

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.IMPROVEMENT_TWEAK

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return (
                    read_u32(
                        rom.loadArm9Overlays([25])[25].data,
                        PATCH_CHECK_ADDR_APPLIED_US,
                    )
                    != PATCH_CHECK_INSTR_APPLIED
                )
            if config.game_region == GAME_REGION_EU:
                return (
                    read_u32(
                        rom.loadArm9Overlays([25])[25].data,
                        PATCH_CHECK_ADDR_APPLIED_EU,
                    )
                    != PATCH_CHECK_INSTR_APPLIED
                )
            if config.game_region == GAME_REGION_JP:
                return (
                    read_u32(
                        rom.loadArm9Overlays([25])[25].data,
                        PATCH_CHECK_ADDR_APPLIED_JP,
                    )
                    != PATCH_CHECK_INSTR_APPLIED
                )
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                overlay_size = OVERLAY25_INITAL_SIZE_US
            if config.game_region == GAME_REGION_EU:
                overlay_size = OVERLAY25_INITAL_SIZE_EU
            if config.game_region == GAME_REGION_JP:
                overlay_size = OVERLAY25_INITAL_SIZE_JP

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
                    int(param["MenuOptionStringID"]) - 1
                ] = get_locales().translate(MENU_OPTION, lang.locale.replace("-", "_"))
                strings.strings[
                    int(param["AppraiseAllConfirmStringID"]) - 1
                ] = get_locales().translate(
                    APPRAISE_ALL_CONFIRM, lang.locale.replace("-", "_")
                )
                strings.strings[
                    int(param["AppraiseRevealBeforeStringID"]) - 1
                ] = get_locales().translate(
                    APPRAISE_REVEAL_BEFORE, lang.locale.replace("-", "_")
                )
                strings.strings[
                    int(param["AppraiseRevealItemStringID"]) - 1
                ] = get_locales().translate(
                    APPRAISE_REVEAL_ITEM, lang.locale.replace("-", "_")
                )
                bin_after = StrHandler.serialize(strings)
                rom.setFileByName(filename, bin_after)

        table = loadOverlayTable(rom.arm9OverlayTable, lambda x, y: bytes())
        ov = table[25]
        ov.ramSize = overlay_size + OVERLAY25_ADD_SIZE
        rom.arm9OverlayTable = saveOverlayTable(table)
        ov25 = rom.files[ov.fileID]
        rom.files[ov.fileID] = ov25[:overlay_size]
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
