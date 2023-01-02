"""Generates output for xgettext for the PPMDU config."""
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

from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_US,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader


def p(string, expl=""):
    string = string.replace('"', '\\"')
    if expl != "":
        expl = "# TRANSLATORS: " + expl
    print(f'_("{string}")  {expl}')


def dump(data: Pmd2Data):
    for lang in data.string_index_data.languages:
        p(lang.name)
    for string_block in data.string_index_data.string_blocks.values():
        p(string_block.name)
    for category in data.dungeon_data.item_categories.values():
        p(category.name)
    for patch in data.asm_patches_constants.patches.values():
        for param in patch.parameters.values():
            p(param.label, "Used in the confirguation dialog for a patch")

    # We don't dump item or dungeon names, since the SkyTemple UI reads them from ROM, always.


if __name__ == "__main__":
    dump(
        Pmd2XmlReader.load_default(
            GAME_VERSION_EOS + "_" + GAME_REGION_US, translate_strings=False
        )
    )
    dump(
        Pmd2XmlReader.load_default(
            GAME_VERSION_EOS + "_" + GAME_REGION_EU, translate_strings=False
        )
    )
