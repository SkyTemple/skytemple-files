"""Module for editing hardcoded data regarding the default starters."""
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
from typing import List

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_uintle, write_uintle, AutoString

SE_PC_LNTRY_LEN = 0x14


class SpecialEpisodePc(AutoString):
    def __init__(self, poke_id: int, joined_at: int, move1: int, move2: int, move3: int, move4: int,
                 do_not_fix_entire_moveset: bool, level: int, iq: int, fixed_hp: int):
        self.poke_id = poke_id
        self.joined_at = joined_at
        self.move1 = move1
        self.move2 = move2
        self.move3 = move3
        self.move4 = move4
        self.do_not_fix_entire_moveset = do_not_fix_entire_moveset
        self.level = level
        self.iq = iq
        # 0 if not fixed
        self.fixed_hp = fixed_hp

    def to_bytes(self) -> bytes:
        b = bytearray(SE_PC_LNTRY_LEN)
        write_uintle(b, self.poke_id, 0, 2)
        write_uintle(b, self.joined_at, 2, 2)
        write_uintle(b, self.move1, 4, 2)
        write_uintle(b, self.move2, 6, 2)
        write_uintle(b, self.move3, 8, 2)
        write_uintle(b, self.move4, 10, 2)
        write_uintle(b, int(self.do_not_fix_entire_moveset), 12, 2)
        write_uintle(b, self.level, 14, 2)
        write_uintle(b, self.iq, 16, 2)
        write_uintle(b, self.fixed_hp, 18, 2)
        return b

    def __eq__(self, other):
        if not isinstance(other, SpecialEpisodePc):
            return False
        return self.poke_id == other.poke_id \
               and self.joined_at == other.joined_at \
               and self.move1 == other.move1 \
               and self.move2 == other.move2 \
               and self.move3 == other.move3 \
               and self.move4 == other.move4 \
               and self.do_not_fix_entire_moveset == other.do_not_fix_entire_moveset \
               and self.level == other.level \
               and self.iq == other.iq \
               and self.fixed_hp == other.fixed_hp


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

    @staticmethod
    def get_special_episode_pcs(arm9: bytes, config: Pmd2Data) -> List[SpecialEpisodePc]:
        """
        Gets the special episode player characters
        """
        block = config.binaries['arm9.bin'].blocks['SpecialEpisodePCs']
        lst = []
        for i in range(block.begin, block.end, SE_PC_LNTRY_LEN):
            lst.append(SpecialEpisodePc(
                read_uintle(arm9, i + 0, 2),
                read_uintle(arm9, i + 2, 2),
                read_uintle(arm9, i + 4, 2),
                read_uintle(arm9, i + 6, 2),
                read_uintle(arm9, i + 8, 2),
                read_uintle(arm9, i + 10, 2),
                bool(read_uintle(arm9, i + 12, 2)),
                read_uintle(arm9, i + 14, 2),
                read_uintle(arm9, i + 16, 2),
                read_uintle(arm9, i + 18, 2),
            ))
        return lst

    @staticmethod
    def set_special_episode_pcs(value: List[SpecialEpisodePc], arm9: bytearray, config: Pmd2Data):
        """
        Sets the special episode player characters
        """
        block = config.binaries['arm9.bin'].blocks['SpecialEpisodePCs']
        expected_length = int((block.end - block.begin) / SE_PC_LNTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            arm9[block.begin + i * SE_PC_LNTRY_LEN:block.begin + (i + 1) * SE_PC_LNTRY_LEN] = entry.to_bytes()
