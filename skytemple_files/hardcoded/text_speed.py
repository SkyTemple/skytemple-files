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

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_uintle, write_uintle


class HardcodedTextSpeed:
    @staticmethod
    def get_text_speed(arm9: bytes, config: Pmd2Data) -> int:
        block = config.binaries['arm9.bin'].blocks['TextSpeedConstant']
        return read_uintle(arm9, block.begin)

    @staticmethod
    def set_text_speed(value: int, arm9: bytearray, config: Pmd2Data):
        block = config.binaries['arm9.bin'].blocks['TextSpeedConstant']
        write_uintle(arm9, value, block.begin)
