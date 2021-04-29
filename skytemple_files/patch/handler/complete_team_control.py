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

from typing import Callable, List

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.data import Pmd2Data, GAME_VERSION_EOS, GAME_REGION_US, GAME_REGION_EU
from skytemple_files.common.util import get_binary_from_rom_ppmdu
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch
from skytemple_files.common.util import _

# This isn't just about checking if my mod is applied - this is also important for checking if this mod will interfere with other mods already installed to the ROM.
ov29EU = 0x022DCB80
ov29US = 0x022DC240
totaloverlay29checks = 6
CHECK_EU = [None] * 7
CHECK_US = [None] * 7
BYTES_EU = [None] * 7
BYTES_US = [None] * 7

CHECK_EU[0] = 0x022F2894 - ov29EU  # where the game checks if you're pressing start
CHECK_US[0] = 0x022F1EE0 - ov29US
BYTES_EU[0] = bytes(b'\xB2\x00\xD0\xE1')
BYTES_US[0] = BYTES_EU[0]
CHECK_EU[1] = 0x022ECD00 - ov29EU  # end of leader's turn verification algorithm
CHECK_US[1] = 0x022EC350 - ov29US
BYTES_EU[1] = bytes(b'\xF1\x00\x90\xE1')
BYTES_US[1] = BYTES_EU[1]
CHECK_EU[2] = 0x022ECE38 - ov29EU  # Jump to the function which executes the leader's action
CHECK_US[2] = 0x022EC488 - ov29US
BYTES_EU[2] = bytes(b'\x27\x48\x00\xEB')
BYTES_US[2] = bytes(b'\x0B\x48\x00\xEB')
CHECK_EU[3] = 0x022EC728 - ov29EU  # When the turns of your partners start
CHECK_US[3] = 0x022EBD78 - ov29US
BYTES_EU[3] = bytes(b'\x00\x50\xA0\xE3')
BYTES_US[3] = BYTES_EU[3]
CHECK_EU[4] = 0x022F1B2C - ov29EU  # Sets partners to look at you
CHECK_US[4] = 0x022F1178 - ov29US
BYTES_EU[4] = bytes(b'\x2A\x51\x00\xEB')
BYTES_US[4] = bytes(b'\x0C\x51\x00\xEB')
CHECK_EU[5] = 0x02305A98 - ov29EU  # Also sets partners to look at you
CHECK_US[5] = 0x0230506C - ov29US
BYTES_EU[5] = bytes(b'\xFE\x17\xD0\xE1')
BYTES_US[5] = BYTES_EU[5]
CHECK_EU[6] = 0x02388154 - 0x02383420  # Jump to team submenu option recorder function
CHECK_US[6] = 0x02387530 - 0x02382820  # this is in overlay 31
BYTES_EU[6] = bytes(b'\x17\x8F\xFD\xEB')
BYTES_US[6] = bytes(b'\xB4\x8F\xFD\xEB')


class CompleteTeamControl(AbstractPatchHandler, DependantPatch):

    @property
    def name(self) -> str:
        return 'CompleteTeamControl'

    @property
    def description(self) -> str:
        return _('Pressing start in a dungeon toggles between automatic and manual mode. In manual mode, you can control your partners on their turns. You must apply the extra code overlay made by End45 before applying this patch.')

    @property
    def author(self) -> str:
        return 'Cipnit'

    @property
    def version(self) -> str:
        return '1.2.3'

    def depends_on(self) -> List[str]:
        return ['ExtraSpace']

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.NEW_MECHANIC

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        overlay29 = get_binary_from_rom_ppmdu(rom, config.binaries['overlay/overlay_0029.bin'])
        overlay31 = get_binary_from_rom_ppmdu(rom, config.binaries['overlay/overlay_0031.bin'])
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                x = 0
                while x < totaloverlay29checks:
                    if overlay29[CHECK_US[x]:CHECK_US[x] + 4] != BYTES_US[x]:
                        return True
                    x += 1
                if overlay31[CHECK_US[6]:CHECK_US[6] + 4] != BYTES_US[6]:
                    return True
                return False
            if config.game_region == GAME_REGION_EU:
                x = 0
                while x < totaloverlay29checks:
                    if overlay29[CHECK_EU[x]:CHECK_EU[x] + 4] != BYTES_EU[x]:
                        return True
                    x += 1
                if overlay31[CHECK_EU[6]:CHECK_EU[6] + 4] != BYTES_EU[6]:
                    return True
                return False
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        apply()

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
