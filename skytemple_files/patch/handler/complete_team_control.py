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

from typing import Callable, Any

from ndspy.rom import NintendoDSRom

from skytemple_files.common.i18n_util import _, get_locales
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_US,
    GAME_REGION_JP,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.util import get_binary_from_rom
from skytemple_files.data.str.handler import StrHandler
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch

# This isn't just about checking if my mod is applied - this is also important for checking if this mod will interfere with other mods already installed to the ROM.
ov29EU = 0x022DCB80
ov29US = 0x022DC240
ov29JP = 0x022DD8E0
totaloverlay29checks = 6
CHECK_EU: list[Any] = [None] * 7
CHECK_US: list[Any] = [None] * 7
CHECK_JP: list[Any] = [None] * 7
BYTES_EU: list[Any] = [None] * 7
BYTES_US: list[Any] = [None] * 7
BYTES_JP: list[Any] = [None] * 7

CHECK_EU[0] = 0x022F2894 - ov29EU  # where the game checks if you're pressing start
CHECK_US[0] = 0x022F1EE0 - ov29US
CHECK_JP[0] = 0x022F34D8 - ov29JP
BYTES_EU[0] = b"\xB2\x00\xD0\xE1"
BYTES_US[0] = BYTES_EU[0]
BYTES_JP[0] = BYTES_EU[0]
CHECK_EU[1] = 0x022ECD00 - ov29EU  # end of leader's turn verification algorithm
CHECK_US[1] = 0x022EC350 - ov29US
CHECK_JP[1] = 0x022ED9B8 - ov29JP
BYTES_EU[1] = b"\xF1\x00\x90\xE1"
BYTES_US[1] = BYTES_EU[1]
BYTES_JP[1] = BYTES_EU[1]
CHECK_EU[2] = (
    0x022ECE38 - ov29EU
)  # Jump to the function which executes the leader's action
CHECK_US[2] = 0x022EC488 - ov29US
CHECK_JP[2] = 0x022EDAF0 - ov29JP
BYTES_EU[2] = b"\x27\x48\x00\xEB"
BYTES_US[2] = b"\x0B\x48\x00\xEB"
BYTES_JP[2] = b"\x6B\x47\x00\xEB"
CHECK_EU[3] = 0x022EC728 - ov29EU  # When the turns of your partners start
CHECK_US[3] = 0x022EBD78 - ov29US
CHECK_JP[3] = 0x022ED3E0 - ov29JP
BYTES_EU[3] = b"\x00\x50\xA0\xE3"
BYTES_US[3] = BYTES_EU[3]
BYTES_JP[3] = BYTES_EU[3]
CHECK_EU[4] = 0x022F1B2C - ov29EU  # Sets partners to look at you
CHECK_US[4] = 0x022F1178 - ov29US
CHECK_JP[4] = 0x022F2770 - ov29JP
BYTES_EU[4] = b"\x2A\x51\x00\xEB"
BYTES_US[4] = b"\x0C\x51\x00\xEB"
BYTES_JP[4] = b"\xE2\x50\x00\xEB"
CHECK_EU[5] = 0x02305A98 - ov29EU  # Also sets partners to look at you
CHECK_US[5] = 0x0230506C - ov29US
CHECK_JP[5] = 0x023065BC - ov29JP
BYTES_EU[5] = b"\xFE\x17\xD0\xE1"
BYTES_US[5] = BYTES_EU[5]
BYTES_JP[5] = b"\xFA\x17\xD0\xE1"
CHECK_EU[6] = 0x02388154 - 0x02383420  # Jump to team submenu option recorder function
CHECK_US[6] = 0x02387530 - 0x02382820  # this is in overlay 31
CHECK_JP[6] = 0x023887AC - 0x02383AA0
BYTES_EU[6] = b"\x17\x8F\xFD\xEB"
BYTES_US[6] = b"\xB4\x8F\xFD\xEB"
BYTES_JP[6] = b"\xAF\x90\xFD\xEB"

STRING_ID0_US = 296
STRING_ID1_US = 297
STRING_ID0_EU = 296
STRING_ID1_EU = 297
STRING_ID0_JP = 9646
STRING_ID1_JP = 9647

CTC_AUTO = "[CS:S]Control mode set to[CR] [CS:C]automatic[CR][CS:S].[CR]"
CTC_MANUAL = "[CS:S]Control mode set to[CR] [CS:E]manual[CR][CS:S].[CR]"

# For xgettext scanning:
_(
    "[CS:S]Control mode set to[CR] [CS:C]automatic[CR][CS:S].[CR]"
)  # TRANSLATORS: Complete Team Control Auto Mode Activation
_(
    "[CS:S]Control mode set to[CR] [CS:E]manual[CR][CS:S].[CR]"
)  # TRANSLATORS: Complete Team Control Manual Mode Activation


class CompleteTeamControl(AbstractPatchHandler, DependantPatch):
    @property
    def name(self) -> str:
        return "CompleteTeamControl"

    @property
    def description(self) -> str:
        return _(
            "Pressing start in a dungeon toggles between automatic and manual mode. In manual mode, you can control your partners on their turns. You must apply the extra code overlay made by End45 before applying this patch."
        )

    @property
    def author(self) -> str:
        return "Cipnit"

    @property
    def version(self) -> str:
        return "1.2.4"

    def depends_on(self) -> list[str]:
        return ["ExtraSpace"]

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.NEW_MECHANIC

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        overlay29 = get_binary_from_rom(rom, config.bin_sections.overlay29)
        overlay31 = get_binary_from_rom(rom, config.bin_sections.overlay31)
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                x = 0
                while x < totaloverlay29checks:
                    if overlay29[CHECK_US[x] : CHECK_US[x] + 4] != BYTES_US[x]:
                        return True
                    x += 1
                if overlay31[CHECK_US[6] : CHECK_US[6] + 4] != BYTES_US[6]:
                    return True
                return False
            if config.game_region == GAME_REGION_EU:
                x = 0
                while x < totaloverlay29checks:
                    if overlay29[CHECK_EU[x] : CHECK_EU[x] + 4] != BYTES_EU[x]:
                        return True
                    x += 1
                if overlay31[CHECK_EU[6] : CHECK_EU[6] + 4] != BYTES_EU[6]:
                    return True
                return False
            if config.game_region == GAME_REGION_JP:
                x = 0
                while x < totaloverlay29checks:
                    if overlay29[CHECK_JP[x] : CHECK_JP[x] + 4] != BYTES_JP[x]:
                        return True
                    x += 1
                if overlay31[CHECK_JP[6] : CHECK_JP[6] + 4] != BYTES_JP[6]:
                    return True
                return False
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                string_id0 = STRING_ID0_US
                string_id1 = STRING_ID1_US
            if config.game_region == GAME_REGION_EU:
                string_id0 = STRING_ID0_EU
                string_id1 = STRING_ID1_EU
            if config.game_region == GAME_REGION_JP:
                string_id0 = STRING_ID0_JP
                string_id1 = STRING_ID1_JP
        # Change dialogue
        for lang in config.string_index_data.languages:
            filename = "MESSAGE/" + lang.filename
            bin_before = rom.getFileByName(filename)
            strings = StrHandler.deserialize(
                bin_before, string_encoding=config.string_encoding
            )
            strings.strings[string_id0 - 1] = get_locales().translate(
                CTC_AUTO, lang.locale.replace("-", "_")
            )
            strings.strings[string_id1 - 1] = get_locales().translate(
                CTC_MANUAL, lang.locale.replace("-", "_")
            )
            bin_after = StrHandler.serialize(strings)
            rom.setFileByName(filename, bin_after)
        apply()

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
