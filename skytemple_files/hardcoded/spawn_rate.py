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

# Normal spawn delay (0x24): [EU]overlay_0010:0x7A74 / [US]overlay_0010:0x7A5C
# Spawn delay after stealing from a shop (3): [EU]overlay_0010:0x7BD8 / [US]overlay_0010:0x7BC0
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_uintle, write_uintle


class HardcodedSpawnRate:
    @staticmethod
    def get_normal_spawn_rate(ov10: bytes, config: Pmd2Data) -> int:
        block = config.binaries['overlay/overlay_0010.bin'].blocks['SpawnDelayNormal']
        return read_uintle(ov10, block.begin, 2)

    @staticmethod
    def set_normal_spawn_rate(value: int, ov10: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0010.bin'].blocks['SpawnDelayNormal']
        write_uintle(ov10, value, block.begin, 2)
        
    @staticmethod
    def get_stolen_spawn_rate(ov10: bytes, config: Pmd2Data) -> int:
        block = config.binaries['overlay/overlay_0010.bin'].blocks['SpawnDelayStealing']
        return read_uintle(ov10, block.begin, 2)

    @staticmethod
    def set_stolen_spawn_rate(value: int, ov10: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0010.bin'].blocks['SpawnDelayStealing']
        write_uintle(ov10, value, block.begin, 2)
