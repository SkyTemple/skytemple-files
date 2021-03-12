"""Module for editing hardcoded menus."""
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
from enum import Enum, auto
from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.i18n_util import _

try:
    from PIL import Image
except ImportError:
    from pil import Image

MENU_ENTRY_LEN = 8
class MenuDataType(Enum):
    NORMAL = auto()
    ADVANCED = auto()

class MenuType(Enum):
    MAIN_MENU = 100, MenuDataType.ADVANCED, 'overlay/overlay_0001.bin', 'MainMenu', _("Game Main Menu")
    SUB_MENU = 101, MenuDataType.ADVANCED, 'overlay/overlay_0001.bin', 'SubMenu', _("Game Sub Menu")
    CONTINUE_CHOICE = 102, MenuDataType.NORMAL, 'overlay/overlay_0001.bin', 'ContinueChoice', _("Continue Choice")
    DEBUG_MENU_1 = 103, MenuDataType.NORMAL, 'overlay/overlay_0001.bin', 'MainDebugMenu1', _("Main Debug Menu") + " 1"
    DEBUG_MENU_2 = 104, MenuDataType.NORMAL, 'overlay/overlay_0001.bin', 'MainDebugMenu2', _("Main Debug Menu") + " 2"
    UNK_MENU_1 = 1300, MenuDataType.NORMAL, 'overlay/overlay_0013.bin', 'UnknownMenu1', _("Unknown Menu") + " 1"
    FOOT_DEBUG_MENU_1 = 1400, MenuDataType.NORMAL, 'overlay/overlay_0014.bin', 'FootprintDebugMenu', _("Footprint Debug Menu")
    BANK_MENU = 1500, MenuDataType.NORMAL, 'overlay/overlay_0015.bin', 'BankMainMenu', _("Bank Main Menu")
    EVO_MENU_CONFIRM = 1601, MenuDataType.NORMAL, 'overlay/overlay_0016.bin', 'EvoMenuConfirm', _("Evolution Menu Confirm")
    EVO_SUB_MENU = 1602, MenuDataType.NORMAL, 'overlay/overlay_0016.bin', 'EvoSubMenu', _("Evolution Sub Menu")
    EVO_MAIN_MENU = 1603, MenuDataType.NORMAL, 'overlay/overlay_0016.bin', 'EvoMainMenu', _("Evolution Main Menu")
    ASSEMBLY_MENU_CONFIRM = 1700, MenuDataType.NORMAL, 'overlay/overlay_0017.bin', 'AssemblyMenuConfirm', _("Assembly Menu Confirm")
    ASSEMBLY_MAIN_MENU_1 = 1701, MenuDataType.NORMAL, 'overlay/overlay_0017.bin', 'AssemblyMainMenu1', _("Assembly Main Menu") + " 1"
    ASSEMBLY_MAIN_MENU_2 = 1702, MenuDataType.NORMAL, 'overlay/overlay_0017.bin', 'AssemblyMainMenu2', _("Assembly Main Menu") + " 2"
    ASSEMBLY_SUB_MENU_1 = 1703, MenuDataType.NORMAL, 'overlay/overlay_0017.bin', 'AssemblySubMenu1', _("Assembly Sub Menu") + " 1"
    ASSEMBLY_SUB_MENU_2 = 1704, MenuDataType.NORMAL, 'overlay/overlay_0017.bin', 'AssemblySubMenu2', _("Assembly Sub Menu") + " 2"
    ASSEMBLY_SUB_MENU_3 = 1705, MenuDataType.NORMAL, 'overlay/overlay_0017.bin', 'AssemblySubMenu3', _("Assembly Sub Menu") + " 3"
    ASSEMBLY_SUB_MENU_4 = 1706, MenuDataType.NORMAL, 'overlay/overlay_0017.bin', 'AssemblySubMenu4', _("Assembly Sub Menu") + " 4"
    ASSEMBLY_SUB_MENU_5 = 1707, MenuDataType.NORMAL, 'overlay/overlay_0017.bin', 'AssemblySubMenu5', _("Assembly Sub Menu") + " 5"
    ASSEMBLY_SUB_MENU_6 = 1708, MenuDataType.NORMAL, 'overlay/overlay_0017.bin', 'AssemblySubMenu6', _("Assembly Sub Menu") + " 6"
    ASSEMBLY_SUB_MENU_7 = 1709, MenuDataType.NORMAL, 'overlay/overlay_0017.bin', 'AssemblySubMenu7', _("Assembly Sub Menu") + " 7"
    MOVES_MENU_CONFIRM = 1800, MenuDataType.NORMAL, 'overlay/overlay_0018.bin', 'MovesMenuConfirm', _("Moves Menu Confirm")
    MOVES_SUB_MENU_1 = 1801, MenuDataType.NORMAL, 'overlay/overlay_0018.bin', 'MovesSubMenu1', _("Moves Sub Menu") + " 1"
    MOVES_SUB_MENU_2 = 1802, MenuDataType.NORMAL, 'overlay/overlay_0018.bin', 'MovesSubMenu2', _("Moves Sub Menu") + " 2"
    MOVES_MAIN_MENU = 1803, MenuDataType.NORMAL, 'overlay/overlay_0018.bin', 'MovesMainMenu', _("Moves Main Menu")
    MOVES_SUB_MENU_3 = 1804, MenuDataType.NORMAL, 'overlay/overlay_0018.bin', 'MovesSubMenu3', _("Moves Sub Menu") + " 3"
    MOVES_SUB_MENU_4 = 1805, MenuDataType.NORMAL, 'overlay/overlay_0018.bin', 'MovesSubMenu4', _("Moves Sub Menu") + " 4"
    MOVES_SUB_MENU_5 = 1806, MenuDataType.NORMAL, 'overlay/overlay_0018.bin', 'MovesSubMenu5', _("Moves Sub Menu") + " 5"
    MOVES_SUB_MENU_6 = 1807, MenuDataType.NORMAL, 'overlay/overlay_0018.bin', 'MovesSubMenu6', _("Moves Sub Menu") + " 6"
    MOVES_SUB_MENU_7 = 1808, MenuDataType.NORMAL, 'overlay/overlay_0018.bin', 'MovesSubMenu7', _("Moves Sub Menu") + " 7"
    BAR_MENU_CONFIRM_1 = 1900, MenuDataType.NORMAL, 'overlay/overlay_0019.bin', 'BarMenuConfirm1', _("Bar Menu Confirm") + " 1"
    BAR_MENU_CONFIRM_2 = 1901, MenuDataType.NORMAL, 'overlay/overlay_0019.bin', 'BarMenuConfirm2', _("Bar Menu Confirm") + " 2"
    BAR_MAIN_MENU = 1902, MenuDataType.NORMAL, 'overlay/overlay_0019.bin', 'BarMainMenu', _("Bar Main Menu")
    BAR_SUB_MENU_1 = 1903, MenuDataType.NORMAL, 'overlay/overlay_0019.bin', 'BarSubMenu1', _("Bar Sub Menu") + " 1"
    BAR_SUB_MENU_2 = 1904, MenuDataType.NORMAL, 'overlay/overlay_0019.bin', 'BarSubMenu2', _("Bar Sub Menu") + " 2"
    RECYCLE_MENU_CONFIRM_1 = 2000, MenuDataType.NORMAL, 'overlay/overlay_0020.bin', 'RecycleMenuConfirm1', _("Recycle Menu Confirm") + " 1"
    RECYCLE_MENU_CONFIRM_2 = 2001, MenuDataType.NORMAL, 'overlay/overlay_0020.bin', 'RecycleMenuConfirm2', _("Recycle Menu Confirm") + " 2"
    RECYCLE_SUB_MENU_1 = 2002, MenuDataType.NORMAL, 'overlay/overlay_0020.bin', 'RecycleSubMenu1', _("Recycle Sub Menu") + " 1"
    RECYCLE_SUB_MENU_2 = 2003, MenuDataType.NORMAL, 'overlay/overlay_0020.bin', 'RecycleSubMenu2', _("Recycle Sub Menu") + " 2"
    RECYCLE_MAIN_MENU_1 = 2004, MenuDataType.NORMAL, 'overlay/overlay_0020.bin', 'RecycleMainMenu1', _("Recycle Main Menu") + " 1"
    RECYCLE_MAIN_MENU_2 = 2005, MenuDataType.NORMAL, 'overlay/overlay_0020.bin', 'RecycleMainMenu2', _("Recycle Main Menu") + " 2"
    RECYCLE_MAIN_MENU_3 = 2006, MenuDataType.NORMAL, 'overlay/overlay_0020.bin', 'RecycleMainMenu3', _("Recycle Main Menu") + " 3"
    SYNTH_MENU_CONFIRM = 2100, MenuDataType.NORMAL, 'overlay/overlay_0021.bin', 'SynthesisMenuConfirm', _("Synthesis Menu Confirm")
    SYNTH_SUB_MENU_1 = 2101, MenuDataType.NORMAL, 'overlay/overlay_0021.bin', 'SynthesisSubMenu1', _("Synthesis Sub Menu") + " 1"
    SYNTH_SUB_MENU_2 = 2102, MenuDataType.NORMAL, 'overlay/overlay_0021.bin', 'SynthesisSubMenu2', _("Synthesis Sub Menu") + " 2"
    SYNTH_MAIN_MENU_1 = 2103, MenuDataType.NORMAL, 'overlay/overlay_0021.bin', 'SynthesisMainMenu1', _("Synthesis Main Menu") + " 1"
    SYNTH_MAIN_MENU_2 = 2104, MenuDataType.NORMAL, 'overlay/overlay_0021.bin', 'SynthesisMainMenu2', _("Synthesis Main Menu") + " 2"
    SYNTH_SUB_MENU_3 = 2105, MenuDataType.NORMAL, 'overlay/overlay_0021.bin', 'SynthesisSubMenu3', _("Synthesis Sub Menu") + " 3"
    SHOP_MENU_CONFIRM = 2200, MenuDataType.NORMAL, 'overlay/overlay_0022.bin', 'ShopMenuConfirm', _("Shop Menu Confirm")
    SHOP_MAIN_MENU_1 = 2201, MenuDataType.NORMAL, 'overlay/overlay_0022.bin', 'ShopMainMenu1', _("Shop Main Menu") + " 1"
    SHOP_MAIN_MENU_2 = 2202, MenuDataType.NORMAL, 'overlay/overlay_0022.bin', 'ShopMainMenu2', _("Shop Main Menu") + " 2"
    SHOP_MAIN_MENU_3 = 2203, MenuDataType.NORMAL, 'overlay/overlay_0022.bin', 'ShopMainMenu3', _("Shop Main Menu") + " 3"
    STORAGE_MENU_CONFIRM = 2300, MenuDataType.NORMAL, 'overlay/overlay_0023.bin', 'StorageMenuConfirm', _("Storage Menu Confirm")
    STORAGE_MAIN_MENU_1 = 2301, MenuDataType.NORMAL, 'overlay/overlay_0023.bin', 'StorageMainMenu1', _("Storage Main Menu") + " 1"
    STORAGE_MAIN_MENU_2 = 2302, MenuDataType.NORMAL, 'overlay/overlay_0023.bin', 'StorageMainMenu2', _("Storage Main Menu") + " 2"
    STORAGE_MAIN_MENU_3 = 2303, MenuDataType.NORMAL, 'overlay/overlay_0023.bin', 'StorageMainMenu3', _("Storage Main Menu") + " 3"
    STORAGE_MAIN_MENU_4 = 2304, MenuDataType.NORMAL, 'overlay/overlay_0023.bin', 'StorageMainMenu4', _("Storage Main Menu") + " 4"
    HATCHER_MENU_CONFIRM = 2400, MenuDataType.NORMAL, 'overlay/overlay_0024.bin', 'HatcherMenuConfirm', _("Hatcher Menu Confirm")
    HATCHER_MAIN_MENU = 2401, MenuDataType.NORMAL, 'overlay/overlay_0024.bin', 'HatcherMainMenu', _("Hatcher Main Menu")
    APPRAISER_MENU_CONFIRM = 2500, MenuDataType.NORMAL, 'overlay/overlay_0025.bin', 'AppraiserMenuConfirm', _("Appraiser Menu Confirm")
    APPRAISER_MAIN_MENU = 2501, MenuDataType.NORMAL, 'overlay/overlay_0025.bin', 'AppraiserMainMenu', _("Appraiser Main Menu")
    APPRAISER_SUB_MENU = 2502, MenuDataType.NORMAL, 'overlay/overlay_0025.bin', 'AppraiserSubMenu', _("Appraiser Sub Menu")
    DISCARD_MENU_CONFIRM = 2700, MenuDataType.NORMAL, 'overlay/overlay_0027.bin', 'DiscardItemsMenuConfirm', _("Discard Items Menu Confirm")
    DISCARD_SUB_MENU_1 = 2701, MenuDataType.NORMAL, 'overlay/overlay_0027.bin', 'DiscardItemsSubMenu1', _("Discard Items Sub Menu") + " 1"
    DISCARD_SUB_MENU_2 = 2702, MenuDataType.NORMAL, 'overlay/overlay_0027.bin', 'DiscardItemsSubMenu2', _("Discard Items Sub Menu") + " 2"
    DISCARD_MAIN_MENU = 2703, MenuDataType.NORMAL, 'overlay/overlay_0027.bin', 'DiscardItemsMainMenu', _("Discard Items Main Menu")
    DUNGEON_MAIN_MENU = 3100, MenuDataType.NORMAL, 'overlay/overlay_0031.bin', 'DungeonMainMenu', _("Dungeon Main Menu")
    DUNGEON_SUB_MENU_1 = 3101, MenuDataType.NORMAL, 'overlay/overlay_0031.bin', 'DungeonSubMenu1', _("Dungeon Sub Menu") + " 1"
    DUNGEON_SUB_MENU_2 = 3102, MenuDataType.NORMAL, 'overlay/overlay_0031.bin', 'DungeonSubMenu2', _("Dungeon Sub Menu") + " 2"
    DUNGEON_SUB_MENU_3 = 3103, MenuDataType.NORMAL, 'overlay/overlay_0031.bin', 'DungeonSubMenu3', _("Dungeon Sub Menu") + " 3"
    DUNGEON_SUB_MENU_4 = 3104, MenuDataType.NORMAL, 'overlay/overlay_0031.bin', 'DungeonSubMenu4', _("Dungeon Sub Menu") + " 4"
    DUNGEON_SUB_MENU_5 = 3105, MenuDataType.NORMAL, 'overlay/overlay_0031.bin', 'DungeonSubMenu5', _("Dungeon Sub Menu") + " 5"
    DUNGEON_SUB_MENU_6 = 3106, MenuDataType.NORMAL, 'overlay/overlay_0031.bin', 'DungeonSubMenu6', _("Dungeon Sub Menu") + " 6"
    UNKNOWN_MENU_CONFIRM = 3400, MenuDataType.NORMAL, 'overlay/overlay_0034.bin', 'UnknownMenuConfirm', _("Unknown Menu Confirm")
    DUNGEON_DEBUG_MENU = 3401, MenuDataType.NORMAL, 'overlay/overlay_0034.bin', 'DungeonDebugMenu', _("Dungeon Debug Menu")
    # TODO: There are more menus
    
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: int, data_type: MenuDataType, binary: str, block: str, menu_name: str
    ):
        self.data_type = data_type
        self.binary = binary
        self.block = block
        self.menu_name = menu_name
        

class MenuEntry:
    def __init__(self, name_id: int, description_id: int, action: int):
        self.name_id = name_id
        self.description_id = description_id
        self.action = action

class HardcodedMenus:
    @staticmethod
    def get_menu(menu: MenuType, binary: bytes, config: Pmd2Data) -> List[MenuEntry]:
        """
        Gets one menu
        """
        block = config.binaries[menu.binary].blocks[menu.block]
        data = binary[block.begin:block.end]
        menu_list: List[MenuEntry] = []
        for i in range(len(data)//MENU_ENTRY_LEN):
            if menu.data_type==MenuDataType.NORMAL:
                name_id = read_uintle(data, i*MENU_ENTRY_LEN, 2)
                description_id = read_uintle(data, i*MENU_ENTRY_LEN+2, 2)
                action = read_sintle(data, i*MENU_ENTRY_LEN+4, 4)
            elif menu.data_type==MenuDataType.ADVANCED:
                action = read_sintle(data, i*MENU_ENTRY_LEN, 4)
                name_id = read_uintle(data, i*MENU_ENTRY_LEN+4, 2)
                description_id = read_uintle(data, i*MENU_ENTRY_LEN+6, 2)
            menu_list.append(MenuEntry(name_id, description_id, action))
        return menu_list

    @staticmethod
    def set_menu(menu: MenuType, menu_data: List[MenuEntry], binary: bytearray, config: Pmd2Data):
        """
        Sets one menu
        """
        block = config.binaries[menu.binary].blocks[menu.block]
        data = bytearray(len(menu_data)*MENU_ENTRY_LEN)
        if len(data)!=block.end-block.begin:
            # noinspection PyUnusedLocal
            num_entries = (block.end-block.begin)//MENU_ENTRY_LEN
            raise Exception(f(_("This menu must have {num_entries} entries!")))
        for i, m in enumerate(menu_data):
            if menu.data_type==MenuDataType.NORMAL:
                write_uintle(data, m.name_id, i*MENU_ENTRY_LEN, 2)
                write_uintle(data, m.description_id, i*MENU_ENTRY_LEN+2, 2)
                write_sintle(data, m.action, i*MENU_ENTRY_LEN+4, 4)
            elif menu.data_type==MenuDataType.ADVANCED:
                write_uintle(data, m.action, i*MENU_ENTRY_LEN, 4)
                write_uintle(data, m.name_id, i*MENU_ENTRY_LEN+4, 2)
                write_sintle(data, m.description_id, i*MENU_ENTRY_LEN+6, 2)
        binary[block.begin:block.end] = data
