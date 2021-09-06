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
from skytemple_files.common.util import read_uintle, write_uintle, AutoString, read_bytes
from skytemple_files.common.i18n_util import _

GUEST_DATA_ENTRY_SIZE = 36
EXTRA_DUNGEON_DATA_ENTRY_SIZE = 2
# Amount of entries in the extra dungeon data table
EXTRA_DUNGEON_DATA_ENTRIES = 0xB4


class ExtraDungeonDataEntry(AutoString):
    def __init__(self, guest1_index: int, guest2_index: int, hlr_uncleared: bool, disable_recruit: bool,
                 side01_check: bool, hlr_cleared: bool):
        # Index inside the guest pokémon data table of the first additional pokémon that will be added to
        # the team in this dungeon
        if self._valid_index(guest1_index):
            self.guest1_index = guest1_index
        else:
            raise ValueError(_(f"'{guest1_index}' is not a valid guest pokémon index"))
        if self._valid_index(guest2_index):
            self.guest2_index = guest2_index
        else:
            raise ValueError(_(f"'{guest2_index}' is not a valid guest pokémon index"))
        # True if Hidden Land-like restrictions should be enabled in this dungeon when it's uncleared
        self.hlr_uncleared = hlr_uncleared
        # True to forcefully disable recruitment
        self.disable_recruit = disable_recruit
        # If true, extra pokémon will only be added to the team if SIDE01_BOSS2ND is 0
        self.side01_check = side01_check
        # True if Hidden Land-like restrictions should be enabled in this dungeon after it's cleared
        self.hlr_cleared = hlr_cleared

    def __eq__(self, other):
        if not isinstance(other, ExtraDungeonDataEntry):
            return False
        else:
            return self.guest1_index == other.guest1_index and \
                self.guest2_index == other.guest2_index and \
                self.hlr_uncleared == other.hlr_uncleared and \
                self.disable_recruit == other.disable_recruit and \
                self.side01_check == other.side01_check and \
                self.hlr_cleared == other.hlr_cleared

    def to_bytes(self) -> bytes:
        buffer = bytearray(2)

        entry = 0
        if self.guest1_index != -1:
            entry = self.guest1_index + 1
        if self.hlr_uncleared:
            entry |= 0x80
        if self.disable_recruit:
            entry |= 0x40
        if self.guest2_index != -1:
            entry += self.guest2_index + 1 << 8
        if self.side01_check:
            entry |= 0x8000
        if self.hlr_cleared:
            entry |= 0x4000

        write_uintle(buffer, entry, 0, 2)
        return buffer

    @classmethod
    def from_bytes(cls, b: bytes) -> 'ExtraDungeonDataEntry':
        data_int = read_uintle(b, 0, 2)
        guest1_index = (data_int & 0x3F) - 1
        guest2_index = ((data_int & 0x3F00) >> 8) - 1
        return cls(guest1_index, guest2_index, bool(data_int & 0x80), bool(data_int & 0x40), bool(data_int & 0x8000),
                   bool(data_int & 0x4000))

    @classmethod
    def _valid_index(cls, index: int):
        """
        Returns true if a given guest pokémon index is valid.
        Valid values are indexes 0 to 62 and -1, which is used as an empty value
        """
        return -1 <= index <= 62


class GuestPokemon(AutoString):
    def __init__(self, unk1: int, poke_id: int, joined_at: int, moves: List[int], hp: int, level: int,
                 iq: int, atk: int, sp_atk: int, def_: int, sp_def: int, unk3: int, exp: int):
        self.unk1 = unk1
        self.poke_id = poke_id
        self.joined_at = joined_at
        self.moves = moves
        self.hp = hp
        self.level = level
        self.iq = iq
        self.atk = atk
        self.sp_atk = sp_atk
        self.def_ = def_
        self.sp_def = sp_def
        self.unk3 = unk3
        self.exp = exp

    def __eq__(self, other):
        if not isinstance(other, GuestPokemon):
            return False
        else:
            return self.unk1 == other.unk1 and \
                   self.poke_id == other.poke_id and \
                   self.joined_at == other.joined_at and \
                   self.moves == other.moves and \
                   self.hp == other.hp and \
                   self.level == other.level and \
                   self.iq == other.iq and \
                   self.atk == other.atk and \
                   self.sp_atk == other.sp_atk and \
                   self.def_ == other.def_ and \
                   self.sp_def == other.sp_def and \
                   self.unk3 == other.unk3 and \
                   self.exp == other.exp

    def is_null(self):
        return self.unk1 == 0 and \
               self.poke_id == 0 and \
               self.joined_at == 0 and \
               self.moves == [0] * 4 and \
               self.hp == 0 and \
               self.level == 0 and \
               self.iq == 0 and \
               self.atk == 0 and \
               self.sp_atk == 0 and \
               self.def_ == 0 and \
               self.sp_def == 0 and \
               self.unk3 == 0 and \
               self.exp == 0

    def to_bytes(self) -> bytes:
        buffer = bytearray(0x24)

        write_uintle(buffer, self.unk1, 0, 4)
        write_uintle(buffer, self.poke_id, 4, 2)
        write_uintle(buffer, self.joined_at, 6, 2)
        write_uintle(buffer, self.moves[0], 8, 2)
        write_uintle(buffer, self.moves[1], 10, 2)
        write_uintle(buffer, self.moves[2], 12, 2)
        write_uintle(buffer, self.moves[3], 14, 2)
        write_uintle(buffer, self.hp, 16, 2)
        write_uintle(buffer, self.level, 18, 2)
        write_uintle(buffer, self.iq, 20, 2)
        write_uintle(buffer, self.atk, 22, 2)
        write_uintle(buffer, self.sp_atk, 24, 2)
        write_uintle(buffer, self.def_, 26, 2)
        write_uintle(buffer, self.sp_def, 28, 2)
        write_uintle(buffer, self.unk3, 30, 2)
        write_uintle(buffer, self.exp, 32, 4)

        return buffer

    @classmethod
    def from_bytes(cls, b: bytes) -> 'GuestPokemon':
        return cls(
            read_uintle(b, 0, 4), read_uintle(b, 4, 2), read_uintle(b, 6, 2),
            [read_uintle(b, 8, 2), read_uintle(b, 10, 2), read_uintle(b, 12, 2), read_uintle(b, 14, 2)],
            read_uintle(b, 16, 2), read_uintle(b, 18, 2), read_uintle(b, 20, 2), read_uintle(b, 22, 2),
            read_uintle(b, 24, 2), read_uintle(b, 26, 2), read_uintle(b, 28, 2), read_uintle(b, 30, 2),
            read_uintle(b, 32, 4)
        )


class ExtraDungeonDataList:
    @staticmethod
    def read(arm9bin: bytes, config: Pmd2Data) -> List[ExtraDungeonDataEntry]:
        """Returns the list of extra dungeon data"""
        block = config.binaries['arm9.bin'].blocks['ExtraDungeonData']
        lst = []
        for i in range(block.begin, block.end, EXTRA_DUNGEON_DATA_ENTRY_SIZE):
            lst.append(ExtraDungeonDataEntry.from_bytes(read_bytes(arm9bin, i, EXTRA_DUNGEON_DATA_ENTRY_SIZE)))
        return lst

    @staticmethod
    def write(lst: List[ExtraDungeonDataEntry], arm9bin: bytearray, config: Pmd2Data):
        """
        Writes the list of dungeon extra data to the arm9 binary provided.
        The list must have exactly 0xB4 entries.
        """
        if len(lst) != EXTRA_DUNGEON_DATA_ENTRIES:
            raise ValueError(f"The extra dungeon data list must have exactly {EXTRA_DUNGEON_DATA_ENTRIES} entries.")

        block = config.binaries['arm9.bin'].blocks['ExtraDungeonData']
        for i, entry in enumerate(lst):
            offset = block.begin + i * EXTRA_DUNGEON_DATA_ENTRY_SIZE
            arm9bin[offset:offset + 2] = entry.to_bytes()[0:2]


class GuestPokemonList:
    @staticmethod
    def get_max_entries(config: Pmd2Data) -> int:
        """Returns the maximum amount of entries that can fit in the binary"""
        block1 = config.binaries['arm9.bin'].blocks['GuestPokemonData']
        block2 = config.binaries['arm9.bin'].blocks['GuestPokemonData2']

        return (block1.end - block1.begin) // GUEST_DATA_ENTRY_SIZE + \
            (block2.end - block2.begin) // GUEST_DATA_ENTRY_SIZE

    @staticmethod
    def read(arm9bin: bytes, config: Pmd2Data) -> List[GuestPokemon]:
        """Returns the list of guest pokémon data"""
        block = config.binaries['arm9.bin'].blocks['GuestPokemonData']
        lst = []
        done = False
        # Read the first list
        for i in range(block.begin, block.end, GUEST_DATA_ENTRY_SIZE):
            read_entry = GuestPokemon.from_bytes(read_bytes(arm9bin, i, GUEST_DATA_ENTRY_SIZE))
            if read_entry.is_null():
                done = True
                break
            lst.append(read_entry)
        if not done:
            # Read the list added by the EditExtraPokemon patch
            block = config.binaries['arm9.bin'].blocks['GuestPokemonData2']
            # Make sure we don't keep reading if there's no space for one more entry, since if we did that
            # we would read out of bounds
            for i in range(block.begin, block.end - GUEST_DATA_ENTRY_SIZE + 1, GUEST_DATA_ENTRY_SIZE):
                read_entry = GuestPokemon.from_bytes(read_bytes(arm9bin, i, GUEST_DATA_ENTRY_SIZE))
                if read_entry.is_null():
                    break
                lst.append(read_entry)
        return lst

    @staticmethod
    def write(lst: List[GuestPokemon], arm9bin: bytearray, config: Pmd2Data):
        """
        Writes the list of guest pokémon data to the arm9 binary.
        The first 18 entries will be written to the GuestPokemonData block, the rest
        will be written to GuestPokemonData2.
        The list can't have more entries than the max amount specified by get_max_entries()
        """
        max_entries = GuestPokemonList.get_max_entries(config)
        if len(lst) > max_entries:
            raise ValueError(f"The guest pokémon data list can't have more than {max_entries} entries.")
        block1 = config.binaries['arm9.bin'].blocks['GuestPokemonData']
        block2 = config.binaries['arm9.bin'].blocks['GuestPokemonData2']

        for i, value in enumerate(lst):
            if i < 18:
                offset = block1.begin + i * GUEST_DATA_ENTRY_SIZE
                arm9bin[offset:offset + GUEST_DATA_ENTRY_SIZE] = lst[i].to_bytes()[0:GUEST_DATA_ENTRY_SIZE]
            else:
                offset = block2.begin + (i - 18) * GUEST_DATA_ENTRY_SIZE
                arm9bin[offset:offset + GUEST_DATA_ENTRY_SIZE] = lst[i].to_bytes()[0:GUEST_DATA_ENTRY_SIZE]

        # Null the rest of the table
        for i in range(len(lst), max_entries):
            if i < 18:
                offset = block1.begin + i * GUEST_DATA_ENTRY_SIZE
                arm9bin[offset:offset + GUEST_DATA_ENTRY_SIZE] = [0] * GUEST_DATA_ENTRY_SIZE
            else:
                offset = block2.begin + (i - 18) * GUEST_DATA_ENTRY_SIZE
                arm9bin[offset:offset + GUEST_DATA_ENTRY_SIZE] = [0] * GUEST_DATA_ENTRY_SIZE
