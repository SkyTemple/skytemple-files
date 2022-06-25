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

from range_typed_integers import u8

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_u8, write_u8


class HardcodedTextSpeed:
    @staticmethod
    def get_text_speed(arm9: bytes, config: Pmd2Data) -> u8:
        block = config.bin_sections.arm9.data.TEXT_SPEED
        return read_u8(arm9, block.address)

    @staticmethod
    def set_text_speed(value: u8, arm9: bytearray, config: Pmd2Data) -> None:
        block = config.bin_sections.arm9.data.TEXT_SPEED
        write_u8(arm9, value, block.address)
