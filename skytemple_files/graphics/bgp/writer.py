"""Converts Bgp models back into the binary format used by the game"""
#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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

import string

from skytemple_files.common.util import *
from skytemple_files.graphics.bgp.model import Bgp, BGP_PAL_NUMBER_COLORS, BGP_PAL_ENTRY_LEN, BGP_TILEMAP_ENTRY_BYTELEN, \
    BGP_HEADER_LENGTH, BGP_TILE_DIM, BGP_PAL_UNKNOWN4_COLOR_VAL


class BgpWriter:
    def __init__(self, model: Bgp):
        self.model = model
        self.data = None
        self.bytes_written = 0

    def write(self) -> bytes:
        bytelen_single_tile = int(BGP_TILE_DIM * BGP_TILE_DIM / 2)

        palette_length = len(self.model.palettes) * BGP_PAL_NUMBER_COLORS * BGP_PAL_ENTRY_LEN
        tiles_length = len(self.model.tiles) * bytelen_single_tile
        tilemapping_length = len(self.model.tilemap) * BGP_TILEMAP_ENTRY_BYTELEN
        palette_begin = BGP_HEADER_LENGTH
        tilemapping_begin = palette_begin + palette_length
        tiles_begin = tilemapping_begin + tilemapping_length
        # 32 byte header + palette, tiles and tilemapping data
        self.data = bytearray(BGP_HEADER_LENGTH + palette_length + tiles_length + tilemapping_length)

        # Header
        write_uintle(self.data, palette_begin, 0, 4)
        write_uintle(self.data, palette_length, 4, 4)
        write_uintle(self.data, tiles_begin, 8, 4)
        write_uintle(self.data, tiles_length, 12, 4)
        write_uintle(self.data, tilemapping_begin, 16, 4)
        write_uintle(self.data, tilemapping_length, 20, 4)
        write_uintle(self.data, self.model.header.unknown3, 24, 4)
        write_uintle(self.data, self.model.header.unknown4, 28, 4)
        self.bytes_written = BGP_HEADER_LENGTH

        assert self.bytes_written == palette_begin
        # Palettes
        for palette in self.model.palettes:
            for i, color in enumerate(palette):
                self._write_byte(color)
                if i % 3 == 2:
                    # Insert the fourth color
                    self._write_byte(BGP_PAL_UNKNOWN4_COLOR_VAL)

        assert self.bytes_written == tilemapping_begin
        # Tile Mappings
        for entry in self.model.tilemap:
            write_uintle(self.data, entry.to_int(), self.bytes_written, BGP_TILEMAP_ENTRY_BYTELEN)
            self.bytes_written += BGP_TILEMAP_ENTRY_BYTELEN

        assert self.bytes_written == tiles_begin
        # Tiles
        for tile in self.model.tiles:
            self.data[self.bytes_written:self.bytes_written+bytelen_single_tile] = tile
            self.bytes_written += bytelen_single_tile

        return self.data

    def _write_byte(self, val):
        write_uintle(self.data, val, self.bytes_written)
        self.bytes_written += 1
