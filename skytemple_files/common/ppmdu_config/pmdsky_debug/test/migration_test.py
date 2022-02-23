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
import unittest


# First tuple entry:   Has end?
# Second tuple entry:  type == Pmd2BinarySymbolType.FUNCTION
from parameterized import parameterized

from skytemple_files.common.ppmdu_config.data import Pmd2GameEdition, GAME_VERSION_EOS, GAME_REGION_EU, GAME_REGION_US
from skytemple_files.common.ppmdu_config.pmdsky_debug.data import SymbolHasNoEndError, Pmd2BinarySymbolType
from skytemple_files.common.ppmdu_config.pmdsky_debug.loader import load_binaries

OLD_ENTRIES = {
    'arm9.bin': {'CartRemovedImgData': (True, False),
                 'CompressedIqGroupsSkills': (True, False),
                 'DebugPrint': (False, True),
                 'DebugPrint0': (False, True),
                 'DebugPrint2': (False, True),
                 'DebugSpecialEpisodeType': (False, False),
                 'DefaultHeroId': (True, False),
                 'DefaultPartnerId': (True, False),
                 #'DungeonData': (False, False),
                 'DungeonList': (True, False),
                 'DungeonRestrictions': (True, False),
                 'Entities': (True, False),
                 'Events': (True, False),
                 'ExtraDungeonData': (True, False),
                 'GameMode': (False, False),
                 'GameStateValues': (False, False),
                 'GameVarsValues': (True, False),
                 'GetDebugFlag1': (False, True),
                 'GetDebugFlag2': (False, True),
                 'GuestPokemonData': (True, False),
                 'GuestPokemonData2': (True, False),
                 'GummiBellyHeal': (True, False),
                 'HeroStartLevel': (False, False),
                 'IqGroupsSkills': (True, False),
                 'IqGummiGain': (True, False),
                 'IqSkillRestrictions': (True, False),
                 'IqSkills': (True, False),
                 'JuiceBarNectarIqGain': (True, False),
                 'LanguageInfoData': (False, False),
                 'MapMarkerPlacements': (True, False),
                 'MemoryAllocTable': (False, False),
                 'MinIqExclusiveMoveUser': (True, False),
                 'MinIqItemMaster': (True, False),
                 'MonsterSpriteData': (True, False),
                 'NotifyNote': (False, False),
                 'PartnerStartLevel': (False, False),
                 'RankUpTable': (True, False),
                 'SaveScriptVariableValue': (False, True),
                 'SaveScriptVariableValueWithOffset': (False, True),
                 #'ScriptVars': (True, False),
                 #'ScriptVarsLocals': (True, False),
                 'SecondaryTerrains': (True, False),
                 'SetDebugFlag1': (False, True),
                 'SetDebugFlag2': (False, True),
                 #'SpecialEpisodePCs': (True, False),
                 'TacticsUnlockLevel': (True, False),
                 'TextSpeedConstant': (True, False),
                 'WonderGummiIqGain': (True, False)},
    'overlay/overlay_0000.bin': {'MainMenuSongId': (False, False)},
    'overlay/overlay_0001.bin': {'ContinueChoice': (True, False),
                                 'MainDebugMenu1': (True, False),
                                 'MainDebugMenu2': (True, False),
                                 'MainMenu': (True, False),
                                 'MainMenuConfirm': (True, False),
                                 'SubMenu': (True, False)},
    'overlay/overlay_0002.bin': {},
    'overlay/overlay_0003.bin': {},
    'overlay/overlay_0004.bin': {},
    'overlay/overlay_0005.bin': {},
    'overlay/overlay_0006.bin': {},
    'overlay/overlay_0007.bin': {},
    'overlay/overlay_0008.bin': {},
    'overlay/overlay_0009.bin': {'MainMenuReturnSongId': (True, False)},
    'overlay/overlay_0010.bin': {'BadPoisonDamageDelay': (True, False),
                                 'BurnDamageDelay': (True, False),
                                 'FixedFloorProperties': (True, False),
                                 'GinsengChance3': (True, False),
                                 'IntimidatorChance': (True, False),
                                 #'LifeSeedHP': (True, False),
                                 'MonsterSpawnStatsTable': (True, False),
                                 'MusicList': (True, False),
                                 #'OranBerryHP': (True, False),
                                 'PoisonDamageDelay': (True, False),
                                 'RandomMusicList': (True, False),
                                 #'SitrusBerryHP': (True, False),
                                 'SpawnDelayNormal': (True, False),
                                 'SpawnDelayStealing': (True, False),
                                 'TilesetProperties': (True, False)},
    'overlay/overlay_0011.bin': {#'CRoutines': (True, False),
                                 'FuncThatCallsCommandParsing': (False, True),
                                 'GroundMainLoop': (False, True),
                                 'GroundStateMap': (False, False),
                                 'GroundStatePntrs': (True, False),
                                 'LevelTilemapList': (True, False),
                                 'MonsterGroundIdleAnim': (True, False),
                                 #'Objects': (True, False),
                                 'RecruitmentTableLevels': (True, False),
                                 'RecruitmentTableLocations': (True, False),
                                 'RecruitmentTableSpecies': (True, False),
                                 'ScriptCommandParsing': (False, True),
                                 #'ScriptOpCodes': (True, False),
                                 'ScriptStationLoadTalk': (False, True),
                                 'SsbLoad1': (False, True),
                                 'SsbLoad2': (False, True),
                                 'StationLoadHanger': (False, True)},
                                 #'UnionallRAMAddress': (False, False)},
    'overlay/overlay_0012.bin': {},
    'overlay/overlay_0013.bin': {#'QuizzAnswerStrs': (True, False),
                                 #'QuizzQuestionStrs': (True, False),
                                 'StartersHeroIds': (True, False),
                                 'StartersPartnerIds': (True, False),
                                 #'StartersStrings': (True, False),
                                 'UnknownMenu1': (True, False)},
    'overlay/overlay_0014.bin': {'FootprintDebugMenu': (True, False)},
    'overlay/overlay_0015.bin': {'BankMainMenu': (True, False)},
    'overlay/overlay_0016.bin': {'EvoMainMenu': (True, False),
                                 'EvoMenuConfirm': (True, False),
                                 'EvoSubMenu': (True, False)},
    'overlay/overlay_0017.bin': {'AssemblyMainMenu1': (True, False),
                                 'AssemblyMainMenu2': (True, False),
                                 'AssemblyMenuConfirm': (True, False),
                                 'AssemblySubMenu1': (True, False),
                                 'AssemblySubMenu2': (True, False),
                                 'AssemblySubMenu3': (True, False),
                                 'AssemblySubMenu4': (True, False),
                                 'AssemblySubMenu5': (True, False),
                                 'AssemblySubMenu6': (True, False),
                                 'AssemblySubMenu7': (True, False)},
    'overlay/overlay_0018.bin': {'MovesMainMenu': (True, False),
                                 'MovesMenuConfirm': (True, False),
                                 'MovesSubMenu1': (True, False),
                                 'MovesSubMenu2': (True, False),
                                 'MovesSubMenu3': (True, False),
                                 'MovesSubMenu4': (True, False),
                                 'MovesSubMenu5': (True, False),
                                 'MovesSubMenu6': (True, False),
                                 'MovesSubMenu7': (True, False)},
    'overlay/overlay_0019.bin': {'BarMainMenu': (True, False),
                                 'BarMenuConfirm1': (True, False),
                                 'BarMenuConfirm2': (True, False),
                                 'BarSubMenu1': (True, False),
                                 'BarSubMenu2': (True, False)},
    'overlay/overlay_0020.bin': {'RecycleMainMenu1': (True, False),
                                 'RecycleMainMenu2': (True, False),
                                 'RecycleMainMenu3': (True, False),
                                 'RecycleMenuConfirm1': (True, False),
                                 'RecycleMenuConfirm2': (True, False),
                                 'RecycleSubMenu1': (True, False),
                                 'RecycleSubMenu2': (True, False)},
    'overlay/overlay_0021.bin': {'SynthesisMainMenu1': (True, False),
                                 'SynthesisMainMenu2': (True, False),
                                 'SynthesisMenuConfirm': (True, False),
                                 'SynthesisSubMenu1': (True, False),
                                 'SynthesisSubMenu2': (True, False),
                                 'SynthesisSubMenu3': (True, False)},
    'overlay/overlay_0022.bin': {'ShopMainMenu1': (True, False),
                                 'ShopMainMenu2': (True, False),
                                 'ShopMainMenu3': (True, False),
                                 'ShopMenuConfirm': (True, False)},
    'overlay/overlay_0023.bin': {'StorageMainMenu1': (True, False),
                                 'StorageMainMenu2': (True, False),
                                 'StorageMainMenu3': (True, False),
                                 'StorageMainMenu4': (True, False),
                                 'StorageMenuConfirm': (True, False)},
    'overlay/overlay_0024.bin': {'HatcherMainMenu': (True, False),
                                 'HatcherMenuConfirm': (True, False)},
    'overlay/overlay_0025.bin': {'AppraiserMainMenu': (True, False),
                                 'AppraiserMenuConfirm': (True, False),
                                 'AppraiserSubMenu': (True, False)},
    'overlay/overlay_0026.bin': {},
    'overlay/overlay_0027.bin': {'DiscardItemsMainMenu': (True, False),
                                 'DiscardItemsMenuConfirm': (True, False),
                                 'DiscardItemsSubMenu1': (True, False),
                                 'DiscardItemsSubMenu2': (True, False)},
    'overlay/overlay_0028.bin': {},
    'overlay/overlay_0029.bin': {'BellyLostTurn': (True, False),
                                 'BellyLostWtw': (True, False),
                                 'BellyLostWtw1000': (True, False),
                                 'EntitySpawnTable': (True, False),
                                 'FixedFloorOverrides': (True, False),
                                 'ItemSpawnTable': (True, False),
                                 'MonsterSpawnTable': (True, False),
                                 'NectarIqGain': (True, False),
                                 'TileSpawnTable': (True, False)},
    'overlay/overlay_0030.bin': {},
    'overlay/overlay_0031.bin': {'DungeonMainMenu': (True, False),
                                 'DungeonSubMenu1': (True, False),
                                 'DungeonSubMenu2': (True, False),
                                 'DungeonSubMenu3': (True, False),
                                 'DungeonSubMenu4': (True, False),
                                 'DungeonSubMenu5': (True, False),
                                 'DungeonSubMenu6': (True, False)},
    'overlay/overlay_0032.bin': {},
    'overlay/overlay_0033.bin': {},
    'overlay/overlay_0034.bin': {'DungeonDebugMenu': (True, False),
                                 'UnknownMenuConfirm': (True, False)},
    'overlay/overlay_0035.bin': {},
    'overlay/overlay_0036.bin': {}}


class MigrationTestCase(unittest.TestCase):
    """
    This tests that all blocks and functions that were formely supported by pmd2data.xml are still accessible
    after migrating to the new pmdsky-debug based solution.
    """
    @parameterized.expand((GAME_REGION_EU, GAME_REGION_US))
    def test_backwards_compatibility(self, region):
        to_check = {x.filepath: x for x in load_binaries(f"{GAME_VERSION_EOS}_{region}")}

        for bin_path, symbol_specs in OLD_ENTRIES.items():
            self.assertIn(bin_path, to_check)
            bin_symbols = to_check[bin_path].symbols
            for symbol_name, (has_end, is_function) in symbol_specs.items():
                self.assertIn(symbol_name, bin_symbols, f"Symbol {symbol_name} in binary {bin_path} must be defined.")
                symbol = bin_symbols[symbol_name]
                if has_end:
                    try:
                        # noinspection PyStatementEffect,PyUnusedLocal
                        _x = symbol.end
                    except SymbolHasNoEndError:
                        self.fail(f"Symbol {symbol_name} in binary {bin_path} must have a defined end.")
                if is_function:
                    self.assertTrue(symbol.type == Pmd2BinarySymbolType.FUNCTION, f"Symbol {symbol_name} in binary {bin_path} must be a function.")
                else:
                    self.assertTrue(symbol.type == Pmd2BinarySymbolType.DATA, f"Symbol {symbol_name} in binary {bin_path} must be data.")
