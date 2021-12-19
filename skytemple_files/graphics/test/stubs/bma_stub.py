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
from typing import Optional, List, Sequence

from PIL import Image

from skytemple_files.graphics.bma.protocol import BmaProtocol, P, C, L


class BmaStub(BmaProtocol[P, C, L]):
    def __init__(self, data: bytes):
        self.stub_init_data = data
        self.map_width_camera: int = 0
        self.map_height_camera: int = 0
        self.tiling_width: int = 0
        self.tiling_height: int = 0
        self.map_width_chunks: int = 0
        self.map_height_chunks: int = 0
        self.number_of_layers: int = 0
        self.unk6: int = 0
        self.number_of_collision_layers: int = 0
        self.layer0: List[int] = []
        self.layer1: Optional[List[int]] = None
        self.unknown_data_block: Optional[List[int]] = None
        self.collision: Optional[List[bool]] = None
        self.collision2: Optional[List[bool]] = None

    def to_pil_single_layer(self, bpc: C, palettes: List[List[int]], bpas: Sequence[P], layer: int) -> Image.Image:
        raise NotImplementedError("Not implemented on stub.")

    def to_pil(self, bpc: C, bpl: L, bpas: List[Optional[P]], include_collision: bool = True,
               include_unknown_data_block: bool = True, pal_ani: bool = True, single_frame: bool = False) -> List[Image.Image]:
        raise NotImplementedError("Not implemented on stub.")

    def from_pil(self, bpc: C, bpl: L, lower_img: Optional[Image.Image] = None, upper_img: Optional[Image.Image] = None,
                 force_import: bool = False, how_many_palettes_lower_layer: int = 16) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def remove_upper_layer(self) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def add_upper_layer(self) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def resize(self, new_width_chunks: int, new_height_chunks: int, new_width_camera: int,
               new_height_camera: int) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def place_chunk(self, layer_id: int, x: int, y: int, chunk_index: int) -> None:
        raise NotImplementedError("Not implemented on stub.")
