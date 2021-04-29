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

from typing import Callable

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.data import Pmd2Data, GAME_VERSION_EOS, GAME_REGION_US, GAME_REGION_EU
from skytemple_files.common.util import get_binary_from_rom_ppmdu
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler
from skytemple_files.common.util import _


ORIGINAL_BYTESEQ = bytes(b'\x20\x00\xD4\xE5')
OFFSET_EU = 0x023061C8 - 0x022DCB80
OFFSET_US = 0x0230579C - 0x022DC240


class PartnersTriggerHiddenTraps(AbstractPatchHandler):

    @property
    def name(self) -> str:
        return 'PartnersTriggerHiddenTraps'

    @property
    def description(self) -> str:
        return _('Recommended for CTC. Without this patch, partners cannot trigger hidden traps - this balances the game, as making your partners dodge traps with manual movement is easy, but this patch is not recommended for mods which use pitfall traps, as they instakill partners which step on them.')

    @property
    def author(self) -> str:
        return 'Cipnit'

    @property
    def version(self) -> str:
        return '1'

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.IMPROVEMENT_TWEAK

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        overlay29 = get_binary_from_rom_ppmdu(rom, config.binaries['overlay/overlay_0029.bin'])
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return overlay29[OFFSET_US:OFFSET_US+4] != ORIGINAL_BYTESEQ
            if config.game_region == GAME_REGION_EU:
                return overlay29[OFFSET_EU:OFFSET_EU+4] != ORIGINAL_BYTESEQ
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        apply()

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
