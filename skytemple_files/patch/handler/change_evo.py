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
from typing import Callable, Dict, List, Set

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data, GAME_VERSION_EOS, GAME_REGION_US, GAME_REGION_EU, GAME_REGION_JP
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler
from skytemple_files.patch.asm_tools import AsmFunction
from skytemple_files.common.i18n_util import _
from skytemple_files.data.md.handler import MdHandler
from skytemple_files.data.md.model import EvolutionMethod, AdditionalRequirement, Gender

PATCH_CHECK_ADDR_APPLIED_US = 0x59B24
PATCH_CHECK_ADDR_APPLIED_EU = 0x59EA0
PATCH_CHECK_ADDR_APPLIED_JP = 0x59E20
PATCH_CHECK_INSTR_APPLIED = 0xE1D960F4

MEVO_PATH = "BALANCE/md_evo.bin"
MEVO_ENTRY_LENGTH = 0x20
MEVO_STATS_LENGTH = 0xA

EVO_HP_BONUS_US = 0xA18C4
EVO_HP_BONUS_EU = 0xA1E48
EVO_HP_BONUS_JP = 0xA2C98
EVO_PHYS_BONUS_US = 0xA18D0
EVO_PHYS_BONUS_EU = 0xA1E54
EVO_PHYS_BONUS_JP = 0xA2CA4
EVO_SPEC_BONUS_US = 0xA18E4
EVO_SPEC_BONUS_EU = 0xA1E68
EVO_SPEC_BONUS_JP = 0xA2CB8

MAX_TRY = 1000

SPECIAL_EVOS = {462: [464],
                463: [465],
                1062: [1064],
                1063: [1065],
                1047: [450],
                1048: [451],
                1049: [452],
                447: [453],
                448: [453],
                449: [453],
                393: [394],
                993: [994],
                993: [520],
                454: [],
                1054: [455]}
SPECIAL_EGGS = {379: [379],
                380: [379],
                381: [379],
                382: [379],
                979: [979],
                980: [979],
                981: [979],
                982: [979],
                460: [460],
                461: [460],
                1060: [1060],
                1061: [1060],
                455: [1054],
                464: [462],
                465: [463],
                1064: [1062],
                1065: [1063],
                450: [1047],
                451: [1048],
                452: [1049],
                453: [447,448,449]}
class ChangeEvoSystemPatchHandler(AbstractPatchHandler):

    @property
    def name(self) -> str:
        return 'ChangeEvoSystem'

    @property
    def description(self) -> str:
        return _("""Change the evolution system.
After applying this, every single Pokémon will have two lists for their evolution and children, and different stat bonuses when a Pokémon evolves into them.
This supposedly removes most of the particular cases the game handles for evolutions. """)

    @property
    def author(self) -> str:
        return 'irdkwia'

    @property
    def version(self) -> str:
        return '0.0.1'

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.UTILITY
    
    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_uintle(rom.arm9, PATCH_CHECK_ADDR_APPLIED_US, 4)!=PATCH_CHECK_INSTR_APPLIED
            if config.game_region == GAME_REGION_EU:
                return read_uintle(rom.arm9, PATCH_CHECK_ADDR_APPLIED_EU, 4)!=PATCH_CHECK_INSTR_APPLIED
            if config.game_region == GAME_REGION_JP:
                return read_uintle(rom.arm9, PATCH_CHECK_ADDR_APPLIED_JP, 4)!=PATCH_CHECK_INSTR_APPLIED
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        if not self.is_applied(rom, config):
            if config.game_version == GAME_VERSION_EOS:
                if config.game_region == GAME_REGION_US:
                    evo_hp_bonus = EVO_HP_BONUS_US
                    evo_ph_bonus = EVO_PHYS_BONUS_US
                    evo_sp_bonus = EVO_SPEC_BONUS_US
                if config.game_region == GAME_REGION_EU:
                    evo_hp_bonus = EVO_HP_BONUS_EU
                    evo_ph_bonus = EVO_PHYS_BONUS_EU
                    evo_sp_bonus = EVO_SPEC_BONUS_EU
                if config.game_region == GAME_REGION_JP:
                    evo_hp_bonus = EVO_HP_BONUS_JP
                    evo_ph_bonus = EVO_PHYS_BONUS_JP
                    evo_sp_bonus = EVO_SPEC_BONUS_JP
            # Create Evo Table
            md_bin = rom.getFileByName('BALANCE/monster.md')
            md_model = MdHandler.deserialize(md_bin)


            mevo_data = bytearray(len(md_model)*MEVO_ENTRY_LENGTH+4)
            write_uintle(mevo_data, len(mevo_data), 0, 4)
            for i in range(len(md_model)):
                if i in SPECIAL_EVOS:
                    next_stage = SPECIAL_EVOS[i]
                else:
                    next_stage = []
                    for j,x in enumerate(md_model):
                        if (i<600 and 1<=j<555) or (i>=600 and 601<=j<1155):
                            if x.pre_evo_index==i and x.evo_method!=EvolutionMethod.NONE and (x.evo_param2!=AdditionalRequirement.MALE or i<600) and (x.evo_param2!=AdditionalRequirement.FEMALE or i>=600):
                                next_stage.append(j)
                write_uintle(mevo_data, len(next_stage), i*MEVO_ENTRY_LENGTH+4, 2)
                for j,x in enumerate(next_stage):
                    write_uintle(mevo_data, x, i*MEVO_ENTRY_LENGTH+j*2+6, 2)
                if i in SPECIAL_EGGS:
                    next_stage = SPECIAL_EGGS[i]
                else:
                    next_stage = []
                    pre_evo = i
                    tries = 0
                    while md_model[pre_evo].pre_evo_index!=0:
                        current = md_model[pre_evo]
                        pre_evo = current.pre_evo_index
                        if current.evo_param2==AdditionalRequirement.MALE and md_model[pre_evo%600].gender==Gender.MALE and md_model[pre_evo%600+600].gender==Gender.FEMALE:
                            pre_evo = pre_evo%600
                        elif current.evo_param2==AdditionalRequirement.FEMALE and md_model[pre_evo%600].gender==Gender.MALE and md_model[pre_evo%600+600].gender==Gender.FEMALE:
                            pre_evo = pre_evo%600+600
                        tries += 1
                        if tries>=MAX_TRY:
                            raise Exception(_("Infinite recursion detected in pre evolutions for md entry {i}. "))
                    next_stage.append(pre_evo)
                if next_stage!=[i]:
                    write_uintle(mevo_data, len(next_stage), i*MEVO_ENTRY_LENGTH+0x16, 2)
                    for j,x in enumerate(next_stage):
                        write_uintle(mevo_data, x, i*MEVO_ENTRY_LENGTH+j*2+0x18, 2)
            
            hp_bonus = read_uintle(rom.arm9, evo_hp_bonus, 4)
            atk_bonus = read_uintle(rom.arm9, evo_ph_bonus, 2)
            def_bonus = read_uintle(rom.arm9, evo_ph_bonus+2, 2)
            spatk_bonus = read_uintle(rom.arm9, evo_sp_bonus, 2)
            spdef_bonus = read_uintle(rom.arm9, evo_sp_bonus+2, 2)
            evo_add_stats = bytearray(MEVO_STATS_LENGTH)
            write_uintle(evo_add_stats, hp_bonus, 0, 2)
            write_uintle(evo_add_stats, atk_bonus, 2, 2)
            write_uintle(evo_add_stats, spatk_bonus, 4, 2)
            write_uintle(evo_add_stats, def_bonus, 6, 2)
            write_uintle(evo_add_stats, spdef_bonus, 8, 2)
            mevo_data += evo_add_stats*len(md_model)
            if MEVO_PATH not in rom.filenames:
                create_file_in_rom(rom, MEVO_PATH, mevo_data)
            else:
                rom.setFileByName(MEVO_PATH, mevo_data)
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    
    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
