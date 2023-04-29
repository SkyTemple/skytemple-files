"""Converts Bpc models back into the binary format used by the game"""
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

from range_typed_integers import u16_checked, u16

from skytemple_files.common.util import write_u16
from skytemple_files.graphics.bpc import BPC_TILE_DIM, BPC_TILEMAP_BYTELEN
from skytemple_files.graphics.bpc._model import Bpc


class BpcWriter:
    def __init__(self) -> None:
        self.bytes_written = 0

    def write(self, model: Bpc) -> bytes:
        assert 0 < model.number_of_layers < 3
        # First collect tiles and tilemaps for both layers, so we can calculate
        # the pointers
        tiles = []
        tilemaps = []
        for i in range(0, model.number_of_layers):
            tiles.append(self._convert_tiles(model, i))
            tilemaps.append(self._convert_tilemap(model, i))

        end_of_layer_specs = u16_checked(4 + (12 * model.number_of_layers))

        length_of_first_layer = len(tiles[0]) + len(tilemaps[0])
        # The length is increased by 1 if a padding has to be added:
        if (end_of_layer_specs + len(tiles[0])) % 2 != 0:
            length_of_first_layer += 1
        if (end_of_layer_specs + length_of_first_layer) % 2 != 0:
            length_of_first_layer += 1

        length_of_second_layer = 0
        if model.number_of_layers > 1:
            length_of_second_layer = len(tiles[1]) + len(tilemaps[1])
            # The length is increased by 1 if a padding has to be added:
            if (end_of_layer_specs + length_of_first_layer + len(tiles[1])) % 2 != 0:
                length_of_second_layer += 1
            if (end_of_layer_specs + length_of_second_layer) % 2 != 0:
                length_of_second_layer += 1

        # 4 byte header + layer specs + layer data
        data = bytearray(
            end_of_layer_specs + length_of_first_layer + length_of_second_layer
        )

        # upper layer pointer
        self._write_16uintle(data, end_of_layer_specs)
        # lower layer pointer ( if two layers )
        if model.number_of_layers > 1:
            self._write_16uintle(
                data, u16_checked(end_of_layer_specs + length_of_first_layer)
            )
        else:
            self._write_16uintle(data, u16(0))

        # for each layer specs:
        for i in range(0, model.number_of_layers):
            # number tiles + 1
            self._write_16uintle(data, u16_checked(model.layers[i].number_tiles + 1))
            # bpa1-4
            self._write_16uintle(data, model.layers[i].bpas[0])
            self._write_16uintle(data, model.layers[i].bpas[1])
            self._write_16uintle(data, model.layers[i].bpas[2])
            self._write_16uintle(data, model.layers[i].bpas[3])
            # tilemap length
            self._write_16uintle(data, model.layers[i].chunk_tilemap_len)

        # for each layer:
        for i in range(0, model.number_of_layers):
            # tiles
            lentiles = len(tiles[i])
            data[self.bytes_written : self.bytes_written + lentiles] = tiles[i]
            self.bytes_written += lentiles
            # 2 bytes alignment
            if self.bytes_written % 2 != 0:
                data[self.bytes_written] = 0
                self.bytes_written += 1
            # tilemap
            lentilemap = len(tilemaps[i])
            data[self.bytes_written : self.bytes_written + lentilemap] = tilemaps[i]
            self.bytes_written += lentilemap
            # 2 bytes alignment
            if self.bytes_written % 2 != 0:
                data[self.bytes_written] = 0
                self.bytes_written += 1

        return data

    @staticmethod
    def _convert_tiles(model: Bpc, layeri: int) -> bytes:
        from skytemple_files.common.types.file_types import FileType

        layer = model.layers[layeri]
        bytelen_single_tile = int(BPC_TILE_DIM * BPC_TILE_DIM / 2)
        data = bytearray(bytelen_single_tile * (len(layer.tiles) - 1))
        bytes_written = 0

        # Skip first (null tile)
        for tile in layer.tiles[1:]:
            data[bytes_written : bytes_written + bytelen_single_tile] = tile
            bytes_written += bytelen_single_tile

        return FileType.BPC_IMAGE.compress(data)

    @staticmethod
    def _convert_tilemap(model: Bpc, layeri: int) -> bytes:
        from skytemple_files.common.types.file_types import FileType

        layer = model.layers[layeri]
        length = (
            (layer.chunk_tilemap_len - 1)
            * (model.tiling_width * model.tiling_height)
            * BPC_TILEMAP_BYTELEN
        )
        data = bytearray(length)
        bytes_written = 0

        # Skip first chunk (null)
        for entry in layer.tilemap[model.tiling_width * model.tiling_height :]:
            write_u16(data, entry.to_int(), bytes_written)
            bytes_written += BPC_TILEMAP_BYTELEN
        assert bytes_written == length

        return FileType.BPC_TILEMAP.compress(data)

    def _write_16uintle(self, data: bytearray, val: u16) -> None:
        write_u16(data, val, self.bytes_written)
        self.bytes_written += 2
