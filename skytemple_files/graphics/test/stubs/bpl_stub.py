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


# Testing stub class
from typing import List

from skytemple_files.graphics.bpl.protocol import BplProtocol, BplAnimationSpecProtocol


class BplAnimationSpecStub(BplAnimationSpecProtocol):
    def __init__(self, duration_per_frame: int, number_of_frames: int):
        self.duration_per_frame = duration_per_frame
        self.number_of_frames = number_of_frames


class BplStub(BplProtocol[BplAnimationSpecStub]):
    def __init__(self, data: bytes) -> None:
        self.stub_init_data = data
        self.number_palettes: int = 0
        self.has_palette_animation: bool = False
        self.palettes: List[List[int]] = []
        self.animation_specs: List[BplAnimationSpecStub] = []
        self.animation_palette: List[List[int]] = []

    def import_palettes(self, palettes: List[List[int]]) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def apply_palette_animations(self, frame: int) -> List[List[int]]:
        raise NotImplementedError("Not implemented on stub.")

    def is_palette_affected_by_animation(self, pal_idx: int) -> bool:
        raise NotImplementedError("Not implemented on stub.")

    def get_real_palettes(self) -> List[List[int]]:
        raise NotImplementedError("Not implemented on stub.")

    def set_palettes(self, palettes: List[List[int]]) -> None:
        raise NotImplementedError("Not implemented on stub.")
