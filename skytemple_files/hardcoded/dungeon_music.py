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
from typing import List, Tuple, Optional

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import read_uintle, write_uintle, AutoString


class DungeonMusicEntry(AutoString):
    def __init__(self, data: Optional[int], track_ref: int = None, is_random_ref: bool = False):
        if track_ref is not None:
            self.track_or_ref = track_ref
            self.is_random_ref = is_random_ref
        else:
            self.track_or_ref = data & ~0x8000
            self.is_random_ref = data & 0x8000 > 0
            assert data == self.to_int()

    def to_int(self) -> int:
        if self.is_random_ref:
            return 0x8000 + self.track_or_ref
        return self.track_or_ref


class HardcodedDungeonMusic:
    @staticmethod
    def get_music_list(ov10: bytes, config: Pmd2Data) -> List[DungeonMusicEntry]:
        block = config.binaries['overlay/overlay_0010.bin'].blocks['MusicList']
        lst = []
        for i in range(block.begin, block.end, 2):
            lst.append(DungeonMusicEntry(
                read_uintle(ov10, i, 2),
            ))
        return lst

    @staticmethod
    def set_music_list(value: List[DungeonMusicEntry], ov10: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0010.bin'].blocks['MusicList']
        expected_length = int((block.end - block.begin) / 2)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            write_uintle(ov10, entry.to_int(), block.begin + i * 2, 2)

    @staticmethod
    def get_random_music_list(ov10: bytes, config: Pmd2Data) -> List[Tuple[int, int, int, int]]:
        block = config.binaries['overlay/overlay_0010.bin'].blocks['RandomMusicList']
        lst = []
        for i in range(block.begin, block.end, 8):
            lst.append((
                read_uintle(ov10, i, 2),
                read_uintle(ov10, i + 2, 2),
                read_uintle(ov10, i + 4, 2),
                read_uintle(ov10, i + 6, 2),
            ))
        return lst

    @staticmethod
    def set_random_music_list(value: List[Tuple[int, int, int, int]], ov10: bytearray, config: Pmd2Data):
        block = config.binaries['overlay/overlay_0010.bin'].blocks['RandomMusicList']
        expected_length = int((block.end - block.begin) / 8)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, (a, b, c, d) in enumerate(value):
            write_uintle(ov10, a, block.begin + i * 8 + 0, 2)
            write_uintle(ov10, b, block.begin + i * 8 + 2, 2)
            write_uintle(ov10, c, block.begin + i * 8 + 4, 2)
            write_uintle(ov10, d, block.begin + i * 8 + 6, 2)
