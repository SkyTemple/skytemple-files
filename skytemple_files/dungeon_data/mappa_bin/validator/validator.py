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


from range_typed_integers import u8, u8_checked

from skytemple_files.dungeon_data.mappa_bin.protocol import (
    MappaBinProtocol,
)
from skytemple_files.dungeon_data.mappa_bin.validator.exception import (
    DungeonMissingFloorError,
    DungeonTotalFloorCountInvalidError,
    DungeonValidatorError,
    FloorReusedError,
    InvalidFloorListReferencedError,
    InvalidFloorReferencedError,
)
from skytemple_files.hardcoded.dungeons import DungeonDefinition


class DungeonValidator:
    def __init__(self, mappa: MappaBinProtocol):
        self.dungeons: list[DungeonDefinition] | None = None
        self.mappa = mappa

        self._errors: list[DungeonValidatorError] = []
        self._validated = False

        # Keys are visited floor lists, values are list of not-yet visited floors.
        self._visited_floor_lists: dict[int, list[int]] = {}
        self._invalid_dungeons: set[int] = set()

    @property
    def errors(self) -> list[DungeonValidatorError]:
        if not self._validated:
            raise ValueError("Call validate first.")
        return self._errors

    @property
    def invalid_dungeons(self) -> set[int]:
        """IDs of invalid dungeons. Dungeons which have non-critical errors are not listed."""
        if not self._validated:
            raise ValueError("Call validate first.")
        return self._invalid_dungeons

    def validate(self, dungeons: list[DungeonDefinition]) -> bool:
        # Reset
        self.__init__(self.mappa)  # type: ignore
        self.dungeons = dungeons
        self._validated = True

        for dungeon_id, dungeon in enumerate(self.dungeons):
            if self._mappa_floor_list_doesnt_exist(dungeon.mappa_index):
                self._errors.append(
                    InvalidFloorListReferencedError(dungeon, dungeon_id)
                )
            if self._mappa_floor_doesnt_exist(
                dungeon.mappa_index, dungeon.start_after, dungeon.number_floors
            ):
                self._errors.append(InvalidFloorReferencedError(dungeon, dungeon_id))

            if dungeon.mappa_index in self._visited_floor_lists.keys():
                if self._mappa_floor_already_visited(
                    dungeon.mappa_index, dungeon.start_after, dungeon.number_floors
                ):
                    self._errors.append(
                        FloorReusedError(
                            dungeon,
                            dungeon_id,
                            self._mappa_which_dungeon_uses(
                                dungeon.mappa_index,
                                dungeon.start_after,
                                dungeon.number_floors,
                            ),
                        )
                    )
            else:
                self._visited_floor_lists[dungeon.mappa_index] = []

            self._add_mappa_visited(
                dungeon.mappa_index, dungeon.start_after, dungeon.number_floors
            )

            if dungeon.start_after == 0:
                expected, invalid_dungeons = self._mappa_group_count_invalid(
                    self.dungeons, dungeon.mappa_index
                )
                for invalid in invalid_dungeons:
                    self._errors.append(
                        DungeonTotalFloorCountInvalidError(
                            self.dungeons[invalid], invalid, expected
                        )
                    )

        for visited_floor_list_id, visited_floors in self._visited_floor_lists.items():
            open_floors = {
                i for i in range(0, len(self.mappa.floor_lists[visited_floor_list_id]))
            } - set(visited_floors)
            already_invalidated: dict[int, DungeonMissingFloorError] = {}
            if len(open_floors) > 0:
                for f_id in open_floors:
                    dungeon_id = self._mappa_get_dungeon_id(visited_floor_list_id, f_id)
                    if dungeon_id in already_invalidated.keys():
                        already_invalidated[dungeon_id].add(f_id)  # type: ignore
                    else:
                        err = DungeonMissingFloorError(
                            self.dungeons[dungeon_id], dungeon_id, [f_id]
                        )
                        self._errors.append(err)
                        already_invalidated[dungeon_id] = err

        for error in self._errors:
            if error.makes_fully_invalid:
                self.invalid_dungeons.add(error.dungeon_id)

        return len(self._errors) < 1

    def _mappa_floor_list_doesnt_exist(self, mappa_index: int) -> bool:
        return len(self.mappa.floor_lists) <= mappa_index

    def _mappa_floor_doesnt_exist(
        self, mappa_index: int, start_after: int, number_floors: int
    ) -> bool:
        return len(self.mappa.floor_lists[mappa_index]) < start_after + number_floors

    def _mappa_floor_already_visited(
        self, mappa_index: int, start_after: int, number_floors: int
    ) -> bool:
        for i in range(start_after, start_after + number_floors):
            if i in self._visited_floor_lists[mappa_index]:
                return True
        return False

    def _init_mappa_visited(self, mappa_index: int) -> list[int]:
        s = []
        for i in range(0, len(self.mappa.floor_lists[mappa_index])):
            s.append(i)
        return s

    def _add_mappa_visited(
        self, mappa_index: int, start_after: int, number_floors: int
    ) -> None:
        for i in range(start_after, start_after + number_floors):
            self._visited_floor_lists[mappa_index].append(i)

    def _mappa_group_count_invalid(
        self, dungeons: list[DungeonDefinition], mappa_index: int
    ) -> tuple[u8, list[int]]:
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
        return u8_checked(count_floor_expected), invalid

    def _mappa_which_dungeon_uses(
        self, mappa_index: int, start_after: int, number_floors: int
    ) -> int:
        for i, dungeon in enumerate(self.dungeons):  # type: ignore
            if dungeon.mappa_index == mappa_index:
                if (
                    dungeon.start_after >= start_after
                    and dungeon.start_after + dungeon.number_floors
                    > start_after + number_floors
                ):
                    return i
        raise ValueError("Invalid reference in dungeon validation")

    def _mappa_get_dungeon_id(self, mappa_index: int, floor_id: int) -> int:
        start_index_prev = -1
        current_i = None
        for i, dungeon in enumerate(self.dungeons):  # type: ignore
            if dungeon.mappa_index == mappa_index:
                if start_index_prev < dungeon.start_after <= floor_id:
                    current_i = i
                    start_index_prev = dungeon.start_after
        if current_i is None:
            raise ValueError("Invalid reference in dungeon validation")
        return current_i
