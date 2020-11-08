#  Copyright 2020 Parakoopa
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

from skytemple_files.common.ppmdu_config.data import Pmd2Data, Pmd2Binary, Pmd2BinaryBlock
from skytemple_files.common.util import read_uintle, write_uintle, AutoString


class EntitySpawnEntry(AutoString):
    def __init__(self, overlay29bin: Pmd2Binary, item_spawn_pointer: int,
                 monster_spawn_pointer: int, tile_spawn_pointer: int):
        self._overlay29bin = overlay29bin
        self.item_id = (item_spawn_pointer - self._overlay29bin.blocks['ItemSpawnTable'].begin_absolute) / 8
        assert self.item_id % 1 == 0
        self.item_id = int(self.item_id)
        self.monster_id = (monster_spawn_pointer - self._overlay29bin.blocks['MonsterSpawnTable'].begin_absolute) / 4
        assert self.monster_id % 1 == 0
        self.monster_id = int(self.monster_id)
        self.tile_id = (tile_spawn_pointer - self._overlay29bin.blocks['TileSpawnTable'].begin_absolute) / 4
        assert self.tile_id % 1 == 0
        self.tile_id = int(self.tile_id)

    def to_bytes(self) -> bytes:
        buffer = bytearray(12)
        write_uintle(buffer, self.item_id * 8 + self._overlay29bin.blocks['ItemSpawnTable'].begin_absolute, 0, 4)
        write_uintle(buffer, self.monster_id * 4 + self._overlay29bin.blocks['MonsterSpawnTable'].begin_absolute, 4, 4)
        write_uintle(buffer, self.tile_id * 4 + self._overlay29bin.blocks['TileSpawnTable'].begin_absolute, 8, 4)
        return buffer

    def __eq__(self, other):
        if not isinstance(other, EntitySpawnEntry):
            return False
        return self.item_id == other.item_id and self.monster_id == other.monster_id and self.tile_id == other.tile_id


class ItemSpawn(AutoString):
    def __init__(self, item_id: int, null1: int, null2: int, null3: int):
        self.item_id = item_id
        self.null1 = null1
        self.null2 = null2
        self.null3 = null3

    def to_bytes(self) -> bytes:
        buffer = bytearray(8)
        write_uintle(buffer, self.item_id, 0, 4)
        write_uintle(buffer, self.null1, 2, 2)
        write_uintle(buffer, self.null2, 4, 2)
        write_uintle(buffer, self.null3, 6, 2)
        return buffer

    def __eq__(self, other):
        if not isinstance(other, ItemSpawn):
            return False
        return self.item_id == other.item_id and \
               self.null1 == other.null1 and \
               self.null2 == other.null2 and \
               self.null3 == other.null3


class MonsterSpawn(AutoString):
    def __init__(self, md_idx: int, stats_entry: int, enemy_settings: int):
        self.md_idx = md_idx
        self.stats_entry = stats_entry
        # 3: (?) 6 if the pokémon is an enemy, 0xA if it's an ally, 9 if the only thing that is being spawned is
        # an item. If it's 6 or 0xA, the stats of the pokémon are determined by the stats entry specified on byte 2.
        self.enemy_settings = enemy_settings

    def to_bytes(self) -> bytes:
        buffer = bytearray(4)
        write_uintle(buffer, self.md_idx, 0, 2)
        write_uintle(buffer, self.stats_entry, 2, 1)
        write_uintle(buffer, self.enemy_settings, 3, 1)
        return buffer

    def __eq__(self, other):
        if not isinstance(other, MonsterSpawn):
            return False
        return self.md_idx == other.md_idx and \
               self.stats_entry == other.stats_entry


class TileSpawn(AutoString):
    def __init__(self, trap_id: int, trap_data: int, room_id: int, flags: int):
        self.trap_id = trap_id
        self.trap_data = trap_data
        self.room_id = room_id
        self.flags = flags

    def to_bytes(self) -> bytes:
        buffer = bytearray(4)
        write_uintle(buffer, self.trap_id, 0, 1)
        write_uintle(buffer, self.trap_data, 1, 1)
        write_uintle(buffer, self.room_id, 2, 1)
        write_uintle(buffer, self.flags, 3, 1)
        return buffer

    def can_be_broken(self):
        return not (self.trap_data & 1)

    def trap_is_visible(self):
        return self.flags & 1

    def is_secondary_terrain(self):
        return self.flags & 0b1000

    def __eq__(self, other):
        if not isinstance(other, TileSpawn):
            return False
        return self.trap_id == other.trap_id and \
               self.trap_data == other.trap_data and \
               self.room_id == other.room_id and \
               self.flags == other.flags


class MonsterSpawnStats(AutoString):
    def __init__(self, level: int, hp: int, null: int,
                 attack: int, special_attack: int, defense: int, special_defense: int, unkA: int):
        self.level = level
        self.hp = hp
        self.null = null
        self.attack = attack
        self.special_attack = special_attack
        self.defense = defense
        self.special_defense = special_defense
        self.unkA = unkA

    def to_bytes(self) -> bytes:
        buffer = bytearray(12)
        write_uintle(buffer, self.level, 0, 2)
        write_uintle(buffer, self.hp, 2, 2)
        write_uintle(buffer, self.null, 4, 2)
        write_uintle(buffer, self.attack, 6, 1)
        write_uintle(buffer, self.special_attack, 7, 1)
        write_uintle(buffer, self.defense, 8, 1)
        write_uintle(buffer, self.special_defense, 9, 1)
        write_uintle(buffer, self.unkA, 10, 2)
        return buffer

    def __eq__(self, other):
        if not isinstance(other, MonsterSpawnStats):
            return False
        return self.level == other.level and \
               self.hp == other.hp and \
               self.null == other.null and \
               self.attack == other.attack and \
               self.special_attack == other.special_attack and \
               self.defense == other.defense and \
               self.special_defense == other.special_defense and \
               self.unkA == other.unkA


class FixedFloorProperties(AutoString):
    def __init__(self, music_track: int, unk4: bool, unk5: bool, moves_enabled: bool, orbs_enabled: bool,
                 unk8: bool, unk9: bool, unk10: bool, null: int):
        self.music_track = music_track
        self.unk4 = unk4
        self.unk5 = unk5
        self.moves_enabled = moves_enabled
        self.orbs_enabled = orbs_enabled
        self.unk8 = unk8
        self.unk9 = unk9
        self.unk10 = unk10
        self.null = null

    def to_bytes(self) -> bytes:
        buffer = bytearray(12)
        write_uintle(buffer, self.music_track, 0, 4)
        write_uintle(buffer, self.unk4, 4, 1)
        write_uintle(buffer, self.unk5, 5, 1)
        write_uintle(buffer, self.moves_enabled, 6, 1)
        write_uintle(buffer, self.orbs_enabled, 7, 1)
        write_uintle(buffer, self.unk8, 8, 1)
        write_uintle(buffer, self.unk9, 9, 1)
        write_uintle(buffer, self.unk10, 10, 1)
        write_uintle(buffer, self.null, 11, 1)
        return buffer

    def __eq__(self, other):
        if not isinstance(other, FixedFloorProperties):
            return False
        return self.music_track == other.music_track and \
               self.unk4 == other.unk4 and \
               self.unk5 == other.unk5 and \
               self.moves_enabled == other.moves_enabled and \
               self.orbs_enabled == other.orbs_enabled and \
               self.unk8 == other.unk8 and \
               self.unk9 == other.unk9 and \
               self.unk10 == other.unk10 and \
               self.null == other.null


class HardcodedFixedFloorTables:
    @classmethod
    def get_entity_spawn_table(cls, overlay29: bytes, config: Pmd2Data) -> List[EntitySpawnEntry]:
        """
        Returns the list of entity spawns. Each entry has three references, one to each of
        the other three tables (item spawn, monster spawn, tile type).
        """
        binary = config.binaries['overlay/overlay_0029.bin']
        block = binary.blocks['EntitySpawnTable']
        lst = []
        for i in range(block.begin, block.end, 12):
            lst.append(EntitySpawnEntry(
                binary,
                read_uintle(overlay29, i + 0x00, 4),
                read_uintle(overlay29, i + 0x04, 4),
                read_uintle(overlay29, i + 0x08, 4),
            ))
        return lst

    @classmethod
    def set_entity_spawn_table(cls, overlay29: bytes, values: List[EntitySpawnEntry], config: Pmd2Data):
        """
        Sets the list of entity spawns.
        The length of the list must exactly match the original ROM's length (see get_entity_spawn_table).
        """
        cls._set(overlay29, values, config,
                 config.binaries['overlay/overlay_0029.bin'].blocks['EntitySpawnTable'], 12)

    @classmethod
    def get_item_spawn_list(cls, overlay29: bytes, config: Pmd2Data) -> List[ItemSpawn]:
        """
        Returns the list of items that can be spawned in fixed floors.
        """
        block = config.binaries['overlay/overlay_0029.bin'].blocks['ItemSpawnTable']
        lst = []
        for i in range(block.begin, block.end, 8):
            lst.append(ItemSpawn(
                read_uintle(overlay29, i + 0x00, 2),
                read_uintle(overlay29, i + 0x02, 2),
                read_uintle(overlay29, i + 0x04, 2),
                read_uintle(overlay29, i + 0x06, 2),
            ))
        return lst

    @classmethod
    def set_item_spawn_list(cls, overlay29: bytes, values: List[ItemSpawn], config: Pmd2Data):
        """
        Returns the list of items that can be spawned in fixed floors.
        The length of the list must exactly match the original ROM's length (see get_item_spawn_list).
        """
        cls._set(overlay29, values, config,
                 config.binaries['overlay/overlay_0029.bin'].blocks['ItemSpawnTable'], 8)

    @classmethod
    def get_monster_spawn_list(cls, overlay29: bytes, config: Pmd2Data) -> List[MonsterSpawn]:
        """
        Returns the list of monsters that can be spawned in fixed floors.
        """
        block = config.binaries['overlay/overlay_0029.bin'].blocks['MonsterSpawnTable']
        lst = []
        for i in range(block.begin, block.end, 4):
            lst.append(MonsterSpawn(
                read_uintle(overlay29, i + 0x00, 2),
                read_uintle(overlay29, i + 0x02, 1),
                read_uintle(overlay29, i + 0x03, 1)
            ))
        return lst

    @classmethod
    def set_monster_spawn_list(cls, overlay29: bytes, values: List[MonsterSpawn], config: Pmd2Data):
        """
        Returns the list of monsters that can be spawned in fixed floors.
        The length of the list must exactly match the original ROM's length (see get_monster_spawn_list).
        """
        cls._set(overlay29, values, config,
                 config.binaries['overlay/overlay_0029.bin'].blocks['MonsterSpawnTable'], 4)

    @classmethod
    def get_tile_spawn_list(cls, overlay29: bytes, config: Pmd2Data) -> List[TileSpawn]:
        """
        Returns the list of tiles that can be spawned in fixed floors.
        """
        block = config.binaries['overlay/overlay_0029.bin'].blocks['TileSpawnTable']
        lst = []
        for i in range(block.begin, block.end, 4):
            lst.append(TileSpawn(
                read_uintle(overlay29, i + 0x00, 1),
                read_uintle(overlay29, i + 0x01, 1),
                read_uintle(overlay29, i + 0x02, 1),
                read_uintle(overlay29, i + 0x03, 1)
            ))
        return lst

    @classmethod
    def set_tile_spawn_list(cls, overlay29: bytes, values: List[TileSpawn], config: Pmd2Data):
        """
        Returns the list of tiles that can be spawned in fixed floors.
        The length of the list must exactly match the original ROM's length (see get_tile_spawn_list).
        """
        cls._set(overlay29, values, config,
                 config.binaries['overlay/overlay_0029.bin'].blocks['TileSpawnTable'], 4)

    @classmethod
    def get_monster_spawn_stats_table(cls, overlay10: bytes, config: Pmd2Data) -> List[MonsterSpawnStats]:
        """
        Returns the list of monsters that can be spawned in fixed floors.
        """
        block = config.binaries['overlay/overlay_0010.bin'].blocks['MonsterSpawnStatsTable']
        lst = []
        for i in range(block.begin, block.end, 12):
            lst.append(MonsterSpawnStats(
                read_uintle(overlay10, i + 0x00, 2),
                read_uintle(overlay10, i + 0x02, 2),
                read_uintle(overlay10, i + 0x04, 2),
                read_uintle(overlay10, i + 0x06, 1),
                read_uintle(overlay10, i + 0x07, 1),
                read_uintle(overlay10, i + 0x08, 1),
                read_uintle(overlay10, i + 0x09, 1),
                read_uintle(overlay10, i + 0x0A, 2)
            ))
        return lst

    @classmethod
    def set_monster_spawn_stats_table(cls, overlay10: bytes, values: List[MonsterSpawnStats], config: Pmd2Data):
        """
        Returns the list of monsters that can be spawned in fixed floors.
        The length of the list must exactly match the original ROM's length (see get_monster_spawn_stats_table).
        """
        cls._set(overlay10, values, config,
                 config.binaries['overlay/overlay_0010.bin'].blocks['MonsterSpawnStatsTable'], 12)

    @classmethod
    def get_fixed_floor_properties(cls, overlay10: bytes, config: Pmd2Data) -> List[FixedFloorProperties]:
        """
        Returns the list of properties for fixed floors.
        """
        block = config.binaries['overlay/overlay_0010.bin'].blocks['FixedFloorProperties']
        lst = []
        for i in range(block.begin, block.end, 12):
            lst.append(FixedFloorProperties(
                read_uintle(overlay10, i + 0x00, 4),
                bool(read_uintle(overlay10, i + 0x04, 1)),
                bool(read_uintle(overlay10, i + 0x05, 1)),
                bool(read_uintle(overlay10, i + 0x06, 1)),
                bool(read_uintle(overlay10, i + 0x07, 1)),
                bool(read_uintle(overlay10, i + 0x08, 1)),
                bool(read_uintle(overlay10, i + 0x09, 1)),
                bool(read_uintle(overlay10, i + 0x0A, 1)),
                read_uintle(overlay10, i + 0x0B, 1)
            ))
        return lst

    @classmethod
    def set_fixed_floor_properties(cls, overlay10: bytes, values: List[FixedFloorProperties], config: Pmd2Data):
        """
        Sets the list of properties for fixed floors.
        The length of the list must exactly match the original ROM's length (see get_fixed_floor_properties).
        """
        cls._set(overlay10, values, config,
                 config.binaries['overlay/overlay_0010.bin'].blocks['FixedFloorProperties'], 12)

    @classmethod
    def get_fixed_floor_overrides(cls, overlay10: bytes, config: Pmd2Data) -> List[int]:
        """
        Returns the list of overrides for fixed floors.
        """
        block = config.binaries['overlay/overlay_0029.bin'].blocks['FixedFloorOverrides']
        lst = []
        for i in range(block.begin, block.end):
            lst.append(read_uintle(overlay10, i, 1))
        return lst

    @classmethod
    def set_fixed_floor_overrides(cls, overlay29: bytearray, values: List[int], config: Pmd2Data):
        """
        Sets the list of overrides for fixed floors.
        The length of the list must exactly match the original ROM's length (see get_fixed_floor_overrides).
        """
        block = config.binaries['overlay/overlay_0029.bin'].blocks['FixedFloorOverrides']
        expected_length = block.end - block.begin
        if len(values) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for entry, i in zip(values, range(block.begin, block.end)):
            overlay29[i] = entry

    @classmethod
    def _set(cls, binary: bytes, values: List, config: Pmd2Data, block: Pmd2BinaryBlock, entry_len: int):
        expected_length = int((block.end - block.begin) / entry_len)
        if len(values) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(values):
            binary[block.begin + (i * entry_len):block.begin + ((i + 1) * entry_len)] = entry.to_bytes()
