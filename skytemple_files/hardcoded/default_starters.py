"""Module for editing hardcoded data regarding the default starters."""
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


class HardcodedDefaultStarters:
    @staticmethod
    def get_partner_md_id(arm9: bytes, config: Pmd2Data) -> int:
        """
        Gets the monster.md index of the default partner starter
        """
        block = config.binaries['arm9.bin'].blocks['DefaultPartnerId']
        return read_uintle(arm9, block.begin, 2)

    @staticmethod
    def set_partner_md_id(value: int, arm9: bytearray, config: Pmd2Data):
        """
        Sets the monster.md index of the default partner starter
        """
        block = config.binaries['arm9.bin'].blocks['DefaultPartnerId']
        write_uintle(arm9, value, block.begin, 2)

    @staticmethod
    def get_player_md_id(arm9: bytes, config: Pmd2Data) -> int:
        """
        Gets the monster.md index of the default player starter
        """
        block = config.binaries['arm9.bin'].blocks['DefaultHeroId']
        return read_uintle(arm9, block.begin, 2)

    @staticmethod
    def set_player_md_id(value: int, arm9: bytearray, config: Pmd2Data):
        """
        Sets the monster.md index of the default player starter
        """
        block = config.binaries['arm9.bin'].blocks['DefaultHeroId']
        write_uintle(arm9, value, block.begin, 2)

    @staticmethod
    def get_partner_level(arm9: bytes, config: Pmd2Data) -> int:
        """
        Gets the level of the partner starter
        """
        block = config.binaries['arm9.bin'].blocks['PartnerStartLevel']
        return read_uintle(arm9, block.begin, 1)

    @staticmethod
    def set_partner_level(value: int, arm9: bytearray, config: Pmd2Data):
        """
        Sets the level of the partner starter
        """
        block = config.binaries['arm9.bin'].blocks['PartnerStartLevel']
        write_uintle(arm9, value, block.begin, 1)

    @staticmethod
    def get_player_level(arm9: bytes, config: Pmd2Data) -> int:
        """
        Gets the level of the player starter
        """
        block = config.binaries['arm9.bin'].blocks['HeroStartLevel']
        return read_uintle(arm9, block.begin, 1)

    @staticmethod
    def set_player_level(value: int, arm9: bytearray, config: Pmd2Data):
        """
        Sets the level of the player starter
        """
        block = config.binaries['arm9.bin'].blocks['HeroStartLevel']
        write_uintle(arm9, value, block.begin, 1)
