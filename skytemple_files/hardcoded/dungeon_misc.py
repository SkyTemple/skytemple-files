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
from math import ceil

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_uintle, write_uintle


class HardcodedDungeonMisc:
    @staticmethod
    def get_burn_damage_delay(ov10: bytes, config: Pmd2Data) -> int:
        block = config.binaries['overlay/overlay_0010.bin'].blocks['BurnDamageDelay']
        return read_uintle(ov10, block.begin, 2)

    @staticmethod
    def set_burn_damage_delay(value: int, ov10: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0010.bin'].blocks['BurnDamageDelay']
        write_uintle(ov10, value, block.begin, 2)

    @staticmethod
    def get_poison_damage_delay(ov10: bytes, config: Pmd2Data) -> int:
        block = config.binaries['overlay/overlay_0010.bin'].blocks['PoisonDamageDelay']
        return read_uintle(ov10, block.begin, 2)

    @staticmethod
    def set_poison_damage_delay(value: int, ov10: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0010.bin'].blocks['PoisonDamageDelay']
        write_uintle(ov10, value, block.begin, 2)

    @staticmethod
    def get_bad_poison_damage_delay(ov10: bytes, config: Pmd2Data) -> int:
        block = config.binaries['overlay/overlay_0010.bin'].blocks['BadPoisonDamageDelay']
        return read_uintle(ov10, block.begin, 2)

    @staticmethod
    def set_bad_poison_damage_delay(value: int, ov10: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0010.bin'].blocks['BadPoisonDamageDelay']
        write_uintle(ov10, value, block.begin, 2)

    @staticmethod
    def get_ginseng_increase_by_3_chance(ov10: bytes, config: Pmd2Data) -> int:
        block = config.binaries['overlay/overlay_0010.bin'].blocks['GinsengChance3']
        return read_uintle(ov10, block.begin, 2)

    @staticmethod
    def set_ginseng_increase_by_3_chance(value: int, ov10: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0010.bin'].blocks['GinsengChance3']
        write_uintle(ov10, value, block.begin, 2)

    @staticmethod
    def get_belly_loss_turn(ov29: bytes, config: Pmd2Data) -> float:
        block = config.binaries['overlay/overlay_0029.bin'].blocks['BellyLostTurn']
        return read_uintle(ov29, block.begin, 4) / 0x10000

    @staticmethod
    def set_belly_loss_turn(value: float, ov29: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0029.bin'].blocks['BellyLostTurn']
        write_uintle(ov29, ceil(value * 0x10000), block.begin, 4)

    @staticmethod
    def get_belly_loss_walk_through_walls(ov29: bytes, config: Pmd2Data) -> int:
        block = config.binaries['overlay/overlay_0029.bin'].blocks['BellyLostWtw']
        return read_uintle(ov29, block.begin, 2)

    @staticmethod
    def set_belly_loss_walk_through_walls(value: int, ov29: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0029.bin'].blocks['BellyLostWtw']
        write_uintle(ov29, value, block.begin, 2)

    @staticmethod
    def get_belly_loss_1000ile_walk_through_walls(ov29: bytes, config: Pmd2Data) -> int:
        block = config.binaries['overlay/overlay_0029.bin'].blocks['BellyLostWtw1000']
        return read_uintle(ov29, block.begin, 2)

    @staticmethod
    def set_belly_loss_1000ile_walk_through_walls(value: int, ov29: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0029.bin'].blocks['BellyLostWtw1000']
        write_uintle(ov29, value, block.begin, 2)
