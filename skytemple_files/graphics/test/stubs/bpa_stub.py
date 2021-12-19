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
from dataclasses import dataclass
from typing import Sequence, List

from PIL import Image

from skytemple_files.graphics.bpa.protocol import BpaProtocol, BpaFrameInfoProtocol


# Testing stub class
class BpaFrameInfoStub(BpaFrameInfoProtocol):
    def __init__(self, duration_per_frame: int, unk2: int):
        self.duration_per_frame = duration_per_frame
        self.unk2 = unk2


# Testing stub class
@dataclass
class BpaStub(BpaProtocol[BpaFrameInfoStub]):
    def __init__(self, data: bytes):
        self.stub_init_data = data
        self.number_of_tiles: int = 0
        self.number_of_frames: int = 0
        self.tiles: List[bytearray] = []
        self.frame_info: List[BpaFrameInfoStub] = []

    def get_tile(self, tile_idx: int, frame_idx: int) -> bytes:
        raise NotImplementedError("Not implemented on stub.")

    def tiles_to_pil_separate(self, palette: List[int], width_in_tiles: int = 20) -> List[Image.Image]:
        raise NotImplementedError("Not implemented on stub.")

    def pil_to_tiles(self, image: Image.Image) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def pil_to_tiles_separate(self, images: List[Image.Image]) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def tiles_for_frame(self, frame: int) -> Sequence[bytearray]:
        raise NotImplementedError("Not implemented on stub.")
