#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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
from typing import Callable, Dict, List, Set

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data, GAME_VERSION_EOS, GAME_REGION_US, GAME_REGION_EU, GAME_REGION_JP
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch
from skytemple_files.common.i18n_util import _, get_locales
from skytemple_files.data.str.handler import StrHandler

PATCH_CHECK_ADDR_APPLIED_US = 0xB3C
PATCH_CHECK_ADDR_APPLIED_EU = 0xB3C
PATCH_CHECK_ADDR_APPLIED_JP = 0xB3C
PATCH_CHECK_INSTR_APPLIED = 0xE2822001

STRING_ID_US = 2613
STRING_ID_EU = 2613
STRING_ID_JP = 2613 #Just a guess

MESSAGE = "Who would you like to be?"
# For xgettext scanning:
_("Who would you like to be?")  # TRANSLATORS: Question in personality test.


class SkipQuizPatchHandler(AbstractPatchHandler, DependantPatch):

    @property
    def name(self) -> str:
        return 'SkipQuiz'

    @property
    def description(self) -> str:
        return _("""Skips the quiz, only leaving the gender question.
Needs ChooseStarter patch to be applied. """)

    @property
    def author(self) -> str:
        return 'irdkwia'

    @property
    def version(self) -> str:
        return '0.0.1'

    def depends_on(self) -> List[str]:
        return ['ChooseStarter']

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.NEW_MECHANIC
    
    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_uintle(rom.loadArm9Overlays([13])[13].data, PATCH_CHECK_ADDR_APPLIED_US, 4)!=PATCH_CHECK_INSTR_APPLIED
            if config.game_region == GAME_REGION_EU:
                return read_uintle(rom.loadArm9Overlays([13])[13].data, PATCH_CHECK_ADDR_APPLIED_EU, 4)!=PATCH_CHECK_INSTR_APPLIED
            if config.game_region == GAME_REGION_JP:
                return read_uintle(rom.loadArm9Overlays([13])[13].data, PATCH_CHECK_ADDR_APPLIED_JP, 4)!=PATCH_CHECK_INSTR_APPLIED
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                string_id = STRING_ID_US
            if config.game_region == GAME_REGION_EU:
                string_id = STRING_ID_EU
            if config.game_region == GAME_REGION_JP:
                string_id = STRING_ID_JP

        # Change dialogue
        for lang in config.string_index_data.languages:
            filename = 'MESSAGE/' + lang.filename
            bin_before = rom.getFileByName(filename)
            strings = StrHandler.deserialize(bin_before)
            strings.strings[string_id-1] = get_locales().translate(MESSAGE, lang.locale.replace('-', '_'))
            bin_after = StrHandler.serialize(strings)
            rom.setFileByName(filename, bin_after)
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    
    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
