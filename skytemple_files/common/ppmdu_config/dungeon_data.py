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
from typing import List, Optional

from skytemple_files.common.util import AutoString


class Pmd2BinPackFile(AutoString):
    def __init__(self, idxfirst: int, idxlast: Optional[int], type: str, name: str):
        self.idxfirst = idxfirst
        self.idxlast = idxlast
        self.type = type
        self.name = name


class Pmd2DungeonItem(AutoString):
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Pmd2DungeonItem):
            return False
        return self.id == other.id  # name is not relevant here

    def __hash__(self):
        return hash(self.id)


class Pmd2DungeonDungeon(AutoString):
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Pmd2DungeonDungeon):
            return False
        return self.id == other.id  # name is not relevant here

    def __hash__(self):
        return hash(self.id)


class Pmd2DungeonBinFiles(AutoString):
    def __init__(self, files: List[Pmd2BinPackFile]):
        self._files = files

    def get(self, idx: int) -> Pmd2BinPackFile:
        for file_def in self._files:
            if file_def.idxlast is None:
                if file_def.idxfirst == idx:
                    return file_def
            elif file_def.idxfirst <= idx <= file_def.idxlast:
                return file_def
        raise IndexError(f"No file definition found for {idx}.")


class Pmd2DungeonData(AutoString):
    def __init__(
            self, dungeon_bin_files: Pmd2DungeonBinFiles, items: List[Pmd2DungeonItem],
            dungeons: List[Pmd2DungeonDungeon]
    ):
        self.dungeon_bin_files = dungeon_bin_files
        self.items = items
        self.dungeons = dungeons
