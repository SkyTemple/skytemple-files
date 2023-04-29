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

from typing import Optional, List, Tuple

from range_typed_integers import u16

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import (
    AutoString,
    read_u16,
    write_u16,
)


class DungeonMusicEntry(AutoString):
    track_or_ref: u16
    is_random_ref: bool

    def __init__(
        self,
        data: Optional[u16],
        track_ref: Optional[u16] = None,
        is_random_ref: bool = False,
    ):
        if track_ref is not None:
            self.track_or_ref = track_ref
            self.is_random_ref = is_random_ref
        else:
            assert data is not None
            self.track_or_ref = u16(data & ~0x8000)
            self.is_random_ref = data & 0x8000 > 0
            assert data == self.to_int()

    def to_int(self) -> u16:
        if self.is_random_ref:
            return u16(0x8000 + self.track_or_ref)
        return self.track_or_ref


class HardcodedDungeonMusic:
    @staticmethod
    def get_music_list(ov10: bytes, config: Pmd2Data) -> List[DungeonMusicEntry]:
        block = config.bin_sections.overlay10.data.MUSIC_ID_TABLE
        lst = []
        for i in range(block.address, block.address + block.length, 2):
            lst.append(
                DungeonMusicEntry(
                    read_u16(ov10, i),
                )
            )
        return lst

    @staticmethod
    def set_music_list(
        value: List[DungeonMusicEntry], ov10: bytearray, config: Pmd2Data
    ) -> None:
        block = config.bin_sections.overlay10.data.MUSIC_ID_TABLE
        assert block.length is not None
        expected_length = int(block.length / 2)
        if len(value) != expected_length:
            raise ValueError(
                f"The list must have exactly the length of {expected_length} entries."
            )
        for i, entry in enumerate(value):
            write_u16(ov10, entry.to_int(), block.address + i * 2)

    @staticmethod
    def get_random_music_list(
        ov10: bytes, config: Pmd2Data
    ) -> List[Tuple[u16, u16, u16, u16]]:
        block = config.bin_sections.overlay10.data.RANDOM_MUSIC_ID_TABLE
        lst = []
        for i in range(block.address, block.address + block.length, 8):
            lst.append(
                (
                    read_u16(ov10, i),
                    read_u16(ov10, i + 2),
                    read_u16(ov10, i + 4),
                    read_u16(ov10, i + 6),
                )
            )
        return lst

    @staticmethod
    def set_random_music_list(
        value: List[Tuple[u16, u16, u16, u16]], ov10: bytearray, config: Pmd2Data
    ) -> None:
        block = config.bin_sections.overlay10.data.RANDOM_MUSIC_ID_TABLE
        assert block.length is not None
        expected_length = int(block.length / 8)
        if len(value) != expected_length:
            raise ValueError(
                f"The list must have exactly the length of {expected_length} entries."
            )
        for i, (a, b, c, d) in enumerate(value):
            write_u16(ov10, a, block.address + i * 8 + 0)
            write_u16(ov10, b, block.address + i * 8 + 2)
            write_u16(ov10, c, block.address + i * 8 + 4)
            write_u16(ov10, d, block.address + i * 8 + 6)
