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
from typing import List, Sequence, Optional

from PIL import Image

from skytemple_files.common.protocol import TilemapEntryProtocol
from skytemple_files.graphics.bpc.protocol import BpcProtocol, BpcLayerProtocol, P


class BpcLayerStub(BpcLayerProtocol):
    def __init__(
            self, number_tiles: int, bpas: List[int], chunk_tilemap_len: int,
            tiles: List[bytearray], tilemap: List[TilemapEntryProtocol]
    ) -> None:
        self.number_tiles = number_tiles
        self.bpas = bpas
        self.chunk_tilemap_len = chunk_tilemap_len
        self.tiles = tiles
        self.tilemap = tilemap


class BpcStub(BpcProtocol[BpcLayerStub, P]):
    def __init__(self, data: bytes, tiling_width: int, tiling_height: int):
        self.stub_init_data = data
        self.tiling_width = tiling_width
        self.tiling_height = tiling_height
        self.number_of_layers: int = 0
        self.layers: List[BpcLayerStub] = []

    def chunks_to_pil(self, layer: int, palettes: Sequence[Sequence[int]], width_in_mtiles: int = 20) -> Image.Image:
        raise NotImplementedError("Not implemented on stub.")

    def single_chunk_to_pil(self, layer: int, chunk_idx: int, palettes: Sequence[Sequence[int]]) -> Image.Image:
        raise NotImplementedError("Not implemented on stub.")

    def tiles_to_pil(self, layer: int, palettes: Sequence[Sequence[int]], width_in_tiles: int = 20,
                     single_palette: Optional[int] = None) -> Image.Image:
        raise NotImplementedError("Not implemented on stub.")

    def chunks_animated_to_pil(self, layer: int, palettes: Sequence[Sequence[int]], bpas: Sequence[Optional[P]],
                               width_in_mtiles: int = 20) -> List[Image.Image]:
        raise NotImplementedError("Not implemented on stub.")

    def single_chunk_animated_to_pil(self, layer: int, chunk_idx: int, palettes: Sequence[Sequence[int]],
                                     bpas: Sequence[Optional[P]]) -> List[Image.Image]:
        raise NotImplementedError("Not implemented on stub.")

    def pil_to_tiles(self, layer: int, image: Image.Image) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def pil_to_chunks(self, layer: int, image: Image.Image, force_import: bool = True) -> List[List[int]]:
        raise NotImplementedError("Not implemented on stub.")

    def get_tile(self, layer: int, index: int) -> TilemapEntryProtocol:
        raise NotImplementedError("Not implemented on stub.")

    def set_tile(self, layer: int, index: int, tile_mapping: TilemapEntryProtocol) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def get_chunk(self, layer: int, index: int) -> Sequence[TilemapEntryProtocol]:
        raise NotImplementedError("Not implemented on stub.")

    def import_tiles(self, layer: int, tiles: List[bytearray], contains_null_tile: bool = False) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def import_tile_mappings(self, layer: int, tile_mappings: List[TilemapEntryProtocol],
                             contains_null_chunk: bool = False, correct_tile_ids: bool = True) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def get_bpas_for_layer(self, layer: int, bpas_from_bg_list: Sequence[Optional[P]]) -> List[P]:
        raise NotImplementedError("Not implemented on stub.")

    def set_chunk(self, layer: int, index: int, new_tilemappings: Sequence[TilemapEntryProtocol]) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def remove_upper_layer(self) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def add_upper_layer(self) -> None:
        raise NotImplementedError("Not implemented on stub.")

    def process_bpa_change(self, bpa_index: int, tiles_bpa_new: int) -> None:
        raise NotImplementedError("Not implemented on stub.")
