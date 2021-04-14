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
from typing import TYPE_CHECKING

from ndspy.rom import NintendoDSRom


if TYPE_CHECKING:
    from skytemple_files.common.ppmdu_config.data import Pmd2Data


FILENAME_ACTOR_LIST = 'BALANCE/actor_list.bin'


class LoadNotSupportedError(RuntimeError):
    pass


class RomDataLoader:
    """Loads supported data from the ROM into the ppmdu configuration."""
    def __init__(self, rom: NintendoDSRom):
        self.rom = rom

    def load_into(self, config_load_into: 'Pmd2Data'):
        self.load_actor_list_into(config_load_into, ignore_not_supported=True)
        self.load_item_categories_into(config_load_into)

    def load_actor_list_into(self, config_load_into: 'Pmd2Data', ignore_not_supported=False):
        from skytemple_files.common.types.file_types import FileType

        if FILENAME_ACTOR_LIST in self.rom.filenames:
            list_bin = self.rom.getFileByName(FILENAME_ACTOR_LIST)
            actor_list = FileType.SIR0.unwrap_obj(
                FileType.SIR0.deserialize(list_bin), FileType.ACTOR_LIST_BIN.type()
            )
            config_load_into.script_data.level_entities = actor_list.list
        elif not ignore_not_supported:
            raise LoadNotSupportedError("The ROM does not contain an actor list.")

    def load_item_categories_into(self, config_load_into: 'Pmd2Data'):
        from skytemple_files.common.types.file_types import FileType

        item_p_bin = self.rom.getFileByName('BALANCE/item_p.bin')
        item_p = FileType.ITEM_P.deserialize(item_p_bin)

        cats = {x: [] for x in config_load_into.dungeon_data.item_categories.values()}

        for idx, entry in enumerate(item_p.item_list):
            cats[entry.category_pmd2obj(config_load_into.dungeon_data.item_categories)].append(idx)

        for category in config_load_into.dungeon_data.item_categories.values():
            category.items = cats[category]
