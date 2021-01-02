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
from typing import List, Tuple, Set, Dict

from skytemple_files.dungeon_data.mappa_bin.floor import MappaFloor
from skytemple_files.dungeon_data.mappa_bin.validator.exception import DungeonValidatorError, \
    InvalidFloorListReferencedError, InvalidFloorReferencedError, FloorReusedError, DungeonTotalFloorCountInvalidError, \
    DungeonMissingFloorError
from skytemple_files.hardcoded.dungeons import DungeonDefinition


class DungeonValidator:
    def __init__(self, floors: List[List[MappaFloor]]):
        self.dungeons = None
        self.floors = floors

        self._errors: List[DungeonValidatorError] = []
        self._validated = False

        # Keys are visited floor lists, values are list of not-yet visited floors.
        self._visited_floor_lists: Dict[int, List[int]] = {}
        self._invalid_dungeons: Set[int] = set()

    @property
    def errors(self) -> List[DungeonValidatorError]:
        if not self._validated:
            raise ValueError("Call validate first.")
        return self._errors

    @property
    def invalid_dungeons(self):
        """IDs of invalid dungeons. Dungeons which have non-critical errors are not listed."""
        if not self._validated:
            raise ValueError("Call validate first.")
        return self._invalid_dungeons

    def validate(self, dungeons: List[DungeonDefinition]) -> bool:
        # Reset
        self.__init__(self.floors)
        self.dungeons = dungeons
        self._validated = True

        for dungeon_id, dungeon in enumerate(self.dungeons):
            if self._mappa_floor_list_doesnt_exist(dungeon.mappa_index):
                self._errors.append(InvalidFloorListReferencedError(dungeon, dungeon_id))
            if self._mappa_floor_doesnt_exist(dungeon.mappa_index, dungeon.start_after, dungeon.number_floors):
                self._errors.append(InvalidFloorReferencedError(dungeon, dungeon_id))

            if dungeon.mappa_index in self._visited_floor_lists.keys():
                if self._mappa_floor_already_visited(dungeon.mappa_index, dungeon.start_after, dungeon.number_floors):
                    self._errors.append(FloorReusedError(
                        dungeon, dungeon_id,
                        self._mappa_which_dungeon_uses(dungeon.mappa_index, dungeon.start_after, dungeon.number_floors)
                    ))
            else:
                self._visited_floor_lists[dungeon.mappa_index] = []

            self._add_mappa_visited(dungeon.mappa_index, dungeon.start_after, dungeon.number_floors)

            if dungeon.start_after == 0:
                expected, invalid_dungeons = self._mappa_group_count_invalid(self.dungeons, dungeon.mappa_index)
                for invalid in invalid_dungeons:
                    self._errors.append(DungeonTotalFloorCountInvalidError(
                        self.dungeons[invalid], invalid, expected
                    ))

        for visited_floor_list_id, visited_floors in self._visited_floor_lists.items():
            open_floors = set(i for i in range(0, len(self.floors[visited_floor_list_id]))) - set(visited_floors)
            already_invalidated: Dict[int, DungeonMissingFloorError] = {}
            if len(open_floors) > 0:
                for f_id in open_floors:
                    dungeon_id = self._mappa_get_dungeon_id(visited_floor_list_id, f_id)
                    if dungeon_id in already_invalidated.keys():
                        already_invalidated[dungeon_id].add(f_id)
                    else:
                        err = DungeonMissingFloorError(self.dungeons[dungeon_id], dungeon_id, [f_id])
                        self._errors.append(err)
                        already_invalidated[dungeon_id] = err

        for error in self._errors:
            if error.makes_fully_invalid:
                self.invalid_dungeons.add(error.dungeon_id)

        return len(self._errors) < 1

    def _mappa_floor_list_doesnt_exist(self, mappa_index):
        return len(self.floors) <= mappa_index

    def _mappa_floor_doesnt_exist(self, mappa_index, start_after, number_floors):
        return len(self.floors[mappa_index]) < start_after + number_floors

    def _mappa_floor_already_visited(self, mappa_index, start_after, number_floors):
        for i in range(start_after, start_after + number_floors):
            if i in self._visited_floor_lists[mappa_index]:
                return True
        return False

    def _init_mappa_visited(self, mappa_index):
        s = []
        for i in range(0, len(self.floors[mappa_index])):
            s.append(i)
        return s

    def _add_mappa_visited(self, mappa_index, start_after, number_floors):
        for i in range(start_after, start_after + number_floors):
            self._visited_floor_lists[mappa_index].append(i)

    def _mappa_group_count_invalid(self, dungeons, mappa_index) -> Tuple[int, List[int]]:
        count_floor_expected = 0
        dungeons_to_check = []
        invalid = []
        for i, dungeon in enumerate(dungeons):
            if dungeon.mappa_index == mappa_index:
                count_floor_expected += dungeon.number_floors
                dungeons_to_check.append(i)
        for i in dungeons_to_check:
            if dungeons[i].number_floors_in_group != count_floor_expected:
                invalid.append(i)
        return count_floor_expected, invalid

    def _mappa_which_dungeon_uses(self, mappa_index, start_after, number_floors):
        for i, dungeon in enumerate(self.dungeons):
            if dungeon.mappa_index == mappa_index:
                if dungeon.start_after >= start_after and dungeon.start_after + dungeon.number_floors > start_after + number_floors:
                    return i
        raise ValueError("Invalid reference in dungeon validation")

    def _mappa_get_dungeon_id(self, mappa_index, floor_id):
        start_index_prev = -1
        current_i = None
        for i, dungeon in enumerate(self.dungeons):
            if dungeon.mappa_index == mappa_index:
                if start_index_prev < dungeon.start_after <= floor_id:
                    current_i = i
                    start_index_prev = dungeon.start_after
        if current_i is None:
            raise ValueError("Invalid reference in dungeon validation")
        return current_i
