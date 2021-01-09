"""Module for editing hardcoded data regarding the starters and the personality test."""
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
from typing import List

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_uintle, write_uintle
from skytemple_files.hardcoded.default_starters import HardcodedDefaultStarters


class HardcodedPersonalityTestStarters:
    @staticmethod
    def get_partner_md_ids(overlay13: bytes, config: Pmd2Data) -> List[int]:
        """Returns the monster.md indices of the partner starter choices (total index, with gender form!)"""
        block = config.binaries['overlay/overlay_0013.bin'].blocks['StartersPartnerIds']
        ids = []
        for i in range(block.begin, block.end, 2):
            ids.append(read_uintle(overlay13, i, 2))
        return ids

    @staticmethod
    def set_partner_md_ids(value: List[int], overlay13: bytearray, config: Pmd2Data) -> None:
        """
        Sets the monster.md indices of the partner starter choices (in place, total index, with gender form!)
        The length of the list must exactly match the original ROM's length (see get_partner_md_ids).
        """
        block = config.binaries['overlay/overlay_0013.bin'].blocks['StartersPartnerIds']
        expected_length = int((block.end - block.begin) / 2)
        if len(value) != expected_length:
            raise ValueError(f"The ID list must have exactly the length of {expected_length} entries.")
        for i, v in enumerate(value):
            write_uintle(overlay13, v, block.begin + (i * 2), 2)

    @staticmethod
    def get_player_md_ids(overlay13: bytes, config: Pmd2Data) -> List[int]:
        """Returns the monster.md indices of the player starter choices (total index, with gender form!)"""
        block = config.binaries['overlay/overlay_0013.bin'].blocks['StartersHeroIds']
        ids = []
        for i in range(block.begin, block.end, 2):
            ids.append(read_uintle(overlay13, i, 2))
        return ids

    @staticmethod
    def set_player_md_ids(value: List[int], overlay13: bytearray, config: Pmd2Data) -> None:
        """
        Sets the monster.md indices of the player partner choices (in place, total index, with gender form!)
        The length of the list must exactly match the original ROM's length (see get_player_md_ids).
        """
        block = config.binaries['overlay/overlay_0013.bin'].blocks['StartersHeroIds']
        expected_length = int((block.end - block.begin) / 2)
        if len(value) != expected_length:
            raise ValueError(f"The ID list must have exactly the length of {expected_length} entries.")
        for i, v in enumerate(value):
            write_uintle(overlay13, v, block.begin + (i * 2), 2)

    @staticmethod
    def get_partner_level(arm9: bytes, config: Pmd2Data) -> int:
        """
        Gets the level of the partner starter
        """
        return HardcodedDefaultStarters.get_partner_level(arm9, config)

    @staticmethod
    def set_partner_level(value: int, arm9: bytearray, config: Pmd2Data):
        """
        Sets the level of the partner starter
        """
        return HardcodedDefaultStarters.set_partner_level(value, arm9, config)

    @staticmethod
    def get_player_level(arm9: bytes, config: Pmd2Data) -> int:
        """
        Gets the level of the player starter
        """
        return HardcodedDefaultStarters.get_player_level(arm9, config)

    @staticmethod
    def set_player_level(value: int, arm9: bytearray, config: Pmd2Data):
        """
        Sets the level of the player starter
        """
        return HardcodedDefaultStarters.set_player_level(value, arm9, config)
