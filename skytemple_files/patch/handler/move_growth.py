#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
from typing import Callable, Dict, List, Set

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data, GAME_VERSION_EOS, GAME_REGION_US, GAME_REGION_EU
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch
from skytemple_files.graphics.fonts.graphic_font.handler import GraphicFontHandler
from skytemple_files.data.waza_p.handler import WazaPHandler
from skytemple_files.data.waza_p.model import WazaMoveCategory
from skytemple_files.common.i18n_util import _


SRC_DIR = os.path.join(get_resources_dir(), 'patches', 'asm_patches', 'irdkwia_asm_mods', 'move_growth', 'src')

PATCH_CHECK_ADDR_APPLIED_US = 0x14A74
PATCH_CHECK_ADDR_APPLIED_EU = 0x14B1C
PATCH_CHECK_INSTR_APPLIED = 0xE2841004

MGROW_PATH = "BALANCE/mgrowth.bin"


MGROW_TABLE = [  25,0,0,0,
                 33,1,1,0,
                 40,1,1,0,
                 50,1,1,1,
                 60,1,1,0,
                 70,1,1,1,
                 80,1,1,0,
                 90,1,1,1,
                100,1,1,1,
                110,1,1,0,
                120,1,1,0,
                150,1,1,1,
                200,3,1,0,
                250,1,1,1,
                300,1,1,0,
                400,1,1,1,
                500,1,3,1,
                750,1,1,0,
               1000,1,1,0,
               1500,1,1,1,
               2000,1,1,0,
               2500,1,1,1,
               3000,1,1,0,
               5000,1,1,1,
                  0,5,5,1]

class MoveGrowthPatchHandler(AbstractPatchHandler, DependantPatch):

    @property
    def name(self) -> str:
        return 'MoveGrowth'

    @property
    def description(self) -> str:
        return _('Implements move growth (PoC/Unfinished). \nNeeds ActorAndLevelLoader, ExtractAnimData and ChangeMoveStatsDisplay patches. \nIf MoveShortcuts is applied, must be re-applied after it. \nThe last version of ChangeMoveStatsDisplay must be used with this.\nMay be incompatible if markfont.dat has been modified (except for ChangeMoveStatsDisplay)\nMakes all prior save files incompatible. ')

    @property
    def author(self) -> str:
        return 'irdkwia'

    @property
    def version(self) -> str:
        return '0.0.0'

    def depends_on(self) -> List[str]:
        return ['ActorAndLevelLoader', 'ExtractAnimData', 'ChangeMoveStatsDisplay']

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.NEW_MECHANIC

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_uintle(rom.arm9, PATCH_CHECK_ADDR_APPLIED_US, 4)!=PATCH_CHECK_INSTR_APPLIED
            if config.game_region == GAME_REGION_EU:
                return read_uintle(rom.arm9, PATCH_CHECK_ADDR_APPLIED_EU, 4)!=PATCH_CHECK_INSTR_APPLIED
        raise NotImplementedError()

    def is_applied_ms(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        # Taken from patch handler
        ORIGINAL_BYTESEQ = bytes(b'\x01 \xa0\xe3')
        OFFSET_EU = 0x158F0
        OFFSET_US = 0x1587C
        overlay29 = get_binary_from_rom_ppmdu(rom, config.binaries['overlay/overlay_0029.bin'])
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return overlay29[OFFSET_US:OFFSET_US+4] != ORIGINAL_BYTESEQ
            if config.game_region == GAME_REGION_EU:
                return overlay29[OFFSET_EU:OFFSET_EU+4] != ORIGINAL_BYTESEQ
        raise NotImplementedError()
    def is_applied_dv(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        PATCH_DV_CHECK_ADDR_APPLIED_US = 0x243F0
        PATCH_DV_CHECK_ADDR_APPLIED_EU = 0x24650
        PATCH_DV_CHECK_INSTR_APPLIED = 0xE3A09001
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_uintle(rom.arm9, PATCH_DV_CHECK_ADDR_APPLIED_US, 4)==PATCH_DV_CHECK_INSTR_APPLIED
            if config.game_region == GAME_REGION_EU:
                return read_uintle(rom.arm9, PATCH_DV_CHECK_ADDR_APPLIED_EU, 4)==PATCH_DV_CHECK_INSTR_APPLIED
        raise NotImplementedError()
    
    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        param = self.get_parameters()
        if self.is_applied_ms(rom, config):
            param["MoveShortcuts"] = 1
        else:
            param["MoveShortcuts"] = 0
        
        if self.is_applied_dv(rom, config):
            param["DisplayVal"] = 1
        else:
            param["DisplayVal"] = 0
        
        START_EXT = param["StartGraphicPos"]
        START_LVL = START_EXT+11
        START_SUB = START_LVL+9
        bin_before = rom.getFileByName("FONT/markfont.dat")
        model = GraphicFontHandler.deserialize(bin_before)
        entries = []
        for x in range(model.get_nb_entries()):
            entries.append(model.get_entry(x))
        while len(entries)<max(START_LVL+9, START_SUB+4, START_EXT+11):
            entries.append(None)
        for x in range(START_EXT, START_EXT+11):
            img = Image.open(os.path.join(SRC_DIR, "ext%d.png"%(x-START_EXT)), 'r')
            entries[x] = img
        for x in range(START_LVL, START_LVL+9):
            img = Image.open(os.path.join(SRC_DIR, "lvl%d.png"%(x-START_LVL)), 'r')
            entries[x] = img
        for x in range(START_SUB, START_SUB+4):
            img = Image.open(os.path.join(SRC_DIR, "sub%d.png"%(x-START_SUB)), 'r')
            entries[x] = img
        model.set_entries(entries)
        bin_after = GraphicFontHandler.serialize(model)
        rom.setFileByName("FONT/markfont.dat", bin_after)
        
        if MGROW_PATH not in rom.filenames:
            mgrow_data_stat = bytearray(0x96)
            mgrow_data_dama = bytearray(0x96)
            for x in range(25):
                exp_req = MGROW_TABLE[x*4]
                pwr = MGROW_TABLE[x*4+1]
                pp = MGROW_TABLE[x*4+2]
                acc = MGROW_TABLE[x*4+3]
                write_uintle(mgrow_data_dama, exp_req, x*6, 2)
                write_uintle(mgrow_data_dama, pwr, x*6+2, 2)
                write_uintle(mgrow_data_dama, pp, x*6+4, 1)
                write_uintle(mgrow_data_dama, acc, x*6+5, 1)
            bin_before = rom.getFileByName("BALANCE/waza_p.bin")
            model = WazaPHandler.deserialize(bin_before)
            total = bytearray(0)
            for m in model.moves:
                if m.category!=WazaMoveCategory.STATUS and m.max_upgrade_level==99:
                    total += mgrow_data_dama
                else:
                    total += mgrow_data_stat
            create_file_in_rom(rom, MGROW_PATH, bytes(total))
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    
    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
