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

import importlib.util
import os
import shutil
from enum import Enum
from functools import partial
from tempfile import TemporaryDirectory
from typing import Any, Dict, Generator, List, Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError
from zipfile import ZipFile

from ndspy.rom import NintendoDSRom
from pmdsky_debug_py.protocol import SectionProtocol

from skytemple_files.common.i18n_util import _, f
from skytemple_files.common.ppmdu_config.data import (
    Pmd2AsmPatchesConstants,
    Pmd2Data,
    Pmd2PatchParameterType,
)
from skytemple_files.common.ppmdu_config.xml_reader import (
    Pmd2AsmPatchesConstantsXmlReader,
)
from skytemple_files.common.util import get_resources_dir, is_binary_in_rom
from skytemple_files.patch.arm_patcher import ArmPatcher
from skytemple_files.patch.errors import (
    PatchDependencyError,
    PatchNotConfiguredError,
    PatchPackageError,
)
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch
from skytemple_files.patch.handler.actor_and_level_loader import (
    ActorAndLevelListLoaderPatchHandler,
)
from skytemple_files.patch.handler.add_type import AddTypePatchHandler
from skytemple_files.patch.handler.allow_unrecruitable_mons import (
    AllowUnrecruitableMonsPatchHandler,
)
from skytemple_files.patch.handler.anti_softlock import AntiSoftlockPatchHandler
from skytemple_files.patch.handler.appraise_all import AppraiseAllPatchHandler
from skytemple_files.patch.handler.better_enemy_evolution import (
    BetterEnemyEvolutionPatchHandler,
)
from skytemple_files.patch.handler.bold_text import (
    BoldTextPatchHandler,
)
from skytemple_files.patch.handler.change_evo import ChangeEvoSystemPatchHandler
from skytemple_files.patch.handler.change_ff_prop import (
    ChangeFixedFloorPropertiesPatchHandler,
)
from skytemple_files.patch.handler.change_tbbg import ChangeTextBoxColorPatchHandler
from skytemple_files.patch.handler.change_text_sound import (
    ChangeTextSoundPatchHandler,
)
from skytemple_files.patch.handler.choose_starter import ChooseStarterPatchHandler
from skytemple_files.patch.handler.complete_team_control import CompleteTeamControl
from skytemple_files.patch.handler.compress_iq_data import CompressIQDataPatchHandler
from skytemple_files.patch.handler.disable_tips import DisableTipsPatch
from skytemple_files.patch.handler.disarm_one_room_mh import DisarmOneRoomMHPatchHandler
from skytemple_files.patch.handler.dungeon_interrupt import DungeonInterruptPatchHandler
from skytemple_files.patch.handler.dynamic_bosses_everywhere import (
    DynamicBossesEverywherePatchHandler,
)
from skytemple_files.patch.handler.edit_extra_pokemon import (
    EditExtraPokemonPatchHandler,
)
from skytemple_files.patch.handler.exp_share import ExpSharePatchHandler
from skytemple_files.patch.handler.expand_poke_list import ExpandPokeListPatchHandler
from skytemple_files.patch.handler.externalize_mappa import ExternalizeMappaPatchHandler
from skytemple_files.patch.handler.externalize_waza import ExternalizeWazaPatchHandler
from skytemple_files.patch.handler.extra_space import ExtraSpacePatch
from skytemple_files.patch.handler.extract_anims import ExtractAnimDataPatchHandler
from skytemple_files.patch.handler.extract_bar_list import (
    ExtractBarItemListPatchHandler,
)
from skytemple_files.patch.handler.extract_dungeon_data import (
    ExtractDungeonDataPatchHandler,
)
from skytemple_files.patch.handler.extract_item_code import ExtractItemCodePatchHandler
from skytemple_files.patch.handler.extract_item_lists import (
    ExtractItemListsPatchHandler,
)
from skytemple_files.patch.handler.extract_move_code import ExtractMoveCodePatchHandler
from skytemple_files.patch.handler.extract_sp_code import ExtractSPCodePatchHandler
from skytemple_files.patch.handler.fairy_gummies import (
    ImplementFairyGummiesPatchHandler,
)
from skytemple_files.patch.handler.far_off_pal_overdrive import FarOffPalOverdrive
from skytemple_files.patch.handler.fix_evolution import FixEvolutionPatchHandler
from skytemple_files.patch.handler.fix_memory_softlock import (
    FixMemorySoftlockPatchHandler,
)
from skytemple_files.patch.handler.fix_nocash_saves import FixNocashSavesPatchHandler
from skytemple_files.patch.handler.move_growth import MoveGrowthPatchHandler
from skytemple_files.patch.handler.move_shortcuts import MoveShortcutsPatch
from skytemple_files.patch.handler.no_weather_stop import NoWeatherStopPatchHandler
from skytemple_files.patch.handler.obj_table import ExtractObjectTablePatchHandler
from skytemple_files.patch.handler.partners_trigger_hidden_traps import (
    PartnersTriggerHiddenTraps,
)
from skytemple_files.patch.handler.pitfall_trap_tweak import (
    PitfallTrapTweakPatchHandler,
)
from skytemple_files.patch.handler.pkmn_ground_anim import PkmnGroundAnimPatchHandler
from skytemple_files.patch.handler.push_allies import PushAlliesPatchHandler
from skytemple_files.patch.handler.reduce_jumpcut_pause_time import (
    ReduceJumpcutPauseTime,
)
from skytemple_files.patch.handler.same_type_partner import SameTypePartnerPatch
from skytemple_files.patch.handler.skip_quiz import SkipQuizPatchHandler
from skytemple_files.patch.handler.stat_disp import ChangeMoveStatDisplayPatchHandler
from skytemple_files.patch.handler.support_atupx import AtupxSupportPatchHandler
from skytemple_files.patch.handler.unused_dungeon_chance import UnusedDungeonChancePatch

CORE_PATCHES_BASE_DIR = os.path.join(get_resources_dir(), "patches")


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
    APPRAISE_ALL = AppraiseAllPatchHandler
    CHOOSE_STARTER = ChooseStarterPatchHandler
    SKIP_QUIZ = SkipQuizPatchHandler
    PUSH_ALLIES = PushAlliesPatchHandler
    DUNGEON_INTERRUPT = DungeonInterruptPatchHandler
    CHANGE_FF_PROP = ChangeFixedFloorPropertiesPatchHandler
    COMPLETE_TEAM_CONTROL = CompleteTeamControl
    FAR_OFF_PAL_OVERDRIVE = FarOffPalOverdrive
    PARTNERS_TRIGGER_HIDDEN_TRAPS = PartnersTriggerHiddenTraps
    REDUCE_JUMPCUT_PAUSE_TIME = ReduceJumpcutPauseTime
    EXTRA_SPACE = ExtraSpacePatch
    EXTERNALIZE_WAZA = ExternalizeWazaPatchHandler
    EXTRACT_MOVE_CODE = ExtractMoveCodePatchHandler
    EXTRACT_ITEM_CODE = ExtractItemCodePatchHandler
    EXTRACT_SP_CODE = ExtractSPCodePatchHandler
    EXTRACT_OBJECT_TABLE = ExtractObjectTablePatchHandler
    MOVE_GROWTH = MoveGrowthPatchHandler
    CHANGE_TBBG = ChangeTextBoxColorPatchHandler
    EXTRACT_ANIM_DATA = ExtractAnimDataPatchHandler
    STAT_DISP = ChangeMoveStatDisplayPatchHandler
    CHANGE_EVO_SYSTEM = ChangeEvoSystemPatchHandler
    GROUND_ANIM = PkmnGroundAnimPatchHandler
    EXTERNALIZE_MAPPA = ExternalizeMappaPatchHandler
    ADD_TYPES = AddTypePatchHandler
    IMPLEMENT_FAIRY_GUMMIES = ImplementFairyGummiesPatchHandler
    EXTRACT_BAR_LIST = ExtractBarItemListPatchHandler
    EXPAND_POKE_LIST = ExpandPokeListPatchHandler
    ALLOW_UNRECRUITABLE_MONS = AllowUnrecruitableMonsPatchHandler
    EDIT_EXTRA_POKEMON = EditExtraPokemonPatchHandler
    FIX_MEMORY_SOFTLOCK = FixMemorySoftlockPatchHandler
    COMPRESS_IQ_DATA = CompressIQDataPatchHandler
    DISARM_ONE_ROOM_MH = DisarmOneRoomMHPatchHandler
    DYNAMIC_BOSSES_EVERYWHERE = DynamicBossesEverywherePatchHandler
    PITFALL_TRAP_TWEAK = PitfallTrapTweakPatchHandler
    FIX_NOCASH_SAVES = FixNocashSavesPatchHandler
    BOLD_TEXT = BoldTextPatchHandler
    CHANGE_TEXT_SOUND = ChangeTextSoundPatchHandler
    ANTI_SOFTLOCK = AntiSoftlockPatchHandler
    BETTER_ENEMY_EVOLUTION = BetterEnemyEvolutionPatchHandler
    NO_WEATHER_STOP = NoWeatherStopPatchHandler


class Patcher:
    def __init__(
        self, rom: NintendoDSRom, config: Pmd2Data, skip_core_patches: bool = False
    ):
        self._rom = rom
        self._config = config
        self._loaded_patches: Dict[str, AbstractPatchHandler] = {}
        # Path to the directories, which contain the ASM files for the handlers.
        self._patch_dirs: Dict[str, str] = {}

        self._arm_patcher = ArmPatcher(self._rom)
        self._created_tmpdirs: List[TemporaryDirectory[Any]] = []

        if not skip_core_patches:
            # Load core patches
            for handler_type in PatchType:
                self.add_manually(handler_type.value(), CORE_PATCHES_BASE_DIR)

    def __del__(self) -> None:
        for tmpdir in self._created_tmpdirs:
            tmpdir.cleanup()

    def is_applied(self, name: str) -> bool:
        if name not in self._loaded_patches:
            raise ValueError(f(_("The patch '{name}' was not found.")))
        return self._loaded_patches[name].is_applied(self._rom, self._config)

    def apply(self, name: str, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Apply a patch.
        If the patch requires parameters, values for ALL of them must be in the dict `config` (even if default values
        are specified in the XML config).
        """
        if name not in self._loaded_patches:
            raise ValueError(f(_("The patch '{name}' was not found.")))
        patch = self._loaded_patches[name]
        if isinstance(patch, DependantPatch):
            for patch_name in patch.depends_on():
                try:
                    if not self.is_applied(patch_name):
                        raise PatchDependencyError(
                            f(
                                _(
                                    "The patch '{patch_name}' needs to be applied before you can "
                                    "apply '{name}'."
                                )
                            )
                        )
                except ValueError as err:
                    raise PatchDependencyError(
                        f(
                            _(
                                "The patch '{patch_name}' needs to be applied before you can "
                                "apply '{name}'. "
                                "This patch could not be found."
                            )
                        )
                    ) from err
        # Check config
        patch_data = self._config.asm_patches_constants.patches[name]
        if patch_data.has_parameters():
            if config is None:
                raise PatchNotConfiguredError(
                    _("No configuration was given."), "*", "No configuration was given."
                )
            for param in patch_data.parameters.values():
                if param.name not in config:
                    raise PatchNotConfiguredError(
                        _("Missing configuration value."), param.name, "Not given."
                    )
                if param.type == Pmd2PatchParameterType.INTEGER:
                    val = config[param.name]
                    if not isinstance(val, int):
                        raise PatchNotConfiguredError(
                            _("Invalid configuration value."),
                            param.name,
                            "Must be int.",
                        )
                    if param.min is not None and val < param.min:
                        raise PatchNotConfiguredError(
                            _("Invalid configuration value."),
                            param.name,
                            _("Must be >= {}.").format(param.min),
                        )
                    if param.max is not None and val > param.max:
                        raise PatchNotConfiguredError(
                            _("Invalid configuration value."),
                            param.name,
                            _("Must be <= {}.").format(param.max),
                        )
                if param.type == Pmd2PatchParameterType.STRING:
                    val = config[param.name]
                    if not isinstance(val, str):
                        raise PatchNotConfiguredError(
                            _("Invalid configuration value."),
                            param.name,
                            "Must be str.",
                        )
                if param.type == Pmd2PatchParameterType.SELECT:
                    val = config[param.name]
                    found = False
                    for option in param.options:  # type: ignore
                        if (
                            not isinstance(val, type(option.value))
                            or option.value != val
                        ):
                            continue
                        found = True
                        break
                    if not found:
                        raise PatchNotConfiguredError(
                            _("Invalid configuration value."),
                            param.name,
                            "Must be one of the options.",
                        )
            patch.supply_parameters(config)
        patch.apply(partial(self._apply_armips, name, patch), self._rom, self._config)

    def _apply_armips(self, name: str, calling_patch: AbstractPatchHandler) -> None:
        patch = self._config.asm_patches_constants.patches[name]
        patch_dir_for_version = self._config.asm_patches_constants.patch_dir.filepath
        stub_path_for_version = self._config.asm_patches_constants.patch_dir.stubpath
        parameter_values = calling_patch.get_parameters()
        binaries: dict[str, SectionProtocol] = {
            "arm9": self._config.bin_sections.arm9,
            "overlay0": self._config.bin_sections.overlay0,
            "overlay1": self._config.bin_sections.overlay1,
            "overlay2": self._config.bin_sections.overlay2,
            "overlay3": self._config.bin_sections.overlay3,
            "overlay4": self._config.bin_sections.overlay4,
            "overlay5": self._config.bin_sections.overlay5,
            "overlay6": self._config.bin_sections.overlay6,
            "overlay7": self._config.bin_sections.overlay7,
            "overlay8": self._config.bin_sections.overlay8,
            "overlay9": self._config.bin_sections.overlay9,
            "overlay10": self._config.bin_sections.overlay10,
            "overlay11": self._config.bin_sections.overlay11,
            "overlay12": self._config.bin_sections.overlay12,
            "overlay13": self._config.bin_sections.overlay13,
            "overlay14": self._config.bin_sections.overlay14,
            "overlay15": self._config.bin_sections.overlay15,
            "overlay16": self._config.bin_sections.overlay16,
            "overlay17": self._config.bin_sections.overlay17,
            "overlay18": self._config.bin_sections.overlay18,
            "overlay19": self._config.bin_sections.overlay19,
            "overlay20": self._config.bin_sections.overlay20,
            "overlay21": self._config.bin_sections.overlay21,
            "overlay22": self._config.bin_sections.overlay22,
            "overlay23": self._config.bin_sections.overlay23,
            "overlay24": self._config.bin_sections.overlay24,
            "overlay25": self._config.bin_sections.overlay25,
            "overlay26": self._config.bin_sections.overlay26,
            "overlay27": self._config.bin_sections.overlay27,
            "overlay28": self._config.bin_sections.overlay28,
            "overlay29": self._config.bin_sections.overlay29,
            "overlay30": self._config.bin_sections.overlay30,
            "overlay31": self._config.bin_sections.overlay31,
            "overlay32": self._config.bin_sections.overlay32,
            "overlay33": self._config.bin_sections.overlay33,
            "overlay34": self._config.bin_sections.overlay34,
            "overlay35": self._config.bin_sections.overlay35,
        }

        if self._config.extra_bin_sections.overlay36 is not None:
            if (
                is_binary_in_rom(self._rom, self._config.extra_bin_sections.overlay36)
                or name == "ExtraSpace"
            ):
                binaries["overlay36"] = self._config.extra_bin_sections.overlay36

        self._arm_patcher.apply(
            patch,
            binaries,
            os.path.join(self._patch_dirs[name], patch_dir_for_version),
            stub_path_for_version,
            self._config.game_edition,
            parameter_values,
        )

    def add_pkg(self, path: str, is_zipped: bool = True) -> AbstractPatchHandler:
        """Loads a skypatch file. Raises PatchPackageError on error."""
        tmpdir = TemporaryDirectory()
        self._created_tmpdirs.append(tmpdir)
        if is_zipped:
            with ZipFile(path, "r") as zip:
                zip.extractall(tmpdir.name)
                f_id = id(zip)
        else:
            shutil.copytree(
                os.path.join(path, "."),
                os.path.join(tmpdir.name, "."),
                dirs_exist_ok=True,
            )
            f_id = id(tmpdir)

        # Load the configuration
        try:
            config_xml = os.path.join(tmpdir.name, "config.xml")
            PatchPackageConfigMerger(config_xml, self._config.game_edition).merge(
                self._config.asm_patches_constants
            )
        except FileNotFoundError as ex:
            raise PatchPackageError(_("config.xml missing in patch package.")) from ex
        except ParseError as ex:
            raise PatchPackageError(
                _("Syntax error in the config.xml while reading patch package.")
            ) from ex

        # Evalulate the module
        try:
            module_name = f"skytemple_files.__patches.p{f_id}"
            spec = importlib.util.spec_from_file_location(
                module_name, os.path.join(tmpdir.name, "patch.py")
            )
            assert spec is not None
            patch = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(patch)  # type: ignore
        except FileNotFoundError as ex:
            raise PatchPackageError(_("patch.py missing in patch package.")) from ex
        except SyntaxError as ex:
            raise PatchPackageError(
                _("The patch.py of the patch package contains a syntax error.")
            ) from ex

        try:
            handler = patch.PatchHandler()  # type: ignore
        except AttributeError as ex:
            raise PatchPackageError(
                _(
                    "The patch.py of the patch package does not contain a 'PatchHandler'."
                )
            ) from ex

        try:
            self.add_manually(handler, tmpdir.name)
        except ValueError as ex:
            raise PatchPackageError(
                _(
                    "The patch package does not contain an entry for the handler's patch name "
                    "in the config.xml."
                )
            ) from ex
        return handler

    def add_manually(self, handler: AbstractPatchHandler, patch_base_dir: str) -> None:
        # Try to find the patch in the config
        if handler.name not in self._config.asm_patches_constants.patches.keys():
            raise ValueError(
                f(
                    _(
                        "No patch for handler '{handler.name}' found in the configuration."
                    )
                )
            )
        self._loaded_patches[handler.name] = handler
        self._patch_dirs[handler.name] = patch_base_dir

    def list(self) -> Generator[AbstractPatchHandler, None, None]:
        for handler in self._loaded_patches.values():
            yield handler

    def get(self, name: str) -> AbstractPatchHandler:
        return self._loaded_patches[name]


class PatchPackageConfigMerger:
    def __init__(self, xml_file_name: str, game_edition: str):
        self._root = ElementTree.parse(xml_file_name).getroot()
        self._game_edition = game_edition

    def merge(self, into: Pmd2AsmPatchesConstants) -> None:
        for e in self._root:
            if e.tag == "ASMPatchesConstants":
                content_of_xml = Pmd2AsmPatchesConstantsXmlReader(self._game_edition).read(e)  # type: ignore
                into.patches.update(content_of_xml.patches)
                into.loose_bin_files.update(content_of_xml.loose_bin_files)
                return
