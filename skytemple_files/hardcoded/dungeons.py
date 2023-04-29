"""Module for editing hardcoded data for the dungeons."""
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

from enum import Enum
from typing import no_type_check, List

from range_typed_integers import u8, i8, i16

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import (
    AutoString,
    write_u32,
    write_i8,
    read_u8,
    read_u16,
    generate_bitfield,
    read_i16,
    write_u16,
    write_i16,
    read_u32,
    write_u8,
    read_i8,
)
from skytemple_files.data.md.protocol import PokeType

DUNGEON_LIST_ENTRY_LEN = 4
DUNGEON_RESTRICTIONS_ENTRY_LEN = 12
SECONDARY_TERRAINS_ENTRY_LEN = 1
MAP_MARKER_PLACEMENTS_ENTRY_LEN = 8
TILESET_PROPERTIES_ENTRY_LEN = 0xC


class DungeonDefinition(AutoString):
    number_floors: u8
    mappa_index: u8
    start_after: u8
    number_floors_in_group: u8

    def __init__(
        self,
        number_floors: u8,
        mappa_index: u8,
        start_after: u8,
        number_floors_in_group: u8,
    ):
        self.number_floors = number_floors
        self.mappa_index = mappa_index
        self.start_after = start_after
        self.number_floors_in_group = number_floors_in_group

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DungeonDefinition):
            return False
        return (
            self.number_floors == other.number_floors
            and self.mappa_index == other.mappa_index
            and self.start_after == other.start_after
            and self.number_floors_in_group == other.number_floors_in_group
        )


class DungeonRestrictionDirection(Enum):
    DOWN = 0
    UP = 1


class DungeonRestriction(AutoString):
    direction: DungeonRestrictionDirection
    enemies_evolve_when_team_member_koed: bool
    enemies_grant_exp: bool
    recruiting_allowed: bool
    level_reset: bool
    money_allowed: bool
    leader_can_be_changed: bool
    dont_save_before_entering: bool
    iq_skills_disabled: bool
    traps_remain_invisible_on_attack: bool
    enemies_can_drop_chests: bool
    max_rescue_attempts: i8
    max_items_allowed: i8
    max_party_members: i8
    null7: i8
    turn_limit: i16
    random_movement_chance: i16

    def __init__(
        self,
        direction: DungeonRestrictionDirection,
        enemies_evolve_when_team_member_koed: bool,
        enemies_grant_exp: bool,
        recruiting_allowed: bool,
        level_reset: bool,
        money_allowed: bool,
        leader_can_be_changed: bool,
        dont_save_before_entering: bool,
        iq_skills_disabled: bool,
        traps_remain_invisible_on_attack: bool,
        enemies_can_drop_chests: bool,
        max_rescue_attempts: i8,
        max_items_allowed: i8,
        max_party_members: i8,
        null7: i8,
        turn_limit: i16,
        random_movement_chance: i16,
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
        self.random_movement_chance = random_movement_chance

    @classmethod
    def from_bytes(cls, b: bytes) -> "DungeonRestriction":
        bitfield0 = read_u8(b, 0)
        bitfield1 = read_u8(b, 1)
        (
            dir_bool,
            enemies_evolve_when_team_member_koed,
            enemies_grant_exp,
            recruiting_allowed,
            level_reset,
            money_allowed,
            leader_can_be_changed,
            dont_save_before_entering,
        ) = (bool(bitfield0 >> i & 1) for i in range(8))
        (
            iq_skills_disabled,
            traps_remain_invisible_on_attack,
            enemies_can_drop_chests,
        ) = (bool(bitfield1 >> i & 1) for i in range(3))
        assert read_u8(b, 2) == 0
        assert read_u8(b, 3) == 0
        return cls(
            DungeonRestrictionDirection(int(dir_bool)),
            enemies_evolve_when_team_member_koed,
            enemies_grant_exp,
            recruiting_allowed,
            level_reset,
            money_allowed,
            leader_can_be_changed,
            dont_save_before_entering,
            iq_skills_disabled,
            traps_remain_invisible_on_attack,
            enemies_can_drop_chests,
            read_i8(b, 4),
            read_i8(b, 5),
            read_i8(b, 6),
            read_i8(b, 7),
            read_i16(b, 8),
            read_i16(b, 10),
        )

    def to_bytes(self) -> bytes:
        bitfield0 = u8(
            generate_bitfield(
                (
                    self.dont_save_before_entering,
                    self.leader_can_be_changed,
                    self.money_allowed,
                    self.level_reset,
                    self.recruiting_allowed,
                    self.enemies_grant_exp,
                    self.enemies_evolve_when_team_member_koed,
                    bool(self.direction.value),
                )
            )
        )
        bitfield1 = u8(
            generate_bitfield(
                (
                    False,
                    False,
                    False,
                    False,
                    False,
                    self.enemies_can_drop_chests,
                    self.traps_remain_invisible_on_attack,
                    self.iq_skills_disabled,
                )
            )
        )
        bitfield2 = u8(0)
        bitfield3 = u8(0)
        buff = bytearray(DUNGEON_RESTRICTIONS_ENTRY_LEN)
        write_u8(buff, bitfield0, 0)
        write_u8(buff, bitfield1, 1)
        write_u8(buff, bitfield2, 2)
        write_u8(buff, bitfield3, 3)
        write_i8(buff, self.max_rescue_attempts, 4)
        write_i8(buff, self.max_items_allowed, 5)
        write_i8(buff, self.max_party_members, 6)
        write_i8(buff, self.null7, 7)
        write_i16(buff, self.turn_limit, 8)
        write_i16(buff, self.random_movement_chance, 10)
        return buff

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DungeonRestriction):
            return False
        return (
            self.direction == other.direction
            and self.enemies_evolve_when_team_member_koed
            == other.enemies_evolve_when_team_member_koed
            and self.enemies_grant_exp == other.enemies_grant_exp
            and self.recruiting_allowed == other.recruiting_allowed
            and self.level_reset == other.level_reset
            and self.money_allowed == other.money_allowed
            and self.leader_can_be_changed == other.leader_can_be_changed
            and self.dont_save_before_entering == other.dont_save_before_entering
            and self.iq_skills_disabled == other.iq_skills_disabled
            and self.traps_remain_invisible_on_attack
            == other.traps_remain_invisible_on_attack
            and self.enemies_can_drop_chests == other.enemies_can_drop_chests
            and self.max_rescue_attempts == other.max_rescue_attempts
            and self.max_items_allowed == other.max_items_allowed
            and self.max_party_members == other.max_party_members
            and self.null7 == other.null7
            and self.turn_limit == other.turn_limit
            and self.random_movement_chance == other.random_movement_chance
        )


class SecondaryTerrainTableEntry(Enum):
    WATER = 0
    LAVA = 1
    VOID = 2


class MapMarkerPlacement(AutoString):
    level_id: i16
    reference_id: i16
    x: i16
    y: i16

    def __init__(self, level_id: i16, reference_id: i16, x: i16, y: i16):
        self.level_id = level_id
        self.reference_id = reference_id
        self.x = x
        self.y = y

    @classmethod
    def from_bytes(cls, b: bytes) -> "MapMarkerPlacement":
        return MapMarkerPlacement(
            read_i16(b, 0), read_i16(b, 2), read_i16(b, 4), read_i16(b, 6)
        )

    def to_bytes(self) -> bytes:
        buff = bytearray(MAP_MARKER_PLACEMENTS_ENTRY_LEN)
        write_i16(buff, self.level_id, 0)
        write_i16(buff, self.reference_id, 2)
        write_i16(buff, self.x, 4)
        write_i16(buff, self.y, 6)
        return buff

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MapMarkerPlacement):
            return False
        return (
            self.level_id == other.level_id
            and self.reference_id == other.reference_id
            and self.x == other.x
            and self.y == other.y
        )


class TilesetBaseEnum(Enum):
    def __new__(cls, *args, **kwargs):  # type: ignore  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, name_localized: str):
        self.name_localized = name_localized

    @property
    def print_name(self) -> str:
        return self.name_localized


class TilesetMapColor(TilesetBaseEnum):
    WHITE = 0, _("White")
    BLACK = 1, _("Black")
    RED = 2, _("Red")
    BLUE = 3, _("Blue")
    GREEN = 4, _("Green")
    YELLOW = 5, _("Yellow")
    ORANGE = 6, _("Orange")
    PURPLE = 7, _("Purple")
    PINK = 8, _("Pink")


class TilesetStirringEffect(TilesetBaseEnum):
    LEAVES = 0, _("Leaves")
    SNOWFLAKES = 1, _("Snowflakes")
    FLAMES = 2, _("Flames")
    SAND = 3, _("Sand")
    BUBBLES = 4, _("Bubbles")
    EARTHQUAKE = 5, _("Earthquake")


class TilesetSecretPowerEffect(TilesetBaseEnum):
    UNK_0 = 0, _("???") + " (0)"
    SLEEP = 1, _("Sleep")  # TRANSLATORS: Move name
    SPEED_DOWN = 2, _(
        "Speed -1"
    )  # TRANSLATORS: Effect of a tileset's secret power move
    ATTACK_DOWN = 3, _(
        "Attack -1"
    )  # TRANSLATORS: Effect of a tileset's secret power move
    UNK_4 = 4, _("???") + " (4)"
    ACCURACY_DOWN = 5, _(
        "Accuracy -1"
    )  # TRANSLATORS: Effect of a tileset's secret power move
    UNK_6 = 6, _("???") + " (6)"
    CRINGE = 7, _("Cringe")  # TRANSLATORS: Move name
    FREEZE = 8, _("Freeze")  # TRANSLATORS: Status
    PARALYSIS = 9, _("Paralysis")  # TRANSLATORS: Status


class TilesetNaturePowerMoveEntry(TilesetBaseEnum):
    UNK_0 = 0, _("???") + " (0)"
    UNK_1 = 1, _("???") + " (1)"
    UNK_2 = 2, _("???") + " (2)"
    UNK_3 = 3, _("???") + " (3)"
    EARTHQUAKE = 4, _("Earthquake")  # TRANSLATORS: Move name
    UNK_5 = 5, _("???") + " (5)"
    UNK_6 = 6, _("???") + " (6)"
    ROCK_SLIDE = 7, _("Rock Slide")  # TRANSLATORS: Move name
    UNK_8 = 8, _("???") + " (8)"
    TRI_ATTACK = 9, _("Tri Attack")  # TRANSLATORS: Move name
    HYDRO_PUMP = 10, _("Hydro Pump")  # TRANSLATORS: Move name
    BLIZZARD = 11, _("Blizzard")  # TRANSLATORS: Move name
    ICE_BEAM = 12, _("Ice Beam")  # TRANSLATORS: Move name
    SEED_BOMB = 13, _("Seed Bomb")  # TRANSLATORS: Move name
    MUD_BOMB = 14, _("Mud Bomb")  # TRANSLATORS: Move name


class TilesetWeatherEffect(TilesetBaseEnum):
    CLEAR = 0, _("Clear")
    FOGGY1 = 1, _("Foggy 1")
    FOGGY2 = 2, _("Foggy 2")
    FOGGY3 = 3, _("Foggy 3")
    FOGGY4 = 4, _("Foggy 4")
    FOGGY5 = 5, _("Foggy 5")
    FOGGY6 = 6, _("Foggy 6")


class TilesetProperties(AutoString):
    map_color: TilesetMapColor
    stirring_effect: TilesetStirringEffect
    secret_power_effect: TilesetSecretPowerEffect
    camouflage_type: PokeType
    nature_power_move_entry: TilesetNaturePowerMoveEntry
    weather_effect: TilesetWeatherEffect
    full_water_floor: bool

    def __init__(
        self,
        map_color: TilesetMapColor,
        stirring_effect: TilesetStirringEffect,
        secret_power_effect: TilesetSecretPowerEffect,
        camouflage_type: PokeType,
        nature_power_move_entry: TilesetNaturePowerMoveEntry,
        weather_effect: TilesetWeatherEffect,
        full_water_floor: bool,
    ):
        self.map_color = map_color
        self.stirring_effect = stirring_effect
        self.secret_power_effect = secret_power_effect
        self.camouflage_type = camouflage_type
        self.nature_power_move_entry = nature_power_move_entry
        self.weather_effect = weather_effect
        self.full_water_floor = full_water_floor

    @classmethod
    @no_type_check
    def from_bytes(cls, b: bytes) -> "TilesetProperties":
        return TilesetProperties(
            TilesetMapColor(read_u32(b, 0)),
            TilesetStirringEffect(read_u8(b, 4)),
            TilesetSecretPowerEffect(read_u8(b, 5)),
            PokeType(read_u16(b, 6)),
            TilesetNaturePowerMoveEntry(read_u16(b, 8)),
            TilesetWeatherEffect(read_u8(b, 10)),
            bool(read_u8(b, 11)),
        )

    def to_bytes(self) -> bytes:
        buff = bytearray(TILESET_PROPERTIES_ENTRY_LEN)
        write_u32(buff, self.map_color.value, 0)
        write_u8(buff, self.stirring_effect.value, 4)
        write_u8(buff, self.secret_power_effect.value, 5)
        write_u16(buff, self.camouflage_type.value, 6)
        write_u16(buff, self.nature_power_move_entry.value, 8)
        write_u8(buff, self.weather_effect.value, 10)
        write_u8(buff, u8(int(self.full_water_floor)), 11)
        return buff

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TilesetProperties):
            return False
        return (
            self.map_color == other.map_color
            and self.stirring_effect == other.stirring_effect
            and self.secret_power_effect == other.secret_power_effect
            and self.camouflage_type == other.camouflage_type
            and self.nature_power_move_entry == other.nature_power_move_entry
            and self.weather_effect == other.weather_effect
            and self.full_water_floor == other.full_water_floor
        )


class HardcodedDungeons:
    @staticmethod
    def get_dungeon_list(arm9bin: bytes, config: Pmd2Data) -> List[DungeonDefinition]:
        """Returns the list of dungeon definitions."""
        block = config.bin_sections.arm9.data.DUNGEON_DATA_LIST
        lst = []
        for i in range(
            block.address, block.address + block.length, DUNGEON_LIST_ENTRY_LEN
        ):
            lst.append(
                DungeonDefinition(
                    read_u8(arm9bin, i),
                    read_u8(arm9bin, i + 1),
                    read_u8(arm9bin, i + 2),
                    read_u8(arm9bin, i + 3),
                )
            )
        return lst

    @staticmethod
    def set_dungeon_list(
        value: List[DungeonDefinition], arm9bin: bytearray, config: Pmd2Data
    ) -> None:
        """
        Sets the dungeon definitions.
        The length of the list must exactly match the original ROM's length (see get_dungeon_list).
        """
        block = config.bin_sections.arm9.data.DUNGEON_DATA_LIST
        assert block.length is not None
        expected_length = int(block.length / DUNGEON_LIST_ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(
                f"The list must have exactly the length of {expected_length} entries."
            )
        for i, entry in enumerate(value):
            arm9bin[
                block.address
                + i * DUNGEON_LIST_ENTRY_LEN : block.address
                + (i + 1) * DUNGEON_LIST_ENTRY_LEN
            ] = bytes(
                [
                    entry.number_floors,
                    entry.mappa_index,
                    entry.start_after,
                    entry.number_floors_in_group,
                ]
            )

    @staticmethod
    def get_dungeon_restrictions(
        arm9bin: bytes, config: Pmd2Data
    ) -> List[DungeonRestriction]:
        """Returns the list of dungeon restrictions."""
        block = config.bin_sections.arm9.data.DUNGEON_RESTRICTIONS
        lst = []
        for i in range(
            block.address, block.address + block.length, DUNGEON_RESTRICTIONS_ENTRY_LEN
        ):
            lst.append(
                DungeonRestriction.from_bytes(
                    arm9bin[i : i + DUNGEON_RESTRICTIONS_ENTRY_LEN]
                )
            )
        return lst

    @staticmethod
    def set_dungeon_restrictions(
        value: List[DungeonRestriction], arm9bin: bytearray, config: Pmd2Data
    ) -> None:
        """
        Sets the dungeon restrictions.
        The length of the list must exactly match the original ROM's length (see get_dungeon_restrictions).
        """
        block = config.bin_sections.arm9.data.DUNGEON_RESTRICTIONS
        assert block.length is not None
        expected_length = int(block.length / DUNGEON_RESTRICTIONS_ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(
                f"The list must have exactly the length of {expected_length} entries."
            )
        for i, entry in enumerate(value):
            start = block.address + (i * DUNGEON_RESTRICTIONS_ENTRY_LEN)
            arm9bin[start : start + DUNGEON_RESTRICTIONS_ENTRY_LEN] = entry.to_bytes()

    @staticmethod
    def get_secondary_terrains(
        arm9bin: bytes, config: Pmd2Data
    ) -> List[SecondaryTerrainTableEntry]:
        """Returns the list of secondary terrains."""
        block = config.bin_sections.arm9.data.SECONDARY_TERRAIN_TYPES
        lst = []
        for i in range(
            block.address, block.address + block.length, SECONDARY_TERRAINS_ENTRY_LEN
        ):
            lst.append(
                SecondaryTerrainTableEntry(
                    int.from_bytes(
                        arm9bin[i : i + SECONDARY_TERRAINS_ENTRY_LEN],
                        "little",
                        signed=False,
                    )
                )
            )
        return lst

    @staticmethod
    def set_secondary_terrains(
        value: List[SecondaryTerrainTableEntry], arm9bin: bytearray, config: Pmd2Data
    ) -> None:
        """
        Sets the secondary terrains.
        The length of the list must exactly match the original ROM's length (see get_secondary_terrains).
        """
        block = config.bin_sections.arm9.data.SECONDARY_TERRAIN_TYPES
        assert block.length is not None
        expected_length = int(block.length / SECONDARY_TERRAINS_ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(
                f"The list must have exactly the length of {expected_length} entries."
            )
        for i, entry in enumerate(value):
            start = block.address + (i * SECONDARY_TERRAINS_ENTRY_LEN)
            arm9bin[
                start : start + SECONDARY_TERRAINS_ENTRY_LEN
            ] = entry.value.to_bytes(
                SECONDARY_TERRAINS_ENTRY_LEN, "little", signed=False
            )

    @staticmethod
    def get_marker_placements(
        arm9bin: bytes, config: Pmd2Data
    ) -> List[MapMarkerPlacement]:
        """Returns the list of secondary terrains."""
        block = config.bin_sections.arm9.data.MAP_MARKER_PLACEMENTS
        lst = []
        for i in range(
            block.address, block.address + block.length, MAP_MARKER_PLACEMENTS_ENTRY_LEN
        ):
            lst.append(
                MapMarkerPlacement.from_bytes(
                    arm9bin[i : i + MAP_MARKER_PLACEMENTS_ENTRY_LEN]
                )
            )
        return lst

    @staticmethod
    def set_marker_placements(
        value: List[MapMarkerPlacement], arm9bin: bytearray, config: Pmd2Data
    ) -> None:
        """
        Sets the secondary terrains.
        The length of the list must exactly match the original ROM's length (see get_secondary_terrains).
        """
        block = config.bin_sections.arm9.data.MAP_MARKER_PLACEMENTS
        assert block.length is not None
        expected_length = int(block.length / MAP_MARKER_PLACEMENTS_ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(
                f"The list must have exactly the length of {expected_length} entries."
            )
        for i, entry in enumerate(value):
            start = block.address + (i * MAP_MARKER_PLACEMENTS_ENTRY_LEN)
            arm9bin[start : start + MAP_MARKER_PLACEMENTS_ENTRY_LEN] = entry.to_bytes()

    @staticmethod
    def get_tileset_properties(
        ov10: bytes, config: Pmd2Data
    ) -> List[TilesetProperties]:
        block = config.bin_sections.overlay10.data.TILESET_PROPERTIES
        lst = []
        for i in range(
            block.address, block.address + block.length, TILESET_PROPERTIES_ENTRY_LEN
        ):
            lst.append(
                TilesetProperties.from_bytes(ov10[i : i + TILESET_PROPERTIES_ENTRY_LEN])
            )
        return lst

    @staticmethod
    def set_tileset_properties(
        value: List[TilesetProperties], ov10: bytearray, config: Pmd2Data
    ) -> None:
        block = config.bin_sections.overlay10.data.TILESET_PROPERTIES
        assert block.length is not None
        expected_length = int(block.length / TILESET_PROPERTIES_ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(
                f"The list must have exactly the length of {expected_length} entries."
            )
        for i, entry in enumerate(value):
            start = block.address + (i * TILESET_PROPERTIES_ENTRY_LEN)
            ov10[start : start + TILESET_PROPERTIES_ENTRY_LEN] = entry.to_bytes()
