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

from typing import TYPE_CHECKING, Dict, List

from ndspy.rom import NintendoDSRom
from range_typed_integers import u32

if TYPE_CHECKING:
    from skytemple_files.common.ppmdu_config.data import Pmd2Data
    from skytemple_files.common.ppmdu_config.dungeon_data import Pmd2DungeonItemCategory


FILENAME_ACTOR_LIST = "BALANCE/actor_list.bin"
FILENAME_LEVEL_LIST = "BALANCE/level_list.bin"
FILENAME_OBJECT_LIST = "BALANCE/objects.bin"


class LoadNotSupportedError(RuntimeError):
    pass


class RomDataLoader:
    """Loads supported data from the ROM into the ppmdu configuration."""

    def __init__(self, rom: NintendoDSRom):
        self.rom = rom

    def load_into(self, config_load_into: "Pmd2Data"):
        self.load_script_var_list_into(config_load_into)
        self.load_actor_list_into(config_load_into, ignore_not_supported=True)
        self.load_level_list_into(config_load_into, ignore_not_supported=True)
        self.load_object_list_into(config_load_into, ignore_not_supported=True)
        self.load_item_categories_into(config_load_into)
        self.load_sprconf_into(config_load_into)

    def load_script_var_list_into(self, config_load_into: "Pmd2Data"):
        from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptGameVar
        from skytemple_rust.st_script_var_table import ScriptVariableTables

        if config_load_into.bin_sections.arm9.loadaddress is not None:
            var_table = ScriptVariableTables(
                bytes(self.rom.arm9),
                config_load_into.bin_sections.arm9.data.SCRIPT_VARS.address,
                config_load_into.bin_sections.arm9.data.SCRIPT_VARS_LOCALS.address,
                u32(config_load_into.bin_sections.arm9.loadaddress),
            )
            variables_converted = []
            for v in var_table.globals:
                variables_converted.append(
                    Pmd2ScriptGameVar(
                        v.id,
                        v.type,
                        v.unk1,
                        v.memoffset,
                        v.bitshift,
                        v.nbvalues,
                        v.default,
                        v.name,
                        False,
                    )
                )
            for v in var_table.locals:
                variables_converted.append(
                    Pmd2ScriptGameVar(
                        v.id,
                        v.type,
                        v.unk1,
                        v.memoffset,
                        v.bitshift,
                        v.nbvalues,
                        v.default,
                        v.name,
                        True,
                    )
                )
            config_load_into.script_data.game_variables = variables_converted

    def load_actor_list_into(
        self, config_load_into: "Pmd2Data", ignore_not_supported=False
    ):
        from skytemple_files.common.types.file_types import FileType

        if FILENAME_ACTOR_LIST in self.rom.filenames:
            list_bin = self.rom.getFileByName(FILENAME_ACTOR_LIST)
            actor_list = FileType.SIR0.unwrap_obj(
                FileType.SIR0.deserialize(list_bin), FileType.ACTOR_LIST_BIN.type()
            )
            config_load_into.script_data.level_entities = actor_list.list
        elif not ignore_not_supported:
            raise LoadNotSupportedError("The ROM does not contain an actor list.")

    def load_level_list_into(
        self, config_load_into: "Pmd2Data", ignore_not_supported=False
    ):
        from skytemple_files.common.types.file_types import FileType

        if FILENAME_LEVEL_LIST in self.rom.filenames:
            list_bin = self.rom.getFileByName(FILENAME_LEVEL_LIST)
            level_list = FileType.SIR0.unwrap_obj(
                FileType.SIR0.deserialize(list_bin), FileType.LEVEL_LIST_BIN.type()
            )
            config_load_into.script_data.level_list = level_list.list
        elif not ignore_not_supported:
            raise LoadNotSupportedError("The ROM does not contain an level list.")

    def load_object_list_into(
        self, config_load_into: "Pmd2Data", ignore_not_supported=False
    ):
        from skytemple_files.common.types.file_types import FileType

        if FILENAME_OBJECT_LIST in self.rom.filenames:
            list_bin = self.rom.getFileByName(FILENAME_OBJECT_LIST)
            object_list = FileType.OBJECT_LIST_BIN.deserialize(list_bin)
            config_load_into.script_data.objects = object_list.list
        elif not ignore_not_supported:
            raise LoadNotSupportedError("The ROM does not contain an level list.")

    def load_item_categories_into(self, config_load_into: "Pmd2Data"):
        from skytemple_files.common.types.file_types import FileType

        item_p_bin = self.rom.getFileByName("BALANCE/item_p.bin")
        item_p = FileType.ITEM_P.deserialize(item_p_bin)

        cats: Dict["Pmd2DungeonItemCategory", List[int]] = {
            x: [] for x in config_load_into.dungeon_data.item_categories.values()
        }

        for idx, entry in enumerate(item_p.item_list):
            cats[config_load_into.dungeon_data.item_categories[entry.category]].append(
                idx
            )

        for category in config_load_into.dungeon_data.item_categories.values():
            category.items = cats[category]

    def load_sprconf_into(self, config_load_into: Pmd2Data):
        """Loads the overrides in the MONSTER/sprconf.json into the configuration."""
        from skytemple_files.common.ppmdu_config.data import Pmd2Sprite, Pmd2Index
        from skytemple_files.common.types.file_types import FileType

        sprconf = FileType.SPRCONF.load(self.rom, create=False)
        for idx, config in sprconf.items():
            indices: Dict[int, Pmd2Index] = {}
            for idx_index, index in config.items():
                indices[idx_index] = Pmd2Index(idx_index, index)
            config_load_into.animation_names[idx] = Pmd2Sprite(idx, indices)
