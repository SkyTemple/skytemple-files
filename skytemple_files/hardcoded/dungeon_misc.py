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
from __future__ import annotations

from math import ceil

from range_typed_integers import u32_checked

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import *


class HardcodedDungeonMisc:
    @staticmethod
    def get_burn_damage_delay(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.binaries["overlay/overlay_0010.bin"].symbols["BurnDamageDelay"]
        return read_u16(ov10, block.begin)

    @staticmethod
    def set_burn_damage_delay(value: u16, ov10: bytearray, config: Pmd2Data) -> None:
        block = config.binaries["overlay/overlay_0010.bin"].symbols["BurnDamageDelay"]
        write_u16(ov10, value, block.begin)

    @staticmethod
    def get_poison_damage_delay(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.binaries["overlay/overlay_0010.bin"].symbols["PoisonDamageDelay"]
        return read_u16(ov10, block.begin)

    @staticmethod
    def set_poison_damage_delay(value: u16, ov10: bytearray, config: Pmd2Data) -> None:
        block = config.binaries["overlay/overlay_0010.bin"].symbols["PoisonDamageDelay"]
        write_u16(ov10, value, block.begin)

    @staticmethod
    def get_bad_poison_damage_delay(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.binaries["overlay/overlay_0010.bin"].symbols[
            "BadPoisonDamageDelay"
        ]
        return read_u16(ov10, block.begin)

    @staticmethod
    def set_bad_poison_damage_delay(
        value: u16, ov10: bytearray, config: Pmd2Data
    ) -> None:
        block = config.binaries["overlay/overlay_0010.bin"].symbols[
            "BadPoisonDamageDelay"
        ]
        write_u16(ov10, value, block.begin)

    @staticmethod
    def get_ginseng_increase_by_3_chance(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.binaries["overlay/overlay_0010.bin"].symbols["GinsengChance3"]
        return read_u16(ov10, block.begin)

    @staticmethod
    def set_ginseng_increase_by_3_chance(
        value: u16, ov10: bytearray, config: Pmd2Data
    ) -> None:
        block = config.binaries["overlay/overlay_0010.bin"].symbols["GinsengChance3"]
        write_u16(ov10, value, block.begin)

    @staticmethod
    def get_belly_loss_turn(ov29: bytes, config: Pmd2Data) -> float:
        block = config.binaries["overlay/overlay_0029.bin"].symbols["BellyLostTurn"]
        return read_u32(ov29, block.begin) / 0x10000

    @staticmethod
    def set_belly_loss_turn(value: float, ov29: bytearray, config: Pmd2Data) -> None:
        block = config.binaries["overlay/overlay_0029.bin"].symbols["BellyLostTurn"]
        write_u32(ov29, u32_checked(ceil(value * 0x10000)), block.begin)

    @staticmethod
    def get_belly_loss_walk_through_walls(ov29: bytes, config: Pmd2Data) -> u16:
        block = config.binaries["overlay/overlay_0029.bin"].symbols["BellyLostWtw"]
        return read_u16(ov29, block.begin)

    @staticmethod
    def set_belly_loss_walk_through_walls(
        value: u16, ov29: bytearray, config: Pmd2Data
    ) -> None:
        block = config.binaries["overlay/overlay_0029.bin"].symbols["BellyLostWtw"]
        write_u16(ov29, value, block.begin)

    @staticmethod
    def get_belly_loss_1000ile_walk_through_walls(ov29: bytes, config: Pmd2Data) -> u16:
        block = config.binaries["overlay/overlay_0029.bin"].symbols["BellyLostWtw1000"]
        return read_u16(ov29, block.begin)

    @staticmethod
    def set_belly_loss_1000ile_walk_through_walls(
        value: u16, ov29: bytearray, config: Pmd2Data
    ) -> None:
        block = config.binaries["overlay/overlay_0029.bin"].symbols["BellyLostWtw1000"]
        write_u16(ov29, value, block.begin)
