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
from typing import Any, List

from pmdsky_debug_py.protocol import Overlay29Protocol, Symbol
from range_typed_integers import u32_checked, u32, u16, u8

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import (
    AutoString,
    write_u32,
    read_u8,
    read_u16,
    write_u16,
    read_u32,
    write_u8,
)


class EntitySpawnEntry(AutoString):
    def __init__(
        self,
        overlay29bin: Overlay29Protocol,
        item_spawn_pointer: u32,
        monster_spawn_pointer: u32,
        tile_spawn_pointer: u32,
    ):
        self._overlay29bin = overlay29bin
        self.item_id = (
            item_spawn_pointer
            - self._overlay29bin.data.FIXED_ROOM_ITEM_SPAWN_TABLE.absolute_address
        ) // 8
        self.monster_id = (
            monster_spawn_pointer
            - self._overlay29bin.data.FIXED_ROOM_MONSTER_SPAWN_TABLE.absolute_address
        ) // 4
        self.tile_id = (
            tile_spawn_pointer
            - self._overlay29bin.data.FIXED_ROOM_TILE_SPAWN_TABLE.absolute_address
        ) // 4

    def to_bytes(self) -> bytes:
        buffer = bytearray(12)
        write_u32(
            buffer,
            u32_checked(
                self.item_id * 8
                + self._overlay29bin.data.FIXED_ROOM_ITEM_SPAWN_TABLE.absolute_address
            ),
            0,
        )
        write_u32(
            buffer,
            u32_checked(
                self.monster_id * 4
                + self._overlay29bin.data.FIXED_ROOM_MONSTER_SPAWN_TABLE.absolute_address
            ),
            4,
        )
        write_u32(
            buffer,
            u32_checked(
                self.tile_id * 4
                + self._overlay29bin.data.FIXED_ROOM_TILE_SPAWN_TABLE.absolute_address
            ),
            8,
        )
        return buffer

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EntitySpawnEntry):
            return False
        return (
            self.item_id == other.item_id
            and self.monster_id == other.monster_id
            and self.tile_id == other.tile_id
        )


class ItemSpawn(AutoString):
    item_id: u16
    quantity: u16
    null2: u16
    null3: u16

    def __init__(self, item_id: u16, quantity: u16, null2: u16, null3: u16):
        self.item_id = item_id
        self.quantity = quantity
        self.null2 = null2
        self.null3 = null3

    def to_bytes(self) -> bytes:
        buffer = bytearray(8)
        write_u16(buffer, self.item_id, 0)
        write_u16(buffer, self.quantity, 2)
        write_u16(buffer, self.null2, 4)
        write_u16(buffer, self.null3, 6)
        return buffer

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ItemSpawn):
            return False
        return (
            self.item_id == other.item_id
            and self.quantity == other.quantity
            and self.null2 == other.null2
            and self.null3 == other.null3
        )


class MonsterSpawnType(Enum):
    # Note: this is based on observations when changing the spawn type
    # So this may be not accurate
    # All seem to have different ways to init their stats

    # A normal enemy, this isn't used in fixed rooms, so it might be
    # the type used for normal spawns in random generated floors
    ENEMY_NORMAL = 0x00, _("Normal Enemy")
    # An outlaw enemy
    OUTLAW = 0x01, _("Outlaw")
    # A strange enemy that has the same behavior as the outlaw type
    ENEMY_OUTLAW = 0x02, _("Outlaw Enemy")
    # An outlaw enemy running away from you
    OUTLAW_RUN = 0x03, _("Outlaw Running Away")

    # The spawn types used for battles against rival teams
    # One for the leader
    TEAM_LEADER = 0x04, _("Rival Team Leader")
    # And one for their members
    TEAM_MEMBER = 0x05, _("Rival Team Member")
    # A strong enemy that uses stats from the fixed stats table
    ENEMY_STRONG = 0x06, _("Strong Enemy")
    # An ally waiting to be rescued. If you talk to them, it will ask you
    # if you want to rescue them
    ALLY_WFR = 0x07, _("Waiting for Rescue Ally")

    # The 8th spawn type is an enemy type with a broken AI
    # and spawn type 8 is not used so it is not included in this enum

    # A normal enemy, except that this time it is used in fixed floors
    ENEMY_NORMAL_2 = 0x09, _("Normal Enemy")
    # An ally who will help you in battles
    ALLY_HELP = 0x0A, _("Helping Ally")

    # Team from another game
    OTHER_GAME_LEADER = 0xB, _("Other Game Team Leader")
    OTHER_GAME_MEMBER_2 = 0xC, _("Other Game Team Member 2")
    OTHER_GAME_MEMBER_3 = 0xD, _("Other Game Team Member 3")
    OTHER_GAME_MEMBER_4 = 0xE, _("Other Game Team Member 4")

    # This entry is unknown and unused
    UNKNOWN_F = 0xF, _("Unknown 5")

    # The one that welcomes you in the bazaar
    BAZAAR_HOST = 0x10, _(
        "Bazaar Host"
    )  # TRANSLATORS: 'Name' of one of the Bazar NPC types
    # The shop that lets you heal all your HP, PP and belly
    BAZAAR_HEAL = 0x11, _(
        "Bazaar Healer"
    )  # TRANSLATORS: 'Name' of one of the Bazar NPC types
    # The shop that lets you buy surprise boxes which contain a random item
    BAZAAR_SURPRISE = 0x12, _(
        "Bazaar Surprise"
    )  # TRANSLATORS: 'Name' of one of the Bazar NPC types
    # The shop that lets you clean all your sticky items
    BAZAAR_CLEAN = 0x13, _(
        "Bazaar Clean Sticky Items"
    )  # TRANSLATORS: 'Name' of one of the Bazar NPC types
    # The shop that lets you escape the dungeon
    BAZAAR_ESCAPE = 0x14, _(
        "Bazaar Escape"
    )  # TRANSLATORS: 'Name' of one of the Bazar NPC types

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, description: str):
        self.description = description


class MonsterSpawn(AutoString):
    md_idx: u16
    stats_entry: u8

    def __init__(self, md_idx: u16, stats_entry: u8, enemy_settings: u8):
        self.md_idx = md_idx
        self.stats_entry = stats_entry
        # 3: (?) 6 if the pokémon is an enemy, 0xA if it's an ally, 9 if the only thing that is being spawned is
        # an item. If it's 6 or 0xA, the stats of the pokémon are determined by the stats entry specified on byte 2.
        self.enemy_settings = MonsterSpawnType(enemy_settings)  # type: ignore

    def to_bytes(self) -> bytes:
        buffer = bytearray(4)
        write_u16(buffer, self.md_idx, 0)
        write_u8(buffer, self.stats_entry, 2)
        write_u8(buffer, u8(self.enemy_settings.value), 3)
        return buffer

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MonsterSpawn):
            return False
        return (
            self.md_idx == other.md_idx
            and self.stats_entry == other.stats_entry
            and self.enemy_settings == other.enemy_settings
        )


class TileSpawn(AutoString):
    trap_id: u8
    trap_data: u8
    room_id: u8
    flags: u8

    def __init__(self, trap_id: u8, trap_data: u8, room_id: u8, flags: u8):
        self.trap_id = trap_id
        self.trap_data = trap_data
        self.room_id = room_id
        self.flags = flags

    def to_bytes(self) -> bytes:
        buffer = bytearray(4)
        write_u8(buffer, self.trap_id, 0)
        write_u8(buffer, self.trap_data, 1)
        write_u8(buffer, self.room_id, 2)
        write_u8(buffer, self.flags, 3)
        return buffer

    def can_be_broken(self) -> bool:
        return not (self.trap_data & 1)

    def trap_is_visible(self) -> bool:
        return self.flags & 1 > 0

    def is_secondary_terrain(self) -> bool:
        return self.flags & 0b1000 > 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TileSpawn):
            return False
        return (
            self.trap_id == other.trap_id
            and self.trap_data == other.trap_data
            and self.room_id == other.room_id
            and self.flags == other.flags
        )


class MonsterSpawnStats(AutoString):
    level: u16
    hp: u16
    exp_yield: u16
    attack: u8
    special_attack: u8
    defense: u8
    special_defense: u8
    unkA: u16

    def __init__(
        self,
        level: u16,
        hp: u16,
        exp_yield: u16,
        attack: u8,
        special_attack: u8,
        defense: u8,
        special_defense: u8,
        unkA: u16,
    ):
        self.level = level
        self.hp = hp
        self.exp_yield = exp_yield
        self.attack = attack
        self.special_attack = special_attack
        self.defense = defense
        self.special_defense = special_defense
        self.unkA = unkA

    def to_bytes(self) -> bytes:
        buffer = bytearray(12)
        write_u16(buffer, self.level, 0)
        write_u16(buffer, self.hp, 2)
        write_u16(buffer, self.exp_yield, 4)
        write_u8(buffer, self.attack, 6)
        write_u8(buffer, self.special_attack, 7)
        write_u8(buffer, self.defense, 8)
        write_u8(buffer, self.special_defense, 9)
        write_u16(buffer, self.unkA, 10)
        return buffer

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MonsterSpawnStats):
            return False
        return (
            self.level == other.level
            and self.hp == other.hp
            and self.exp_yield == other.exp_yield
            and self.attack == other.attack
            and self.special_attack == other.special_attack
            and self.defense == other.defense
            and self.special_defense == other.special_defense
            and self.unkA == other.unkA
        )


class FixedFloorProperties(AutoString):
    music_track: u32
    unk4: bool
    unk5: bool
    moves_enabled: bool
    orbs_enabled: bool
    unk8: bool
    unk9: bool
    exit_floor_when_defeating_enemies: bool
    null: u8

    def __init__(
        self,
        music_track: u32,
        unk4: bool,
        unk5: bool,
        moves_enabled: bool,
        orbs_enabled: bool,
        unk8: bool,
        unk9: bool,
        exit_floor_when_defeating_enemies: bool,
        null: u8,
    ):
        self.music_track = music_track
        self.unk4 = unk4
        self.unk5 = unk5
        self.moves_enabled = moves_enabled
        self.orbs_enabled = orbs_enabled
        self.unk8 = unk8
        self.unk9 = unk9
        self.exit_floor_when_defeating_enemies = exit_floor_when_defeating_enemies
        self.null = null

    def to_bytes(self) -> bytes:
        buffer = bytearray(12)
        write_u32(buffer, self.music_track, 0)
        write_u8(buffer, u8(int(self.unk4)), 4)
        write_u8(buffer, u8(int(self.unk5)), 5)
        write_u8(buffer, u8(int(self.moves_enabled)), 6)
        write_u8(buffer, u8(int(self.orbs_enabled)), 7)
        write_u8(buffer, u8(int(self.unk8)), 8)
        write_u8(buffer, u8(int(self.unk9)), 9)
        write_u8(buffer, u8(int(self.exit_floor_when_defeating_enemies)), 10)
        write_u8(buffer, self.null, 11)
        return buffer

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FixedFloorProperties):
            return False
        return (
            self.music_track == other.music_track
            and self.unk4 == other.unk4
            and self.unk5 == other.unk5
            and self.moves_enabled == other.moves_enabled
            and self.orbs_enabled == other.orbs_enabled
            and self.unk8 == other.unk8
            and self.unk9 == other.unk9
            and self.exit_floor_when_defeating_enemies
            == other.exit_floor_when_defeating_enemies
            and self.null == other.null
        )


class HardcodedFixedFloorTables:
    @classmethod
    def get_entity_spawn_table(
        cls, overlay29: bytes, config: Pmd2Data
    ) -> List[EntitySpawnEntry]:
        """
        Returns the list of entity spawns. Each entry has three references, one to each of
        the other three tables (item spawn, monster spawn, tile type).
        """
        binary = config.bin_sections.overlay29
        block = binary.data.FIXED_ROOM_ENTITY_SPAWN_TABLE
        lst = []
        for i in range(block.address, block.address + block.length, 12):
            lst.append(
                EntitySpawnEntry(
                    binary,
                    read_u32(overlay29, i + 0x00),
                    read_u32(overlay29, i + 0x04),
                    read_u32(overlay29, i + 0x08),
                )
            )
        return lst

    @classmethod
    def set_entity_spawn_table(
        cls, overlay29: bytearray, values: List[EntitySpawnEntry], config: Pmd2Data
    ) -> None:
        """
        Sets the list of entity spawns.
        The length of the list must exactly match the original ROM's length (see get_entity_spawn_table).
        """
        cls._set(
            overlay29,
            values,
            config,
            config.bin_sections.overlay29.data.FIXED_ROOM_ENTITY_SPAWN_TABLE,
            12,
        )

    @classmethod
    def get_item_spawn_list(cls, overlay29: bytes, config: Pmd2Data) -> List[ItemSpawn]:
        """
        Returns the list of items that can be spawned in fixed floors.
        """
        block = config.bin_sections.overlay29.data.FIXED_ROOM_ITEM_SPAWN_TABLE
        lst = []
        for i in range(block.address, block.address + block.length, 8):
            lst.append(
                ItemSpawn(
                    read_u16(overlay29, i + 0x00),
                    read_u16(overlay29, i + 0x02),
                    read_u16(overlay29, i + 0x04),
                    read_u16(overlay29, i + 0x06),
                )
            )
        return lst

    @classmethod
    def set_item_spawn_list(
        cls, overlay29: bytearray, values: List[ItemSpawn], config: Pmd2Data
    ) -> None:
        """
        Returns the list of items that can be spawned in fixed floors.
        The length of the list must exactly match the original ROM's length (see get_item_spawn_list).
        """
        cls._set(
            overlay29,
            values,
            config,
            config.bin_sections.overlay29.data.FIXED_ROOM_ITEM_SPAWN_TABLE,
            8,
        )

    @classmethod
    def get_monster_spawn_list(
        cls, overlay29: bytes, config: Pmd2Data
    ) -> List[MonsterSpawn]:
        """
        Returns the list of monsters that can be spawned in fixed floors.
        """
        block = config.bin_sections.overlay29.data.FIXED_ROOM_MONSTER_SPAWN_TABLE
        lst = []
        for i in range(block.address, block.address + block.length, 4):
            lst.append(
                MonsterSpawn(
                    read_u16(overlay29, i + 0x00),
                    read_u8(overlay29, i + 0x02),
                    read_u8(overlay29, i + 0x03),
                )
            )
        return lst

    @classmethod
    def set_monster_spawn_list(
        cls, overlay29: bytearray, values: List[MonsterSpawn], config: Pmd2Data
    ) -> None:
        """
        Returns the list of monsters that can be spawned in fixed floors.
        The length of the list must exactly match the original ROM's length (see get_monster_spawn_list).
        """
        cls._set(
            overlay29,
            values,
            config,
            config.bin_sections.overlay29.data.FIXED_ROOM_MONSTER_SPAWN_TABLE,
            4,
        )

    @classmethod
    def get_tile_spawn_list(cls, overlay29: bytes, config: Pmd2Data) -> List[TileSpawn]:
        """
        Returns the list of tiles that can be spawned in fixed floors.
        """
        block = config.bin_sections.overlay29.data.FIXED_ROOM_TILE_SPAWN_TABLE
        lst = []
        for i in range(block.address, block.address + block.length, 4):
            lst.append(
                TileSpawn(
                    read_u8(overlay29, i + 0x00),
                    read_u8(overlay29, i + 0x01),
                    read_u8(overlay29, i + 0x02),
                    read_u8(overlay29, i + 0x03),
                )
            )
        return lst

    @classmethod
    def set_tile_spawn_list(
        cls, overlay29: bytearray, values: List[TileSpawn], config: Pmd2Data
    ) -> None:
        """
        Returns the list of tiles that can be spawned in fixed floors.
        The length of the list must exactly match the original ROM's length (see get_tile_spawn_list).
        """
        cls._set(
            overlay29,
            values,
            config,
            config.bin_sections.overlay29.data.FIXED_ROOM_TILE_SPAWN_TABLE,
            4,
        )

    @classmethod
    def get_monster_spawn_stats_table(
        cls, overlay10: bytes, config: Pmd2Data
    ) -> List[MonsterSpawnStats]:
        """
        Returns the list of monsters that can be spawned in fixed floors.
        """
        block = config.bin_sections.overlay10.data.FIXED_ROOM_MONSTER_SPAWN_STATS_TABLE
        lst = []
        for i in range(block.address, block.address + block.length, 12):
            lst.append(
                MonsterSpawnStats(
                    read_u16(overlay10, i + 0x00),
                    read_u16(overlay10, i + 0x02),
                    read_u16(overlay10, i + 0x04),
                    read_u8(overlay10, i + 0x06),
                    read_u8(overlay10, i + 0x07),
                    read_u8(overlay10, i + 0x08),
                    read_u8(overlay10, i + 0x09),
                    read_u16(overlay10, i + 0x0A),
                )
            )
        return lst

    @classmethod
    def set_monster_spawn_stats_table(
        cls, overlay10: bytearray, values: List[MonsterSpawnStats], config: Pmd2Data
    ) -> None:
        """
        Returns the list of monsters that can be spawned in fixed floors.
        The length of the list must exactly match the original ROM's length (see get_monster_spawn_stats_table).
        """
        cls._set(
            overlay10,
            values,
            config,
            config.bin_sections.overlay10.data.FIXED_ROOM_MONSTER_SPAWN_STATS_TABLE,
            12,
        )

    @classmethod
    def get_fixed_floor_properties(
        cls, overlay10: bytes, config: Pmd2Data
    ) -> List[FixedFloorProperties]:
        """
        Returns the list of properties for fixed floors.
        """
        block = config.bin_sections.overlay10.data.FIXED_ROOM_PROPERTIES_TABLE
        lst = []
        for i in range(block.address, block.address + block.length, 12):
            lst.append(
                FixedFloorProperties(
                    read_u32(overlay10, i + 0x00),
                    bool(read_u8(overlay10, i + 0x04)),
                    bool(read_u8(overlay10, i + 0x05)),
                    bool(read_u8(overlay10, i + 0x06)),
                    bool(read_u8(overlay10, i + 0x07)),
                    bool(read_u8(overlay10, i + 0x08)),
                    bool(read_u8(overlay10, i + 0x09)),
                    bool(read_u8(overlay10, i + 0x0A)),
                    read_u8(overlay10, i + 0x0B),
                )
            )
        return lst

    @classmethod
    def set_fixed_floor_properties(
        cls, overlay10: bytearray, values: List[FixedFloorProperties], config: Pmd2Data
    ) -> None:
        """
        Sets the list of properties for fixed floors.
        The length of the list must exactly match the original ROM's length (see get_fixed_floor_properties).
        """
        cls._set(
            overlay10,
            values,
            config,
            config.bin_sections.overlay10.data.FIXED_ROOM_PROPERTIES_TABLE,
            12,
        )

    @classmethod
    def get_fixed_floor_overrides(cls, overlay29: bytes, config: Pmd2Data) -> List[u8]:
        """
        Returns the list of overrides for fixed floors.
        """
        block = config.bin_sections.overlay29.data.FIXED_ROOM_REVISIT_OVERRIDES
        lst = []
        for i in range(block.address, block.address + block.length):
            lst.append(read_u8(overlay29, i))
        return lst

    @classmethod
    def set_fixed_floor_overrides(
        cls, overlay29: bytearray, values: List[u8], config: Pmd2Data
    ) -> None:
        """
        Sets the list of overrides for fixed floors.
        The length of the list must exactly match the original ROM's length (see get_fixed_floor_overrides).
        """
        block = config.bin_sections.overlay29.data.FIXED_ROOM_REVISIT_OVERRIDES
        expected_length = block.length
        if len(values) != expected_length:
            raise ValueError(
                f"The list must have exactly the length of {expected_length} entries."
            )
        for entry, i in zip(values, range(block.address, block.address + block.length)):
            overlay29[i] = entry

    @classmethod
    def _set(cls, binary: bytearray, values: List[Any], config: Pmd2Data, block: Symbol, entry_len: int) -> None:  # type: ignore
        expected_length = int(block.length / entry_len)
        if len(values) != expected_length:
            raise ValueError(
                f"The list must have exactly the length of {expected_length} entries."
            )
        for i, entry in enumerate(values):
            binary[
                block.address + (i * entry_len) : block.address + ((i + 1) * entry_len)
            ] = entry.to_bytes()
