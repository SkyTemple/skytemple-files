"""
Main static configuration for SkyTemple itself and a ROM.
For now, the documentation of fields is in the pmd2data.xml.
"""
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

from enum import Enum
from typing import Any, Dict, List, Optional, Pattern, Union

import pmdsky_debug_py

from skytemple_files.common.compat_13x import _DeprecatedBinaries
from skytemple_files.common.ppmdu_config.dungeon_data import Pmd2DungeonData
from skytemple_files.common.ppmdu_config.pmdsky_debug.extras import (
    ExtraAllSymbolsProtocol,
    ExtraNaSections,
    ExtraEuSections,
    ExtraJpSections,
)

from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptData
from skytemple_files.common.util import AutoString

GAME_VERSION_EOT = "EoT"
GAME_VERSION_EOD = "EoD"
GAME_VERSION_EOS = "EoS"

GAME_REGION_US = "NA"
GAME_REGION_EU = "EU"
GAME_REGION_JP = "JP"


LANG_JP = "japanese"
LANG_EN = "english"
LANG_FR = "french"
LANG_DE = "german"
LANG_IT = "italian"
LANG_SP = "spanish"


class Pmd2GameEdition(AutoString):
    def __init__(
        self,
        id: str,
        gamecode: str,
        version: str,
        region: str,
        arm9off14: int,
        defaultlang: str,
        issupported: bool,
    ):
        self.id = id
        self.gamecode = gamecode
        self.version = version
        self.region = region
        self.arm9off14 = arm9off14
        self.defaultlang = defaultlang
        self.issupported = issupported


class Pmd2SortLists(AutoString):
    def __init__(self, m2n: Optional[str], n2m: Optional[str], i2n: Optional[str]):
        self.m2n = m2n
        self.n2m = n2m
        self.i2n = i2n


class Pmd2Language(AutoString):
    def __init__(
        self,
        filename: str,
        name: str,
        name_localized: str,
        locale: str,
        sort_lists: Pmd2SortLists,
    ):
        self.filename = filename
        self.name = name
        self.name_localized = name_localized
        self.locale = locale
        self.sort_lists = sort_lists

    def __str__(self) -> str:
        return self.name_localized


class Pmd2StringBlock(AutoString):
    def __init__(self, name: str, name_localized: str, begin: int, end: int):
        self.name = name
        self.name_localized = name_localized
        self.begin = begin
        self.end = end

    def __str__(self) -> str:
        return self.name_localized


class Pmd2StringIndexData(AutoString):
    def __init__(
        self, languages: List[Pmd2Language], string_blocks: List[Pmd2StringBlock]
    ):
        self.languages = languages
        self.string_blocks: Dict[str, Pmd2StringBlock] = {
            blk.name: blk for blk in string_blocks
        }


class Pmd2LooseBinFile(AutoString):
    def __init__(self, srcdata: str, filepath: str):
        self.srcdata = srcdata
        self.filepath = filepath


class Pmd2PatchDir(AutoString):
    def __init__(self, filepath: str, stubpath: str):
        self.filepath = filepath
        self.stubpath = stubpath


class Pmd2PatchInclude(AutoString):
    def __init__(self, filename: str):
        self.filename = filename


class Pmd2PatchOpenBin(AutoString):
    def __init__(self, filepath: str, includes: List[Pmd2PatchInclude]):
        self.filepath = filepath
        self.includes = includes


class Pmd2PatchParameterType(Enum):
    STRING = "str"
    INTEGER = "int"
    SELECT = "select"


class Pmd2PatchParameterOption(AutoString):
    def __init__(
        self, type: Pmd2PatchParameterType, label: str, value: Union[int, str]
    ):
        self.type = type
        self.label = label
        self.value = value


class Pmd2PatchParameter(AutoString):
    def __init__(
        self,
        name: str,
        type: Pmd2PatchParameterType,
        label: str,
        *,
        min: Optional[int] = None,
        max: Optional[int] = None,
        options: Optional[List[Pmd2PatchParameterOption]] = None,
        default: Union[int, str, None] = None,
    ):
        self.name = name
        self.type = type
        self.label = label
        self.min = min
        self.max = max
        self.default = default
        self.options = options


class Pmd2Patch(AutoString):
    def __init__(
        self,
        id: str,
        includes: List[Pmd2PatchInclude],
        open_bins: List[Pmd2PatchOpenBin],
        parameters: List[Pmd2PatchParameter],
    ):
        self.id = id
        self.includes = includes
        self.open_bins = open_bins
        self.parameters: Dict[str, Pmd2PatchParameter] = {
            param.name: param for param in parameters
        }

    def has_parameters(self) -> bool:
        return len(self.parameters) > 0


class Pmd2PatchStringReplacementGame(AutoString):
    def __init__(self, game_id: str, replace: str):
        self.game_id = game_id
        self.replace = replace


class Pmd2PatchStringReplacement(AutoString):
    def __init__(
        self,
        filename: str,
        regexp: Pattern[Any],
        games: List[Pmd2PatchStringReplacementGame],
    ):
        self.filename = filename
        self.regexp = regexp
        self.games = games


class Pmd2SimplePatch(AutoString):
    def __init__(
        self,
        id: str,
        includes: List[Pmd2PatchInclude],
        string_replacements: List[Pmd2PatchStringReplacement],
        parameters: List[Pmd2PatchParameter],
    ):
        self.id = id
        self.includes = includes
        self.string_replacements = string_replacements
        self.parameters: Dict[str, Pmd2PatchParameter] = {
            param.name: param for param in parameters
        }

    def has_parameters(self) -> bool:
        return len(self.parameters) > 0


class Pmd2AsmPatchesConstants(AutoString):
    def __init__(
        self,
        loose_bin_files: List[Pmd2LooseBinFile],
        patch_dir: Pmd2PatchDir,
        patches: List[Union[Pmd2Patch, Pmd2SimplePatch]],
    ):
        self.loose_bin_files: Dict[str, Pmd2LooseBinFile] = {
            var.srcdata: var for var in loose_bin_files
        }
        self.patch_dir = patch_dir
        self.patches: Dict[str, Union[Pmd2Patch, Pmd2SimplePatch]] = {
            var.id: var for var in patches
        }


class Pmd2Index(AutoString):
    def __init__(self, id: int, names: List[str]):
        self.id = id
        self.names = names


class Pmd2Sprite(AutoString):
    def __init__(self, id: int, indices: Dict[int, Pmd2Index]):
        self.id = id
        self.indices: Dict[int, Pmd2Index] = {k: indices[k] for k in sorted(indices)}


class Pmd2Data(AutoString):
    def __init__(
        self,
        game_edition: Pmd2GameEdition,
        game_editions: List[Pmd2GameEdition],
        game_constants: Dict[str, int],
        string_index_data: Pmd2StringIndexData,
        asm_patches_constants: Pmd2AsmPatchesConstants,
        script_data: Pmd2ScriptData,
        dungeon_data: Pmd2DungeonData,
        string_encoding: str,
        animation_names: Dict[int, Pmd2Sprite],
    ):
        self.game_edition = game_edition.id
        self.game_version = game_edition.version
        self.game_region = self.get_region_constant_for_region_name(game_edition.region)
        self.game_editions: Dict[str, Pmd2GameEdition] = {
            edi.id: edi for edi in game_editions
        }
        self.game_constants = game_constants
        self.string_index_data = string_index_data
        self.asm_patches_constants = asm_patches_constants
        self.script_data = script_data
        self.dungeon_data = dungeon_data
        self.string_encoding = string_encoding
        self.animation_names: Dict[int, Pmd2Sprite] = {
            k: animation_names[k] for k in sorted(animation_names)
        }
        self.bin_sections: pmdsky_debug_py.AllSymbolsProtocol
        if self.game_region == GAME_REGION_US:
            self.bin_sections = pmdsky_debug_py.na
        if self.game_region == GAME_REGION_EU:
            self.bin_sections = pmdsky_debug_py.eu
        if self.game_region == GAME_REGION_JP:
            self.bin_sections = pmdsky_debug_py.jp

        # SkyTemple specific / non pmdsky-debug symbols
        self.extra_bin_sections: ExtraAllSymbolsProtocol
        # regarding the type ignores, see: https://github.com/python/mypy/issues/5018#issuecomment-1165828654
        if self.game_region == GAME_REGION_US:
            self.extra_bin_sections = ExtraNaSections  # type: ignore
        if self.game_region == GAME_REGION_EU:
            self.extra_bin_sections = ExtraEuSections  # type: ignore
        if self.game_region == GAME_REGION_JP:
            self.extra_bin_sections = ExtraJpSections  # type: ignore

        # Backwards compatibility, deprecated
        self.binaries = _DeprecatedBinaries(self)

    @staticmethod
    def get_region_constant_for_region_name(region: str) -> str:
        if region == "NorthAmerica":
            return GAME_REGION_US
        if region == "Europe":
            return GAME_REGION_EU
        if region == "Japan":
            return GAME_REGION_JP
        raise ValueError(f"Unknown region {region}.")
