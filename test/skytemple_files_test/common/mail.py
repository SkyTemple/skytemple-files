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

import unittest

from range_typed_integers import u8

from skytemple_files.common.bit_stream import BitStream
from skytemple_files.common.mail import (
    MISSION_TYPE_RESCUE_CLIENT,
    MISSION_TYPE_TAKE_ITEM_FROM_OUTLAW,
    MISSION_TYPE_TAKE_ITEM_FROM_OUTLAW__HIDDEN_OUTLAW,
    MISSION_TYPE_ARREST_OUTLAW,
    MISSION_TYPE_ARREST_OUTLAW__NORMAL_0,
    MISSION_TYPE_TREASURE_MEMO,
    MISSION_TYPE_CHALLENGE_REQUEST,
    MISSION_TYPE_CHALLENGE_REQUEST__MEWTWO,
    MISSION_TYPE_FIND_ITEM,
    MISSION_TYPE_PROSPECT_WITH_CLIENT,
    RESTRICTION_TYPE_TYPE_OR_NONE,
    REWARD_TYPE_ITEM_HIDDEN,
    REWARD_TYPE_SPECIAL,
    REWARD_TYPE_MONEY_AND_MORE,
    REWARD_TYPE_MONEY,
    REWARD_TYPE_MONEY_HIDDEN,
    REWARD_TYPE_ITEM_AND_MORE,
    WonderMailS,
    MISSION_TYPE_CHALLENGE_REQUEST__ENTEI,
    RESTRICTION_TYPE_MONSTER,
)
from skytemple_files.common.util import u24, u11, u10


def bs(s: str) -> BitStream:
    return BitStream([x == "1" for x in s])


# fmt: off
FIX_FULL_MAIL = [
    {
        "input": {"mission_type": MISSION_TYPE_RESCUE_CLIENT, "mission_subtype": 0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_ITEM_AND_MORE, "client": 1, "target_monster": 1, "outlaw_backup_species": 0, "reward_item": 15, "target_item": 109, "dungeon": 1, "floor": 1, "fixed_room": 0, "description_id": 300000},
        "output": "7K9QS &P91#+2 1H9X6\n-C-%S @8+93Q3 W5KQT",
        "is_eu": False
    },
    {
        "input": {"mission_type": MISSION_TYPE_RESCUE_CLIENT, "mission_subtype": 0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_ITEM_AND_MORE, "client": 1, "target_monster": 1, "outlaw_backup_species": 0, "reward_item": 15, "target_item": 109, "dungeon": 1, "floor": 1, "fixed_room": 0, "description_id": 300000},
        "output": "519HQ 6X%2SPS Q-998\n9T+#& QWK+C7- 13@K3",
        "is_eu": True
    },
    {
        "input": {"mission_type": MISSION_TYPE_TAKE_ITEM_FROM_OUTLAW, "mission_subtype": MISSION_TYPE_TAKE_ITEM_FROM_OUTLAW__HIDDEN_OUTLAW, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_ITEM_HIDDEN, "client": 39, "target_monster": 1, "outlaw_backup_species": 0, "reward_item": 15, "target_item": 14, "dungeon": 21, "floor": 33, "fixed_room": 0, "description_id": 2},
        "output": "N1WP& M+CH304 R2+2%\n8R8WR @P5+4=@ 948RH",
        "is_eu": True
    },
    {
        "input": {"mission_type": MISSION_TYPE_ARREST_OUTLAW, "mission_subtype": MISSION_TYPE_ARREST_OUTLAW__NORMAL_0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_MONEY, "client": 81, "target_monster": 1, "outlaw_backup_species": 0, "reward_item": 109, "target_item": 109, "dungeon": 102, "floor": 33, "fixed_room": 0, "description_id": 2},
        "output": "637N7 4QK7M#6 +&1#F\nS&Y+Q -Y&PF8& 68#2N",
        "is_eu": False
    },
    {
        "input": {"mission_type": MISSION_TYPE_TREASURE_MEMO, "mission_subtype": 0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_MONEY_AND_MORE, "client": 422, "target_monster": 422, "outlaw_backup_species": 0, "reward_item": 109, "target_item": 109, "dungeon": 91, "floor": 4, "fixed_room": 136, "description_id": 4},
        "output": "JF7X6 JK0@&3X X@QHC\nN63T8 K#S6FC+ @TTJR",
        "is_eu": False
    },
    {
        "input": {"mission_type": MISSION_TYPE_CHALLENGE_REQUEST, "mission_subtype": MISSION_TYPE_CHALLENGE_REQUEST__MEWTWO, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_MONEY_HIDDEN, "client": 150, "target_monster": 150, "outlaw_backup_species": 0, "reward_item": 150, "target_item": 109, "dungeon": 81, "floor": 5, "fixed_room": 145, "description_id": 5},
        "output": "4@6MK 0J%XN4P S#5FQ\nNNRJ4 R@3T8NF K5KC7",
        "is_eu": True
    },
    {
        "input": {"mission_type": MISSION_TYPE_FIND_ITEM, "mission_subtype": 0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_ITEM_HIDDEN, "client": 639, "target_monster": 639, "outlaw_backup_species": 0, "reward_item": 48, "target_item": 34, "dungeon": 81, "floor": 5, "fixed_room": 0, "description_id": 5},
        "output": "1Y@@Y -#F61T9 #+N2C\nK8X9C 7578Y7M YC+JM",
        "is_eu": False
    },
    {
        "input": {"mission_type": MISSION_TYPE_PROSPECT_WITH_CLIENT, "mission_subtype": 0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_SPECIAL, "client": 639, "target_monster": 639, "outlaw_backup_species": 0, "reward_item": 639, "target_item": 34, "dungeon": 81, "floor": 5, "fixed_room": 0, "description_id": 5},
        "output": "34715 46K40%0 3K4RQ\n1N=8W 6186342 PH2NH",
        "is_eu": False
    },
    {
        "input": {"mission_type": MISSION_TYPE_PROSPECT_WITH_CLIENT, "mission_subtype": 0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_MONEY_AND_MORE, "client": 666, "target_monster": 666, "outlaw_backup_species": 0, "reward_item": 81, "target_item": 24, "dungeon": 17, "floor": 2, "fixed_room": 0, "description_id": 5},
        "output": "08S55 X7+TQCQ #+C4S\nP2J5W M@P198# 37QTF",
        "is_eu": True
    },
]

FIX_CALCULATE_CHECKSUM = [
    {
        "input": bs("0000000000000000000001000000010000010010010011111000000000000000000000000111100110001101101000000000000000000000100000000001000000000100"),
        "output": 952882087
    },
    {
        "input": bs("0000000000000000000001000000010000010010010011111000000000000000000000000111100110001101101000000000000000000000100000000001000000000100"),
        "output": 952882087
    },
    {
        "input": bs("0000000000000000100001000101010000000000000000000000100000000000000000000111101000000001110000000000000000000000100000100111000110010100"),
        "output": 1640534026
    },
    {
        "input": bs("0000000000000000100001011001100000000000000000000000100000000000000000110110100000001101101000000000000000000000100001010001000010100100"),
        "output": 1372946647
    },
    {
        "input": bs("0000001000100000000100010110110000000000000000000001000000000000000000110110100010001101101000000000000011010011000110100110000011000100"),
        "output": 3496409705
    },
    {
        "input": bs("0000001001000100000101010100010000000000000000000001010000000000000001001011001010001101101000000000000001001011000010010110000110110100"),
        "output": 574507761
    },
    {
        "input": bs("0000000000000000000101010100010000000000000000000001010000000000000000011000001000000100010000000000000100111111101001111111000001100100"),
        "output": 3744802888
    },
    {
        "input": bs("0000000000000000000101010100010000000000000000000001010000000000000100111111101100000100010000000000000100111111101001111111000001000100"),
        "output": 2046615063
    },
    {
        "input": bs("0000000000000000000010000100010000000000000000000001010000000000000000101000100010000011000000000000000101001101001010011010000001000100"),
        "output": 3318892083
    },
]

FIX_MAIL_BITS = [
    {
        "fields": {"mission_type": MISSION_TYPE_RESCUE_CLIENT, "mission_subtype": 0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_ITEM_AND_MORE, "client": 1, "target_monster": 1, "outlaw_backup_species": 0, "reward_item": 15, "target_item": 109, "dungeon": 1, "floor": 1, "fixed_room": 0, "description_id": 300000},
        "bits": bs("00000000000000000000000100000001000001001001001111100000000000000000000000011110011000110110100000000000000000000010000000000100000000010000111000110010111101001110100111")
    },
    {
        "fields": {"mission_type": MISSION_TYPE_RESCUE_CLIENT, "mission_subtype": 0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_ITEM_AND_MORE, "client": 1, "target_monster": 1, "outlaw_backup_species": 0, "reward_item": 15, "target_item": 109, "dungeon": 1, "floor": 1, "fixed_room": 0, "description_id": 300000},
        "bits": bs("00000000000000000000000100000001000001001001001111100000000000000000000000011110011000110110100000000000000000000010000000000100000000010000111000110010111101001110100111")
    },
    {
        "fields": {"mission_type": MISSION_TYPE_TAKE_ITEM_FROM_OUTLAW, "mission_subtype": MISSION_TYPE_TAKE_ITEM_FROM_OUTLAW__HIDDEN_OUTLAW, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_ITEM_HIDDEN, "client": 39, "target_monster": 1, "outlaw_backup_species": 0, "reward_item": 15, "target_item": 14, "dungeon": 21, "floor": 33, "fixed_room": 0, "description_id": 2},
        "bits": bs("00000000000000000010000100010101000000000000000000000010000000000000000000011110100000000111000000000000000000000010000010011100011001010001100001110010001001000000001010")
    },
    {
        "fields": {"mission_type": MISSION_TYPE_ARREST_OUTLAW, "mission_subtype": MISSION_TYPE_ARREST_OUTLAW__NORMAL_0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_MONEY, "client": 81, "target_monster": 1, "outlaw_backup_species": 0, "reward_item": 109, "target_item": 109, "dungeon": 102, "floor": 33, "fixed_room": 0, "description_id": 2},
        "bits": bs("00000000000000000010000101100110000000000000000000000010000000000000000011011010000000110110100000000000000000000010000101000100001010010001010001110101011000000011010111")
    },
    {
        "fields": {"mission_type": MISSION_TYPE_TREASURE_MEMO, "mission_subtype": 0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_MONEY_AND_MORE, "client": 422, "target_monster": 422, "outlaw_backup_species": 0, "reward_item": 109, "target_item": 109, "dungeon": 91, "floor": 4, "fixed_room": 136, "description_id": 4},
        "bits": bs("00000000100010000000010001011011000000000000000000000100000000000000000011011010001000110110100000000000001101001100011010011000001100010011010000011001101111101001101001")
    },
    {
        "fields": {"mission_type": MISSION_TYPE_CHALLENGE_REQUEST, "mission_subtype": MISSION_TYPE_CHALLENGE_REQUEST__MEWTWO, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_MONEY_HIDDEN, "client": 150, "target_monster": 150, "outlaw_backup_species": 0, "reward_item": 150, "target_item": 109, "dungeon": 81, "floor": 5, "fixed_room": 145, "description_id": 5},
        "bits": bs("00000000100100010000010101010001000000000000000000000101000000000000000100101100101000110110100000000000000100101100001001011000011011010000100010001111100100101011110001")
    },
    {
        "fields": {"mission_type": MISSION_TYPE_FIND_ITEM, "mission_subtype": 0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_ITEM_HIDDEN, "client": 639, "target_monster": 639, "outlaw_backup_species": 0, "reward_item": 48, "target_item": 34, "dungeon": 81, "floor": 5, "fixed_room": 0, "description_id": 5},
        "bits": bs("00000000000000000000010101010001000000000000000000000101000000000000000001100000100000010001000000000000010011111110100111111100000110010011011111001101010010100001001000")
    },
    {
        "fields": {"mission_type": MISSION_TYPE_PROSPECT_WITH_CLIENT, "mission_subtype": 0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_SPECIAL, "client": 639, "target_monster": 639, "outlaw_backup_species": 0, "reward_item": 639, "target_item": 34, "dungeon": 81, "floor": 5, "fixed_room": 0, "description_id": 5},
        "bits": bs("00000000000000000000010101010001000000000000000000000101000000000000010011111110110000010001000000000000010011111110100111111100000100010001111001111111001101111000010111")
    },
    {
        "fields": {"mission_type": MISSION_TYPE_PROSPECT_WITH_CLIENT, "mission_subtype": 0, "null_bits": 0, "mail_type": 4, "restriction": 0, "restriction_type": RESTRICTION_TYPE_TYPE_OR_NONE, "reward_type": REWARD_TYPE_MONEY_AND_MORE, "client": 666, "target_monster": 666, "outlaw_backup_species": 0, "reward_item": 81, "target_item": 24, "dungeon": 17, "floor": 2, "fixed_room": 0, "description_id": 5},
        "bits": bs("00000000000000000000001000010001000000000000000000000101000000000000000010100010001000001100000000000000010100110100101001101000000100010011000101110100100100011000110011")
    },
]

FIX_RESET_BYTE = [
    {
        "input": 952882087,
        "output": -1
    },
    {
        "input": 952882087,
        "output": -1
    },
    {
        "input": 952882087,
        "output": -1
    },
    {
        "input": 952882087,
        "output": -1
    },
    {
        "input": 1640534026,
        "output": -1
    },
    {
        "input": 1372946647,
        "output": -1
    },
    {
        "input": 3496409705,
        "output": -1
    },
    {
        "input": 574507761,
        "output": -1
    },
    {
        "input": 3744802888,
        "output": -1
    },
    {
        "input": 2046615063,
        "output": 16
    },
    {
        "input": 3318892083,
        "output": 14
    },
]

FIX_ENCRYPTION_ENTRIES = [
    {
        "input": 167,
        "output": [181, 118, 47, 168, 122, 200, 129, 6, 187, 133, 117, 17, 12, 210, 209, 201, 248]
    },
    {
        "input": 167,
        "output": [181, 118, 47, 168, 122, 200, 129, 6, 187, 133, 117, 17, 12, 210, 209, 201, 248]
    },
    {
        "input": 10,
        "output": [150, 42, 124, 97, 188, 108, 9, 153, 63, 117, 46, 5, 126, 4, 208, 166, 199]
    },
    {
        "input": 215,
        "output": [67, 255, 195, 179, 50, 122, 62, 156, 163, 194, 171, 16, 96, 153, 251, 8, 138]
    },
    {
        "input": 105,
        "output": [129, 235, 103, 243, 235, 140, 71, 147, 206, 42, 175, 53, 244, 116, 135, 80, 44]
    },
    {
        "input": 241,
        "output": [232, 252, 75, 13, 74, 122, 72, 201, 176, 199, 166, 208, 4, 126, 5, 46, 117]
    },
    {
        "input": 72,
        "output": [22, 97, 59, 154, 233, 84, 53, 58, 122, 176, 255, 214, 140, 163, 112, 63, 203]
    },
    {
        "input": 23,
        "output": [60, 72, 128, 123, 70, 103, 1, 23, 89, 184, 250, 112, 192, 68, 120, 72, 251]
    },
    {
        "input": 51,
        "output": [40, 108, 156, 7, 164, 203, 63, 112, 163, 140, 214, 255, 176, 122, 58, 53, 84]
    },
]

FIX_ENCRYPT_BITS = [
    {
        "input": bs("00000000000000000000000100000001000001001001001111100000000000000000000000011110011000110110100000000000000000000010000000000100000000010000111000110010111101001110100111"),
        "output": bs("00111110001100100111010101110101100001111001100000111101011000010110111011011111110000111001101000011110101010100010101111100001101011100100111000110010111101001110100111")
    },
    {
        "input": bs("00000000000000000000000100000001000001001001001111100000000000000000000000011110011000110110100000000000000000000010000000000100000000010000111000110010111101001110100111"),
        "output": bs("00111110001100100111010101110101100001111001100000111101011000010110111011011111110000111001101000011110101010100010101111100001101011100100111000110010111101001110100111")
    },
    {
        "input": bs("00000000000000000010000100010101000000000000000000000010000000000000000000011110100000000111000000000000000000000010000010011100011001010001100001110010001001000000001010"),
        "output": bs("00110001111010011001010100010110000111111000000101001101100111010100111111000100110000101000101100101111000110000111111110100110110010101001100001110010001001000000001010")
    },
    {
        "input": bs("00000000000000000010000101100110000000000000000000000010000000000000000011011010000000110110100000000000000000000010000101000100001010010001010001110101011000000011010111"),
        "output": bs("00100010100000100010000000001100010110000000010000101100111100001010100110000001000100101100011010001100101011001101001000000011111110011101010001110101011000000011010111")
    },
    {
        "input": bs("00000000100010000000010001011011000000000000000000000100000000000000000011011010001000110110100000000000001101001100011010011000001100010011010000011001101111101001101001"),
        "output": bs("00001011100111000010011000111000001111010000110101101111110010101011010001111110111101010000101100111010111100011010000001010010110100010111010000011001101111101001101001")
    },
    {
        "input": bs("00000000100100010000010101010001000000000000000000000101000000000000000100101100101000110110100000000000000100101100001001011000011011010000100010001111100100101011110001"),
        "output": bs("00011101110111001000011010110000100000010011010000101110101100011110110100011110111101010100011010010010100101100001010100010111011001110000100010001111100100101011110001")
    },
    {
        "input": bs("00000000000000000000010101010001000000000000000000000101000000000000000001100000100000010001000000000000010011111110100111111100000110010011011111001101010010100001001000"),
        "output": bs("00110010110011111110000101111001111000110011010110000100111011000001111011101111000011100110010100111010101101100111100010010100010111101011011111001101010010100001001000")
    },
    {
        "input": bs("00000000000000000000010101010001000000000000000000000101000000000000010011111110110000010001000000000000010011111110100111111100000100010001111001111111001101111000010111"),
        "output": bs("00001111000100100010001101100010001100000001110000000011101011100001101100000100100000010110100111010001111011101000100111001110001000000001111001111111001101111000010111")
    },
    {
        "input": bs("00000000000000000000001000010001000000000000000000000101000000000000000010100010001000001100000000000000010100110100101001101000000100010011000101110100100100011000110011"),
        "output": bs("00100111000110110000110000101111101011000011111111111010101000110010100101111110001100001011001011101001010101010011000101000011000110110011000101110100100100011000110011")
    },
]

FIX_BITS_TO_BYTES = [
    {
        "input": bs("00111110001100100111010101110101100001111001100000111101011000010110111011011111110000111001101000011110101010100010101111100001101011100100111000110010111101001110100111"),
        "output": "9QHKS3PK83#5+Q6TX1W-%7-@&C9SQ+9219"
    },
    {
        "input": bs("00111110001100100111010101110101100001111001100000111101011000010110111011011111110000111001101000011110101010100010101111100001101011100100111000110010111101001110100111"),
        "output": "9QHKS3PK83#5+Q6TX1W-%7-@&C9SQ+9219"
    },
    {
        "input": bs("00110001111010011001010100010110000111111000000101001101100111010100111111000100110000101000101100101111000110000111111110100110110010101001100001110010001001000000001010"),
        "output": "+&P5340R%HWN8@MR+1P@C=28R4W4R+2H98"
    },
    {
        "input": bs("00100010100000100010000000001100010110000000010000101100111100001010100110000001000100101100011010001100101011001101001000000011111110011101010001110101011000000011010111"),
        "output": "K8&#QFQ3Y&M8#2FN#76S+6Y-4&17N&76+P"
    },
    {
        "input": bs("00001011100111000010011000111000001111010000110101101111110010101011010001111110111101010000101100111010111100011010000001010010110100010111010000011001101111101001101001"),
        "output": "0C@T8FKF#+&T3JCRH@@NTJ3KJ6Q6XS7XX6"
    },
    {
        "input": bs("00011101110111001000011010110000100000010011010000101110101100011110110100011110111101010100011010010010100101100001010100010111011001110000100010001111100100101011110001"),
        "output": "5KM3N54CQ7J4RR0NJ@@F%N#K486PSTFXKN"
    },
    {
        "input": bs("00110010110011111110000101111001111000110011010110000100111011000001111011101111000011100110010100111010101101100111100010010100010111101011011111001101010010100001001000"),
        "output": "F7++CY#Y5M1CTJCM26YK91X7-8NY@7@9#8"
    },
    {
        "input": bs("00001111000100100010001101100010001100000001110000000011101011100001101100000100100000010110100111010001111011101000100111001110001000000001111001111111001101111000010111"),
        "output": "K4K2W364120H%NQHR4P183=64N45187036"
    },
    {
        "input": bs("00100111000110110000110000101111101011000011111111111010101000110010100101111110001100001011001011101001010101010011000101000011000110110011000101110100100100011000110011"),
        "output": "C55PQ7CTSF50JMX278@#+8+QW9SQ#14T3P"
    },
]

FIX_SCRAMBLE = [
    {
        "input": "9QHKS3PK83#5+Q6TX1W-%7-@&C9SQ+9219",
        "output": "7K9QS&P91#+21H9X6-C-%S@8+93Q3W5KQT",
        "is_eu": False
    },
    {
        "input": "9QHKS3PK83#5+Q6TX1W-%7-@&C9SQ+9219",
        "output": "519HQ6X%2SPSQ-9989T+#&QWK+C7-13@K3",
        "is_eu": True
    },
    {
        "input": "+&P5340R%HWN8@MR+1P@C=28R4W4R+2H98",
        "output": "N1WP&M+CH304R2+2%8R8WR@P5+4=@948RH",
        "is_eu": True
    },
    {
        "input": "K8&#QFQ3Y&M8#2FN#76S+6Y-4&17N&76+P",
        "output": "637N74QK7M#6+&1#FS&Y+Q-Y&PF8&68#2N",
        "is_eu": False
    },
    {
        "input": "0C@T8FKF#+&T3JCRH@@NTJ3KJ6Q6XS7XX6",
        "output": "JF7X6JK0@&3XX@QHCN63T8K#S6FC+@TTJR",
        "is_eu": False
    },
    {
        "input": "5KM3N54CQ7J4RR0NJ@@F%N#K486PSTFXKN",
        "output": "4@6MK0J%XN4PS#5FQNNRJ4R@3T8NFK5KC7",
        "is_eu": True
    },
    {
        "input": "F7++CY#Y5M1CTJCM26YK91X7-8NY@7@9#8",
        "output": "1Y@@Y-#F61T9#+N2CK8X9C7578Y7MYC+JM",
        "is_eu": False
    },
    {
        "input": "K4K2W364120H%NQHR4P183=64N45187036",
        "output": "3471546K40%03K4RQ1N=8W6186342PH2NH",
        "is_eu": False
    },
    {
        "input": "C55PQ7CTSF50JMX278@#+8+QW9SQ#14T3P",
        "output": "08S55X7+TQCQ#+C4SP2J5WM@P198#37QTF",
        "is_eu": True
    },
]
# fmt: on


class MailTestCase(unittest.TestCase):
    def test_wonder_mail_s_init(self):
        fix = WonderMailS(
            floor=u8(12),
            dungeon=u8(65),
            mission_type=MISSION_TYPE_RESCUE_CLIENT,
            mission_subtype=MISSION_TYPE_CHALLENGE_REQUEST__ENTEI,
            null_bits=u8(4),
            fixed_room=u8(5),
            description_id=u24(1234),
            restriction=u11(44),
            restriction_type=RESTRICTION_TYPE_MONSTER,
            reward_item=u11(999),
            reward_type=REWARD_TYPE_ITEM_HIDDEN,
            target_item=u10(1023),
            target_monster=u11(599),
            outlaw_backup_species=u11(9),
            client=u11(99),
        )

        self.assertEqual(12, fix.floor)
        self.assertEqual(65, fix.dungeon)
        self.assertEqual(MISSION_TYPE_RESCUE_CLIENT, fix.mission_type)
        self.assertEqual(MISSION_TYPE_CHALLENGE_REQUEST__ENTEI, fix.mission_subtype)
        self.assertEqual(4, fix.null_bits)
        self.assertEqual(5, fix.fixed_room)
        self.assertEqual(1234, fix.description_id)
        self.assertEqual(44, fix.restriction)
        self.assertEqual(RESTRICTION_TYPE_MONSTER, fix.restriction_type)
        self.assertEqual(999, fix.reward_item)
        self.assertEqual(REWARD_TYPE_ITEM_HIDDEN, fix.reward_type)
        self.assertEqual(1023, fix.target_item)
        self.assertEqual(599, fix.target_monster)
        self.assertEqual(9, fix.outlaw_backup_species)
        self.assertEqual(99, fix.client)

    def test_wonder_mail_s_from_decrypted_bits(self):
        raise NotImplementedError()

    def test_wonder_mail_s_from_encrypted_bits(self):
        raise NotImplementedError()

    def test_wonder_mail_s_from_code(self):
        raise NotImplementedError()

    def test_wonder_mail_s_to_decrypted_bits(self):
        raise NotImplementedError()

    def test_wonder_mail_s_to_encrypted_bits(self):
        raise NotImplementedError()

    def test_wonder_mail_s_to_code(self):
        raise NotImplementedError()

    def test_mail_checksum(self):
        # calculateChecksum
        # -- checksum
        # -- Mail.checksum
        raise NotImplementedError()

    def test_checksum_fn(self):
        # calculateChecksum
        # -- checksum
        # -- Mail.checksum
        raise NotImplementedError()

    def test_mail_code_to_bits(self):
        raise NotImplementedError()

    def test_bits_to_mail_code(self):
        raise NotImplementedError()

    def test_code_bytes_to_bitstream(self):
        # bitsToBytes
        # -- _code_bytes_to_bitstream
        # -- _bitstream_to_code_bytes
        raise NotImplementedError()

    def test_bitstream_to_code_bytes(self):
        # bitsToBytes
        # -- _code_bytes_to_bitstream
        # -- _bitstream_to_code_bytes
        raise NotImplementedError()

    def test_scramble(self):
        # scrambleString
        # -- _scramble
        # -- _unscramble
        raise NotImplementedError()

    def test_unscramble(self):
        # scrambleString
        # -- _scramble
        # -- _unscramble
        raise NotImplementedError()

    def test_decrypt(self):
        # encryptBitStream
        # -- mail_decrypt
        # -- mail_encrypt
        raise NotImplementedError()

    def test_encrypt(self):
        # encryptBitStream
        # -- mail_decrypt
        # -- mail_encrypt
        raise NotImplementedError()

    def test_encryption_entries(self):
        # encryptionEntries
        # -- _encryption_entries
        raise NotImplementedError()

    def test_reset_byte(self):
        # getResetByte
        # -- _reset_byte
        raise NotImplementedError()
