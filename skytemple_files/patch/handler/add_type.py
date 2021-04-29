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
from typing import Callable, Dict, List, Set

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data, GAME_VERSION_EOS, GAME_REGION_US, GAME_REGION_EU, GAME_REGION_JP
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler
from skytemple_files.data.str.handler import StrHandler
from skytemple_files.patch.asm_tools import AsmFunction
from skytemple_files.common.i18n_util import _

PATCH_CHECK_ADDR_APPLIED_US = 0x2EAA4
PATCH_CHECK_ADDR_APPLIED_EU = 0x2EBD8
PATCH_CHECK_ADDR_APPLIED_JP = 0x2E97C
PATCH_CHECK_INSTR_APPLIED = 0xE3A00024


TYPE_TABLE_US = 0x8C30
TYPE_TABLE_EU = 0x8C48
TYPE_TABLE_JP = 0x8B78

GUMMI_IQ_TABLE_US = 0xA22B0
GUMMI_IQ_TABLE_EU = 0xA2834
GUMMI_IQ_TABLE_JP = 0xA3684

GUMMI_BELLY_TABLE_US = 0xA2538
GUMMI_BELLY_TABLE_EU = 0xA2ABC
GUMMI_BELLY_TABLE_JP = 0xA390C

TABLE_LEN = 648

NEW_TYPES = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 1, 1, 3, 2, 3, 2, 2, 2, 2, 2, 3, 1, 2, 1, 2, 3, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 3, 1, 1, 2, 2, 2, 2, 3, 2, 2, 2, 3, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 1, 3, 1, 2, 2, 2, 1, 3, 1, 2, 1, 3, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 3, 1, 1, 2, 2, 2, 0, 3, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 1, 1, 3, 2, 1, 2, 2, 3, 3, 2, 2, 2, 2, 3, 2, 1, 2, 2, 2, 2, 2, 2, 2,
             2, 3, 2, 2, 2, 2, 3, 2, 1, 2, 1, 1, 1, 3, 0, 2, 3, 3, 1, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 3, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 0, 3, 2, 2, 2, 2, 2, 2,
             2, 2, 3, 2, 1, 3, 2, 2, 3, 2, 0, 2, 1, 3, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 3, 1, 2, 3, 2, 2, 2, 2, 3, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 1, 2, 2, 2, 2, 0, 1, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 1, 2, 3, 2, 2, 1, 1, 2, 1, 3, 2, 2, 1, 2, 3, 1, 1, 2, 2, 2, 2, 2, 2,
             2, 2, 3, 2, 2, 2, 3, 1, 2, 1, 3, 2, 3, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2,
             2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 3, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 1, 0, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 3, 2, 2, 3, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2,
             2, 2, 1, 1, 2, 1, 3, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 1, 3, 2, 2, 2, 2, 2, 2,
             2, 2, 1, 2, 2, 2, 2, 3, 1, 2, 2, 2, 2, 2, 2, 3, 3, 1, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # Leftovers

NEW_IQ_GUMMI = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 5, 3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                0, 3, 5, 4, 2, 3, 2, 3, 3, 4, 3, 3, 2, 4, 3, 3, 3, 2, 2, 0, 0, 0, 0, 0, 0,
                0, 3, 2, 5, 4, 4, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 0, 0, 0, 0, 0, 0,
                0, 3, 4, 2, 5, 2, 4, 3, 4, 2, 4, 3, 4, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                0, 3, 3, 3, 3, 5, 3, 3, 3, 4, 2, 3, 3, 3, 3, 3, 3, 2, 3, 0, 0, 0, 0, 0, 0,
                0, 3, 4, 3, 3, 3, 5, 4, 3, 3, 3, 3, 3, 4, 3, 3, 3, 4, 3, 0, 0, 0, 0, 0, 0,
                0, 3, 3, 3, 3, 3, 3, 5, 3, 3, 4, 4, 2, 2, 3, 3, 2, 3, 4, 0, 0, 0, 0, 0, 0,
                0, 3, 3, 3, 2, 3, 3, 2, 5, 4, 3, 4, 2, 3, 3, 3, 3, 3, 2, 0, 0, 0, 0, 0, 0,
                0, 3, 3, 4, 4, 1, 4, 3, 2, 5, 3, 3, 3, 2, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                0, 3, 3, 3, 2, 4, 4, 2, 3, 1, 5, 3, 2, 4, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                0, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 5, 4, 3, 4, 3, 4, 3, 3, 0, 0, 0, 0, 0, 0,
                0, 3, 4, 3, 2, 3, 3, 2, 3, 2, 4, 3, 5, 4, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                0, 2, 2, 4, 4, 3, 3, 4, 2, 4, 2, 3, 3, 5, 3, 3, 3, 4, 3, 0, 0, 0, 0, 0, 0,
                0, 1, 3, 3, 3, 3, 3, 1, 2, 3, 3, 3, 2, 3, 5, 3, 4, 3, 3, 0, 0, 0, 0, 0, 0,
                0, 3, 2, 2, 2, 2, 4, 3, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3, 4, 0, 0, 0, 0, 0, 0,
                0, 3, 3, 3, 3, 3, 3, 4, 3, 3, 3, 1, 4, 3, 2, 3, 5, 3, 4, 0, 0, 0, 0, 0, 0,
                0, 2, 4, 3, 2, 3, 2, 4, 1, 4, 2, 2, 2, 2, 3, 2, 3, 5, 2, 0, 0, 0, 0, 0, 0,
                0, 3, 3, 3, 3, 3, 3, 2, 4, 3, 3, 3, 2, 3, 3, 1, 2, 4, 5, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

NEW_BELLY_GUMMI = [30 if x==5 else x*5 for x in NEW_IQ_GUMMI]

TYPE_LIST = {"MESSAGE/text_e.str": "Fairy",
             "MESSAGE/text_f.str": "Fée",
             "MESSAGE/text_g.str": "Fee",
             "MESSAGE/text_i.str": "Folletto",
             "MESSAGE/text_s.str": "Hada",
             "MESSAGE/text_j.str": "フェアリー"}

class AddTypePatchHandler(AbstractPatchHandler):

    @property
    def name(self) -> str:
        return 'AddTypes'

    @property
    def description(self) -> str:
        return _('Add types to the type matchup table. This will replace the old matchup table by the 6th+ Gen type table, Fairy type being added to the end.')

    @property
    def author(self) -> str:
        return 'irdkwia'

    @property
    def version(self) -> str:
        return '0.0.1'

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.NEW_MECHANIC

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return read_uintle(rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_US, 4)!=PATCH_CHECK_INSTR_APPLIED
            if config.game_region == GAME_REGION_EU:
                return read_uintle(rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_EU, 4)!=PATCH_CHECK_INSTR_APPLIED
            if config.game_region == GAME_REGION_JP:
                return read_uintle(rom.loadArm9Overlays([29])[29].data, PATCH_CHECK_ADDR_APPLIED_JP, 4)!=PATCH_CHECK_INSTR_APPLIED
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                type_table = TYPE_TABLE_US
                gummi_iq_table = GUMMI_IQ_TABLE_US
                gummi_belly_table = GUMMI_BELLY_TABLE_US
            if config.game_region == GAME_REGION_EU:
                type_table = TYPE_TABLE_EU
                gummi_iq_table = GUMMI_IQ_TABLE_EU
                gummi_belly_table = GUMMI_BELLY_TABLE_EU
            if config.game_region == GAME_REGION_JP:
                type_table = TYPE_TABLE_JP
                gummi_iq_table = GUMMI_IQ_TABLE_JP
                gummi_belly_table = GUMMI_BELLY_TABLE_JP
        
        bincfg = config.binaries['overlay/overlay_0010.bin']
        data = bytearray(get_binary_from_rom_ppmdu(rom, bincfg))
        data[type_table:type_table+TABLE_LEN] = bytearray(NEW_TYPES)
        set_binary_in_rom_ppmdu(rom, bincfg, bytes(data))

        # Change Fairy's type name
        for filename in get_files_from_rom_with_extension(rom, 'str'):
            bin_before = rom.getFileByName(filename)
            strings = StrHandler.deserialize(bin_before)
            block = config.string_index_data.string_blocks['Type Names']
            strings.strings[block.begin+18] = TYPE_LIST[filename]
            bin_after = StrHandler.serialize(strings)
            rom.setFileByName(filename, bin_after)
        
        bincfg = config.binaries['arm9.bin']
        data = bytearray(get_binary_from_rom_ppmdu(rom, bincfg))
        data[gummi_iq_table:gummi_iq_table+TABLE_LEN] = bytearray(NEW_IQ_GUMMI)
        data[gummi_belly_table:gummi_belly_table+TABLE_LEN] = bytearray(NEW_BELLY_GUMMI)
        set_binary_in_rom_ppmdu(rom, bincfg, bytes(data))

        try:
            apply()
        except RuntimeError as ex:
            raise ex

    
    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
