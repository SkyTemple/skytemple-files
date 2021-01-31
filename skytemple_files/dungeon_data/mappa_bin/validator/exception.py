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
from typing import List

from skytemple_files.hardcoded.dungeons import DungeonDefinition
from skytemple_files.common.i18n_util import f, _


class DungeonValidatorError(BaseException):
    def __init__(self, dungeon: DungeonDefinition, dungeon_id: int):
        self.dungeon = dungeon
        self.dungeon_id = dungeon_id
        self.makes_fully_invalid = True

    @property
    def name(self):
        return self.__class__.__name__


class InvalidFloorListReferencedError(DungeonValidatorError):
    @property
    def name(self):
        return _('Invalid Floor List')

    def __str__(self):
        return _("References a dungeon floor list that doesn't exist.")


class InvalidFloorReferencedError(DungeonValidatorError):
    @property
    def name(self):
        return _('Invalid Floor')

    def __str__(self):
        return _("References floor that is out of bounds in the floor list for this group.")


class FloorReusedError(DungeonValidatorError):
    def __init__(self, dungeon: DungeonDefinition, dungeon_id: int, reused_of_dungeon_with_id: int):
        super().__init__(dungeon, dungeon_id)
        self.reused_of_dungeon_with_id = reused_of_dungeon_with_id
        self.reused_of_dungeon_name = None

    @property
    def name(self):
        return _('Re-uses Floor')

    def __str__(self):
        name = self.reused_of_dungeon_name if self.reused_of_dungeon_name is not None else f'{_("dungeon")} {self.reused_of_dungeon_with_id}'
        return f(_("Re-uses floors that are already used by {name}."))


class DungeonTotalFloorCountInvalidError(DungeonValidatorError):
    def __init__(self, dungeon: DungeonDefinition, dungeon_id: int, expected_floor_count_in_group: int):
        super().__init__(dungeon, dungeon_id)
        self.expected_floor_count_in_group = expected_floor_count_in_group
        self.makes_fully_invalid = False


class DungeonMissingFloorError(DungeonValidatorError):
    def __init__(self, dungeon: DungeonDefinition, dungeon_id: int, floors_in_mappa_not_referenced: List[int]):
        super().__init__(dungeon, dungeon_id)
        self.floors_in_mappa_not_referenced = floors_in_mappa_not_referenced
        self.makes_fully_invalid = False

    def add(self, f_id):
        self.floors_in_mappa_not_referenced.append(f_id)

    @property
    def name(self):
        return _('Unused Floors')

    def __str__(self):
        return f(_("Has {len(self.floors_in_mappa_not_referenced)} extra floors in it's floor list, "
                   "which are not assigned to any dungeon."))
