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
import itertools
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional, Union

from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptDirection
from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.common.i18n_util import f, _
END_OF_LIST_PADDING = b'\xaa\xaa\xaa\xaa'


class FloorType(Enum):
    FLOOR = auto()
    WALL = auto()
    SECONDARY = auto()
    FLOOR_OR_WALL = auto()


class RoomType(Enum):
    ROOM = auto()
    HALLWAY = auto()


class TileRuleType(Enum):
    FLOOR_ROOM                 = 0x00, _('Floor, Room'), \
                                 FloorType.FLOOR, RoomType.ROOM, False, False, \
                                ''
    WALL_HALLWAY               = 0x01, _('Wall, Hallway; Absolute Mover'), \
                                 FloorType.WALL, RoomType.HALLWAY, False, True, \
                                 ''
    WALL_HALLWAY_IMPASSABLE    = 0x02, _('Wall, Hallway; Impassable'), \
                                 FloorType.WALL, RoomType.HALLWAY, True, False, \
                                 ''
    WALL_HALLWAY_DEFAULT       = 0x03, _('Wall, Hallway'), \
                                 FloorType.WALL, RoomType.HALLWAY, False, False, \
                                 ''
    LEADER_SPAWN               = 0x04, _('Leader Spawn Floor'), \
                                 FloorType.FLOOR, RoomType.ROOM, False, False, \
                                 ''
    SECONDARY_ROOM             = 0x05, _('Secondary, Room'), \
                                 FloorType.SECONDARY, RoomType.ROOM, False, False, \
                                 ''
    SECONDARY_HALLWAY_VOID     = 0x06, _('Chasm, Hallway'), \
                                 FloorType.SECONDARY, RoomType.HALLWAY, False, False, \
                                 _('Tile type is forced to be "Void / Chasm" (Still rendered as tileset\'s secondary terrain!).')
    SECONDARY_HALLWAY_VOID_ALL = 0x07, _('Chasm, Hallway; All Chasm'), \
                                 FloorType.SECONDARY, RoomType.HALLWAY, True, False, \
                                 _('Tile type is forced to be "Void / Chasm" (Still rendered as tileset\'s secondary terrain!). '
                                   'All tiles outside of defined room are made the tileset\'s defined secondary terrain.')
    WARP_ZONE                  = 0x08, _('Warp Zone, Room'), \
                                 FloorType.FLOOR, RoomType.ROOM, False, False, \
                                 _('Creates a Warp Zone.')
    FLOOR_HALLWAY              = 0x09, _('Floor, Hallway'), \
                                 FloorType.FLOOR, RoomType.HALLWAY, False, False, \
                                 ''
    SECONDARY_HALLWAY_VOID_IMPASSABLE = 0x0A, _('Chasm, Hallway; Impassable'), \
                                 FloorType.SECONDARY, RoomType.HALLWAY, True, False, \
                                 _('Tile type is forced to be "Void / Chasm" (Still rendered as tileset\'s secondary terrain!).')
    FLOOR_HALLWAY_FLAG_0A      = 0x0B, _('Floor, Hallway; Flag 0xA'), \
                                 FloorType.FLOOR, RoomType.HALLWAY, False, False, \
                                 _('Tile flag 0xA is set to 1 (Unknown what this does).')
    FL_WA_ROOM_FLAG_0C         = 0x0C, _('F/W, Room; Key Door (0xC)'), \
                                 FloorType.FLOOR_OR_WALL, RoomType.ROOM, True, False, \
                                 _('Tile flag 0xC is set to 1 and spawns a key Door. '
                                   'If the fixed room id is &lt; 0xA5, this will be a Wall. Otherwise it will be Floor.')
    FL_WA_ROOM_FLAG_0D         = 0x0D, _('F/W, Room; Key Door (0xD)'), \
                                 FloorType.FLOOR_OR_WALL, RoomType.ROOM, True, False, \
                                 _('Tile flag 0xD is set to 1 and spawns a key Door. '
                                   'If the fixed room id is &lt; 0xA5, this will be a Wall. Otherwise it will be Floor.')
    WALL_HALLWAY_IMPASSABLE_2  = 0x0E, _('Wall, Hallway; Impassable'), \
                                 FloorType.WALL, RoomType.HALLWAY, True, False, \
                                 ''
    WALL_HALLWAY_DEFAULT_2     = 0x0F, _('Wall, Hallway'), \
                                 FloorType.WALL, RoomType.HALLWAY, False, False, \
                                 ''
    ATTENDANT1_SPAWN           = 0x60, _('Attendant1 Spawn Floor'), \
                                 FloorType.FLOOR, RoomType.ROOM, False, False, \
                                 ''
    ATTENDANT2_SPAWN           = 0x61, _('Attendant2 Spawn Floor'), \
                                 FloorType.FLOOR, RoomType.ROOM, False, False, \
                                 ''
    ATTENDANT3_SPAWN           = 0x62, _('Attendant3 Spawn Floor'), \
                                 FloorType.FLOOR, RoomType.ROOM, False, False, \
                                 ''
    FLOOR_ROOM_63              = 0x63, _('Floor, Room'), \
                                 FloorType.FLOOR, RoomType.ROOM, False, False, \
                                 ''
    WARP_ZONE_2                = 0x6B, _('Warp Zone, Room'), \
                                 FloorType.FLOOR, RoomType.ROOM, False, False, \
                                 _('Creates a Warp Zone.')
    FLOOR_ROOM_64              = 0x6C, _('Floor, Room'), \
                                 FloorType.FLOOR, RoomType.ROOM, False, False, \
                                 ''
    FLOOR_ROOM_65              = 0x6D, _('Floor, Room'), \
                                 FloorType.FLOOR, RoomType.ROOM, False, False, \
                                 ''

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: str, explanation: str, floor_type: FloorType, room_type: RoomType,
            impassable: bool, absolute_mover: bool, notes: str
    ):
        self.explanation = explanation
        self.floor_type = floor_type
        self.room_type = room_type
        self.impassable = impassable
        self.absolute_mover = absolute_mover
        self.notes = notes

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    def __str__(self):
        return f'TileRule<"{self.explanation}">'

    def __repr__(self):
        return str(self)


class FixedFloorActionRule(ABC, AutoString):
    def __init__(self, direction: Optional[Pmd2ScriptDirection]):
        self.direction = direction

    @abstractmethod
    def _get_action_id(self):
        pass

    def __int__(self):
        return (self._get_action_id() & 0xFFF) + ((self.direction.ssa_id if self.direction is not None else 0) << 0xC)


class TileRule(FixedFloorActionRule):
    def __init__(self, tr_type: TileRuleType, direction: Optional[Pmd2ScriptDirection] = None):
        super().__init__(direction)
        self.tr_type = tr_type

    def _get_action_id(self):
        return self.tr_type.value


class EntityRule(FixedFloorActionRule):
    def __init__(self, entity_rule_id: int, direction: Optional[Pmd2ScriptDirection] = None):
        super().__init__(direction)
        self.entity_rule_id = entity_rule_id

    def _get_action_id(self):
        return self.entity_rule_id + 16


class FixedFloor:
    def __init__(self, data: bytes, floor_pointer: int, static_data: Pmd2Data):
        self.width = read_uintle(data, floor_pointer, 2)
        self.height = read_uintle(data, floor_pointer + 2, 2)
        self.unk4 = read_uintle(data, floor_pointer + 4, 2)
        self.static_data = static_data
        self.actions = self.read_actions(data, floor_pointer + 6, self.width * self.height)

    def read_actions(self, data: bytes, action_list_start: int, max_actions: int) -> List[FixedFloorActionRule]:
        cursor = action_list_start
        actions = []
        while len(actions) < max_actions:
            action, repeat_times = self._read_action(data, cursor)
            cursor += 4
            actions += [action] * (repeat_times + 1)
        assert len(actions) == max_actions, "The number of actions encoded does not match the width & height of the map."
        return actions

    def _read_action(self, data: bytes, action_pointer: int) -> Tuple[FixedFloorActionRule, int]:
        action_value = read_uintle(data, action_pointer, 2)
        action_id = action_value & 0xFFF
        parameter = action_value >> 0xC
        direction = None
        if parameter > 0:
            direction = self.static_data.script_data.directions__by_ssa_id[parameter]

        repeat_times = read_uintle(data, action_pointer + 2, 2)
        if TileRuleType.has_value(action_id):
            return TileRule(
                TileRuleType(action_id), direction
            ), repeat_times
        return EntityRule(
            action_id - 16, direction
        ), repeat_times

    def to_bytes(self) -> bytes:
        header = bytearray(6)
        write_uintle(header, self.width, 0x00, 2)
        write_uintle(header, self.height, 0x02, 2)
        write_uintle(header, self.unk4, 0x04, 2)
        return header + self._actions_to_bytes()

    def resize(self, width, height):
        # Convert existing data into a grid
        rows = []
        current_row = []
        for i, el in enumerate(self.actions):
            current_row.append(el)
            if i % self.width == self.width - 1:
                rows.append(current_row)
                current_row = []

        # Shrink / enlarge the grid
        # Y: Enlarge
        for _ in range(0, height - len(rows)):
            rows.append([])
        # Y: Shrink
        rows = rows[:height]
        for row_i, row in enumerate(rows):
            # X: Enlarge
            for _ in range(0, width - len(row)):
                row.append(TileRule(TileRuleType.FLOOR_ROOM, None))
            # X: Shrink
            rows[row_i] = row[:width]

        self.actions = list(itertools.chain.from_iterable(rows))
        self.width = width
        self.height = height

    def _actions_to_bytes(self) -> bytes:
        actions: List[Tuple[FixedFloorActionRule, int]] = shrink_list(self.actions)
        buffer = bytearray(4 * len(actions))

        for i, (action, n_times) in enumerate(actions):
            write_uintle(buffer, int(action), i * 4, 2)
            write_uintle(buffer, n_times - 1, i * 4 + 0x02, 2)

        return buffer


class FixedBin(Sir0Serializable):
    def __init__(self, data: bytes, floor_list_offset: int, static_data: Pmd2Data):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        cursor = floor_list_offset
        self.fixed_floors = []
        while data[cursor:cursor+4] != END_OF_LIST_PADDING:
            self.fixed_floors.append(FixedFloor(data, read_uintle(data, cursor, 4), static_data))
            cursor += 4
            assert cursor < len(data)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.dungeon_data.fixed_bin.writer import FixedBinWriter
        return FixedBinWriter(self).write()

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int, static_data: Optional[Pmd2Data] = None) -> 'FixedBin':
        return cls(content_data, data_pointer, static_data)
