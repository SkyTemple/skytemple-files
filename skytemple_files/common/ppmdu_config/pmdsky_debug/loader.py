"""
This module constructs Pmd2Binary lists from the pmdsky-debug repository.

It is not as advanced as resymgen and does way less error checking. We assume
pmdsky-debug has good data.  Check with resymgen if you are unsure.
"""
#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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
import re
import warnings
from dataclasses import dataclass, field
from glob import glob
from typing import List, Dict, Optional

import yaml

from skytemple_files.common.ppmdu_config.data import Pmd2GameEdition, GAME_VERSION_EOS
from skytemple_files.common.ppmdu_config.pmdsky_debug.data import Pmd2Binary, Pmd2BinarySymbol, Pmd2BinarySymbolType
from skytemple_files.common.util import get_resources_dir, open_utf8

SYMBOLS_DIR = os.path.join(get_resources_dir(), 'pmdsky-debug', 'symbols')
OVERLAY_REGEX = re.compile(r"overlay(\d+)")
# Aliase for backwards compatibility:
ALIAS_MAP = {
    "DEBUG_SPECIAL_EPISODE_NUMBER": ["DEBUG_SPECIAL_EPISODE_TYPE"],
    "DUNGEON_DATA_LIST": ["DUNGEON_LIST"],
    "GUEST_MONSTER_DATA": ["GUEST_POKEMON_DATA"],
    "GUEST_MONSTER_DATA2": ["GUEST_POKEMON_DATA2"],
    "SCRIPT_VARS_VALUES": ["GAME_VARS_VALUES"],
    "GUMMI_BELLY_RESTORE_TABLE": ["GUMMI_BELLY_HEAL"],
    "IQ_GUMMI_GAIN_TABLE": ["IQ_GUMMI_GAIN"],
    "IQ_GROUP_SKILLS": ["IQ_GROUPS_SKILLS"],
    "COMPRESSED_IQ_GROUP_SKILLS": ["COMPRESSED_IQ_GROUPS_SKILLS"],
    "MEMORY_ALLOCATION_TABLE": ["MEMORY_ALLOC_TABLE"],
    "SECONDARY_TERRAIN_TYPES": ["SECONDARY_TERRAINS"],
    "TACTICS_UNLOCK_LEVEL_TABLE": ["TACTICS_UNLOCK_LEVEL"],
    "TEXT_SPEED": ["TEXT_SPEED_CONSTANT"],
    "MAIN_DEBUG_MENU_1": ["MAIN_DEBUG_MENU1"],
    "MAIN_DEBUG_MENU_2": ["MAIN_DEBUG_MENU2"],
    "SUBMENU": ["SUB_MENU"],
    "BAD_POISON_DAMAGE_COOLDOWN": ["BAD_POISON_DAMAGE_DELAY"],
    "POISON_DAMAGE_COOLDOWN": ["POISON_DAMAGE_DELAY"],
    "BURN_DAMAGE_COOLDOWN": ["BURN_DAMAGE_DELAY"],
    "FIXED_ROOM_PROPERTIES_TABLE": ["FIXED_FLOOR_PROPERTIES"],
    "INTIMIDATOR_ACTIVATION_CHANCE": ["INTIMIDATOR_CHANCE"],
    "GINSENG_CHANCE_3": ["GINSENG_CHANCE3"],
    "FIXED_ROOM_MONSTER_SPAWN_STATS_TABLE": ["MONSTER_SPAWN_STATS_TABLE"],
    "MUSIC_ID_TABLE": ["MUSIC_LIST"],
    "RANDOM_MUSIC_ID_TABLE": ["RANDOM_MUSIC_LIST"],
    "SPAWN_COOLDOWN": ["SPAWN_DELAY_NORMAL"],
    "SPAWN_COOLDOWN_THIEF_ALERT": ["SPAWN_DELAY_STEALING"],
    "GROUND_STATE_PTRS": ["GROUND_STATE_PNTRS"],
    "UNKNOWN_MENU_1": ["UNKNOWN_MENU1"],
    "EVO_SUBMENU": ["EVO_SUB_MENU"],
    "ASSEMBLY_MAIN_MENU_1": ["ASSEMBLY_MAIN_MENU1"],
    "ASSEMBLY_MAIN_MENU_2": ["ASSEMBLY_MAIN_MENU2"],
    "ASSEMBLY_SUBMENU_1": ["ASSEMBLY_SUB_MENU1"],
    "ASSEMBLY_SUBMENU_2": ["ASSEMBLY_SUB_MENU2"],
    "ASSEMBLY_SUBMENU_3": ["ASSEMBLY_SUB_MENU3"],
    "ASSEMBLY_SUBMENU_4": ["ASSEMBLY_SUB_MENU4"],
    "ASSEMBLY_SUBMENU_5": ["ASSEMBLY_SUB_MENU5"],
    "ASSEMBLY_SUBMENU_6": ["ASSEMBLY_SUB_MENU6"],
    "ASSEMBLY_SUBMENU_7": ["ASSEMBLY_SUB_MENU7"],
    "MOVES_MAIN_MENU_1": ["MOVES_MAIN_MENU1"],
    "MOVES_MAIN_MENU_2": ["MOVES_MAIN_MENU2"],
    "MOVES_SUBMENU_1": ["MOVES_SUB_MENU1"],
    "MOVES_SUBMENU_2": ["MOVES_SUB_MENU2"],
    "MOVES_SUBMENU_3": ["MOVES_SUB_MENU3"],
    "MOVES_SUBMENU_4": ["MOVES_SUB_MENU4"],
    "MOVES_SUBMENU_5": ["MOVES_SUB_MENU5"],
    "MOVES_SUBMENU_6": ["MOVES_SUB_MENU6"],
    "MOVES_SUBMENU_7": ["MOVES_SUB_MENU7"],
    "BAR_MENU_CONFIRM_1": ["BAR_MENU_CONFIRM1"],
    "BAR_MENU_CONFIRM_2": ["BAR_MENU_CONFIRM2"],
    "BAR_SUBMENU_1": ["BAR_SUB_MENU1"],
    "BAR_SUBMENU_2": ["BAR_SUB_MENU2"],
    "RECYCLE_MENU_CONFIRM_1": ["RECYCLE_MENU_CONFIRM1"],
    "RECYCLE_MENU_CONFIRM_2": ["RECYCLE_MENU_CONFIRM2"],
    "RECYCLE_SUBMENU_1": ["RECYCLE_SUB_MENU1"],
    "RECYCLE_SUBMENU_2": ["RECYCLE_SUB_MENU2"],
    "RECYCLE_MAIN_MENU_1": ["RECYCLE_MAIN_MENU1"],
    "RECYCLE_MAIN_MENU_2": ["RECYCLE_MAIN_MENU2"],
    "RECYCLE_MAIN_MENU_3": ["RECYCLE_MAIN_MENU3"],
    "SWAP_SHOP_MAIN_MENU_1": ["SYNTHESIS_MAIN_MENU1"],
    "SWAP_SHOP_MAIN_MENU_2": ["SYNTHESIS_MAIN_MENU2"],
    "SWAP_SHOP_SUBMENU_1": ["SYNTHESIS_SUB_MENU1"],
    "SWAP_SHOP_SUBMENU_2": ["SYNTHESIS_SUB_MENU2"],
    "SWAP_SHOP_SUBMENU_3": ["SYNTHESIS_SUB_MENU3"],
    "SWAP_SHOP_MENU_CONFIRM": ["SYNTHESIS_MENU_CONFIRM"],
    "SHOP_MAIN_MENU_1": ["SHOP_MAIN_MENU1"],
    "SHOP_MAIN_MENU_2": ["SHOP_MAIN_MENU2"],
    "SHOP_MAIN_MENU_3": ["SHOP_MAIN_MENU3"],
    "STORAGE_MAIN_MENU_1": ["STORAGE_MAIN_MENU1"],
    "STORAGE_MAIN_MENU_2": ["STORAGE_MAIN_MENU2"],
    "STORAGE_MAIN_MENU_3": ["STORAGE_MAIN_MENU3"],
    "STORAGE_MAIN_MENU_4": ["STORAGE_MAIN_MENU4"],
    "DAYCARE_MENU_CONFIRM": ["HATCHER_MENU_CONFIRM"],
    "DAYCARE_MAIN_MENU": ["HATCHER_MAIN_MENU"],
    "APPRAISAL_MENU_CONFIRM": ["APPRAISER_MENU_CONFIRM"],
    "APPRAISAL_MAIN_MENU": ["APPRAISER_MAIN_MENU"],
    "APPRAISAL_SUBMENU": ["APPRAISER_SUB_MENU"],
    "DISCARD_ITEMS_SUBMENU_1": ["DISCARD_ITEMS_SUB_MENU1"],
    "DISCARD_ITEMS_SUBMENU_2": ["DISCARD_ITEMS_SUB_MENU2"],
    "DISCARD_ITEMS_SUBMENU_3": ["DISCARD_ITEMS_SUB_MENU3"],
    "DUNGEON_SUBMENU_1": ["DUNGEON_SUB_MENU1"],
    "DUNGEON_SUBMENU_2": ["DUNGEON_SUB_MENU2"],
    "DUNGEON_SUBMENU_3": ["DUNGEON_SUB_MENU3"],
    "DUNGEON_SUBMENU_4": ["DUNGEON_SUB_MENU4"],
    "DUNGEON_SUBMENU_5": ["DUNGEON_SUB_MENU5"],
    "DUNGEON_SUBMENU_6": ["DUNGEON_SUB_MENU6"],
    "BELLY_LOST_PER_TURN": ["BELLY_LOST_TURN"],
    "BELLY_DRAIN_IN_WALLS_INT": ["BELLY_LOST_WTW"],
    "BELLY_DRAIN_IN_WALLS_THOUSANDTHS": ["BELLY_LOST_WTW1000"],
    "FIXED_ROOM_ENTITY_SPAWN_TABLE": ["ENTITY_SPAWN_TABLE"],
    "FIXED_ROOM_REVISIT_OVERRIDES": ["FIXED_FLOOR_OVERRIDES"],
    "FIXED_ROOM_ITEM_SPAWN_TABLE": ["ITEM_SPAWN_TABLE"],
    "FIXED_ROOM_MONSTER_SPAWN_TABLE": ["MONSTER_SPAWN_TABLE"],
    "NECTAR_IQ_BOOST": ["NECTAR_IQ_GAIN"],
    "FIXED_ROOM_TILE_SPAWN_TABLE": ["TILE_SPAWN_TABLE"],
    "TOP_MENU_MUSIC_ID": ["MAIN_MENU_SONG_ID"],
    "TOP_MENU_RETURN_MUSIC_ID": ["MAIN_MENU_RETURN_SONG_ID"]
}


class DeprecatedPmd2BinarySymbol(Pmd2BinarySymbol):
    _DEPRECATION_WARNING = "The symbol {} is deprecated, use {} instead."

    def __init__(self, name: str, begin: int, end: Optional[int], description: str,
                 typ: Optional[Pmd2BinarySymbolType], new_name: str):
        self._begin: int = None  # type: ignore
        self.new_name: str = new_name
        super().__init__(name, begin, end, description, typ)

    @property  # type: ignore
    def begin(self):
        warnings.warn(self.__class__._DEPRECATION_WARNING.format(self.name, self.new_name), DeprecationWarning)
        return self._begin

    @begin.setter
    def begin(self, value):
        self._begin = value

    @property
    def end(self):
        warnings.warn(self.__class__._DEPRECATION_WARNING.format(self.name, self.new_name), DeprecationWarning)
        return self._end


@dataclass
class _IncompleteBinary:
    loadaddress: Optional[int] = None
    length: Optional[int] = None
    symbols: List[Pmd2BinarySymbol] = field(default_factory=list)
    description: str = field(default_factory=str)

    _discard: bool = False

    @classmethod
    def get(cls, pool: Dict[str, '_IncompleteBinary'], name: str) -> '_IncompleteBinary':
        if name in pool:
            return pool[name]
        newobj = _IncompleteBinary()
        pool[name] = newobj
        return newobj


def _read_symbol(loadaddr: int, symbol_def: dict, typ: Pmd2BinarySymbolType, region: str) -> Optional[Pmd2BinarySymbol]:
    assert isinstance(loadaddr, int)
    if 'name' in symbol_def:
        name = symbol_def['name']
    else:
        raise ValueError("Symbol is missing its name.")
    
    if 'address' in symbol_def:
        if region in symbol_def['address']:
            if isinstance(symbol_def['address'][region], list):
                begin = symbol_def['address'][region][0] - loadaddr
            else:
                begin = symbol_def['address'][region] - loadaddr
        else:
            return None
    else:
        raise ValueError(f"Symbol {name} is missing an address.")

    end = None
    if 'length' in symbol_def:
        if region in symbol_def['length']:
            end = begin + symbol_def['length'][region]

    description = symbol_def.get('description', "")

    return Pmd2BinarySymbol(
        name=name,
        typ=typ,
        begin=begin,
        end=end,
        description=description
    )


def _read(binaries: Dict[str, _IncompleteBinary], yml: dict, region: str):
    # arm9.bin and the overlays MUST be read first.
    for bin_name, definition in yml.items():
        assert isinstance(bin_name, str)
        binary = _IncompleteBinary.get(binaries, bin_name)
        if 'versions' in definition:
            # If it isn't we assume it's valid for all regions.
            if region not in definition['versions']:
                binary._discard = True
                continue
        if 'address' in definition:
            if region in definition['address']:
                if binary.loadaddress is None:
                    binary.loadaddress = int(definition['address'][region])
        if 'length' in definition:
            if region in definition['length']:
                if binary.length is None:
                    binary.length = int(definition['length'][region])
        if 'functions' in definition:
            assert binary.loadaddress is not None
            for symbol_def in definition['functions']:
                sym = _read_symbol(binary.loadaddress, symbol_def, Pmd2BinarySymbolType.FUNCTION, region)
                if sym is not None:
                    binary.symbols.append(sym)
        if 'data' in definition:
            assert binary.loadaddress is not None
            for symbol_def in definition['data']:
                sym = _read_symbol(binary.loadaddress, symbol_def, Pmd2BinarySymbolType.DATA, region)
                if sym is not None:
                    binary.symbols.append(sym)
        if 'description' in definition:
            if binary.description == "":
                binary.description = definition['description']


def _build(binaries: Dict[str, _IncompleteBinary]) -> List[Pmd2Binary]:
    # Merge ram into arm9 blocks (for backwards compatibility RAM is treated as arm9 by SkyTemple):
    if 'ram' in binaries and 'arm9' in binaries:
        binaries['arm9'].symbols += binaries['ram'].symbols
        del binaries['ram']
    out = []
    for bin_name, incl_bin in binaries.items():
        if incl_bin._discard:
            continue
        if incl_bin.loadaddress is None:
            raise ValueError(f"Did not find a load address for {bin_name}.")
        if incl_bin.length is None:
            raise ValueError(f"Did not find a length for {bin_name}.")
        translated_bin_name = f"{bin_name}.bin"
        overlay_match = OVERLAY_REGEX.match(bin_name)
        if overlay_match:
            translated_bin_name = f"overlay/overlay_{int(overlay_match.group(1)):04}.bin"
        alias_symbols: List[Pmd2BinarySymbol] = []
        for symbol in incl_bin.symbols:
            # Provide aliases for some symbols for backwards compatibility.
            if symbol.name in ALIAS_MAP:
                for entry in ALIAS_MAP[symbol.name]:
                    # noinspection PyProtectedMember
                    alias_symbols.append(DeprecatedPmd2BinarySymbol(
                        name=entry, begin=symbol.begin, end=symbol._end, description=symbol.description, typ=symbol.type,
                        new_name=symbol.name
                    ))
        binary = Pmd2Binary(
            filepath=translated_bin_name,
            loadaddress=incl_bin.loadaddress,
            length=incl_bin.length,
            symbols=incl_bin.symbols + alias_symbols,
            description=incl_bin.description
        )
        for symbol in binary.symbols.values():
            symbol.parent = binary
        out.append(binary)

    return out


def load_binaries(edition: str) -> List[Pmd2Binary]:
    version, region = edition.split("_")
    if version != GAME_VERSION_EOS:
        raise ValueError("This game version is not supported.")

    binaries: Dict[str, _IncompleteBinary] = {}

    files = glob(os.path.join(SYMBOLS_DIR, '*.yml'))

    # Make sure the arm and overlay files are read this: These are the main files.
    # They will contain the address, length and description.
    files.sort(key=lambda key: -1 if key.startswith('arm') or key.startswith('overlay') else 1)

    for yml_path in files:
        with open_utf8(yml_path, 'r') as f:
            _read(binaries, yaml.safe_load(f), region)

    with open_utf8(os.path.join(get_resources_dir(), "skytemple_pmdsky_debug_symbols.yml"), 'r') as f:
        _read(binaries, yaml.safe_load(f), region)

    return _build(binaries)
