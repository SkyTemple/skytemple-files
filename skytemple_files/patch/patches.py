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
import os
from enum import Enum
from functools import partial
from tempfile import TemporaryDirectory
from typing import Type, Dict, List, Generator
from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError
from zipfile import ZipFile
import importlib.util

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.data import Pmd2Data, Pmd2AsmPatchesConstants
from skytemple_files.common.ppmdu_config.xml_reader import Pmd2AsmPatchesConstantsXmlReader
from skytemple_files.common.util import get_resources_dir
from skytemple_files.patch.arm_patcher import ArmPatcher
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch
from skytemple_files.patch.handler.actor_and_level_loader import ActorAndLevelListLoaderPatchHandler
from skytemple_files.patch.handler.disable_tips import DisableTipsPatch
from skytemple_files.patch.handler.extra_space import ExtraSpacePatch
from skytemple_files.patch.handler.move_shortcuts import MoveShortcutsPatch
from skytemple_files.patch.handler.same_type_partner import SameTypePartnerPatch
from skytemple_files.patch.handler.unused_dungeon_chance import UnusedDungeonChancePatch
from skytemple_files.patch.handler.support_atupx import AtupxSupportPatchHandler
from skytemple_files.patch.handler.extract_item_lists import ExtractItemListsPatchHandler
from skytemple_files.patch.handler.extract_dungeon_data import ExtractDungeonDataPatchHandler
from skytemple_files.patch.handler.fix_evolution import FixEvolutionPatchHandler
from skytemple_files.patch.handler.add_type import AddTypePatchHandler
from skytemple_files.patch.handler.fairy_gummies import ImplementFairyGummiesPatchHandler
from skytemple_files.patch.handler.extract_bar_list import ExtractBarItemListPatchHandler
from skytemple_files.patch.handler.exp_share import ExpSharePatchHandler
from skytemple_files.patch.handler.choose_starter import ChooseStarterPatchHandler
from skytemple_files.patch.handler.skip_quiz import SkipQuizPatchHandler
from skytemple_files.patch.handler.complete_team_control import CompleteTeamControl
from skytemple_files.patch.handler.far_off_pal_overdrive import FarOffPalOverdrive
from skytemple_files.patch.handler.partners_trigger_hidden_traps import PartnersTriggerHiddenTraps
from skytemple_files.patch.handler.reduce_jumpcut_pause_time import ReduceJumpcutPauseTime
from skytemple_files.patch.handler.extract_move_code import ExtractMoveCodePatchHandler
from skytemple_files.patch.handler.extract_item_code import ExtractItemCodePatchHandler
from skytemple_files.patch.handler.extract_sp_code import ExtractSPCodePatchHandler
from skytemple_files.common.i18n_util import f, _

CORE_PATCHES_BASE_DIR = os.path.join(get_resources_dir(), 'patches')


class PatchType(Enum):
    ACTOR_AND_LEVEL_LIST_LOADER = ActorAndLevelListLoaderPatchHandler
    UNUSED_DUNGEON_CHANCE_PATCH = UnusedDungeonChancePatch
    MOVE_SHORTCUTS = MoveShortcutsPatch
    DISABLE_TIPS = DisableTipsPatch
    SAME_TYPE_PARTNER = SameTypePartnerPatch
    SUPPORT_ATUPX = AtupxSupportPatchHandler
    EXTRACT_ITEM_LISTS = ExtractItemListsPatchHandler
    EXTRACT_DUNGEON_DATA = ExtractDungeonDataPatchHandler
    FIX_EVOLUTION = FixEvolutionPatchHandler
    EXP_SHARE = ExpSharePatchHandler
    CHOOSE_STARTER = ChooseStarterPatchHandler
    SKIP_QUIZ = SkipQuizPatchHandler
    COMPLETE_TEAM_CONTROL = CompleteTeamControl
    FAR_OFF_PAL_OVERDRIVE = FarOffPalOverdrive
    PARTNERS_TRIGGER_HIDDEN_TRAPS = PartnersTriggerHiddenTraps
    REDUCE_JUMPCUT_PAUSE_TIME = ReduceJumpcutPauseTime
    EXTRA_SPACE = ExtraSpacePatch
    EXTRACT_MOVE_CODE = ExtractMoveCodePatchHandler
    EXTRACT_ITEM_CODE = ExtractItemCodePatchHandler
    #EXTRACT_SP_CODE = ExtractSPCodePatchHandler
    ADD_TYPES = AddTypePatchHandler
    IMPLEMENT_FAIRY_GUMMIES = ImplementFairyGummiesPatchHandler
    EXTRACT_BAR_LIST = ExtractBarItemListPatchHandler


class PatchPackageError(RuntimeError):
    pass


class PatchDependencyError(RuntimeError):
    pass


class Patcher:
    def __init__(self, rom: NintendoDSRom, config: Pmd2Data, skip_core_patches=False):
        self._rom = rom
        self._config = config
        self._loaded_patches: Dict[str, AbstractPatchHandler] = {}
        # Path to the directories, which contain the ASM files for the handlers.
        self._patch_dirs: Dict[str, str] = {}

        self._arm_patcher = ArmPatcher(self._rom)
        self._created_tmpdirs: List[TemporaryDirectory] = []

        if not skip_core_patches:
            # Load core patches
            for handler_type in PatchType:
                self.add_manually(handler_type.value(), CORE_PATCHES_BASE_DIR)

    def __del__(self):
        for tmpdir in self._created_tmpdirs:
            tmpdir.cleanup()

    def is_applied(self, name: str):
        if name not in self._loaded_patches:
            raise ValueError(f(_("The patch '{name}' was not found.")))
        return self._loaded_patches[name].is_applied(self._rom, self._config)

    def apply(self, name: str):
        if name not in self._loaded_patches:
            raise ValueError(f(_("The patch '{name}' was not found.")))
        patch = self._loaded_patches[name]
        if isinstance(patch, DependantPatch):
            for patch_name in patch.depends_on():
                try:
                    if not self.is_applied(patch_name):
                        raise PatchDependencyError(f(_("The patch '{patch_name}' needs to be applied before you can "
                                                       "apply '{name}'.")))
                except ValueError as err:
                    raise PatchDependencyError(f(_("The patch '{patch_name}' needs to be applied before you can "
                                                   "apply '{name}'. "
                                                   "This patch could not be found."))) from err
        patch.apply(
            partial(self._apply_armips, name),
            self._rom, self._config
        )

    def _apply_armips(self, name: str):
        patch = self._config.asm_patches_constants.patches[name]
        patch_dir_for_version = self._config.asm_patches_constants.patch_dir.filepath
        stub_path_for_version = self._config.asm_patches_constants.patch_dir.stubpath
        self._arm_patcher.apply(patch, self._config.binaries,
                                os.path.join(self._patch_dirs[name], patch_dir_for_version),
                                stub_path_for_version, self._config.game_edition)

    def add_pkg(self, zip_path: str):
        """Loads a skypatch file. Raises PatchPackageError on error."""
        tmpdir = TemporaryDirectory()
        self._created_tmpdirs.append(tmpdir)
        with ZipFile(zip_path, 'r') as zip:
            zip.extractall(tmpdir.name)
            zip_id = id(zip)

        # Load the configuration
        try:
            config_xml = os.path.join(tmpdir.name, 'config.xml')
            PatchPackageConfigMerger(config_xml, self._config.game_edition).merge(self._config.asm_patches_constants)
        except FileNotFoundError as ex:
            raise PatchPackageError(_("config.xml missing in patch package.")) from ex
        except ParseError as ex:
            raise PatchPackageError(_("Syntax error in the config.xml while reading patch package.")) from ex

        # Evalulate the module
        try:
            module_name = f"skytemple_files.__patches.p{zip_id}"
            spec = importlib.util.spec_from_file_location(module_name,
                                                          os.path.join(tmpdir.name, 'patch.py'))
            patch = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(patch)
        except FileNotFoundError as ex:
            raise PatchPackageError(_("patch.py missing in patch package.")) from ex
        except SyntaxError as ex:
            raise PatchPackageError(_("The patch.py of the patch package contains a syntax error.")) from ex

        try:
            handler = patch.PatchHandler()
        except AttributeError as ex:
            raise PatchPackageError(_("The patch.py of the patch package does not contain a 'PatchHandler'.")) from ex

        try:
            self.add_manually(handler, tmpdir.name)
        except ValueError as ex:
            raise PatchPackageError(_("The patch package does not contain an entry for the handler's patch name "
                                      "in the config.xml.")) from ex

    def add_manually(self, handler: AbstractPatchHandler, patch_base_dir: str):
        # Try to find the patch in the config
        if handler.name not in self._config.asm_patches_constants.patches.keys():
            raise ValueError(f(_("No patch for handler '{handler.name}' found in the configuration.")))
        self._loaded_patches[handler.name] = handler
        self._patch_dirs[handler.name] = patch_base_dir

    def list(self) -> Generator[AbstractPatchHandler, None, None]:
        for handler in self._loaded_patches.values():
            yield handler

    def get(self, name) -> AbstractPatchHandler:
        return self._loaded_patches[name]


class PatchPackageConfigMerger:
    def __init__(self, xml_file_name: str, game_edition: str):
        self._root = ElementTree.parse(xml_file_name).getroot()
        self._game_edition = game_edition

    def merge(self, into: Pmd2AsmPatchesConstants):
        for e in self._root:
            if e.tag == 'ASMPatchesConstants':
                content_of_xml = Pmd2AsmPatchesConstantsXmlReader(self._game_edition).read(e)
                into.patches.update(content_of_xml.patches)
                into.loose_bin_files.update(content_of_xml.loose_bin_files)
                return
