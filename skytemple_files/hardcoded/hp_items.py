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

from range_typed_integers import u16

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_u16, write_u16


class HardcodedHpItems:
    @staticmethod
    def get_life_seed_hp(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.overlay10.data.LIFE_SEED_HP_BOOST
        return read_u16(ov10, block.address)

    @staticmethod
    def set_life_seed_hp(value: u16, ov10: bytearray, config: Pmd2Data) -> None:
        block = config.bin_sections.overlay10.data.LIFE_SEED_HP_BOOST
        write_u16(ov10, value, block.address)

    @staticmethod
    def get_sitrus_berry_hp(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.overlay10.data.SITRUS_BERRY_HP_RESTORATION
        return read_u16(ov10, block.address)

    @staticmethod
    def set_sitrus_berry_hp(value: u16, ov10: bytearray, config: Pmd2Data) -> None:
        block = config.bin_sections.overlay10.data.SITRUS_BERRY_HP_RESTORATION
        write_u16(ov10, value, block.address)

    @staticmethod
    def get_oran_berry_hp(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.overlay10.data.ORAN_BERRY_HP_RESTORATION
        return read_u16(ov10, block.address)

    @staticmethod
    def set_oran_berry_hp(value: u16, ov10: bytearray, config: Pmd2Data) -> None:
        block = config.bin_sections.overlay10.data.ORAN_BERRY_HP_RESTORATION
        write_u16(ov10, value, block.address)
