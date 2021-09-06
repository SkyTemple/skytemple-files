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
from typing import List

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_sintle, write_sintle

ENTRY_LEN = 2


class HardcodedTactics:
    @staticmethod
    def get_unlock_levels(arm9: bytes, config: Pmd2Data) -> List[int]:
        block = config.binaries['arm9.bin'].blocks['TacticsUnlockLevel']
        lst = []
        for i in range(block.begin, block.end, ENTRY_LEN):
            lst.append(read_sintle(arm9, i, 2))
        return lst

    @staticmethod
    def set_unlock_levels(value: List[int], arm9: bytearray, config: Pmd2Data):
        block = config.binaries['arm9.bin'].blocks['TacticsUnlockLevel']
        expected_length = int((block.end - block.begin) / ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            write_sintle(arm9, entry, block.begin + i * ENTRY_LEN, 2)
