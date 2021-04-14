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
from enum import Enum
from typing import Optional, Union

from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.container.sir0.sir0_util import decode_sir0_pointer_offsets
from skytemple_files.data.md.model import PokeType
from skytemple_files.data.waza_p import WAZA_MOVE_ENTRY_LEN
from skytemple_files.common.i18n_util import _

# TODO: Consider actually reading until the header later, in case modded games
#       have added move moves.
MOVE_COUNT = 559
MOVE_ENTRY_BYTELEN = 26


class LevelUpMove(AutoString):
    def __init__(self, move_id: int, level_id: int):
        self.move_id = move_id
        self.level_id = level_id

    def __eq__(self, other):
        if not isinstance(other, LevelUpMove):
            return False
        return self.move_id == other.move_id and self.level_id == other.level_id


class MoveLearnset(AutoString):
    def __init__(self, level_up_moves: List[LevelUpMove], tm_hm_moves: List[int], egg_moves: List[int]):
        self.level_up_moves = level_up_moves
        self.tm_hm_moves = tm_hm_moves
        self.egg_moves = egg_moves

    def __eq__(self, other):
        if not isinstance(other, MoveLearnset):
            return False
        return self.level_up_moves == other.level_up_moves \
               and self.tm_hm_moves == other.tm_hm_moves \
               and self.egg_moves == other.egg_moves


class WazaMoveCategory(Enum):
    PHYSICAL = 0, _("Physical Move")
    SPECIAL = 1, _("Special Move")
    STATUS = 2, _("Status Move")

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: str, name_localized: str
    ):
        self.name_localized = name_localized

    def __str__(self):
        return f'WazaMoveCategory.{self.name}'

    def __repr__(self):
        return str(self)

    @property
    def print_name(self):
        return self.name_localized


class WazaMoveRangeTarget(Enum):
    ENEMIES = 0, _("Enemies")
    ALLIES = 1, _("Allies")
    EVERYONE = 2, _("Everyone")
    USER = 3, _("User")
    TWO_TURN = 4, _("Two-turn move")
    EVERYONE_EXCEPT_USER = 5, _("Everyone except user")
    ALLIES_EXCEPT_USER = 6, _("All allies except user")
    U7 = 7, _("Invalid ") + "7"
    U8 = 8, _("Invalid ") + "8"
    U9 = 9, _("Invalid ") + "9"
    U10 = 10, _("Invalid ") + "10"
    U11 = 11, _("Invalid ") + "11"
    U12 = 12, _("Invalid ") + "12"
    U13 = 13, _("Invalid ") + "13"
    U14 = 14, _("Invalid ") + "14"
    SPECIAL = 15, _("Special / Invalid")

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: str, name_localized: str
    ):
        self.name_localized = name_localized

    def __str__(self):
        return f'WazaMoveRangeTarget.{self.name}'

    def __repr__(self):
        return str(self)

    @property
    def print_name(self):
        return self.name_localized


class WazaMoveRangeRange(Enum):
    IN_FRONT = 0, _("In front")
    TRHEE_IN_FRONT = 1, _("In front + adjacent (like Wide Slash)")
    AROUND = 2, _("8 tiles around user")
    ROOM = 3, _("Room")
    TWO_TILES = 4, _("Two tiles away")  # Also cuts corners, but the AI doesn't account for that
    STRAIGHT_LINE = 5, _("Straight line")
    FLOOR = 6, _("Floor")
    USER = 7, _("User")
    IN_FRONT_CORNERS = 8, _("In front; cuts corners")
    TWO_TILES_CORNERS = 9, _("Two tiles away; cuts corners")
    U10 = 10, _("Invalid ") + "10"
    U11 = 11, _("Invalid ") + "11"
    U12 = 12, _("Invalid ") + "12"
    U13 = 13, _("Invalid ") + "13"
    U14 = 14, _("Invalid ") + "14"
    SPECIAL = 15, _("Special / Invalid")

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: str, name_localized: str
    ):
        self.name_localized = name_localized

    def __str__(self):
        return f'WazaMoveRangeRange.{self.name}'

    def __repr__(self):
        return str(self)

    @property
    def print_name(self):
        return self.name_localized


class WazaMoveRangeCondition(Enum):
    """Only relevant for AI setting."""
    NO_CONDITION = 0, _("No condition")
    CHANCE_AI_WEIGHT = 1, _("Based on AI Condition 1 Chance")
    CRITICAL_HP = 2, _("Current HP <= 25%")
    NEGATIVE_STATUS = 3, _("Has at least one negative status condition")
    ASLEEP = 4, _("Is asleep, in a nightmare or napping")
    GHOST = 5, _("Is a ghost-type Pokémon and does not have the exposed status")
    CRITICAL_HP_NEGATIVE_STATUS = 6, _("Current HP <= 25% or has at least one negative status condition")
    U7 = 7, _("Invalid ") + "7"
    U8 = 8, _("Invalid ") + "8"
    U9 = 9, _("Invalid ") + "9"
    U10 = 10, _("Invalid ") + "10"
    U11 = 11, _("Invalid ") + "11"
    U12 = 12, _("Invalid ") + "12"
    U13 = 13, _("Invalid ") + "13"
    U14 = 14, _("Invalid ") + "14"
    U15 = 15, _("Invalid ") + "15"

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: str, name_localized: str
    ):
        self.name_localized = name_localized

    def __str__(self):
        return f'WazaMoveRangeCondition.{self.name}'

    def __repr__(self):
        return str(self)

    @property
    def print_name(self):
        return self.name_localized


class WazaMoveRangeSettings(AutoString):
    def __init__(self, data: Union[memoryview, bytes]):
        val = read_uintle(data, 0, 2)
        n4, n3, n2, n1 = val >> 12 & 0xf, val >> 8 & 0xf, val >> 4 & 0xf, val & 0xf
        self.target = WazaMoveRangeTarget(int(n1))
        self.range = WazaMoveRangeRange(int(n2))
        self.condition = WazaMoveRangeCondition(int(n3))
        self.unused = int(n4)

    def __int__(self):
        return (self.unused << 12) + (self.condition.value << 8) + (self.range.value << 4) + self.target.value

    def __eq__(self, other):
        if not isinstance(other, WazaMoveRangeSettings):
            return False
        return self.target == other.target and \
               self.range == other.range and \
               self.condition == other.condition and \
               self.unused == other.unused


class WazaMove(AutoString):
    def __init__(self, data: Union[memoryview, bytes]):
        # 0x00	2	uint16	Base Power	The base power of the move.
        self.base_power = read_uintle(data, 0x00, 2)
        # 0x02	1	uint8	Type	The type of the move.
        self.type = PokeType(read_uintle(data, 0x02))
        # 0x03	1	uint8	Category	What kind of move is it.
        self.category = WazaMoveCategory(read_uintle(data, 0x03))
        # 0x04	2	4xunit4	4 Nibbles enconding different values, see WazaMoveSettings. Actual values.
        self.settings_range = WazaMoveRangeSettings(data[0x04:0x06])
        assert read_uintle(data, 0x04, 2) == int(self.settings_range)
        # 0x06	2	4xunit4	4 Nibbles enconding different values, see WazaMoveSettings. Settings for AI calculation.
        self.settings_range_ai = WazaMoveRangeSettings(data[0x06:0x08])
        # 0x08	1	uint8	Base PPs	The base amount of PP for the move.
        self.base_pp = read_uintle(data, 0x08)
        # 0x09	1	uint8	Unk#6	Possibly move weight to specify how likely the AI will use the move.
        self.ai_weight = read_uintle(data, 0x09)
        # 0x0A	1	uint8	Unk#7	Possibly secondary accuracy value.
        # A different message will be shown if this accuracy test fails.
        self.miss_accuracy = read_uintle(data, 0x0A)
        # 0x0B	1	uint8	Move Accuracy
        # The percentage indicating the chances the move will succeed.
        # 100 is perfect accuracy. Anything higher than 100 is a never-miss move.
        self.accuracy = read_uintle(data, 0x0B)
        # 0x0C	1	uint8	Unk#9	Unknown.
        self.ai_condition1_chance = read_uintle(data, 0x0C)
        # 0x0D	1	uint8	Unk#10	Possibly the number of times a move hits in a row.
        self.number_chained_hits = read_uintle(data, 0x0D)
        # 0x0E	1	uint8	Unk#11	Max number of time the move can be powered up.
        self.max_upgrade_level = read_uintle(data, 0x0E)
        # 0x0F	1	uint8	Unk#12	Critical hit chance. 60 is apparently pretty much guaranteed crit.
        self.crit_chance = read_uintle(data, 0x0F)
        # 0x10	1	uint8	Unk#13	Boolean, whether the move is affected by magic coat.
        self.affected_by_magic_coat = bool(read_uintle(data, 0x10))
        # 0x11	1	uint8	Unk#14	Boolean, whether the move is affected by snatch.
        self.is_snatchable = bool(read_uintle(data, 0x11))
        # 0x12	1	uint8	Unk#15	Boolean, whether the move is disabled by the "muzzled" status.
        self.uses_mouth = bool(read_uintle(data, 0x12))
        # 0x13	1	uint8	Unk#16	Unknown.
        self.unk13 = read_uintle(data, 0x13)
        # 0x14	1	uint8	Unk#17	Boolean, whether the move can be used while taunted.
        self.ignores_taunted = bool(read_uintle(data, 0x14))
        # 0x15	1	uint8	Unk#18	Unknown. Possible bitfield.
        self.unk15 = read_uintle(data, 0x15)
        # 0x16	2	uint16	Move ID	The move's ID, possibly used by the game code for allocating resources and etc..
        self.move_id = read_uintle(data, 0x16, 2)
        # 0x18	1	uint8	Unk#19	Message ID offset that is displayed for the move.
        # 0 = Is default, higher values are added as string offset from the default string.
        self.message_id = read_uintle(data, 0x18)

    def to_bytes(self) -> bytes:
        data = bytearray(WAZA_MOVE_ENTRY_LEN)
        write_uintle(data, self.base_power, 0, 2)
        write_uintle(data, self.type.value, 2, 1)
        write_uintle(data, self.category.value, 3, 1)
        write_uintle(data, int(self.settings_range), 4, 2)
        write_uintle(data, int(self.settings_range_ai), 6, 2)
        write_uintle(data, self.base_pp, 8, 1)
        write_uintle(data, self.ai_weight, 9, 1)
        write_uintle(data, self.miss_accuracy, 10, 1)
        write_uintle(data, self.accuracy, 11, 1)
        write_uintle(data, self.ai_condition1_chance, 12, 1)
        write_uintle(data, self.number_chained_hits, 13, 1)
        write_uintle(data, self.max_upgrade_level, 14, 1)
        write_uintle(data, self.crit_chance, 15, 1)
        write_uintle(data, int(self.affected_by_magic_coat), 16, 1)
        write_uintle(data, int(self.is_snatchable), 17, 1)
        write_uintle(data, int(self.uses_mouth), 18, 1)
        write_uintle(data, self.unk13, 19, 1)
        write_uintle(data, int(self.ignores_taunted), 20, 1)
        write_uintle(data, self.unk15, 21, 1)
        write_uintle(data, self.move_id, 22, 2)
        write_uintle(data, self.message_id, 24, 1)
        return bytes(data)

    def __eq__(self, other):
        if not isinstance(other, WazaMove):
            return False
        return self.base_power == other.base_power and \
               self.type == other.type and \
               self.category == other.category and \
               self.settings_range == other.settings_range and \
               self.settings_range_ai == other.settings_range_ai and \
               self.base_pp == other.base_pp and \
               self.ai_weight == other.ai_weight and \
               self.miss_accuracy == other.miss_accuracy and \
               self.accuracy == other.accuracy and \
               self.ai_condition1_chance == other.ai_condition1_chance and \
               self.number_chained_hits == other.number_chained_hits and \
               self.max_upgrade_level == other.max_upgrade_level and \
               self.crit_chance == other.crit_chance and \
               self.affected_by_magic_coat == other.affected_by_magic_coat and \
               self.is_snatchable == other.is_snatchable and \
               self.uses_mouth == other.uses_mouth and \
               self.unk13 == other.unk13 and \
               self.ignores_taunted == other.ignores_taunted and \
               self.unk15 == other.unk15 and \
               self.move_id == other.move_id and \
               self.message_id == other.message_id


class WazaP(Sir0Serializable, AutoString):
    def __init__(self, data: bytes, waza_content_pointer: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        move_data_pointer = read_uintle(data, waza_content_pointer, 4)
        move_learnset_pointer = read_uintle(data, waza_content_pointer + 4, 4)

        self.moves = list(self._read_moves(data[move_data_pointer:move_data_pointer+(MOVE_COUNT*MOVE_ENTRY_BYTELEN)]))

        self.learnsets: List[MoveLearnset] = []
        i = 0
        while True:
            if move_learnset_pointer+(i*12) >= waza_content_pointer:
                break
            list_pointers = data[move_learnset_pointer+(i*12):move_learnset_pointer+((i+1)*12)]
            level_up = []
            tm_hm = []
            egg = []

            pointer_level_up = read_uintle(list_pointers, 0, 4)
            pointer_tm_hm = read_uintle(list_pointers, 4, 4)
            pointer_egg = read_uintle(list_pointers, 8, 4)
            if pointer_level_up == 0xAAAAAAAA or pointer_tm_hm == 0xAAAAAAAA or pointer_egg == 0xAAAAAAAA:
                break

            # Read Level Up Data
            if pointer_level_up != 0:
                level_up_raw = self._decode_ints(data, pointer_level_up)
                for move_id, level_id in chunks(level_up_raw, 2):
                    level_up.append(LevelUpMove(move_id, level_id))

            # TM/HM Move data
            if pointer_tm_hm:
                tm_hm = self._decode_ints(data, pointer_tm_hm)

            # TM/HM Move data
            if pointer_egg:
                egg = self._decode_ints(data, pointer_egg)

            self.learnsets.append(MoveLearnset(
                level_up, tm_hm, egg
            ))
            i += 1

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int,
                    static_data: Optional[Pmd2Data] = None) -> 'Sir0Serializable':
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.data.waza_p.writer import WazaPWriter
        return WazaPWriter(self).write()

    def __eq__(self, other):
        if not isinstance(other, WazaP):
            return False
        return self.learnsets == other.learnsets and self.moves == other.moves

    @staticmethod
    def _decode_ints(data: bytes, pnt_start: int) -> List[int]:
        return decode_sir0_pointer_offsets(data, pnt_start, False)

    def _read_moves(self, moves: Union[bytes, memoryview]) -> Iterable[WazaMove]:
        for data in chunks(moves, WAZA_MOVE_ENTRY_LEN):
            yield WazaMove(data)
