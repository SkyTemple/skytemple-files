"""Module for editing hardcoded menus."""
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

from enum import Enum, auto
from typing import Any, List

from pmdsky_debug_py.protocol import (
    Overlay1DataProtocol,
    Overlay13DataProtocol,
    Overlay14DataProtocol,
    Overlay15DataProtocol,
    Overlay16DataProtocol,
    Overlay17DataProtocol,
    Overlay18DataProtocol,
    Overlay19DataProtocol,
    Overlay20DataProtocol,
    Overlay21DataProtocol,
    Overlay22DataProtocol,
    Overlay23DataProtocol,
    Overlay24DataProtocol,
    Overlay25DataProtocol,
    Overlay27DataProtocol,
    Overlay31DataProtocol,
    Overlay34DataProtocol,
)
from range_typed_integers import u16, i32

from skytemple_files.common.i18n_util import _, f
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import (
    read_i32,
    read_u16,
    write_i32,
    write_u16,
)

MENU_ENTRY_LEN = 8


class MenuDataType(Enum):
    NORMAL = auto()
    ADVANCED = auto()


class MenuType(Enum):
    MAIN_MENU = (
        100,
        MenuDataType.ADVANCED,
        "overlay1",
        "MAIN_MENU",
        lambda: Overlay1DataProtocol.MAIN_MENU,
        _("Game Main Menu"),
    )
    SUB_MENU = (
        101,
        MenuDataType.ADVANCED,
        "overlay1",
        "SUBMENU",
        lambda: Overlay1DataProtocol.SUBMENU,
        _("Game Sub Menu"),
    )
    CONTINUE_CHOICE = (
        102,
        MenuDataType.NORMAL,
        "overlay1",
        "CONTINUE_CHOICE",
        lambda: Overlay1DataProtocol.CONTINUE_CHOICE,
        _("Continue Choice"),
    )
    DEBUG_MENU_1 = (
        103,
        MenuDataType.NORMAL,
        "overlay1",
        "MAIN_DEBUG_MENU_1",
        lambda: Overlay1DataProtocol.MAIN_DEBUG_MENU_1,
        _("Main Debug Menu") + " 1",
    )
    DEBUG_MENU_2 = (
        104,
        MenuDataType.NORMAL,
        "overlay1",
        "MAIN_DEBUG_MENU_2",
        lambda: Overlay1DataProtocol.MAIN_DEBUG_MENU_2,
        _("Main Debug Menu") + " 2",
    )
    UNK_MENU_1 = (
        1300,
        MenuDataType.NORMAL,
        "overlay13",
        "QUIZ_DEBUG_MENU",
        lambda: Overlay13DataProtocol.QUIZ_DEBUG_MENU,
        _("Quiz Debug Menu"),
    )
    FOOT_DEBUG_MENU_1 = (
        1400,
        MenuDataType.NORMAL,
        "overlay14",
        "FOOTPRINT_DEBUG_MENU",
        lambda: Overlay14DataProtocol.FOOTPRINT_DEBUG_MENU,
        _("Footprint Debug Menu"),
    )
    BANK_MENU = (
        1500,
        MenuDataType.NORMAL,
        "overlay15",
        "BANK_MAIN_MENU",
        lambda: Overlay15DataProtocol.BANK_MAIN_MENU,
        _("Bank Main Menu"),
    )
    EVO_MENU_CONFIRM = (
        1601,
        MenuDataType.NORMAL,
        "overlay16",
        "EVO_MENU_CONFIRM",
        lambda: Overlay16DataProtocol.EVO_MENU_CONFIRM,
        _("Evolution Menu Confirm"),
    )
    EVO_SUB_MENU = (
        1602,
        MenuDataType.NORMAL,
        "overlay16",
        "EVO_SUBMENU",
        lambda: Overlay16DataProtocol.EVO_SUBMENU,
        _("Evolution Sub Menu"),
    )
    EVO_MAIN_MENU = (
        1603,
        MenuDataType.NORMAL,
        "overlay16",
        "EVO_MAIN_MENU",
        lambda: Overlay16DataProtocol.EVO_MAIN_MENU,
        _("Evolution Main Menu"),
    )
    ASSEMBLY_MENU_CONFIRM = (
        1700,
        MenuDataType.NORMAL,
        "overlay17",
        "ASSEMBLY_MENU_CONFIRM",
        lambda: Overlay17DataProtocol.ASSEMBLY_MENU_CONFIRM,
        _("Assembly Menu Confirm"),
    )
    ASSEMBLY_MAIN_MENU_1 = (
        1701,
        MenuDataType.NORMAL,
        "overlay17",
        "ASSEMBLY_MAIN_MENU_1",
        lambda: Overlay17DataProtocol.ASSEMBLY_MAIN_MENU_1,
        _("Assembly Main Menu") + " 1",
    )
    ASSEMBLY_MAIN_MENU_2 = (
        1702,
        MenuDataType.NORMAL,
        "overlay17",
        "ASSEMBLY_MAIN_MENU_2",
        lambda: Overlay17DataProtocol.ASSEMBLY_MAIN_MENU_2,
        _("Assembly Main Menu") + " 2",
    )
    ASSEMBLY_SUB_MENU_1 = (
        1703,
        MenuDataType.NORMAL,
        "overlay17",
        "ASSEMBLY_SUBMENU_1",
        lambda: Overlay17DataProtocol.ASSEMBLY_SUBMENU_1,
        _("Assembly Sub Menu") + " 1",
    )
    ASSEMBLY_SUB_MENU_2 = (
        1704,
        MenuDataType.NORMAL,
        "overlay17",
        "ASSEMBLY_SUBMENU_2",
        lambda: Overlay17DataProtocol.ASSEMBLY_SUBMENU_2,
        _("Assembly Sub Menu") + " 2",
    )
    ASSEMBLY_SUB_MENU_3 = (
        1705,
        MenuDataType.NORMAL,
        "overlay17",
        "ASSEMBLY_SUBMENU_3",
        lambda: Overlay17DataProtocol.ASSEMBLY_SUBMENU_3,
        _("Assembly Sub Menu") + " 3",
    )
    ASSEMBLY_SUB_MENU_4 = (
        1706,
        MenuDataType.NORMAL,
        "overlay17",
        "ASSEMBLY_SUBMENU_4",
        lambda: Overlay17DataProtocol.ASSEMBLY_SUBMENU_4,
        _("Assembly Sub Menu") + " 4",
    )
    ASSEMBLY_SUB_MENU_5 = (
        1707,
        MenuDataType.NORMAL,
        "overlay17",
        "ASSEMBLY_SUBMENU_5",
        lambda: Overlay17DataProtocol.ASSEMBLY_SUBMENU_5,
        _("Assembly Sub Menu") + " 5",
    )
    ASSEMBLY_SUB_MENU_6 = (
        1708,
        MenuDataType.NORMAL,
        "overlay17",
        "ASSEMBLY_SUBMENU_6",
        lambda: Overlay17DataProtocol.ASSEMBLY_SUBMENU_6,
        _("Assembly Sub Menu") + " 6",
    )
    ASSEMBLY_SUB_MENU_7 = (
        1709,
        MenuDataType.NORMAL,
        "overlay17",
        "ASSEMBLY_SUBMENU_7",
        lambda: Overlay17DataProtocol.ASSEMBLY_SUBMENU_7,
        _("Assembly Sub Menu") + " 7",
    )
    MOVES_MENU_CONFIRM = (
        1800,
        MenuDataType.NORMAL,
        "overlay18",
        "MOVES_MENU_CONFIRM",
        lambda: Overlay18DataProtocol.MOVES_MENU_CONFIRM,
        _("Moves Menu Confirm"),
    )
    MOVES_SUB_MENU_1 = (
        1801,
        MenuDataType.NORMAL,
        "overlay18",
        "MOVES_SUBMENU_1",
        lambda: Overlay18DataProtocol.MOVES_SUBMENU_1,
        _("Moves Sub Menu") + " 1",
    )
    MOVES_SUB_MENU_2 = (
        1802,
        MenuDataType.NORMAL,
        "overlay18",
        "MOVES_SUBMENU_2",
        lambda: Overlay18DataProtocol.MOVES_SUBMENU_2,
        _("Moves Sub Menu") + " 2",
    )
    MOVES_MAIN_MENU = (
        1803,
        MenuDataType.NORMAL,
        "overlay18",
        "MOVES_MAIN_MENU",
        lambda: Overlay18DataProtocol.MOVES_MAIN_MENU,
        _("Moves Main Menu"),
    )
    MOVES_SUB_MENU_3 = (
        1804,
        MenuDataType.NORMAL,
        "overlay18",
        "MOVES_SUBMENU_3",
        lambda: Overlay18DataProtocol.MOVES_SUBMENU_3,
        _("Moves Sub Menu") + " 3",
    )
    MOVES_SUB_MENU_4 = (
        1805,
        MenuDataType.NORMAL,
        "overlay18",
        "MOVES_SUBMENU_4",
        lambda: Overlay18DataProtocol.MOVES_SUBMENU_4,
        _("Moves Sub Menu") + " 4",
    )
    MOVES_SUB_MENU_5 = (
        1806,
        MenuDataType.NORMAL,
        "overlay18",
        "MOVES_SUBMENU_5",
        lambda: Overlay18DataProtocol.MOVES_SUBMENU_5,
        _("Moves Sub Menu") + " 5",
    )
    MOVES_SUB_MENU_6 = (
        1807,
        MenuDataType.NORMAL,
        "overlay18",
        "MOVES_SUBMENU_6",
        lambda: Overlay18DataProtocol.MOVES_SUBMENU_6,
        _("Moves Sub Menu") + " 6",
    )
    MOVES_SUB_MENU_7 = (
        1808,
        MenuDataType.NORMAL,
        "overlay18",
        "MOVES_SUBMENU_7",
        lambda: Overlay18DataProtocol.MOVES_SUBMENU_7,
        _("Moves Sub Menu") + " 7",
    )
    BAR_MENU_CONFIRM_1 = (
        1900,
        MenuDataType.NORMAL,
        "overlay19",
        "BAR_MENU_CONFIRM_1",
        lambda: Overlay19DataProtocol.BAR_MENU_CONFIRM_1,
        _("Bar Menu Confirm") + " 1",
    )
    BAR_MENU_CONFIRM_2 = (
        1901,
        MenuDataType.NORMAL,
        "overlay19",
        "BAR_MENU_CONFIRM_2",
        lambda: Overlay19DataProtocol.BAR_MENU_CONFIRM_2,
        _("Bar Menu Confirm") + " 2",
    )
    BAR_MAIN_MENU = (
        1902,
        MenuDataType.NORMAL,
        "overlay19",
        "BAR_MAIN_MENU",
        lambda: Overlay19DataProtocol.BAR_MAIN_MENU,
        _("Bar Main Menu"),
    )
    BAR_SUB_MENU_1 = (
        1903,
        MenuDataType.NORMAL,
        "overlay19",
        "BAR_SUBMENU_1",
        lambda: Overlay19DataProtocol.BAR_SUBMENU_1,
        _("Bar Sub Menu") + " 1",
    )
    BAR_SUB_MENU_2 = (
        1904,
        MenuDataType.NORMAL,
        "overlay19",
        "BAR_SUBMENU_2",
        lambda: Overlay19DataProtocol.BAR_SUBMENU_2,
        _("Bar Sub Menu") + " 2",
    )
    RECYCLE_MENU_CONFIRM_1 = (
        2000,
        MenuDataType.NORMAL,
        "overlay20",
        "RECYCLE_MENU_CONFIRM_1",
        lambda: Overlay20DataProtocol.RECYCLE_MENU_CONFIRM_1,
        _("Recycle Menu Confirm") + " 1",
    )
    RECYCLE_MENU_CONFIRM_2 = (
        2001,
        MenuDataType.NORMAL,
        "overlay20",
        "RECYCLE_MENU_CONFIRM_2",
        lambda: Overlay20DataProtocol.RECYCLE_MENU_CONFIRM_2,
        _("Recycle Menu Confirm") + " 2",
    )
    RECYCLE_SUB_MENU_1 = (
        2002,
        MenuDataType.NORMAL,
        "overlay20",
        "RECYCLE_SUBMENU_1",
        lambda: Overlay20DataProtocol.RECYCLE_SUBMENU_1,
        _("Recycle Sub Menu") + " 1",
    )
    RECYCLE_SUB_MENU_2 = (
        2003,
        MenuDataType.NORMAL,
        "overlay20",
        "RECYCLE_SUBMENU_2",
        lambda: Overlay20DataProtocol.RECYCLE_SUBMENU_2,
        _("Recycle Sub Menu") + " 2",
    )
    RECYCLE_MAIN_MENU_1 = (
        2004,
        MenuDataType.NORMAL,
        "overlay20",
        "RECYCLE_MAIN_MENU_1",
        lambda: Overlay20DataProtocol.RECYCLE_MAIN_MENU_1,
        _("Recycle Main Menu") + " 1",
    )
    RECYCLE_MAIN_MENU_2 = (
        2005,
        MenuDataType.NORMAL,
        "overlay20",
        "RECYCLE_MAIN_MENU_2",
        lambda: Overlay20DataProtocol.RECYCLE_MAIN_MENU_2,
        _("Recycle Main Menu") + " 2",
    )
    RECYCLE_MAIN_MENU_3 = (
        2006,
        MenuDataType.NORMAL,
        "overlay20",
        "RECYCLE_MAIN_MENU_3",
        lambda: Overlay20DataProtocol.RECYCLE_MAIN_MENU_3,
        _("Recycle Main Menu") + " 3",
    )
    SYNTH_MENU_CONFIRM = (
        2100,
        MenuDataType.NORMAL,
        "overlay21",
        "SWAP_SHOP_MENU_CONFIRM",
        lambda: Overlay21DataProtocol.SWAP_SHOP_MENU_CONFIRM,
        _("Synthesis Menu Confirm"),
    )
    SYNTH_SUB_MENU_1 = (
        2101,
        MenuDataType.NORMAL,
        "overlay21",
        "SWAP_SHOP_SUBMENU_1",
        lambda: Overlay21DataProtocol.SWAP_SHOP_SUBMENU_1,
        _("Synthesis Sub Menu") + " 1",
    )
    SYNTH_SUB_MENU_2 = (
        2102,
        MenuDataType.NORMAL,
        "overlay21",
        "SWAP_SHOP_SUBMENU_2",
        lambda: Overlay21DataProtocol.SWAP_SHOP_SUBMENU_2,
        _("Synthesis Sub Menu") + " 2",
    )
    SYNTH_MAIN_MENU_1 = (
        2103,
        MenuDataType.NORMAL,
        "overlay21",
        "SWAP_SHOP_MAIN_MENU_1",
        lambda: Overlay21DataProtocol.SWAP_SHOP_MAIN_MENU_1,
        _("Synthesis Main Menu") + " 1",
    )
    SYNTH_MAIN_MENU_2 = (
        2104,
        MenuDataType.NORMAL,
        "overlay21",
        "SWAP_SHOP_MAIN_MENU_2",
        lambda: Overlay21DataProtocol.SWAP_SHOP_MAIN_MENU_2,
        _("Synthesis Main Menu") + " 2",
    )
    SYNTH_SUB_MENU_3 = (
        2105,
        MenuDataType.NORMAL,
        "overlay21",
        "SWAP_SHOP_SUBMENU_3",
        lambda: Overlay21DataProtocol.SWAP_SHOP_SUBMENU_3,
        _("Synthesis Sub Menu") + " 3",
    )
    SHOP_MENU_CONFIRM = (
        2200,
        MenuDataType.NORMAL,
        "overlay22",
        "SHOP_MENU_CONFIRM",
        lambda: Overlay22DataProtocol.SHOP_MENU_CONFIRM,
        _("Shop Menu Confirm"),
    )
    SHOP_MAIN_MENU_1 = (
        2201,
        MenuDataType.NORMAL,
        "overlay22",
        "SHOP_MAIN_MENU_1",
        lambda: Overlay22DataProtocol.SHOP_MAIN_MENU_1,
        _("Shop Main Menu") + " 1",
    )
    SHOP_MAIN_MENU_2 = (
        2202,
        MenuDataType.NORMAL,
        "overlay22",
        "SHOP_MAIN_MENU_2",
        lambda: Overlay22DataProtocol.SHOP_MAIN_MENU_2,
        _("Shop Main Menu") + " 2",
    )
    SHOP_MAIN_MENU_3 = (
        2203,
        MenuDataType.NORMAL,
        "overlay22",
        "SHOP_MAIN_MENU_3",
        lambda: Overlay22DataProtocol.SHOP_MAIN_MENU_3,
        _("Shop Main Menu") + " 3",
    )
    STORAGE_MENU_CONFIRM = (
        2300,
        MenuDataType.NORMAL,
        "overlay23",
        "STORAGE_MENU_CONFIRM",
        lambda: Overlay23DataProtocol.STORAGE_MENU_CONFIRM,
        _("Storage Menu Confirm"),
    )
    STORAGE_MAIN_MENU_1 = (
        2301,
        MenuDataType.NORMAL,
        "overlay23",
        "STORAGE_MAIN_MENU_1",
        lambda: Overlay23DataProtocol.STORAGE_MAIN_MENU_1,
        _("Storage Main Menu") + " 1",
    )
    STORAGE_MAIN_MENU_2 = (
        2302,
        MenuDataType.NORMAL,
        "overlay23",
        "STORAGE_MAIN_MENU_2",
        lambda: Overlay23DataProtocol.STORAGE_MAIN_MENU_2,
        _("Storage Main Menu") + " 2",
    )
    STORAGE_MAIN_MENU_3 = (
        2303,
        MenuDataType.NORMAL,
        "overlay23",
        "STORAGE_MAIN_MENU_3",
        lambda: Overlay23DataProtocol.STORAGE_MAIN_MENU_3,
        _("Storage Main Menu") + " 3",
    )
    STORAGE_MAIN_MENU_4 = (
        2304,
        MenuDataType.NORMAL,
        "overlay23",
        "STORAGE_MAIN_MENU_4",
        lambda: Overlay23DataProtocol.STORAGE_MAIN_MENU_4,
        _("Storage Main Menu") + " 4",
    )
    HATCHER_MENU_CONFIRM = (
        2400,
        MenuDataType.NORMAL,
        "overlay24",
        "DAYCARE_MENU_CONFIRM",
        lambda: Overlay24DataProtocol.DAYCARE_MENU_CONFIRM,
        _("Hatcher Menu Confirm"),
    )
    HATCHER_MAIN_MENU = (
        2401,
        MenuDataType.NORMAL,
        "overlay24",
        "DAYCARE_MAIN_MENU",
        lambda: Overlay24DataProtocol.DAYCARE_MAIN_MENU,
        _("Hatcher Main Menu"),
    )
    APPRAISER_MENU_CONFIRM = (
        2500,
        MenuDataType.NORMAL,
        "overlay25",
        "APPRAISAL_MENU_CONFIRM",
        lambda: Overlay25DataProtocol.APPRAISAL_MENU_CONFIRM,
        _("Appraiser Menu Confirm"),
    )
    APPRAISER_MAIN_MENU = (
        2501,
        MenuDataType.NORMAL,
        "overlay25",
        "APPRAISAL_MAIN_MENU",
        lambda: Overlay25DataProtocol.APPRAISAL_MAIN_MENU,
        _("Appraiser Main Menu"),
    )
    APPRAISER_SUB_MENU = (
        2502,
        MenuDataType.NORMAL,
        "overlay25",
        "APPRAISAL_SUBMENU",
        lambda: Overlay25DataProtocol.APPRAISAL_SUBMENU,
        _("Appraiser Sub Menu"),
    )
    DISCARD_MENU_CONFIRM = (
        2700,
        MenuDataType.NORMAL,
        "overlay27",
        "DISCARD_ITEMS_MENU_CONFIRM",
        lambda: Overlay27DataProtocol.DISCARD_ITEMS_MENU_CONFIRM,
        _("Discard Items Menu Confirm"),
    )
    DISCARD_SUB_MENU_1 = (
        2701,
        MenuDataType.NORMAL,
        "overlay27",
        "DISCARD_ITEMS_SUBMENU_1",
        lambda: Overlay27DataProtocol.DISCARD_ITEMS_SUBMENU_1,
        _("Discard Items Sub Menu") + " 1",
    )
    DISCARD_SUB_MENU_2 = (
        2702,
        MenuDataType.NORMAL,
        "overlay27",
        "DISCARD_ITEMS_SUBMENU_2",
        lambda: Overlay27DataProtocol.DISCARD_ITEMS_SUBMENU_2,
        _("Discard Items Sub Menu") + " 2",
    )
    DISCARD_MAIN_MENU = (
        2703,
        MenuDataType.NORMAL,
        "overlay27",
        "DISCARD_ITEMS_MAIN_MENU",
        lambda: Overlay27DataProtocol.DISCARD_ITEMS_MAIN_MENU,
        _("Discard Items Main Menu"),
    )
    DUNGEON_MAIN_MENU = (
        3100,
        MenuDataType.NORMAL,
        "overlay31",
        "DUNGEON_MAIN_MENU",
        lambda: Overlay31DataProtocol.DUNGEON_MAIN_MENU,
        _("Dungeon Main Menu"),
    )
    DUNGEON_SUB_MENU_1 = (
        3101,
        MenuDataType.NORMAL,
        "overlay31",
        "DUNGEON_SUBMENU_1",
        lambda: Overlay31DataProtocol.DUNGEON_SUBMENU_1,
        _("Dungeon Sub Menu") + " 1",
    )
    DUNGEON_SUB_MENU_2 = (
        3102,
        MenuDataType.NORMAL,
        "overlay31",
        "DUNGEON_SUBMENU_2",
        lambda: Overlay31DataProtocol.DUNGEON_SUBMENU_2,
        _("Dungeon Sub Menu") + " 2",
    )
    DUNGEON_SUB_MENU_3 = (
        3103,
        MenuDataType.NORMAL,
        "overlay31",
        "DUNGEON_SUBMENU_3",
        lambda: Overlay31DataProtocol.DUNGEON_SUBMENU_3,
        _("Dungeon Sub Menu") + " 3",
    )
    DUNGEON_SUB_MENU_4 = (
        3104,
        MenuDataType.NORMAL,
        "overlay31",
        "DUNGEON_SUBMENU_4",
        lambda: Overlay31DataProtocol.DUNGEON_SUBMENU_4,
        _("Dungeon Sub Menu") + " 4",
    )
    DUNGEON_SUB_MENU_5 = (
        3105,
        MenuDataType.NORMAL,
        "overlay31",
        "DUNGEON_SUBMENU_5",
        lambda: Overlay31DataProtocol.DUNGEON_SUBMENU_5,
        _("Dungeon Sub Menu") + " 5",
    )
    DUNGEON_SUB_MENU_6 = (
        3106,
        MenuDataType.NORMAL,
        "overlay31",
        "DUNGEON_SUBMENU_6",
        lambda: Overlay31DataProtocol.DUNGEON_SUBMENU_6,
        _("Dungeon Sub Menu") + " 6",
    )
    UNKNOWN_MENU_CONFIRM = (
        3400,
        MenuDataType.NORMAL,
        "overlay34",
        "START_MENU_CONFIRM",
        lambda: Overlay34DataProtocol.START_MENU_CONFIRM,
        _("Start Menu Confirm"),
    )
    DUNGEON_DEBUG_MENU = (
        3401,
        MenuDataType.NORMAL,
        "overlay34",
        "DUNGEON_DEBUG_MENU",
        lambda: Overlay34DataProtocol.DUNGEON_DEBUG_MENU,
        _("Dungeon Debug Menu"),
    )

    # TODO: There are more menus

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
        self,
        _: int,
        data_type: MenuDataType,
        binary: str,
        block: str,
        _static_block: Any,
        menu_name: str,
    ):
        self.data_type = data_type
        self.binary = binary
        self.block = block
        # This is ONLY used for static type checks; so we get a build error when the name over at
        # pmdsky-debug changes. If that happens, you also NEED to update the name of 'block'.
        self._static_block = _static_block
        self.menu_name = menu_name


class MenuEntry:
    name_id: u16
    description_id: u16
    action: i32

    def __init__(self, name_id: u16, description_id: u16, action: i32):
        self.name_id = name_id
        self.description_id = description_id
        self.action = action


class HardcodedMenus:
    @staticmethod
    def get_menu(menu: MenuType, binary: bytes, config: Pmd2Data) -> List[MenuEntry]:
        """
        Gets one menu
        """
        bin_block = getattr(config.bin_sections, menu.binary)
        block = getattr(bin_block.data, menu.block)
        data = binary[block.address : block.address + block.length]
        menu_list: List[MenuEntry] = []
        for i in range(len(data) // MENU_ENTRY_LEN):
            if menu.data_type == MenuDataType.NORMAL:
                name_id = read_u16(data, i * MENU_ENTRY_LEN)
                description_id = read_u16(data, i * MENU_ENTRY_LEN + 2)
                action = read_i32(data, i * MENU_ENTRY_LEN + 4)
            elif menu.data_type == MenuDataType.ADVANCED:
                action = read_i32(data, i * MENU_ENTRY_LEN)
                name_id = read_u16(data, i * MENU_ENTRY_LEN + 4)
                description_id = read_u16(data, i * MENU_ENTRY_LEN + 6)
            menu_list.append(MenuEntry(name_id, description_id, action))
        return menu_list

    @staticmethod
    def set_menu(
        menu: MenuType, menu_data: List[MenuEntry], binary: bytearray, config: Pmd2Data
    ) -> None:
        """
        Sets one menu
        """
        bin_block = getattr(config.bin_sections, menu.binary)
        block = getattr(bin_block.data, menu.block)
        data = bytearray(len(menu_data) * MENU_ENTRY_LEN)
        if len(data) != block.length:
            # noinspection PyUnusedLocal
            num_entries = block.length // MENU_ENTRY_LEN
            raise Exception(f(_("This menu must have {num_entries} entries!")))
        for i, m in enumerate(menu_data):
            if menu.data_type == MenuDataType.NORMAL:
                write_u16(data, m.name_id, i * MENU_ENTRY_LEN)
                write_u16(data, m.description_id, i * MENU_ENTRY_LEN + 2)
                write_i32(data, m.action, i * MENU_ENTRY_LEN + 4)
            elif menu.data_type == MenuDataType.ADVANCED:
                write_i32(data, m.action, i * MENU_ENTRY_LEN)
                write_u16(data, m.name_id, i * MENU_ENTRY_LEN + 4)
                write_u16(data, m.description_id, i * MENU_ENTRY_LEN + 6)
        binary[block.address : block.address + block.length] = data
