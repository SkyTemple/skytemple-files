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

from abc import abstractmethod
from typing import List, Protocol, Sequence, TypeVar, runtime_checkable

from range_typed_integers import u16


@runtime_checkable
class BplAnimationSpecProtocol(Protocol):
    duration_per_frame: u16
    number_of_frames: u16

    @abstractmethod
    def __init__(self, duration_per_frame: u16, number_of_frames: u16):
        ...


T = TypeVar("T", bound=BplAnimationSpecProtocol)


@runtime_checkable
class BplProtocol(Protocol[T]):
    number_palettes: u16
    has_palette_animation: bool
    palettes: Sequence[Sequence[int]]
    animation_specs: Sequence[T]
    animation_palette: Sequence[Sequence[int]]

    @abstractmethod
    def __init__(self, data: bytes) -> None:
        ...

    @abstractmethod
    def import_palettes(self, palettes: List[List[int]]) -> None:
        """
        Replace all palettes with the ones passed in
        Animated palette is not changed, but the number of spec entries is adjusted.
        """
        ...

    @abstractmethod
    def apply_palette_animations(self, frame: int) -> List[List[int]]:
        """
        Returns a modified copy of self.palettes.

        This copy is modified to have colors swapped out for the current frame of palette animation.
        The information for this is stored in self.animation_specs and the animation palette in
        self.animation_palette.

        Only available if self.has_palette_animation.

        The maximum number of frames is the length of self.animation_palette
        """
        ...

    @abstractmethod
    def is_palette_affected_by_animation(self, pal_idx: int) -> bool:
        """Returns whether or not the palette with that index is affected by animation."""
        ...

    @abstractmethod
    def get_real_palettes(self) -> List[List[int]]:
        """Gets the actual palettes defined (without dummy grayscale entries)."""
        ...

    @abstractmethod
    def set_palettes(self, palettes: List[List[int]]) -> None:
        """Sets the palette properly, adding dummy grayscale entries if needed."""
        ...
