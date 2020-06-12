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
from typing import Callable

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.data import Pmd2Data, GAME_VERSION_EOS, GAME_REGION_US, GAME_REGION_EU
from skytemple_files.list.actor.model import LEN_ACTOR_ENTRY
from skytemple_files.patch.list_extractor import ListExtractor
from skytemple_files.patch.handler.abstract import AbstractPatchHandler

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
        return 'Tells the game, to load the actor and level lists from a separate file. ' \
               'Extracts both files on applying the patch.'

    @property
    def author(self) -> str:
        return 'psy_commando'

    @property
    def version(self) -> str:
        return '0.1.0'

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        # TODO: The patch overwrites this region again, atm. Instead we check against the original value there
        pattern = b'PLAYER\x00\x00TALK_SUB\x00\x00\x00\x00NPC_MY'
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                #return rom.arm9[PATCH_STRING_ADDR_ARM9_US:PATCH_STRING_ADDR_ARM9_US + len(PATCH_STRING)] == PATCH_STRING
                return rom.arm9[PATCH_STRING_ADDR_ARM9_US:PATCH_STRING_ADDR_ARM9_US + len(PATCH_STRING)] != pattern
            # TODO: The EU version patch doesn't work at the moment.
            #if config.game_region == GAME_REGION_EU:
            #    return rom.arm9[PATCH_STRING_ADDR_ARM9_EU:PATCH_STRING_ADDR_ARM9_EU + len(PATCH_STRING)] != pattern
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        # First make absolute sure, that we aren't doing it again by accident, this isn't supported.
        if self.is_applied(rom, config):
            raise RuntimeError("This patch can not be re-applied.")

        # Extract the actor list
        if EXTRACT_LOOSE_BIN_SRCDATA__ACTORS not in config.asm_patches_constants.loose_bin_files:
            raise ValueError("The source data specification was not found in the configuration.")
        loose_bin_spec = config.asm_patches_constants.loose_bin_files[EXTRACT_LOOSE_BIN_SRCDATA__ACTORS]
        ListExtractor(rom, config.binaries['arm9.bin'], loose_bin_spec).extract(LEN_ACTOR_ENTRY, [4])

        # Extract the level list
        if EXTRACT_LOOSE_BIN_SRCDATA__LEVELS not in config.asm_patches_constants.loose_bin_files:
            raise ValueError("The source data specification was not found in the configuration.")
        loose_bin_spec = config.asm_patches_constants.loose_bin_files[EXTRACT_LOOSE_BIN_SRCDATA__LEVELS]
        ListExtractor(rom, config.binaries['arm9.bin'], loose_bin_spec).extract(12, [8], write_subheader=False)

        # Apply the patch
        apply()

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
