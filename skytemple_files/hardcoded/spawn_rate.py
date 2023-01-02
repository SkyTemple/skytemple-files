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

# Normal spawn delay (0x24): [EU]overlay_0010:0x7A74 / [US]overlay_0010:0x7A5C
# Spawn delay after stealing from a shop (3): [EU]overlay_0010:0x7BD8 / [US]overlay_0010:0x7BC0
from range_typed_integers import u16

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_u16, write_u16


class HardcodedSpawnRate:
    @staticmethod
    def get_normal_spawn_rate(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.overlay10.data.SPAWN_COOLDOWN
        return read_u16(ov10, block.address)

    @staticmethod
    def set_normal_spawn_rate(value: u16, ov10: bytearray, config: Pmd2Data) -> None:
        block = config.bin_sections.overlay10.data.SPAWN_COOLDOWN
        write_u16(ov10, value, block.address)

    @staticmethod
    def get_stolen_spawn_rate(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.overlay10.data.SPAWN_COOLDOWN_THIEF_ALERT
        return read_u16(ov10, block.address)

    @staticmethod
    def set_stolen_spawn_rate(value: u16, ov10: bytearray, config: Pmd2Data) -> None:
        block = config.bin_sections.overlay10.data.SPAWN_COOLDOWN_THIEF_ALERT
        write_u16(ov10, value, block.address)
