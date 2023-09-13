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

import os
from typing import Callable, cast, Optional, List

from ndspy.rom import NintendoDSRom
from PIL import Image

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_US,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.util import (
    get_files_from_rom_with_extension,
    get_resources_dir,
    read_u32,
)
from skytemple_files.data.str.handler import StrHandler
from skytemple_files.graphics.fonts.graphic_font.handler import GraphicFontHandler
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler

PATCH_CHECK_ADDR_APPLIED_US = 0x243A0
PATCH_CHECK_ADDR_APPLIED_EU = 0x24600
PATCH_CHECK_INSTR_APPLIED = 0xEA000004

SRC_DIR = os.path.join(
    get_resources_dir(),
    "patches",
    "asm_patches",
    "anonymous_asm_mods",
    "stat_disp",
    "src",
)

OLD_STAT = "[M:S3]" * 8


class ChangeMoveStatDisplayPatchHandler(AbstractPatchHandler):
    @property
    def name(self) -> str:
        return "ChangeMoveStatsDisplay"

    @property
    def description(self) -> str:
        return _(
            """Replaces old move stats display with bars.
This patch may not be compatible if the markfont.dat file has been modified."""
        )

    @property
    def author(self) -> str:
        return "Anonymous"

    @property
    def version(self) -> str:
        return "0.0.1"

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.UTILITY

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return (
                    read_u32(rom.arm9, PATCH_CHECK_ADDR_APPLIED_US)
                    != PATCH_CHECK_INSTR_APPLIED
                )
            if config.game_region == GAME_REGION_EU:
                return (
                    read_u32(rom.arm9, PATCH_CHECK_ADDR_APPLIED_EU)
                    != PATCH_CHECK_INSTR_APPLIED
                )
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        START_ACCURACY = cast(int, self.get_parameter("StartGraphicPos"))
        START_POWER = START_ACCURACY + 12
        MAX_POWER = (
            f"[M:B{START_POWER}]"
            + (f"[M:B{START_POWER + 10}]") * 9
            + f"[M:B{START_POWER + 9}]"
        )
        MAX_ACCU = (
            f"[M:B{START_POWER}]"
            + (f"[M:B{START_ACCURACY + 11}]") * 10
            + f"[M:B{START_POWER}]"
        )
        DESC_CHANGES = {
            8: MAX_POWER,
            60: MAX_POWER,
            75: MAX_POWER,
            100: MAX_POWER,
            153: MAX_POWER,
            156: MAX_POWER,
            205: MAX_POWER,
            206: MAX_POWER,
            348: MAX_POWER,
            477: MAX_POWER,
            61: MAX_ACCU,
            340: MAX_ACCU,
            535: MAX_ACCU,
        }
        bin_before = rom.getFileByName("FONT/markfont.dat")
        model = GraphicFontHandler.deserialize(bin_before)
        entries: List[Optional[Image.Image]] = []
        for x in range(model.get_nb_entries()):
            entries.append(model.get_entry(x))
        while len(entries) < max(START_ACCURACY + 12, START_POWER + 11):
            entries.append(None)

        for x in range(START_ACCURACY, START_ACCURACY + 12):
            img = Image.open(
                os.path.join(SRC_DIR, "accu_%02d.png" % (x - START_ACCURACY)), "r"
            )
            entries[x] = img
        for x in range(START_POWER, START_POWER + 11):
            img = Image.open(
                os.path.join(SRC_DIR, "pow_%02d.png" % (x - START_POWER)), "r"
            )
            entries[x] = img
        model.set_entries(entries)
        bin_after = GraphicFontHandler.serialize(model)
        rom.setFileByName("FONT/markfont.dat", bin_after)

        # Change some move descriptions
        for filename in get_files_from_rom_with_extension(rom, "str"):
            bin_before = rom.getFileByName(filename)
            strings = StrHandler.deserialize(
                bin_before, string_encoding=config.string_encoding
            )
            block = config.string_index_data.string_blocks["Move Descriptions"]
            for k, v in DESC_CHANGES.items():
                strings.strings[block.begin + k] = strings.strings[
                    block.begin + k
                ].replace(OLD_STAT, v)
            bin_after = StrHandler.serialize(strings)
            rom.setFileByName(filename, bin_after)

        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
