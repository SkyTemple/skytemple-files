#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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

from typing import Callable

from ndspy.rom import NintendoDSRom

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_US,
    GAME_REGION_JP,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_binary_from_rom, read_u32
from skytemple_files.data.md.handler import MdHandler
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch

PATCH_CHECK_ADDR_APPLIED_US = 0x527E4
PATCH_CHECK_ADDR_APPLIED_EU = 0x52B1C
PATCH_CHECK_ADDR_APPLIED_JP = 0x52B1C
PATCH_CHECK_INSTR_APPLIED = 0xE3A01F96


class SpriteSizePatchHandler(AbstractPatchHandler):
    @property
    def name(self) -> str:
        return "SpriteSizeInMonsterData"

    @property
    def description(self) -> str:
        return _(
            """Changes Sprite Size and Sprite File Size values to be in each Pokémon's data."""
        )

    @property
    def author(self) -> str:
        return "Anonymous"

    @property
    def version(self) -> str:
        return "0.8.6"

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.IMPROVEMENT_TWEAK
    
    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_u32(rom.arm9, PATCH_CHECK_ADDR_APPLIED_US) != PATCH_CHECK_INSTR_APPLIED
            if config.game_region == GAME_REGION_EU:
                return read_u32(rom.arm9, PATCH_CHECK_ADDR_APPLIED_EU) != PATCH_CHECK_INSTR_APPLIED
            if config.game_region == GAME_REGION_JP:
                return read_u32(rom.arm9, PATCH_CHECK_ADDR_APPLIED_JP) != PATCH_CHECK_INSTR_APPLIED
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data) -> None:
        if not self.is_applied(rom, config):
            bincfg = config.bin_sections.arm9
            binary = bytearray(get_binary_from_rom(rom, bincfg))
            
            md_bin = rom.getFileByName("BALANCE/monster.md")
            md_model = MdHandler.deserialize(md_bin)
            block2 = bincfg.data.MONSTER_SPRITE_DATA
            data = (
                binary[block2.address : block2.address + block2.length]
                + binary[block2.address : block2.address + block2.length]
            )
            for i, e in enumerate(md_model.entries):
                e.unk17 = data[i*2]
                e.unk18 = data[i*2 + 1]
            rom.setFileByName("BALANCE/monster.md", MdHandler.serialize(md_model))
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data) -> None:
        raise NotImplementedError()
