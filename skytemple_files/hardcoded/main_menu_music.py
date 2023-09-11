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

# Normal spawn delay (0x24): [EU]overlay_0010:0x7A74 / [US]overlay_0010:0x7A5C
# Spawn delay after stealing from a shop (3): [EU]overlay_0010:0x7BD8 / [US]overlay_0010:0x7BC0
from typing import Optional, Tuple, Union, overload

from range_typed_integers import u8

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_u8, write_u8


class HardcodedMainMenuMusic:
    @staticmethod
    @overload
    def get_main_menu_music(ov00: bytes, config: Pmd2Data, ov09: None = None) -> u8:
        ...

    @staticmethod
    @overload
    def get_main_menu_music(
        ov00: bytes, config: Pmd2Data, ov09: bytes
    ) -> Tuple[u8, u8]:
        ...

    @staticmethod
    def get_main_menu_music(
        ov00: bytes, config: Pmd2Data, ov09: Optional[bytes] = None
    ) -> Union[u8, Tuple[u8, u8]]:
        """Set ov09 to also return the Sky Jukebox return music"""
        main_block = config.bin_sections.overlay0.data.TOP_MENU_MUSIC_ID
        skyj_block = config.bin_sections.overlay9.data.TOP_MENU_RETURN_MUSIC_ID
        ov00_value = read_u8(ov00, main_block.address)
        if ov09:
            return ov00_value, read_u8(ov09, skyj_block.address)
        return ov00_value

    @staticmethod
    def set_main_menu_music(
        value: u8, ov00: bytearray, config: Pmd2Data, ov09: Optional[bytearray] = None
    ) -> None:
        """Set ov09 to also update the Sky Jukebox return music"""
        main_block = config.bin_sections.overlay0.data.TOP_MENU_MUSIC_ID
        skyj_block = config.bin_sections.overlay9.data.TOP_MENU_RETURN_MUSIC_ID
        write_u8(ov00, value, main_block.address)
        if ov09:
            write_u8(ov09, value, skyj_block.address)
