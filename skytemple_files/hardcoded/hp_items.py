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


class HardcodedHpItems:
    @staticmethod
    def get_life_seed_hp(ov10: bytes, config: Pmd2Data) -> int:
        block = config.binaries['overlay/overlay_0010.bin'].blocks['LifeSeedHP']
        return read_uintle(ov10, block.begin, 2)

    @staticmethod
    def set_life_seed_hp(value: int, ov10: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0010.bin'].blocks['LifeSeedHP']
        write_uintle(ov10, value, block.begin, 2)

    @staticmethod
    def get_sitrus_berry_hp(ov10: bytes, config: Pmd2Data) -> int:
        block = config.binaries['overlay/overlay_0010.bin'].blocks['SitrusBerryHP']
        return read_uintle(ov10, block.begin, 2)

    @staticmethod
    def set_sitrus_berry_hp(value: int, ov10: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0010.bin'].blocks['SitrusBerryHP']
        write_uintle(ov10, value, block.begin, 2)

    @staticmethod
    def get_oran_berry_hp(ov10: bytes, config: Pmd2Data) -> int:
        block = config.binaries['overlay/overlay_0010.bin'].blocks['OranBerryHP']
        return read_uintle(ov10, block.begin, 2)

    @staticmethod
    def set_oran_berry_hp(value: int, ov10: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0010.bin'].blocks['OranBerryHP']
        write_uintle(ov10, value, block.begin, 2)
