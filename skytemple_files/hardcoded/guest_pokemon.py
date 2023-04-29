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

from typing import List

from range_typed_integers import u16, u32

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import (
    AutoString,
    write_u32,
    read_bytes,
    read_u16,
    write_u16,
    read_u32,
)

GUEST_DATA_ENTRY_SIZE = 36
EXTRA_DUNGEON_DATA_ENTRY_SIZE = 2
# Amount of entries in the extra dungeon data table
EXTRA_DUNGEON_DATA_ENTRIES = 0xB4


class ExtraDungeonDataEntry(AutoString):
    def __init__(
        self,
        guest1_index: int,
        guest2_index: int,
        hlr_uncleared: bool,
        disable_recruit: bool,
        side01_check: bool,
        hlr_cleared: bool,
    ):
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExtraDungeonDataEntry):
            return False
        else:
            return (
                self.guest1_index == other.guest1_index
                and self.guest2_index == other.guest2_index
                and self.hlr_uncleared == other.hlr_uncleared
                and self.disable_recruit == other.disable_recruit
                and self.side01_check == other.side01_check
                and self.hlr_cleared == other.hlr_cleared
            )

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

        write_u16(buffer, u16(entry), 0)
        return buffer

    @classmethod
    def from_bytes(cls, b: bytes) -> "ExtraDungeonDataEntry":
        data_int = read_u16(b, 0)
        guest1_index = (data_int & 0x3F) - 1
        guest2_index = ((data_int & 0x3F00) >> 8) - 1
        return cls(
            guest1_index,
            guest2_index,
            bool(data_int & 0x80),
            bool(data_int & 0x40),
            bool(data_int & 0x8000),
            bool(data_int & 0x4000),
        )

    @classmethod
    def _valid_index(cls, index: int) -> bool:
        """
        Returns true if a given guest pokémon index is valid.
        Valid values are indexes 0 to 62 and -1, which is used as an empty value
        """
        return -1 <= index <= 62


class GuestPokemon(AutoString):
    unk1: u32
    poke_id: u16
    joined_at: u16
    moves: List[u16]
    hp: u16
    level: u16
    iq: u16
    atk: u16
    sp_atk: u16
    def_: u16
    sp_def: u16
    unk3: u16
    exp: u32

    def __init__(
        self,
        unk1: u32,
        poke_id: u16,
        joined_at: u16,
        moves: List[u16],
        hp: u16,
        level: u16,
        iq: u16,
        atk: u16,
        sp_atk: u16,
        def_: u16,
        sp_def: u16,
        unk3: u16,
        exp: u32,
    ):
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GuestPokemon):
            return False
        else:
            return (
                self.unk1 == other.unk1
                and self.poke_id == other.poke_id
                and self.joined_at == other.joined_at
                and self.moves == other.moves
                and self.hp == other.hp
                and self.level == other.level
                and self.iq == other.iq
                and self.atk == other.atk
                and self.sp_atk == other.sp_atk
                and self.def_ == other.def_
                and self.sp_def == other.sp_def
                and self.unk3 == other.unk3
                and self.exp == other.exp
            )

    def is_null(self) -> bool:
        return (
            self.unk1 == 0
            and self.poke_id == 0
            and self.joined_at == 0
            and self.moves == [0] * 4
            and self.hp == 0
            and self.level == 0
            and self.iq == 0
            and self.atk == 0
            and self.sp_atk == 0
            and self.def_ == 0
            and self.sp_def == 0
            and self.unk3 == 0
            and self.exp == 0
        )

    def to_bytes(self) -> bytes:
        buffer = bytearray(0x24)

        write_u32(buffer, self.unk1, 0)
        write_u16(buffer, self.poke_id, 4)
        write_u16(buffer, self.joined_at, 6)
        write_u16(buffer, self.moves[0], 8)
        write_u16(buffer, self.moves[1], 10)
        write_u16(buffer, self.moves[2], 12)
        write_u16(buffer, self.moves[3], 14)
        write_u16(buffer, self.hp, 16)
        write_u16(buffer, self.level, 18)
        write_u16(buffer, self.iq, 20)
        write_u16(buffer, self.atk, 22)
        write_u16(buffer, self.sp_atk, 24)
        write_u16(buffer, self.def_, 26)
        write_u16(buffer, self.sp_def, 28)
        write_u16(buffer, self.unk3, 30)
        write_u32(buffer, self.exp, 32)

        return buffer

    @classmethod
    def from_bytes(cls, b: bytes) -> "GuestPokemon":
        return cls(
            read_u32(b, 0),
            read_u16(b, 4),
            read_u16(b, 6),
            [read_u16(b, 8), read_u16(b, 10), read_u16(b, 12), read_u16(b, 14)],
            read_u16(b, 16),
            read_u16(b, 18),
            read_u16(b, 20),
            read_u16(b, 22),
            read_u16(b, 24),
            read_u16(b, 26),
            read_u16(b, 28),
            read_u16(b, 30),
            read_u32(b, 32),
        )


class ExtraDungeonDataList:
    @staticmethod
    def read(arm9bin: bytes, config: Pmd2Data) -> List[ExtraDungeonDataEntry]:
        """Returns the list of extra dungeon data"""
        block = config.extra_bin_sections.arm9.data.EXTRA_DUNGEON_DATA
        lst = []
        for i in range(
            block.address, block.address + block.length, EXTRA_DUNGEON_DATA_ENTRY_SIZE
        ):
            lst.append(
                ExtraDungeonDataEntry.from_bytes(
                    read_bytes(arm9bin, i, EXTRA_DUNGEON_DATA_ENTRY_SIZE)
                )
            )
        return lst

    @staticmethod
    def write(
        lst: List[ExtraDungeonDataEntry], arm9bin: bytearray, config: Pmd2Data
    ) -> None:
        """
        Writes the list of dungeon extra data to the arm9 binary provided.
        The list must have exactly 0xB4 entries.
        """
        if len(lst) != EXTRA_DUNGEON_DATA_ENTRIES:
            raise ValueError(
                f"The extra dungeon data list must have exactly {EXTRA_DUNGEON_DATA_ENTRIES} entries."
            )

        block = config.extra_bin_sections.arm9.data.EXTRA_DUNGEON_DATA
        for i, entry in enumerate(lst):
            offset = block.address + i * EXTRA_DUNGEON_DATA_ENTRY_SIZE
            arm9bin[offset : offset + 2] = entry.to_bytes()[0:2]


class GuestPokemonList:
    @staticmethod
    def get_max_entries(config: Pmd2Data) -> int:
        """Returns the maximum amount of entries that can fit in the binary"""
        block1 = config.bin_sections.arm9.data.GUEST_MONSTER_DATA
        block2 = config.extra_bin_sections.arm9.data.GUEST_MONSTER_DATA2
        assert block1.length is not None
        assert block2.length is not None

        return (
            block1.length // GUEST_DATA_ENTRY_SIZE
            + block2.length // GUEST_DATA_ENTRY_SIZE
        )

    @staticmethod
    def read(arm9bin: bytes, config: Pmd2Data) -> List[GuestPokemon]:
        """Returns the list of guest pokémon data"""
        block = config.bin_sections.arm9.data.GUEST_MONSTER_DATA
        lst = []
        done = False
        # Read the first list
        for i in range(
            block.address, block.address + block.length, GUEST_DATA_ENTRY_SIZE
        ):
            read_entry = GuestPokemon.from_bytes(
                read_bytes(arm9bin, i, GUEST_DATA_ENTRY_SIZE)
            )
            if read_entry.is_null():
                done = True
                break
            lst.append(read_entry)
        if not done:
            # Read the list added by the EditExtraPokemon patch
            block = config.extra_bin_sections.arm9.data.GUEST_MONSTER_DATA2
            # Make sure we don't keep reading if there's no space for one more entry, since if we did that
            # we would read out of bounds
            for i in range(
                block.address,
                (block.address + block.length) - GUEST_DATA_ENTRY_SIZE + 1,
                GUEST_DATA_ENTRY_SIZE,
            ):
                read_entry = GuestPokemon.from_bytes(
                    read_bytes(arm9bin, i, GUEST_DATA_ENTRY_SIZE)
                )
                if read_entry.is_null():
                    break
                lst.append(read_entry)
        return lst

    @staticmethod
    def write(lst: List[GuestPokemon], arm9bin: bytearray, config: Pmd2Data) -> None:
        """
        Writes the list of guest pokémon data to the arm9 binary.
        The first 18 entries will be written to the GuestPokemonData block, the rest
        will be written to GuestPokemonData2.
        The list can't have more entries than the max amount specified by get_max_entries()
        """
        max_entries = GuestPokemonList.get_max_entries(config)
        if len(lst) > max_entries:
            raise ValueError(
                f"The guest pokémon data list can't have more than {max_entries} entries."
            )
        block1 = config.bin_sections.arm9.data.GUEST_MONSTER_DATA
        block2 = config.extra_bin_sections.arm9.data.GUEST_MONSTER_DATA2

        for i, value in enumerate(lst):
            if i < 18:
                offset = block1.address + i * GUEST_DATA_ENTRY_SIZE
                arm9bin[offset : offset + GUEST_DATA_ENTRY_SIZE] = lst[i].to_bytes()[
                    0:GUEST_DATA_ENTRY_SIZE
                ]
            else:
                offset = block2.address + (i - 18) * GUEST_DATA_ENTRY_SIZE
                arm9bin[offset : offset + GUEST_DATA_ENTRY_SIZE] = lst[i].to_bytes()[
                    0:GUEST_DATA_ENTRY_SIZE
                ]

        # Null the rest of the table
        for i in range(len(lst), max_entries):
            if i < 18:
                offset = block1.address + i * GUEST_DATA_ENTRY_SIZE
                arm9bin[offset : offset + GUEST_DATA_ENTRY_SIZE] = [
                    0
                ] * GUEST_DATA_ENTRY_SIZE
            else:
                offset = block2.address + (i - 18) * GUEST_DATA_ENTRY_SIZE
                arm9bin[offset : offset + GUEST_DATA_ENTRY_SIZE] = [
                    0
                ] * GUEST_DATA_ENTRY_SIZE
