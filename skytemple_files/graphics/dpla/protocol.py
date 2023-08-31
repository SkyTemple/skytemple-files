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
from abc import abstractmethod
from itertools import islice
from typing import Protocol, Sequence, List

from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable


class DplaProtocol(Sir0Serializable, Protocol):
    colors: Sequence[Sequence[int]]
    durations_per_frame_for_colors: Sequence[int]

    @abstractmethod
    def __init__(self, data: bytes, pointer_to_pointers: int):
        ...

    @abstractmethod
    def get_palette_for_frame(self, pal_idx: int, frame_id: int) -> List[int]:
        """
        Returns the color palette at the given frame id. Returned is a stream of RGB colors: [R, G, B, R, G, B...].
        Returned are always 16 colors. If the palette file has more than 16 colors, the pal_idx specifies what set
        of 16 colors to return.
        """
        ...

    @abstractmethod
    def has_for_palette(self, palette_idx: int) -> bool:
        ...

    @abstractmethod
    def get_frame_count_for_palette(self, palette_idx: int) -> int:
        ...

    @abstractmethod
    def enable_for_palette(self, palid: int) -> None:
        ...

    @abstractmethod
    def disable_for_palette(self, palid: int) -> None:
        ...

    @abstractmethod
    def get_duration_for_palette(self, palette_idx: int) -> int:
        """
        Warning: Colors in-game are animated separately. There is no speed for an entire palette.
        We are asuming there's one speed for the entire palette.
        This could be inaccurate.
        """
        ...

    @abstractmethod
    def set_duration_for_palette(self, palid: int, duration: int) -> None:
        """
        Warning: Colors in-game are animated separately. There is no speed for an entire palette.
        We are asuming there's one speed for the entire palette.
        This could be inaccurate.
        """
        ...

    @abstractmethod
    def apply_palette_animations(
        self, palettes: Sequence[Sequence[int]], frame_idx: int
    ) -> List[List[int]]:
        """
        Returns a modified copy of `palettes`.

        This copy is modified to have colors swapped out for the current frame of palette animation.
        > The first 16 colors of the DPLA model are placed in the palette 11 (if color 0 has at least one frame).
        > The second 16 colors of the DPLA model are placed in the palette 12 (if color 16 has at least one frame).
        > If the model has more colors, they are ignored.

        Warning: Colors in-game are animated separately. There is no speed for an entire palette.
        We are asuming there's one speed for the entire palette.
        This could be inaccurate.
        """
        ...


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())
