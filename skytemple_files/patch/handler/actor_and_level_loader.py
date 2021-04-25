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
from typing import Callable

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.data import Pmd2Data, GAME_VERSION_EOS, GAME_REGION_US, GAME_REGION_EU
from skytemple_files.list.actor.model import LEN_ACTOR_ENTRY
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.list_extractor import ListExtractor
from skytemple_files.patch.handler.abstract import AbstractPatchHandler
from skytemple_files.common.i18n_util import f, _

EXTRACT_LOOSE_BIN_SRCDATA__ACTORS = 'Entities'
EXTRACT_LOOSE_BIN_SRCDATA__LEVELS = 'Events'
PATCH_STRING = b'PATCH PPMD ActorLoader 0.1'
PATCH_STRING_ADDR_ARM9_US = 0xA6910
PATCH_STRING_ADDR_ARM9_EU = 0xA71B0


class ActorAndLevelListLoaderPatchHandler(AbstractPatchHandler):

    @property
    def name(self) -> str:
        return 'ActorAndLevelLoader'

    @property
    def description(self) -> str:
        return _('Tells the game, to load the actor and level lists from a separate file. '
                 'Extracts both files on applying the patch.')

    @property
    def author(self) -> str:
        return 'psy_commando'

    @property
    def version(self) -> str:
        return '0.1.0'

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.UTILITY

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                # TODO: The patch overwrites this region again, atm. Instead we check against the original value there
                #return rom.arm9[PATCH_STRING_ADDR_ARM9_US:PATCH_STRING_ADDR_ARM9_US + len(PATCH_STRING)] == PATCH_STRING
                return rom.arm9[PATCH_STRING_ADDR_ARM9_US:PATCH_STRING_ADDR_ARM9_US + len(PATCH_STRING)] != b'PLAYER\x00\x00TALK_SUB\x00\x00\x00\x00NPC_MY'
            
            if config.game_region == GAME_REGION_EU:
                # TODO: The patch overwrites this region again, atm. Instead we check against the original value there
                #return rom.arm9[PATCH_STRING_ADDR_ARM9_EU:PATCH_STRING_ADDR_ARM9_EU + len(PATCH_STRING)] == PATCH_STRING
                return rom.arm9[PATCH_STRING_ADDR_ARM9_EU:PATCH_STRING_ADDR_ARM9_EU + len(PATCH_STRING)] != b'PLAYER\x00\x00TALK_SUB\x00\x00\x00\x00NPC_MY'
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        # First make absolute sure, that we aren't doing it again by accident, this isn't supported.
        if self.is_applied(rom, config):
            raise RuntimeError(_("This patch can not be re-applied."))

        extracted_a_list = False

        # Extract the actor list
        if EXTRACT_LOOSE_BIN_SRCDATA__ACTORS not in config.asm_patches_constants.loose_bin_files:
            raise ValueError(_("The source data specification was not found in the configuration."))
        loose_bin_spec = config.asm_patches_constants.loose_bin_files[EXTRACT_LOOSE_BIN_SRCDATA__ACTORS]
        if loose_bin_spec.filepath not in rom.filenames:
            ListExtractor(rom, config.binaries['arm9.bin'], loose_bin_spec).extract(LEN_ACTOR_ENTRY, [4])
            extracted_a_list = True

        # Extract the level list
        if EXTRACT_LOOSE_BIN_SRCDATA__LEVELS not in config.asm_patches_constants.loose_bin_files:
            raise ValueError(_("The source data specification was not found in the configuration."))
        loose_bin_spec = config.asm_patches_constants.loose_bin_files[EXTRACT_LOOSE_BIN_SRCDATA__LEVELS]
        if loose_bin_spec.filepath not in rom.filenames:
            ListExtractor(rom, config.binaries['arm9.bin'], loose_bin_spec).extract(12, [8], write_subheader=False)
            extracted_a_list = True

        # Apply the patch
        try:
            apply()
        except RuntimeError as ex:
            if extracted_a_list:
                raise RuntimeError(str(ex) + _("\n\nThe list was extracted anyway.\n"
                                               "You can already edit it through SkyTemple, but it won't be "
                                               "used in game, until you successfully apply the patch.")) from ex
            raise ex

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
