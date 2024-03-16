"""
Code to generate Wonder Mail S codes and in the future other types of mail.

Main source: https://github.com/dengler9/wmsgenerator
"""

#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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

import string
from math import floor
from typing import Optional, Type, TypeVar, cast

from range_typed_integers import u8, get_range, IntegerBoundError

from skytemple_files.common.bit_stream import BitStream
from skytemple_files.common.ppmdu_config.data import GAME_REGION_US, GAME_REGION_EU
from skytemple_files.common.util import u4, u24, u11, u10, chunks

# Some more references used:
# https://github.com/UsernameFodder/pmdsky-debug/blob/26ac048819b1b79c5babf647b099dda2f9639f62/headers/types/common/common.h#L785-L810
# https://github.com/UsernameFodder/pmdsky-debug/blob/26ac048819b1b79c5babf647b099dda2f9639f62/headers/types/dungeon_mode/enums.h#L719-L841


# TYPES AND CONSTANTS
MissionType = u4
MissionSubtype = u4

MISSION_TYPE_RESCUE_CLIENT = u4(0)

MISSION_TYPE_RESCUE_TARGET = u4(1)

MISSION_TYPE_ESCORT_TO_TARGET = u4(2)

MISSION_TYPE_EXPLORE_WITH_CLIENT = u4(3)
MISSION_TYPE_EXPLORE_WITH_CLIENT__NORMAL = u4(0)
MISSION_TYPE_EXPLORE_WITH_CLIENT__SEALED_CHAMBER = u4(1)
MISSION_TYPE_EXPLORE_WITH_CLIENT__GOLDEN_CHAMBER = u4(2)
MISSION_TYPE_EXPLORE_WITH_CLIENT__NEW_DUNGEON = u4(3)

MISSION_TYPE_PROSPECT_WITH_CLIENT = u4(4)

MISSION_TYPE_GUIDE_CLIENT = u4(5)

MISSION_TYPE_FIND_ITEM = u4(6)

MISSION_TYPE_DELIVER_ITEM = u4(7)

MISSION_TYPE_SEARCH_FOR_TARGET = u4(8)

MISSION_TYPE_TAKE_ITEM_FROM_OUTLAW = u4(9)
MISSION_TYPE_TAKE_ITEM_FROM_OUTLAW__NORMAL_OUTLAW = u4(0)
MISSION_TYPE_TAKE_ITEM_FROM_OUTLAW__HIDDEN_OUTLAW = u4(1)
MISSION_TYPE_TAKE_ITEM_FROM_OUTLAW__FLEEING_OUTLAW = u4(2)

MISSION_TYPE_ARREST_OUTLAW = u4(10)
MISSION_TYPE_ARREST_OUTLAW__NORMAL_0 = u4(0)
MISSION_TYPE_ARREST_OUTLAW__NORMAL_1 = u4(1)
MISSION_TYPE_ARREST_OUTLAW__NORMAL_2 = u4(2)
MISSION_TYPE_ARREST_OUTLAW__NORMAL_3 = u4(3)
MISSION_TYPE_ARREST_OUTLAW__ESCORT = u4(4)
MISSION_TYPE_ARREST_OUTLAW__FLEEING = u4(5)
MISSION_TYPE_ARREST_OUTLAW__HIDEOUT = u4(6)
MISSION_TYPE_ARREST_OUTLAW__MONSTER_HOUSE = u4(7)

MISSION_TYPE_CHALLENGE_REQUEST = u4(11)
MISSION_TYPE_CHALLENGE_REQUEST__NORMAL = u4(0)
MISSION_TYPE_CHALLENGE_REQUEST__MEWTWO = u4(1)
MISSION_TYPE_CHALLENGE_REQUEST__ENTEI = u4(2)
MISSION_TYPE_CHALLENGE_REQUEST__RAIKOU = u4(3)
MISSION_TYPE_CHALLENGE_REQUEST__SUICUNE = u4(4)
MISSION_TYPE_CHALLENGE_REQUEST__JIRACHI = u4(5)

MISSION_TYPE_TREASURE_MEMO = u4(12)

MISSION_TYPE_SPECIAL_EPISODE = u4(14)

RestrictionType = bool  # Usually one of the RESTRICTION_TYPE constants below
# In this case restriction should be type ID. 0 for no restriction.
RESTRICTION_TYPE_TYPE_OR_NONE = False
# In this case restriction should be a monster ID.
RESTRICTION_TYPE_MONSTER = True

RewardType = u4
# TODO: These values are from pmdsky-debug. Confirm!
REWARD_TYPE_MONEY = u4(0)
# Money + (?)
REWARD_TYPE_MONEY_AND_MORE = u4(1)
REWARD_TYPE_ITEM = u4(2)
# Item + (?)
REWARD_TYPE_ITEM_AND_MORE = u4(3)
# Item, displayed as "(?)"
REWARD_TYPE_ITEM_HIDDEN = u4(4)
# Money, displayed as "(?)"
REWARD_TYPE_MONEY_HIDDEN = u4(5)
# Either an egg or the client requests to join the team, displayed as "(?)":
REWARD_TYPE_SPECIAL = u4(6)

# Other constants
_DEBUG = False
_LEN_MAIL_WO_CHECKSUM = 138
_OFFSET_CHECKSUM_START = 2
_LEN_CHECKSUM = 32

# fmt: off
# Encryption data. From source.
_ENCRYPTION_DATA = [
    # Listed vertical: first part of the 2-character hex code range
    # Listed horizontal: second part of the 2-character hex code
    # 0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F
    0x2E, 0x75, 0x3F, 0x99, 0x09, 0x6C, 0xBC, 0x61, 0x7C, 0x2A, 0x96, 0x4A, 0xF4, 0x6D, 0x29, 0xFA, # 00-0F
    0x90, 0x14, 0x9D, 0x33, 0x6F, 0xCB, 0x49, 0x3C, 0x48, 0x80, 0x7B, 0x46, 0x67, 0x01, 0x17, 0x59, # 10-1F
    0xB8, 0xFA, 0x70, 0xC0, 0x44, 0x78, 0x48, 0xFB, 0x26, 0x80, 0x81, 0xFC, 0xFD, 0x61, 0x70, 0xC7, # 20-2F
    0xFE, 0xA8, 0x70, 0x28, 0x6C, 0x9C, 0x07, 0xA4, 0xCB, 0x3F, 0x70, 0xA3, 0x8C, 0xD6, 0xFF, 0xB0, # 30-3F
    0x7A, 0x3A, 0x35, 0x54, 0xE9, 0x9A, 0x3B, 0x61, 0x16, 0x41, 0xE9, 0xA3, 0x90, 0xA3, 0xE9, 0xEE, # 40-4F
    0x0E, 0xFA, 0xDC, 0x9B, 0xD6, 0xFB, 0x24, 0xB5, 0x41, 0x9A, 0x20, 0xBA, 0xB3, 0x51, 0x7A, 0x36, # 50-5F
    0x3E, 0x60, 0x0E, 0x3D, 0x02, 0xB0, 0x34, 0x57, 0x69, 0x81, 0xEB, 0x67, 0xF3, 0xEB, 0x8C, 0x47, # 60-6F
    0x93, 0xCE, 0x2A, 0xAF, 0x35, 0xF4, 0x74, 0x87, 0x50, 0x2C, 0x39, 0x68, 0xBB, 0x47, 0x1A, 0x02, # 70-7F
    0xA3, 0x93, 0x64, 0x2E, 0x8C, 0xAD, 0xB1, 0xC4, 0x61, 0x04, 0x5F, 0xBD, 0x59, 0x21, 0x1C, 0xE7, # 80-8F
    0x0E, 0x29, 0x26, 0x97, 0x70, 0xA9, 0xCD, 0x18, 0xA3, 0x7B, 0x74, 0x70, 0x96, 0xDE, 0xA6, 0x72, # 90-9F
    0xDD, 0x13, 0x93, 0xAA, 0x90, 0x6C, 0xA7, 0xB5, 0x76, 0x2F, 0xA8, 0x7A, 0xC8, 0x81, 0x06, 0xBB, # A0-AF
    0x85, 0x75, 0x11, 0x0C, 0xD2, 0xD1, 0xC9, 0xF8, 0x81, 0x70, 0xEE, 0xC8, 0x71, 0x53, 0x3D, 0xAF, # B0-BF
    0x76, 0xCB, 0x0D, 0xC1, 0x56, 0x28, 0xE8, 0x3C, 0x61, 0x64, 0x4B, 0xB8, 0xEF, 0x3B, 0x41, 0x09, # C0-CF
    0x72, 0x07, 0x50, 0xAD, 0xF3, 0x2E, 0x5C, 0x43, 0xFF, 0xC3, 0xB3, 0x32, 0x7A, 0x3E, 0x9C, 0xA3, # D0-DF
    0xC2, 0xAB, 0x10, 0x60, 0x99, 0xFB, 0x08, 0x8A, 0x90, 0x57, 0x8A, 0x7F, 0x61, 0x90, 0x21, 0x88, # E0-EF
    0x55, 0xE8, 0xFC, 0x4B, 0x0D, 0x4A, 0x7A, 0x48, 0xC9, 0xB0, 0xC7, 0xA6, 0xD0, 0x04, 0x7E, 0x05  # F0-FF
]
# fmt: on

# Each WM byte maps to these bit values
# http://www.gamefaqs.com/boards/genmessage.php?board=938931&topic=42726909&page=9
# http://www.gamefaqs.com/boards/genmessage.php?board=938931&topic=42949038
_BIT_VALUES = "&67NPR89F0+#STXY45MCHJ-K12=%3Q@W"

# fmt: off
# Byte-swap patterns
# NA: 07 1B 0D 1F 15 1A 06 01 17 1C 09 1E 0A 20 10 21 0F 08 1D 11 14 00 13 16 05 12 0E 04 03 18 02 0B 0C 19
# http://www.gamefaqs.com/boards/detail.php?board=955859&topic=51920426&message=571612360
_BYTE_SWAP_NA = [
    0x07, 0x1B, 0x0D, 0x1F, 0x15, 0x1A, 0x06, 0x01,
    0x17, 0x1C, 0x09, 0x1E, 0x0A, 0x20, 0x10, 0x21,
    0x0F, 0x08, 0x1D, 0x11, 0x14, 0x00, 0x13, 0x16,
    0x05, 0x12, 0x0E, 0x04, 0x03, 0x18, 0x02, 0x0B,
    0x0C, 0x19
]
_BYTE_SWAP_EU = [
    0x0E, 0x04, 0x03, 0x18, 0x09, 0x1E, 0x0A, 0x20,
    0x10, 0x21, 0x14, 0x00, 0x13, 0x16, 0x05, 0x12,
    0x06, 0x01, 0x17, 0x1C, 0x07, 0x1B, 0x0D, 0x1F,
    0x15, 0x1A, 0x02, 0x0B, 0x0C, 0x19, 0x0F, 0x08,
    0x1D, 0x11
]
# fmt: on

T = TypeVar("T", bound=int)


# Implementation
class Mail:
    """A Mail. Currently only Wonder Mail S is properly and fully implemented. See subclass `WonderMailS`."""

    _OFFSET_MAIL_TYPE = 134
    _OFFSET_MAIL_TYPE_END = _OFFSET_MAIL_TYPE + 4

    # Data of the mail as a 138 bits stream. A 32 bit checksum is added at the end before code conversion, that
    # checksum is only done for the 136 bits at the end (first two bits skipped).
    _data: BitStream

    def __init__(self):
        raise TypeError(
            "The Mail base class can not be directly instantiated. Use a subclass or from_*_bits."
        )

    def mail_type(self) -> Type[Mail]:
        return Mail._determine_type_of(self._data)

    @classmethod
    def from_decrypted_bits(
        cls, input_data: BitStream | bytes, ignore_checksum=False
    ) -> Mail:
        """
        Tries to initialize mail from raw struct data. These bits need to be decrypted already.
        Returns subclass based on mail type (if a specialized subclass is available).
        """
        data_full = BitStream(input_data[0 : _LEN_MAIL_WO_CHECKSUM + _LEN_CHECKSUM])
        if len(data_full) < _LEN_MAIL_WO_CHECKSUM + _LEN_CHECKSUM:
            raise ValueError("Not enough data for mail.")
        typ = cls._determine_type_of(data_full)
        slf = typ.__new__(typ)
        slf._data = BitStream(input_data[0:_LEN_MAIL_WO_CHECKSUM])
        if not ignore_checksum:
            actual_checksum = data_full[len(data_full) - _LEN_CHECKSUM : len(data_full)]
            expected_checksum = slf.checksum()
            if expected_checksum != actual_checksum:
                raise ValueError(
                    f"Checksum mismatch for mail. Expected checksum: {expected_checksum.to_bytes().hex()}, got {actual_checksum.to_bytes().hex()}"
                )
        return slf

    @classmethod
    def from_encrypted_bits(cls, input_data: BitStream | bytes) -> Mail:
        """
        Tries to initialize mail from an encrypted stream of bits.
        Returns subclass based on mail type (if a specialized subclass is available).
        """
        return cls.from_decrypted_bits(mail_decrypt(BitStream(input_data)))

    @classmethod
    def from_code(cls, code: str, region: str) -> Mail:
        """
        Tries to initialize mail from a mail code. Whitespaces and new lines are removed.
        Returns subclass based on mail type (if a specialized subclass is available).

        Region is one of the GAME_REGION_* constants. Currently, EU and NA are supported.
        """
        return cls.from_encrypted_bits(mail_code_to_bits(code, region))

    def to_decrypted_bits(self) -> BitStream:
        """Converts the code into a bit stream, including valid checksum."""
        return self._data + self.checksum()

    def to_encrypted_bits(self) -> BitStream:
        """Converts the code into a bit stream (encrypted form), including valid checksum."""
        return mail_encrypt(self.to_decrypted_bits())

    def to_code(self, region: str) -> str:
        """
        Converts the mail into a code.

        Region is one of the GAME_REGION_* constants. Currently, EU and NA are supported.
        """
        return _pretty_mail_string(
            bits_to_mail_code(self.to_encrypted_bits(), region), 2, 7
        )

    def checksum(self) -> BitStream:
        """Calculates and returns the current checksum."""
        return checksum(self._data)

    @classmethod
    def _determine_type_of(cls, data: BitStream) -> Type[Mail]:
        type_id = data[cls._OFFSET_MAIL_TYPE : cls._OFFSET_MAIL_TYPE_END].to_number()
        if type_id == WonderMailS.MAIL_TYPE:
            return WonderMailS
        return Mail

    def _get(self, offset: int, length: int, typ: type[T]) -> T:
        raw = self._data[offset : offset + length]

        if typ == bool:
            return typ(raw[0])

        r = get_range(typ)
        number = raw.to_number("little", signed=(r is not None and r.min < 0))
        if _DEBUG:
            assert r
            if not r.min <= number <= r.max:
                raise IntegerBoundError(
                    f"Value {number} is out of range for {typ} (must be between {r.min} and {r.max})"
                )
        return typ(number)

    def _set(self, offset: int, length: int, typ: type[T], value: T):
        if typ == bool:
            assert isinstance(value, bool)
        else:
            r = get_range(typ)
            if r is not None:
                if not r.min <= value <= r.max:
                    raise IntegerBoundError(
                        f"Value {value} is out of range for {typ} (must be between {r.min} and {r.max})"
                    )
        self._data[offset : offset + length] = value

    def __str__(self):
        return self.to_code(GAME_REGION_EU)

    def __repr__(self):
        return f'{self.__class__.__name__}.from_code("{str(self).translate({ord(c): None for c in string.whitespace})}", GAME_REGION_EU)'


class WonderMailS(Mail):
    """A Wonder Mail S"""

    MAIL_TYPE = 4

    _OFFSET_NULL_BITS = 0
    _OFFSET_FIXED_ROOM = 8
    _OFFSET_FLOOR = 16
    _OFFSET_DUNGEON = 24
    _OFFSET_DESCRIPTION_ID = 32
    _OFFSET_RESTRICTION = 56
    _OFFSET_RESTRICTION_TYPE = 67
    _OFFSET_REWARD_ITEM = 68
    _OFFSET_REWARD_TYPE = 79
    _OFFSET_TARGET_ITEM = 83
    _OFFSET_OUTLAW_BACKUP_SPECIES = 93
    _OFFSET_TARGET_MONSTER = 104
    _OFFSET_CLIENT = 115
    _OFFSET_MISSION_SUBTYPE = 126
    _OFFSET_MISSION_TYPE = 130

    # noinspection PyMissingConstructor
    def __init__(
        self,
        *,
        floor: u8,
        dungeon: u8,
        mission_type: MissionType,
        mission_subtype: Optional[MissionSubtype],
        null_bits: u8 = u8(0),
        fixed_room: u8 = u8(0),
        description_id: u24 = u24(0),
        restriction: u11 = u11(0),
        restriction_type: RestrictionType = RESTRICTION_TYPE_TYPE_OR_NONE,
        reward_item: u11 = u11(0),
        reward_type: RewardType = REWARD_TYPE_MONEY,
        target_item: u10 = u10(0),
        target_monster: u11 = u11(0),
        outlaw_backup_species: u11 = u11(0),
        client: u11 = u11(0),
    ):
        """
        Create a new Wonder Mail S. There is no validation.
        See getter docstrings for documentation of the properties.
        """
        self._data = BitStream([False] * _LEN_MAIL_WO_CHECKSUM)

        self.null_bits = null_bits
        self.fixed_room = fixed_room
        self.floor = floor
        self.dungeon = dungeon
        self.description_id = description_id
        self.restriction = restriction
        self.restriction_type = restriction_type
        self.reward_item = reward_item
        self.reward_type = reward_type
        self.target_item = target_item
        self.outlaw_backup_species = outlaw_backup_species
        self.target_monster = target_monster
        self.client = client
        self.mission_subtype = mission_subtype if mission_subtype is not None else u4(0)
        self.mission_type = mission_type

        self._data[Mail._OFFSET_MAIL_TYPE : Mail._OFFSET_MAIL_TYPE_END] = (
            WonderMailS.MAIL_TYPE
        )

    @property
    def null_bits(self) -> u8:
        """
        Null bits at the beginning of the code. The first two are not part of the checksum.
        These should normally all be 0.
        """
        return self._get(WonderMailS._OFFSET_NULL_BITS, 8, u8)

    @null_bits.setter
    def null_bits(self, value: u8):
        self._set(WonderMailS._OFFSET_NULL_BITS, 8, u8, value)

    @property
    def fixed_room(self) -> u8:
        """
        Fixed room to use for the mission (used for some mission types).
        """
        return self._get(WonderMailS._OFFSET_FIXED_ROOM, 8, u8)

    @fixed_room.setter
    def fixed_room(self, value: u8):
        self._set(WonderMailS._OFFSET_FIXED_ROOM, 8, u8, value)

    @property
    def floor(self) -> u8:
        """
        Floor ID to use for mission.
        """
        return self._get(WonderMailS._OFFSET_FLOOR, 8, u8)

    @floor.setter
    def floor(self, value: u8):
        self._set(WonderMailS._OFFSET_FLOOR, 8, u8, value)

    @property
    def dungeon(self) -> u8:
        """
        Dungeon ID (not group ID) to use for the mission.
        """
        return self._get(WonderMailS._OFFSET_DUNGEON, 8, u8)

    @dungeon.setter
    def dungeon(self, value: u8):
        self._set(WonderMailS._OFFSET_DUNGEON, 8, u8, value)

    @property
    def description_id(self) -> u24:
        """
        Index of the text shown as the description / flavor text of the mission. Table used unknown (as of writing).
        """
        return self._get(WonderMailS._OFFSET_DESCRIPTION_ID, 24, u24)

    @description_id.setter
    def description_id(self, value: u24):
        self._set(WonderMailS._OFFSET_DESCRIPTION_ID, 24, u24, value)

    @property
    def restriction(self) -> u11:
        """
        Restriction for the mission. The interpretation of the value depends on the type. See constants.
        """
        return self._get(WonderMailS._OFFSET_RESTRICTION, 11, u11)

    @restriction.setter
    def restriction(self, value: u11):
        self._set(WonderMailS._OFFSET_RESTRICTION, 11, u11, value)

    @property
    def restriction_type(self) -> RestrictionType:
        """
        Restriction_Type for the mission. The interpretation of the value depends on the type. See constants.
        """
        return self._get(WonderMailS._OFFSET_RESTRICTION_TYPE, 1, RestrictionType)

    @restriction_type.setter
    def restriction_type(self, value: u11):
        self._set(WonderMailS._OFFSET_RESTRICTION_TYPE, 1, RestrictionType, value)

    @property
    def reward_item(self) -> u11:
        """
        Item ID of the item to reward the player with after a mission (only for some reward types).
        """
        return self._get(WonderMailS._OFFSET_REWARD_ITEM, 11, u11)

    @reward_item.setter
    def reward_item(self, value: u11):
        self._set(WonderMailS._OFFSET_REWARD_ITEM, 11, u11, value)

    @property
    def reward_type(self) -> RewardType:
        """
        Reward type.
        """
        return self._get(WonderMailS._OFFSET_REWARD_TYPE, 4, RewardType)

    @reward_type.setter
    def reward_type(self, value: RewardType):
        self._set(WonderMailS._OFFSET_REWARD_TYPE, 4, RewardType, value)

    @property
    def target_item(self) -> u10:
        """
        ID of an item to retrieve (for some mission types).
        """
        return self._get(WonderMailS._OFFSET_TARGET_ITEM, 10, u10)

    @target_item.setter
    def target_item(self, value: u10):
        self._set(WonderMailS._OFFSET_TARGET_ITEM, 10, u10, value)

    @property
    def outlaw_backup_species(self) -> u11:
        """
        ID of a monster to use for some types of outlaw missions.
        """
        return self._get(WonderMailS._OFFSET_OUTLAW_BACKUP_SPECIES, 11, u11)

    @outlaw_backup_species.setter
    def outlaw_backup_species(self, value: u11):
        self._set(WonderMailS._OFFSET_OUTLAW_BACKUP_SPECIES, 11, u11, value)

    @property
    def target_monster(self) -> u11:
        """
        ID of a target monster to use for some types of missions.
        """
        return self._get(WonderMailS._OFFSET_TARGET_MONSTER, 11, u11)

    @target_monster.setter
    def target_monster(self, value: u11):
        self._set(WonderMailS._OFFSET_TARGET_MONSTER, 11, u11, value)

    @property
    def client(self) -> u11:
        """
        ID of a monster to use as the client handing out the mission.
        """
        return self._get(WonderMailS._OFFSET_CLIENT, 11, u11)

    @client.setter
    def client(self, value: u11):
        self._set(WonderMailS._OFFSET_CLIENT, 11, u11, value)

    @property
    def mission_subtype(self) -> MissionSubtype:
        """
        Subtype of the mission. What this is interpreted as depends on main mission type.
        """
        return self._get(WonderMailS._OFFSET_MISSION_SUBTYPE, 4, MissionSubtype)

    @mission_subtype.setter
    def mission_subtype(self, value: MissionSubtype):
        self._set(WonderMailS._OFFSET_MISSION_SUBTYPE, 4, MissionSubtype, value)

    @property
    def mission_type(self) -> MissionType:
        """
        Type of the mission.
        """
        return self._get(WonderMailS._OFFSET_MISSION_TYPE, 4, MissionType)

    @mission_type.setter
    def mission_type(self, value: MissionType):
        self._set(WonderMailS._OFFSET_MISSION_TYPE, 4, MissionType, value)


def checksum(bit_stream: BitStream) -> BitStream:
    # Calculate the checksum - Sky. This is simple CRC32 with LSB.
    # http://www.gamefaqs.com/boards/detail.php?board=955859&topic=51920426&message=582176885
    if len(bit_stream) == 170:
        bit_stream = bit_stream[_OFFSET_CHECKSUM_START:_LEN_MAIL_WO_CHECKSUM]

    if len(bit_stream) < 136:
        raise ValueError("Invalid stream length for checksum calculation: {len(data)}")

    # Start with 0xFFFFFFFF.
    csum = 0xFFFFFFFF

    crctable = crc32_table()

    # We have 17 blocks of 8 bits in the bitStream (136 bits).
    for i in reversed(range(0, 17)):
        # Grab 8 bits from the stream and convert it to a number.
        num = bit_stream[i * 8 : i * 8 + 8].to_number("little")

        # Grab a entry from the data table. The entry gotten is equal to
        # The entry is NOT'ed with our current checksum rsl'd 8 times. The result of this will be the new checksum
        # for this round.
        csum = (csum >> 8) ^ crctable[(csum ^ num) & 0xFF]

    #  Our final checksum is NOT'ed with 0xFFFFFFFF.
    csum ^= 0xFFFFFFFF

    return BitStream(csum.to_bytes(32, "little"))


def mail_code_to_bits(code: str, region: str) -> BitStream:
    # Remove all white-spaces
    code = code.translate({ord(c): None for c in string.whitespace})
    # Unscramble
    unscrambled = _unscramble(code, _byte_swap_for_region(region))
    return _code_bytes_to_bitstream(unscrambled)


def bits_to_mail_code(data: BitStream, region: str) -> str:
    packed = _bitstream_to_code_bytes(data)

    # Scramble
    return _scramble(packed, _byte_swap_for_region(region))


def _byte_swap_for_region(region: str):
    if region == GAME_REGION_US:
        return _BYTE_SWAP_NA
    if region == GAME_REGION_EU:
        return _BYTE_SWAP_EU
    else:
        raise NotImplementedError(
            f"Mail generation not implemented for game region {region}."
        )


def _code_bytes_to_bitstream(code: str) -> BitStream:
    """
    Converts a mail code byte string into a bit stream. Raises an error if any character is found in the string,
    which is not representable by a mail code.
    """
    out = BitStream([])
    for cur_char in reversed(code):
        try:
            index = _BIT_VALUES.index(cur_char)
            out += BitStream.from_number(index, 5)
        except ValueError as e:
            raise ValueError(f"Mail code contained invalid character {cur_char}") from e
    return out


def _bitstream_to_code_bytes(bit_stream: BitStream) -> str:
    """Converts a BitStream into a mail code byte string, so a string only containing mail characters."""
    out_string = ""
    for cur_chars in chunks(bit_stream, 5):
        num = cast(BitStream, cur_chars).to_number()
        out_string += _BIT_VALUES[num]
    return out_string


def _scramble(wm_string: str, swap_array: list[int]) -> str:
    out_array = ["" * len(swap_array)]
    for i, target in enumerate(swap_array):
        out_array[target] += wm_string[i]

    return "".join(out_array)


def _unscramble(wm_string: str, swap_array: list[int]) -> str:
    out_string = ""
    for source in swap_array:
        out_string += wm_string[source]
    return out_string


def mail_decrypt(inp: BitStream) -> BitStream:
    return _do_mail_encryption(inp, False)


def mail_encrypt(inp: BitStream) -> BitStream:
    return _do_mail_encryption(inp, True)


def _do_mail_encryption(inp: BitStream, encrypt: bool) -> BitStream:
    # This will contain the 8-bit blocks as numbers (0-255), each representing one byte.
    # The checksum byte is NOT included in these blocks.
    # The first block in the array is the last block in the bitstream (we work backwards).
    orig_blocks = []

    # Checksum data
    # Go 8 bits back from the end. We'll read the next 8 bits as our checksum.
    bit_ptr = len(inp) - 8
    checksum_bits = inp[bit_ptr : bit_ptr + 8]
    checksum_byte = checksum_bits.to_number()

    # The Sky Checksum is 24 bits.
    bit_ptr -= 24
    sky_checksum_bits = inp[bit_ptr : bit_ptr + 24]
    full_checksum = (sky_checksum_bits + checksum_bits).to_number("little")

    # Parse everything into blocks.
    # Sky: 1 2-bit block + 16 8-bit blocks + 24-bit skyChecksum + 8-bit checksum.
    while bit_ptr > 7:
        bit_ptr -= 8
        data = inp[bit_ptr : bit_ptr + 8].to_number()
        orig_blocks.append(data)

    # Handle the 2-bit block at the beginning (should always be 00?)
    two_bits_start = inp[0:2]
    bit_ptr -= 2

    # Get our encryption entries.
    entries = _encryption_entries(checksum_byte)

    # Figure out the resetByte.
    reset_byte = _reset_byte(full_checksum)

    # Do the en-/decryption.
    enc_ptr = 0
    blocks = []
    for input_byte in orig_blocks:
        if enc_ptr == reset_byte:
            # Resetting.
            enc_ptr = 0

        # Add or subtract the number in the encryption entry from it.
        if encrypt:
            result = (input_byte + entries[enc_ptr]) & 0xFF
        else:
            result = (input_byte - entries[enc_ptr]) & 0xFF

        # Update the data in the block.
        blocks.append(result)

        # Update blockPtr.
        enc_ptr += 1

    # String everything together. If we use two_bits_start, that will be our base point.
    out_bits: BitStream = two_bits_start

    # We start at the end and work backwards; the last encryption block is the first 8 bits in the bitstream.
    # That's just how it works.
    for block in blocks:
        out_bits += block

    # Re-add the checksums to the data.
    out_bits += sky_checksum_bits + checksum_bits

    return out_bits


def _encryption_entries(the_checksum: int):
    amount = 17
    entries = []
    enc_pointer = the_checksum
    # http://www.gamefaqs.com/boards/genmessage.php?board=938931&topic=42949038&page=6
    # "At the moment, I figured out what the game is doing with the other half of the encryption.
    # Apparently, if you have an even checksum, you go backwards through the encryption bytes.
    # With an odd checksum, you go forwards through the encryption bytes."
    backwards = (the_checksum & 0x01) == 0
    for _ in range(0, amount):
        entries.append(_ENCRYPTION_DATA[enc_pointer])
        if backwards:
            enc_pointer -= 1
            if enc_pointer < 0:
                enc_pointer = len(_ENCRYPTION_DATA) - 1
        else:
            enc_pointer += 1
            if enc_pointer >= len(_ENCRYPTION_DATA):
                enc_pointer = 0
    return entries


def _reset_byte(the_checksum: int):
    checksum_byte = the_checksum % 256
    reset_byte = floor((checksum_byte / 16) + 8 + (checksum_byte % 16))
    # The reset_byte must be under 17. If not, the code doesn't use a reset_byte.
    return reset_byte if (reset_byte < 17) else -1


_CRC32_TABLE: Optional[list[int]] = None


def crc32_table() -> list[int]:
    global _CRC32_TABLE
    if _CRC32_TABLE is None:
        _CRC32_TABLE = []
        for i in range(256):
            k = i
            for j in range(8):
                if k & 1:
                    k = 0xEDB88320 ^ (k >> 1)
                else:
                    k >>= 1
            _CRC32_TABLE.append(k)
    return _CRC32_TABLE


def _pretty_mail_string(mail_string, rows, middle_column_size):
    # If our mailString is 18 bytes and the middle column is 5 bytes with 2 rows, we'll have 8 bytes left for the rest.
    # There'll be 2 columns for 2 rows each = 8/2/2 = 2 bytes.
    #                   (18               - (2 * 5))                     / (2 * 2)    = 2
    outer_column_size = (len(mail_string) - (rows * middle_column_size)) / (rows * 2)

    pretty_string = ""
    string_ptr = 0
    for _ in range(0, rows):
        if pretty_string != "":
            pretty_string += "\n"
        pretty_string += mail_string[string_ptr : string_ptr + outer_column_size] + " "
        string_ptr += outer_column_size
        pretty_string += mail_string[string_ptr : string_ptr + middle_column_size] + " "
        string_ptr += middle_column_size
        pretty_string += mail_string[string_ptr : string_ptr + outer_column_size]
        string_ptr += outer_column_size
    return pretty_string
