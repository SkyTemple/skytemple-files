#  Copyright 2020-2025 Capypara and the SkyTemple Contributors
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
from __future__ import (
    annotations,
)
from typing import Callable

from ndspy.rom import NintendoDSRom
from skytemple_files.data.item_p.handler import ItemPHandler
from skytemple_files.common.util import read_u32, get_binary_from_rom
from skytemple_files.common.ppmdu_config.data import (
    Pmd2Data,
    GAME_VERSION_EOS,
    GAME_REGION_US,
    GAME_REGION_EU,
)
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler
from skytemple_files.common.i18n_util import _

MODIFIED_INSTRUCTION = 0xE8BD83F8  # ldmia all the shit
OFFSET_EU = 0x231F29C + 12 - 0x22DCB80  # location of the instruction minus starting point of overlay 29
OFFSET_US = 0x231E834 + 12 - 0x22DC240  # same but US HeHeHaHa

ADD_TYPES_ADDRESS_NA = 0x2EAA4
ADD_TYPES_ADDRESS_EU = 0x2EBD8
ADD_TYPES_ORIGINAL_CODE = 0xE3A00024


# the function where all the magic happens
def set_item_ai_flags(item_p_model, item_id: int, ai_flag_1: bool, ai_flag_2: bool, ai_flag_3: bool):
    item = item_p_model.item_list[item_id]
    item.ai_flag_1 = ai_flag_1
    item.ai_flag_2 = ai_flag_2
    item.ai_flag_3 = ai_flag_3


class AiItemImprovementsHandler(AbstractPatchHandler):
    @property
    def name(self) -> str:
        return "AiItemImprovements"

    @property
    def description(self) -> str:
        return _("Tweaks team and enemy AI to use more types of items, and use them more effectively. Overwrites AiItemOptimizations.")

    @property
    def author(self) -> str:
        return "happylappy"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.IMPROVEMENT_TWEAK

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        patch_area = get_binary_from_rom(rom, config.bin_sections.overlay29)
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_u32(patch_area, OFFSET_US) == MODIFIED_INSTRUCTION
            if config.game_region == GAME_REGION_EU:
                return read_u32(patch_area, OFFSET_EU) == MODIFIED_INSTRUCTION
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data) -> None:
        param = self.get_parameters()
        # do an is_applied check for AddTypes. This is necessary because the Gummi table size changes if this patch is applied!
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                add_types_applied = (
                    read_u32(rom.loadArm9Overlays([29])[29].data, ADD_TYPES_ADDRESS_NA) != ADD_TYPES_ORIGINAL_CODE
                )
            elif config.game_region == GAME_REGION_EU:
                add_types_applied = (
                    read_u32(rom.loadArm9Overlays([29])[29].data, ADD_TYPES_ADDRESS_EU) != ADD_TYPES_ORIGINAL_CODE
                )
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()
        if add_types_applied
            param["AddTypesApplied"] = 1
        else:
            param["AddTypesApplied"] = 0
        self.__parameters = param
        if param["AssignAiFlags"] == "1":
            # load rom data
            item_p_model = ItemPHandler.deserialize(rom.getFileByName("BALANCE/item_p.bin"))
            # call set_item_ai_flags for every item you want to modify
            # Gold Thorn & Rare Fossil
            set_item_ai_flags(item_p_model, 9, True, False, False)
            set_item_ai_flags(item_p_model, 10, True, False, False)
            # Warp/Via/Gravelyrock/Gone Pebble/Wander Gummi Fire on all cylindars
            set_item_ai_flags(item_p_model, 86, True, True, True)
            set_item_ai_flags(item_p_model, 107, True, True, True)
            set_item_ai_flags(item_p_model, 137, True, False, True)
            set_item_ai_flags(item_p_model, 167, True, False, True)
            set_item_ai_flags(item_p_model, 168, True, True, True)

            # Blast Seed Eat but don't throw at allies
            set_item_ai_flags(item_p_model, 87, True, False, True)
            # Ginseng Allow use on self
            set_item_ai_flags(item_p_model, 88, False, True, True)
            # Pure Seeds need use on self or allies
            set_item_ai_flags(item_p_model, 95, False, True, True)
            # Grimy Food/Oren enable all use cases!
            set_item_ai_flags(item_p_model, 111, True, True, True)
            set_item_ai_flags(item_p_model, 117, True, True, True)
            # All Gummis/Nectar need self-use flag
            set_item_ai_flags(item_p_model, 103, False, True, True)
            set_item_ai_flags(item_p_model, 119, False, True, True)
            set_item_ai_flags(item_p_model, 120, False, True, True)
            set_item_ai_flags(item_p_model, 121, False, True, True)
            set_item_ai_flags(item_p_model, 122, False, True, True)
            set_item_ai_flags(item_p_model, 123, False, True, True)
            set_item_ai_flags(item_p_model, 124, False, True, True)
            set_item_ai_flags(item_p_model, 125, False, True, True)
            set_item_ai_flags(item_p_model, 126, False, True, True)
            set_item_ai_flags(item_p_model, 127, False, True, True)
            set_item_ai_flags(item_p_model, 128, False, True, True)
            set_item_ai_flags(item_p_model, 129, False, True, True)
            set_item_ai_flags(item_p_model, 130, False, True, True)
            set_item_ai_flags(item_p_model, 131, False, True, True)
            set_item_ai_flags(item_p_model, 132, False, True, True)
            set_item_ai_flags(item_p_model, 133, False, True, True)
            set_item_ai_flags(item_p_model, 134, False, True, True)
            set_item_ai_flags(item_p_model, 135, False, True, True)
            set_item_ai_flags(item_p_model, 136, False, True, True)
            if param["AddTypesApplied"] == 1:
                set_item_ai_flags(item_p_model, 138, False, True, True)
            # Enable Key Use
            set_item_ai_flags(item_p_model, 182, False, False, True)
            # Enable the use of certain orbs:
            set_item_ai_flags(item_p_model, 301, False, False, True)
            set_item_ai_flags(item_p_model, 302, False, False, True)
            set_item_ai_flags(item_p_model, 303, False, False, True)
            set_item_ai_flags(item_p_model, 304, False, False, True)
            set_item_ai_flags(item_p_model, 305, False, False, True)
            set_item_ai_flags(item_p_model, 310, False, False, True)
            set_item_ai_flags(item_p_model, 312, False, False, True)
            set_item_ai_flags(item_p_model, 313, False, False, True)
            set_item_ai_flags(item_p_model, 318, False, False, True)
            set_item_ai_flags(item_p_model, 321, False, False, True)
            set_item_ai_flags(item_p_model, 322, False, False, True)
            set_item_ai_flags(item_p_model, 333, False, False, True)
            set_item_ai_flags(item_p_model, 336, False, False, True)
            set_item_ai_flags(item_p_model, 348, False, False, True)
            # Unown Rock go brrrrrrrrrr
            set_item_ai_flags(item_p_model, 400, True, False, False)
            set_item_ai_flags(item_p_model, 401, True, False, False)
            set_item_ai_flags(item_p_model, 402, True, False, False)
            set_item_ai_flags(item_p_model, 403, True, False, False)
            set_item_ai_flags(item_p_model, 404, True, False, False)
            set_item_ai_flags(item_p_model, 405, True, False, False)
            set_item_ai_flags(item_p_model, 406, True, False, False)
            set_item_ai_flags(item_p_model, 407, True, False, False)
            set_item_ai_flags(item_p_model, 408, True, False, False)
            set_item_ai_flags(item_p_model, 409, True, False, False)
            set_item_ai_flags(item_p_model, 410, True, False, False)
            set_item_ai_flags(item_p_model, 411, True, False, False)
            set_item_ai_flags(item_p_model, 412, True, False, False)
            set_item_ai_flags(item_p_model, 413, True, False, False)
            set_item_ai_flags(item_p_model, 414, True, False, False)
            set_item_ai_flags(item_p_model, 415, True, False, False)
            set_item_ai_flags(item_p_model, 416, True, False, False)
            set_item_ai_flags(item_p_model, 417, True, False, False)
            set_item_ai_flags(item_p_model, 418, True, False, False)
            set_item_ai_flags(item_p_model, 419, True, False, False)
            set_item_ai_flags(item_p_model, 420, True, False, False)
            set_item_ai_flags(item_p_model, 421, True, False, False)
            set_item_ai_flags(item_p_model, 422, True, False, False)
            set_item_ai_flags(item_p_model, 423, True, False, False)
            set_item_ai_flags(item_p_model, 424, True, False, False)
            set_item_ai_flags(item_p_model, 425, True, False, False)
            set_item_ai_flags(item_p_model, 426, True, False, False)
            set_item_ai_flags(item_p_model, 427, True, False, False)
            # save rom data
            rom.setFileByName("BALANCE/item_p.bin", ItemPHandler.serialize(item_p_model))
        # Apply the patch
        apply()

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
