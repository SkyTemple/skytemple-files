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

from typing import Optional, Union, MutableSequence, Sequence, List, Tuple, Iterable

from range_typed_integers import u32_checked, u16, u32, u8
from skytemple_files.common.i18n_util import _
from skytemple_files.common.util import (
    AutoString,
    chunks,
    write_u32,
    read_u8,
    read_u16,
    write_u16,
    read_u32,
    write_u8,
)
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.container.sir0.sir0_util import (
    decode_sir0_pointer_offsets,
    encode_sir0_pointer_offsets,
)
from skytemple_files.data.waza_p import WAZA_MOVE_ENTRY_LEN
from skytemple_files.data.waza_p.protocol import (
    LevelUpMoveProtocol,
    MoveLearnsetProtocol,
    WazaMoveRangeSettingsProtocol,
    WazaMoveProtocol,
    _WazaMoveCategory,
    WazaPProtocol,
    _PokeType,
)

# TODO: Consider actually reading until the header later, in case modded games
#       have added more moves.
MOVE_COUNT = 559
MOVE_ENTRY_BYTELEN = 26


class LevelUpMove(LevelUpMoveProtocol, AutoString):
    move_id: u16
    level_id: u16

    def __init__(self, move_id: u16, level_id: u16):
        self.move_id = move_id
        self.level_id = level_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LevelUpMove):
            return False
        return self.move_id == other.move_id and self.level_id == other.level_id


class MoveLearnset(MoveLearnsetProtocol[LevelUpMove], AutoString):
    level_up_moves: MutableSequence[LevelUpMove]
    tm_hm_moves: MutableSequence[u32]
    egg_moves: MutableSequence[u32]

    def __init__(
        self,
        level_up_moves: Sequence[LevelUpMove],
        tm_hm_moves: Sequence[u32],
        egg_moves: Sequence[u32],
    ):
        self.level_up_moves = list(level_up_moves)
        self.tm_hm_moves = list(tm_hm_moves)
        self.egg_moves = list(egg_moves)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MoveLearnset):
            return False
        return (
            self.level_up_moves == other.level_up_moves
            and self.tm_hm_moves == other.tm_hm_moves
            and self.egg_moves == other.egg_moves
        )


class WazaMoveRangeSettings(WazaMoveRangeSettingsProtocol, AutoString):
    def __init__(self, data: bytes):
        val = read_u16(data, 0)
        n4, n3, n2, n1 = val >> 12 & 0xF, val >> 8 & 0xF, val >> 4 & 0xF, val & 0xF
        self.target = int(n1)
        self.range = int(n2)
        self.condition = int(n3)
        self.unused = int(n4)

    def __int__(self):
        return (
            (self.unused << 12)
            + (self.condition << 8)
            + (self.range << 4)
            + self.target
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WazaMoveRangeSettings):
            return False
        return (
            self.target == other.target
            and self.range == other.range
            and self.condition == other.condition
            and self.unused == other.unused
        )


class WazaMove(WazaMoveProtocol[WazaMoveRangeSettings], AutoString):
    base_power: u16
    type: _PokeType
    category: _WazaMoveCategory
    settings_range: WazaMoveRangeSettings
    settings_range_ai: WazaMoveRangeSettings
    base_pp: u8
    ai_weight: u8
    miss_accuracy: u8
    accuracy: u8
    ai_condition1_chance: u8
    number_chained_hits: u8
    max_upgrade_level: u8
    crit_chance: u8
    affected_by_magic_coat: bool
    is_snatchable: bool
    uses_mouth: bool
    ai_frozen_check: bool
    ignores_taunted: bool
    range_check_text: u8
    move_id: u16
    message_id: u8

    def __init__(self, data: bytes):
        # 0x00	2	uint16	Base Power	The base power of the move.
        self.base_power = read_u16(data, 0x00)
        # 0x02	1	uint8	Type	The type of the move.
        self.type = read_u8(data, 0x02)
        # 0x03	1	uint8	Category	What kind of move is it.
        self.category = read_u8(data, 0x03)
        # 0x04	2	4xunit4	4 Nibbles enconding different values, see WazaMoveSettings. Actual values.
        self.settings_range = WazaMoveRangeSettings(data[0x04:0x06])
        assert read_u16(data, 0x04) == int(self.settings_range)
        # 0x06	2	4xunit4	4 Nibbles enconding different values, see WazaMoveSettings. Settings for AI calculation.
        self.settings_range_ai = WazaMoveRangeSettings(data[0x06:0x08])
        # 0x08	1	uint8	Base PPs	The base amount of PP for the move.
        self.base_pp = read_u8(data, 0x08)
        # 0x09	1	uint8	Unk#6	Possibly move weight to specify how likely the AI will use the move.
        self.ai_weight = read_u8(data, 0x09)
        # 0x0A	1	uint8	Unk#7	Possibly secondary accuracy value.
        # A different message will be shown if this accuracy test fails.
        self.miss_accuracy = read_u8(data, 0x0A)
        # 0x0B	1	uint8	Move Accuracy
        # The percentage indicating the chances the move will succeed.
        # 100 is perfect accuracy. Anything higher than 100 is a never-miss move.
        self.accuracy = read_u8(data, 0x0B)
        # 0x0C	1	uint8	Unk#9	Unknown.
        self.ai_condition1_chance = read_u8(data, 0x0C)
        # 0x0D	1	uint8	Unk#10	Possibly the number of times a move hits in a row.
        self.number_chained_hits = read_u8(data, 0x0D)
        # 0x0E	1	uint8	Unk#11	Max number of time the move can be powered up.
        self.max_upgrade_level = read_u8(data, 0x0E)
        # 0x0F	1	uint8	Unk#12	Critical hit chance. 60 is apparently pretty much guaranteed crit.
        self.crit_chance = read_u8(data, 0x0F)
        # 0x10	1	uint8	Unk#13	Boolean, whether the move is affected by magic coat.
        self.affected_by_magic_coat = bool(read_u8(data, 0x10))
        # 0x11	1	uint8	Unk#14	Boolean, whether the move is affected by snatch.
        self.is_snatchable = bool(read_u8(data, 0x11))
        # 0x12	1	uint8	Unk#15	Boolean, whether the move is disabled by the "muzzled" status.
        self.uses_mouth = bool(read_u8(data, 0x12))
        # 0x13	1	uint8	Unk#16	If true, the AI won't try to use the move on frozen targets.
        self.ai_frozen_check = bool(read_u8(data, 0x13))
        # 0x14	1	uint8	Unk#17	Boolean, whether the move can be used while taunted.
        self.ignores_taunted = bool(read_u8(data, 0x14))
        # 0x15	1	uint8	Unk#18	Determines the string that is displayed for the range of the move in-game
        self.range_check_text = read_u8(data, 0x15)
        # 0x16	2	uint16	Move ID	The move's ID, possibly used by the game code for allocating resources and etc..
        self.move_id = read_u16(data, 0x16)
        # 0x18	1	uint8	Unk#19	Message ID offset that is displayed for the move.
        # 0 = Is default, higher values are added as string offset from the default string.
        self.message_id = read_u8(data, 0x18)

    def to_bytes(self) -> bytes:
        data = bytearray(WAZA_MOVE_ENTRY_LEN)
        write_u16(data, self.base_power, 0)
        write_u8(data, self.type, 2)
        write_u8(data, self.category, 3)
        write_u16(data, u16(int(self.settings_range)), 4)
        write_u16(data, u16(int(self.settings_range_ai)), 6)
        write_u8(data, self.base_pp, 8)
        write_u8(data, self.ai_weight, 9)
        write_u8(data, self.miss_accuracy, 10)
        write_u8(data, self.accuracy, 11)
        write_u8(data, self.ai_condition1_chance, 12)
        write_u8(data, self.number_chained_hits, 13)
        write_u8(data, self.max_upgrade_level, 14)
        write_u8(data, self.crit_chance, 15)
        write_u8(data, u8(int(self.affected_by_magic_coat)), 16)
        write_u8(data, u8(int(self.is_snatchable)), 17)
        write_u8(data, u8(int(self.uses_mouth)), 18)
        write_u8(data, u8(int(self.ai_frozen_check)), 19)
        write_u8(data, u8(int(self.ignores_taunted)), 20)
        write_u8(data, self.range_check_text, 21)
        write_u16(data, self.move_id, 22)
        write_u8(data, self.message_id, 24)
        return bytes(data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WazaMove):
            return False
        return (
            self.base_power == other.base_power
            and self.type == other.type
            and self.category == other.category
            and self.settings_range == other.settings_range
            and self.settings_range_ai == other.settings_range_ai
            and self.base_pp == other.base_pp
            and self.ai_weight == other.ai_weight
            and self.miss_accuracy == other.miss_accuracy
            and self.accuracy == other.accuracy
            and self.ai_condition1_chance == other.ai_condition1_chance
            and self.number_chained_hits == other.number_chained_hits
            and self.max_upgrade_level == other.max_upgrade_level
            and self.crit_chance == other.crit_chance
            and self.affected_by_magic_coat == other.affected_by_magic_coat
            and self.is_snatchable == other.is_snatchable
            and self.uses_mouth == other.uses_mouth
            and self.ai_frozen_check == other.ai_frozen_check
            and self.ignores_taunted == other.ignores_taunted
            and self.range_check_text == other.range_check_text
            and self.move_id == other.move_id
            and self.message_id == other.message_id
        )


class WazaP(WazaPProtocol[WazaMove, MoveLearnset], Sir0Serializable, AutoString):
    moves: MutableSequence[WazaMove]
    learnsets: MutableSequence[MoveLearnset]

    def __init__(self, data: bytes, waza_content_pointer: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        move_data_pointer = read_u32(data, waza_content_pointer)
        move_learnset_pointer = read_u32(data, waza_content_pointer + 4)

        self.moves = list(
            self._read_moves(
                data[
                    move_data_pointer : move_data_pointer
                    + (MOVE_COUNT * MOVE_ENTRY_BYTELEN)
                ]
            )
        )

        self.learnsets: List[MoveLearnset] = []
        i = 0
        while True:
            if move_learnset_pointer + (i * 12) >= waza_content_pointer:
                break
            list_pointers = data[
                move_learnset_pointer
                + (i * 12) : move_learnset_pointer
                + ((i + 1) * 12)
            ]
            level_up = []
            tm_hm: Sequence[u32] = []
            egg: Sequence[u32] = []

            pointer_level_up = read_u32(list_pointers, 0)
            pointer_tm_hm = read_u32(list_pointers, 4)
            pointer_egg = read_u32(list_pointers, 8)
            if (
                pointer_level_up == 0xAAAAAAAA
                or pointer_tm_hm == 0xAAAAAAAA
                or pointer_egg == 0xAAAAAAAA
            ):
                break

            # Read Level Up Data
            if pointer_level_up != 0:
                level_up_raw = self._decode_ints(data, pointer_level_up)
                for move_id, level_id in chunks(level_up_raw, 2):
                    level_up.append(LevelUpMove(u16(move_id), u16(level_id)))

            # TM/HM Move data
            if pointer_tm_hm:
                tm_hm = self._decode_ints(data, pointer_tm_hm)

            # TM/HM Move data
            if pointer_egg:
                egg = self._decode_ints(data, pointer_egg)

            self.learnsets.append(MoveLearnset(level_up, tm_hm, egg))
            i += 1

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: u32,
    ) -> "Sir0Serializable":
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[u32], Optional[u32]]:
        pointer_offsets: List[u32] = []
        data = bytearray(3)
        # Learnset
        learnset_pointers: List[Tuple[u32, u32, u32]] = []
        for learnset in self.learnsets:
            # Level Up
            pnt_lvlup = len(data)
            buff = bytearray(8 * (len(learnset.level_up_moves) + 1))
            lvl_up_move_list = []
            for lvl_up_move in learnset.level_up_moves:
                lvl_up_move_list.append(lvl_up_move.move_id)
                lvl_up_move_list.append(lvl_up_move.level_id)
            c = encode_sir0_pointer_offsets(buff, lvl_up_move_list, False)
            data += buff[:c]
            # TM/HM
            pnt_tm_hm = len(data)
            buff = bytearray(4 * (len(learnset.tm_hm_moves) + 1))
            c = encode_sir0_pointer_offsets(buff, learnset.tm_hm_moves, False)
            data += buff[:c]
            # Egg
            pnt_egg = len(data)
            buff = bytearray(4 * (len(learnset.egg_moves) + 1))
            c = encode_sir0_pointer_offsets(buff, learnset.egg_moves, False)
            data += buff[:c]

            learnset_pointers.append(
                (u32_checked(pnt_lvlup), u32_checked(pnt_tm_hm), u32_checked(pnt_egg))
            )
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        # Move data
        move_pointer = len(data)
        for move in self.moves:
            data += move.to_bytes()
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        # Learnset pointer table
        learnset_pointer_table_pnt = len(data)
        learnset_pointer_table = bytearray(len(learnset_pointers) * 12)
        for i, (lvlup, tm_hm, egg) in enumerate(learnset_pointers):
            pointer_offsets.append(u32(len(data) + i * 12))
            pointer_offsets.append(u32(len(data) + i * 12 + 4))
            pointer_offsets.append(u32(len(data) + i * 12 + 8))
            write_u32(learnset_pointer_table, lvlup, i * 12)
            write_u32(learnset_pointer_table, tm_hm, i * 12 + 4)
            write_u32(learnset_pointer_table, egg, i * 12 + 8)
        data += learnset_pointer_table
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        # Waza Header (<- content pointer)
        header = bytearray(8)
        waza_header_start = u32(len(data))
        pointer_offsets.append(waza_header_start)
        write_u32(header, u32_checked(move_pointer), 0)
        pointer_offsets.append(u32(waza_header_start + 4))
        write_u32(header, u32_checked(learnset_pointer_table_pnt), 4)
        data += header
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        return data, pointer_offsets, waza_header_start

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WazaP):
            return False
        return self.learnsets == other.learnsets and self.moves == other.moves

    @staticmethod
    def _decode_ints(data: bytes, pnt_start: u32) -> Sequence[u32]:
        return decode_sir0_pointer_offsets(data, pnt_start, False)

    def _read_moves(self, moves: Union[bytes, memoryview]) -> Iterable[WazaMove]:
        for data in chunks(moves, WAZA_MOVE_ENTRY_LEN):
            yield WazaMove(data)  # type: ignore
