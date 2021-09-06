#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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

# Normal spawn delay (0x24): [EU]overlay_0010:0x7A74 / [US]overlay_0010:0x7A5C
# Spawn delay after stealing from a shop (3): [EU]overlay_0010:0x7BD8 / [US]overlay_0010:0x7BC0
from typing import Union, Tuple

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_uintle, write_uintle


class HardcodedMainMenuMusic:
    @staticmethod
    def get_main_menu_music(ov00: bytes, config: Pmd2Data, ov09: bytes = None) -> Union[int, Tuple[int, int]]:
        """Set ov09 to also return the Sky Jukebox return music"""
        main_block = config.binaries['overlay/overlay_0000.bin'].blocks['MainMenuSongId']
        skyj_block = config.binaries['overlay/overlay_0009.bin'].blocks['MainMenuReturnSongId']
        ov00_value = read_uintle(ov00, main_block.begin, 1)
        if ov09:
            return ov00_value, read_uintle(ov09, skyj_block.begin, 1)
        return ov00_value

    @staticmethod
    def set_main_menu_music(value: int, ov00: bytearray, config: Pmd2Data, ov09: bytearray = None):
        """Set ov09 to also update the Sky Jukebox return music"""
        main_block = config.binaries['overlay/overlay_0000.bin'].blocks['MainMenuSongId']
        skyj_block = config.binaries['overlay/overlay_0009.bin'].blocks['MainMenuReturnSongId']
        write_uintle(ov00, value, main_block.begin, 1)
        if ov09:
            write_uintle(ov09, value, skyj_block.begin, 1)
