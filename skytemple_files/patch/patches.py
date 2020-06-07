#  Copyright 2020 Parakoopa
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
import os
from enum import Enum
from functools import partial
from typing import Type, Dict

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import get_resources_dir
from skytemple_files.patch.arm_patcher import ArmPatcher
from skytemple_files.patch.handler.abstract import AbstractPatchHandler
from skytemple_files.patch.handler.actor_loader import ActorLoaderPatchHandler


CORE_PATCHES_BASE_DIR = os.path.join(get_resources_dir(), 'ppmdu_patches')


class PatchType(Enum):
    ACTOR_LOADER = ActorLoaderPatchHandler


class Patcher:
    def __init__(self, rom: NintendoDSRom, config: Pmd2Data, skip_core_patches=False):
        self._rom = rom
        self._config = config
        self._loaded_patches: Dict[str, AbstractPatchHandler] = {}
        # Path to the directories, which contain the ASM files for the handlers.
        self._patch_dirs: Dict[str, str] = {}

        self._arm_patcher = ArmPatcher(self._rom)

        if not skip_core_patches:
            # Load core patches
            for handler_type in PatchType:
                self.add_manually(handler_type.value(), CORE_PATCHES_BASE_DIR)

    def is_applied(self, name: str):
        if name not in self._loaded_patches:
            raise ValueError(f"The patch '{name}' was not found.")
        return self._loaded_patches[name].is_applied(self._rom, self._config)

    def apply(self, name: str):
        if name not in self._loaded_patches:
            raise ValueError(f"The patch '{name}' was not found.")
        self._loaded_patches[name].apply(
            partial(self._apply_armips, name),
            self._rom, self._config
        )

    def _apply_armips(self, name: str):
        patch = self._config.asm_patches_constants.patches[name]
        patch_dir_for_version = self._config.asm_patches_constants.patch_dir.filepath
        self._arm_patcher.apply(patch, self._config.binaries, os.path.join(self._patch_dirs[name], patch_dir_for_version))

    def add_pkg(self, zip_path: str):
        pass  # todo

    def add_manually(self, handler: AbstractPatchHandler, patch_base_dir: str):
        # Try to find the patch in the config
        if handler.name not in self._config.asm_patches_constants.patches.keys():
            raise ValueError(f"No patch for handler '{handler.name}' found in the configuration.")
        self._loaded_patches[handler.name] = handler
        self._patch_dirs[handler.name] = os.path.realpath(patch_base_dir)
