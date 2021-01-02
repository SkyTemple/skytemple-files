"""Module for editing hardcoded data for the dungeons."""
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
from typing import List

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_uintle, write_uintle, AutoString, read_sintle, write_sintle, \
    generate_bitfield

DUNGEON_LIST_ENTRY_LEN = 4
DUNGEON_RESTRICTIONS_ENTRY_LEN = 12
SECONDARY_TERRAINS_ENTRY_LEN = 1
MAP_MARKER_PLACEMENTS_ENTRY_LEN = 8


class DungeonDefinition(AutoString):
    def __init__(self, number_floors: int, mappa_index: int, start_after: int, number_floors_in_group: int):
        self.number_floors = number_floors
        self.mappa_index = mappa_index
        self.start_after = start_after
        self.number_floors_in_group = number_floors_in_group

    def __eq__(self, other):
        if not isinstance(other, DungeonDefinition):
            return False
        return self.number_floors == other.number_floors and \
               self.mappa_index == other.mappa_index and \
               self.start_after == other.start_after and \
               self.number_floors_in_group == other.number_floors_in_group


class DungeonRestrictionDirection(Enum):
    DOWN = 0
    UP = 1


class DungeonRestriction(AutoString):
    def __init__(
            self, direction: DungeonRestrictionDirection, enemies_evolve_when_team_member_koed: bool, enemies_grant_exp: bool,
            recruiting_allowed: bool, level_reset: bool, money_allowed: bool, leader_can_be_changed: bool,
            dont_save_before_entering: bool, iq_skills_disabled: bool, traps_remain_invisible_on_attack: bool,
            enemies_can_drop_chests: bool, max_rescue_attempts: int, max_items_allowed: int, max_party_members: int,
            null7: int, turn_limit: int, nullA: int, nullB: int
    ):
        self.direction = direction
        self.enemies_evolve_when_team_member_koed = enemies_evolve_when_team_member_koed
        self.enemies_grant_exp = enemies_grant_exp
        self.recruiting_allowed = recruiting_allowed
        self.level_reset = level_reset
        self.money_allowed = money_allowed
        self.leader_can_be_changed = leader_can_be_changed
        self.dont_save_before_entering = dont_save_before_entering
        self.iq_skills_disabled = iq_skills_disabled
        self.traps_remain_invisible_on_attack = traps_remain_invisible_on_attack
        self.enemies_can_drop_chests = enemies_can_drop_chests
        self.max_rescue_attempts = max_rescue_attempts
        self.max_items_allowed = max_items_allowed
        self.max_party_members = max_party_members
        self.null7 = null7
        self.turn_limit = turn_limit
        self.nullA = nullA
        self.nullB = nullB

    @classmethod
    def from_bytes(cls, b: bytes) -> 'DungeonRestriction':
        bitfield0 = read_uintle(b, 0)
        bitfield1 = read_uintle(b, 1)
        dir_bool, enemies_evolve_when_team_member_koed, enemies_grant_exp, recruiting_allowed, \
            level_reset, money_allowed, leader_can_be_changed, dont_save_before_entering = \
            (bool(bitfield0 >> i & 1) for i in range(8))
        iq_skills_disabled, traps_remain_invisible_on_attack, enemies_can_drop_chests = \
            (bool(bitfield1 >> i & 1) for i in range(3))
        assert read_uintle(b, 2) == 0
        assert read_uintle(b, 3) == 0
        return cls(
            DungeonRestrictionDirection(int(dir_bool)), enemies_evolve_when_team_member_koed, enemies_grant_exp, recruiting_allowed,
            level_reset, money_allowed, leader_can_be_changed, dont_save_before_entering,
            iq_skills_disabled, traps_remain_invisible_on_attack, enemies_can_drop_chests,
            read_sintle(b, 4), read_sintle(b, 5), read_sintle(b, 6),
            read_sintle(b, 7), read_sintle(b, 8, 2), read_sintle(b, 10), read_sintle(b, 11),
        )

    def to_bytes(self) -> bytes:
        bitfield0 = generate_bitfield((self.dont_save_before_entering, self.leader_can_be_changed, self.money_allowed,
                                       self.level_reset, self.recruiting_allowed, self.enemies_grant_exp,
                                       self.enemies_evolve_when_team_member_koed, bool(self.direction.value)))
        bitfield1 = generate_bitfield((False, False, False, False, False,
                                      self.enemies_can_drop_chests, self.traps_remain_invisible_on_attack,
                                      self.iq_skills_disabled))
        bitfield2 = 0
        bitfield3 = 0
        buff = bytearray(DUNGEON_RESTRICTIONS_ENTRY_LEN)
        write_uintle(buff, bitfield0, 0, 1)
        write_uintle(buff, bitfield1, 1, 1)
        write_uintle(buff, bitfield2, 2, 1)
        write_uintle(buff, bitfield3, 3, 1)
        write_sintle(buff, self.max_rescue_attempts, 4, 1)
        write_sintle(buff, self.max_items_allowed, 5, 1)
        write_sintle(buff, self.max_party_members, 6, 1)
        write_sintle(buff, self.null7, 7, 1)
        write_sintle(buff, self.turn_limit, 8, 2)
        write_sintle(buff, self.nullA, 10, 1)
        write_sintle(buff, self.nullB, 11, 1)
        return buff

    def __eq__(self, other):
        if not isinstance(other, DungeonRestriction):
            return False
        return self.direction == other.direction and \
               self.enemies_evolve_when_team_member_koed == other.enemies_evolve_when_team_member_koed and \
               self.enemies_grant_exp == other.enemies_grant_exp and \
               self.recruiting_allowed == other.recruiting_allowed and \
               self.level_reset == other.level_reset and \
               self.money_allowed == other.money_allowed and \
               self.leader_can_be_changed == other.leader_can_be_changed and \
               self.dont_save_before_entering == other.dont_save_before_entering and \
               self.iq_skills_disabled == other.iq_skills_disabled and \
               self.traps_remain_invisible_on_attack == other.traps_remain_invisible_on_attack and \
               self.enemies_can_drop_chests == other.enemies_can_drop_chests and \
               self.max_rescue_attempts == other.max_rescue_attempts and \
               self.max_items_allowed == other.max_items_allowed and \
               self.max_party_members == other.max_party_members and \
               self.null7 == other.null7 and \
               self.turn_limit == other.turn_limit and \
               self.nullA == other.nullA and \
               self.nullB == other.nullB


class SecondaryTerrainTableEntry(Enum):
    WATER = 0
    LAVA = 1
    VOID = 2


class MapMarkerPlacement(AutoString):
    def __init__(self, level_id: int, reference_id: int, x: int, y: int):
        self.level_id = level_id
        self.reference_id = reference_id
        self.x = x
        self.y = y

    @classmethod
    def from_bytes(cls, b: bytes) -> 'MapMarkerPlacement':
        return MapMarkerPlacement(
            read_sintle(b, 0, 2),
            read_sintle(b, 2, 2),
            read_sintle(b, 4, 2),
            read_sintle(b, 6, 2)
        )

    def to_bytes(self) -> bytes:
        buff = bytearray(MAP_MARKER_PLACEMENTS_ENTRY_LEN)
        write_sintle(buff, self.level_id, 0, 2)
        write_sintle(buff, self.reference_id, 2, 2)
        write_sintle(buff, self.x, 4, 2)
        write_sintle(buff, self.y, 6, 2)
        return buff

    def __eq__(self, other):
        if not isinstance(other, MapMarkerPlacement):
            return False
        return self.level_id == other.level_id and \
               self.reference_id == other.reference_id and \
               self.x == other.x and \
               self.y == other.y


class HardcodedDungeons:
    @staticmethod
    def get_dungeon_list(arm9bin: bytes, config: Pmd2Data) -> List[DungeonDefinition]:
        """Returns the list of dungeon definitions."""
        block = config.binaries['arm9.bin'].blocks['DungeonList']
        lst = []
        for i in range(block.begin, block.end, DUNGEON_LIST_ENTRY_LEN):
            lst.append(DungeonDefinition(
                read_uintle(arm9bin, i),
                read_uintle(arm9bin, i + 1),
                read_uintle(arm9bin, i + 2),
                read_uintle(arm9bin, i + 3),
            ))
        return lst

    @staticmethod
    def set_dungeon_list(value: List[DungeonDefinition], arm9bin: bytearray, config: Pmd2Data):
        """
        Sets the dungeon definitions.
        The length of the list must exactly match the original ROM's length (see get_dungeon_list).
        """
        block = config.binaries['arm9.bin'].blocks['DungeonList']
        expected_length = int((block.end - block.begin) / DUNGEON_LIST_ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            arm9bin[block.begin + i * DUNGEON_LIST_ENTRY_LEN:block.begin + (i + 1) * DUNGEON_LIST_ENTRY_LEN] = bytes([
                entry.number_floors, entry.mappa_index, entry.start_after, entry.number_floors_in_group
            ])

    @staticmethod
    def get_dungeon_restrictions(arm9bin: bytes, config: Pmd2Data) -> List[DungeonRestriction]:
        """Returns the list of dungeon restrictions."""
        block = config.binaries['arm9.bin'].blocks['DungeonRestrictions']
        lst = []
        for i in range(block.begin, block.end, DUNGEON_RESTRICTIONS_ENTRY_LEN):
            lst.append(DungeonRestriction.from_bytes(arm9bin[i:i+DUNGEON_RESTRICTIONS_ENTRY_LEN]))
        return lst

    @staticmethod
    def set_dungeon_restrictions(value: List[DungeonRestriction], arm9bin: bytearray, config: Pmd2Data):
        """
        Sets the dungeon restrictions.
        The length of the list must exactly match the original ROM's length (see get_dungeon_restrictions).
        """
        block = config.binaries['arm9.bin'].blocks['DungeonRestrictions']
        expected_length = int((block.end - block.begin) / DUNGEON_RESTRICTIONS_ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            start = block.begin + (i * DUNGEON_RESTRICTIONS_ENTRY_LEN)
            arm9bin[start:start + DUNGEON_RESTRICTIONS_ENTRY_LEN] = entry.to_bytes()

    @staticmethod
    def get_secondary_terrains(arm9bin: bytes, config: Pmd2Data) -> List[SecondaryTerrainTableEntry]:
        """Returns the list of secondary terrains."""
        block = config.binaries['arm9.bin'].blocks['SecondaryTerrains']
        lst = []
        for i in range(block.begin, block.end, SECONDARY_TERRAINS_ENTRY_LEN):
            lst.append(SecondaryTerrainTableEntry(
                int.from_bytes(arm9bin[i:i+ SECONDARY_TERRAINS_ENTRY_LEN], 'little',
                               signed=False)
            ))
        return lst

    @staticmethod
    def set_secondary_terrains(value: List[SecondaryTerrainTableEntry], arm9bin: bytearray, config: Pmd2Data):
        """
        Sets the secondary terrains.
        The length of the list must exactly match the original ROM's length (see get_secondary_terrains).
        """
        block = config.binaries['arm9.bin'].blocks['SecondaryTerrains']
        expected_length = int((block.end - block.begin) / SECONDARY_TERRAINS_ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            start = block.begin + (i * SECONDARY_TERRAINS_ENTRY_LEN)
            arm9bin[start:start + SECONDARY_TERRAINS_ENTRY_LEN] = entry.value.to_bytes(SECONDARY_TERRAINS_ENTRY_LEN,
                                                                                       'little', signed=False)

    @staticmethod
    def get_marker_placements(arm9bin: bytes, config: Pmd2Data) -> List[MapMarkerPlacement]:
        """Returns the list of secondary terrains."""
        block = config.binaries['arm9.bin'].blocks['MapMarkerPlacements']
        lst = []
        for i in range(block.begin, block.end, MAP_MARKER_PLACEMENTS_ENTRY_LEN):
            lst.append(MapMarkerPlacement.from_bytes(arm9bin[i:i+MAP_MARKER_PLACEMENTS_ENTRY_LEN]))
        return lst

    @staticmethod
    def set_marker_placements(value: List[MapMarkerPlacement], arm9bin: bytearray, config: Pmd2Data):
        """
        Sets the secondary terrains.
        The length of the list must exactly match the original ROM's length (see get_secondary_terrains).
        """
        block = config.binaries['arm9.bin'].blocks['MapMarkerPlacements']
        expected_length = int((block.end - block.begin) / MAP_MARKER_PLACEMENTS_ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            start = block.begin + (i * MAP_MARKER_PLACEMENTS_ENTRY_LEN)
            arm9bin[start:start + MAP_MARKER_PLACEMENTS_ENTRY_LEN] = entry.to_bytes()
