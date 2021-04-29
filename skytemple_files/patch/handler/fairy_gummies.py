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
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch
from skytemple_files.patch.asm_tools import AsmFunction
from skytemple_files.common.i18n_util import _
from skytemple_files.data.item_p.handler import ItemPHandler
from skytemple_files.data.data_st.handler import DataSTHandler
from skytemple_files.data.data_cd.handler import DataCDHandler
from skytemple_files.data.str.handler import StrHandler

PATCH_CHECK_ADDR_APPLIED_US = 0xCBF8
PATCH_CHECK_ADDR_APPLIED_EU = 0xCC80
PATCH_CHECK_ADDR_APPLIED_JP = 0xCBF8
PATCH_CHECK_INSTR_APPLIED = 0xB3A00000

# Too lazy to put that in an actual file
ITEM_EFFECT_US = b'\x08\x00\xa0\xe1\x010\xa0\xe3\x07\x10\xa0\xe1\x12 \xa0\xe3\x96\x04\x00\xeb*\x03\x00\xea'
ITEM_EFFECT_EU = b'\x08\x00\xa0\xe1\x010\xa0\xe3\x07\x10\xa0\xe1\x12 \xa0\xe3\x98\x04\x00\xeb*\x03\x00\xea'
ITEM_EFFECT_JP = None #TODO

GUMMI_ITEM_ID = 138
OTHER_GUMMI_ID = 136

# TODO; support other languages
NAME_LIST = {"MESSAGE/text_e.str": "Fairy Gummi",
             "MESSAGE/text_f.str": "Gelée Féerique",
             "MESSAGE/text_g.str": "Feegummi",
             "MESSAGE/text_i.str": "Gommafolletto",
             "MESSAGE/text_s.str": "Gomi Hada",
             "MESSAGE/text_j.str": "---"}

# TODO; support other languages
SDES_LIST = {"MESSAGE/text_e.str": "Raises IQ.",
             "MESSAGE/text_f.str": "Augmente le Q.I.",
             "MESSAGE/text_g.str": "Erhöht den IQ.",
             "MESSAGE/text_i.str": "Aumenta il QI.",
             "MESSAGE/text_s.str": "Sube el CI.",
             "MESSAGE/text_j.str": "---"}

# TODO; support other languages
LDES_LIST = {"MESSAGE/text_e.str": """A food item that permanently
raises the [CS:E]IQ[CR] of a team member.
Fairy-type Pokémon like it most.
It also somewhat fills the Pokémon's
[CS:E]Belly[CR].""",
             "MESSAGE/text_f.str": """Aliment augmentant de façon
permanente le [CS:E]Q.I.[CR] du Pokémon
qui le mange. Plaît particulièrement
aux Pokémon de type Fée.
Remplit un peu l'[CS:E]Estomac[CR]
du Pokémon.""",
             "MESSAGE/text_g.str": """Nahrungsmittel, das den [CS:E]IQ[CR] eines
Team-Mitglieds dauerhaft erhöht.
Fee-Pokémon mögen es besonders.
Füllt den [CS:E]Magen[CR] des
Pokémon ein wenig.""",
             "MESSAGE/text_i.str": """Un cibo che riempie un po' la [CS:E]pancia[CR] e fa
crescere permanentemente il [CS:E]QI[CR] di un
membro della squadra. È la preferita
dei Pokémon di tipo Folletto.""",
             "MESSAGE/text_s.str": """Alimento que eleva de manera
permanente el [CS:E]CI[CR] del Pokémon.
Los de tipo Hada las adoran.
También llena ligeramente su
[CS:E]Tripa[CR].""",
             "MESSAGE/text_j.str": "---"}
class ImplementFairyGummiesPatchHandler(AbstractPatchHandler, DependantPatch):

    @property
    def name(self) -> str:
        return 'ImplementFairyGummies'

    @property
    def description(self) -> str:
        return _("""Implements Fairy-type specialized gummies. Uses unused item 138.
Needs ExtractItemCode, ExtractBarItemList and AddTypes patches to be applied for this patch to work.
Also, you'll need to reapply this if you apply AddTypes again. """)

    @property
    def author(self) -> str:
        return 'irdkwia'

    @property
    def version(self) -> str:
        return '0.0.1'
    
    def depends_on(self) -> List[str]:
        return ['ExtractItemCode', 'ExtractBarItemList', 'AddTypes']

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.NEW_MECHANIC
    
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
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                item_effect = ITEM_EFFECT_US
            if config.game_region == GAME_REGION_EU:
                item_effect = ITEM_EFFECT_EU
            if config.game_region == GAME_REGION_JP:
                item_effect = ITEM_EFFECT_JP

        # Apply Gummi item properties
        item_p_bin = rom.getFileByName('BALANCE/item_p.bin')
        item_p_model = ItemPHandler.deserialize(item_p_bin)
        gummi = item_p_model.item_list[GUMMI_ITEM_ID]
        gummi.buy_price = 800
        gummi.sell_price = 50
        gummi.category = 3
        gummi.sprite = 17
        gummi.item_id = GUMMI_ITEM_ID
        gummi.move_id = 0
        gummi.range_min = 0
        gummi.range_max = 0
        gummi.palette = 14
        gummi.action_name = 4
        gummi.is_valid = True
        gummi.is_in_td = False
        gummi.ai_flag_1 = False
        gummi.ai_flag_2 = True
        gummi.ai_flag_3 = False
        rom.setFileByName('BALANCE/item_p.bin', ItemPHandler.serialize(item_p_model))
        
        # Apply Gummi item dungeon effect
        item_cd_bin = rom.getFileByName('BALANCE/item_cd.bin')
        item_cd_model = DataCDHandler.deserialize(item_cd_bin)
        effect_id = item_cd_model.nb_effects()
        item_cd_model.add_effect_code(item_effect)
        item_cd_model.set_item_effect_id(GUMMI_ITEM_ID, effect_id)
        rom.setFileByName('BALANCE/item_cd.bin', DataCDHandler.serialize(item_cd_model))
        
        # Change item's text attributes
        for filename in get_files_from_rom_with_extension(rom, 'str'):
            bin_before = rom.getFileByName(filename)
            strings = StrHandler.deserialize(bin_before)
            block = config.string_index_data.string_blocks['Item Names']
            strings.strings[block.begin+GUMMI_ITEM_ID] = NAME_LIST[filename]
            block = config.string_index_data.string_blocks['Item Short Descriptions']
            strings.strings[block.begin+GUMMI_ITEM_ID] = SDES_LIST[filename]
            block = config.string_index_data.string_blocks['Item Long Descriptions']
            strings.strings[block.begin+GUMMI_ITEM_ID] = LDES_LIST[filename]
            bin_after = StrHandler.serialize(strings)
            rom.setFileByName(filename, bin_after)
        
        bar_bin = rom.getFileByName('BALANCE/itembar.bin')
        bar_model = DataSTHandler.deserialize(bar_bin)
        gummi_id = bar_model.get_item_struct_id(OTHER_GUMMI_ID)
        bar_model.set_item_struct_id(GUMMI_ITEM_ID, gummi_id)
        rom.setFileByName('BALANCE/itembar.bin', DataSTHandler.serialize(bar_model))

        try:
            apply()
        except RuntimeError as ex:
            raise ex

    
    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
