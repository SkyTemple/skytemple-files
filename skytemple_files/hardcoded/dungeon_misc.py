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

from math import ceil

from range_typed_integers import u32_checked, u16

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import write_u16, read_u16, read_u32, write_u32


class HardcodedDungeonMisc:
    @staticmethod
    def get_burn_damage_delay(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.overlay10.data.BURN_DAMAGE_COOLDOWN
        return read_u16(ov10, block.address)

    @staticmethod
    def set_burn_damage_delay(value: u16, ov10: bytearray, config: Pmd2Data) -> None:
        block = config.bin_sections.overlay10.data.BURN_DAMAGE_COOLDOWN
        write_u16(ov10, value, block.address)

    @staticmethod
    def get_poison_damage_delay(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.overlay10.data.POISON_DAMAGE_COOLDOWN
        return read_u16(ov10, block.address)

    @staticmethod
    def set_poison_damage_delay(value: u16, ov10: bytearray, config: Pmd2Data) -> None:
        block = config.bin_sections.overlay10.data.POISON_DAMAGE_COOLDOWN
        write_u16(ov10, value, block.address)

    @staticmethod
    def get_bad_poison_damage_delay(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.overlay10.data.BAD_POISON_DAMAGE_COOLDOWN
        return read_u16(ov10, block.address)

    @staticmethod
    def set_bad_poison_damage_delay(
        value: u16, ov10: bytearray, config: Pmd2Data
    ) -> None:
        block = config.bin_sections.overlay10.data.BAD_POISON_DAMAGE_COOLDOWN
        write_u16(ov10, value, block.address)

    @staticmethod
    def get_ginseng_increase_by_3_chance(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.overlay10.data.GINSENG_CHANCE_3
        return read_u16(ov10, block.address)

    @staticmethod
    def set_ginseng_increase_by_3_chance(
        value: u16, ov10: bytearray, config: Pmd2Data
    ) -> None:
        block = config.bin_sections.overlay10.data.GINSENG_CHANCE_3
        write_u16(ov10, value, block.address)

    @staticmethod
    def get_belly_loss_turn(ov29: bytes, config: Pmd2Data) -> float:
        block = config.bin_sections.overlay29.data.BELLY_LOST_PER_TURN
        return read_u32(ov29, block.address) / 0x10000

    @staticmethod
    def set_belly_loss_turn(value: float, ov29: bytearray, config: Pmd2Data) -> None:
        block = config.bin_sections.overlay29.data.BELLY_LOST_PER_TURN
        write_u32(ov29, u32_checked(ceil(value * 0x10000)), block.address)

    @staticmethod
    def get_belly_loss_walk_through_walls(ov29: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.overlay29.data.BELLY_DRAIN_IN_WALLS_INT
        return read_u16(ov29, block.address)

    @staticmethod
    def set_belly_loss_walk_through_walls(
        value: u16, ov29: bytearray, config: Pmd2Data
    ) -> None:
        block = config.bin_sections.overlay29.data.BELLY_DRAIN_IN_WALLS_INT
        write_u16(ov29, value, block.address)

    @staticmethod
    def get_belly_loss_1000ile_walk_through_walls(ov29: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.overlay29.data.BELLY_DRAIN_IN_WALLS_THOUSANDTHS
        return read_u16(ov29, block.address)

    @staticmethod
    def set_belly_loss_1000ile_walk_through_walls(
        value: u16, ov29: bytearray, config: Pmd2Data
    ) -> None:
        block = config.bin_sections.overlay29.data.BELLY_DRAIN_IN_WALLS_THOUSANDTHS
        write_u16(ov29, value, block.address)
