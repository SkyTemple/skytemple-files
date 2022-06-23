"""Converts Bgp models back into the binary format used by the game"""
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


from __future__ import annotations

from range_typed_integers import u32_checked

from skytemple_files.common.util import *
from skytemple_files.graphics.bgp.model import (
    BGP_HEADER_LENGTH,
    BGP_PAL_ENTRY_LEN,
    BGP_PAL_NUMBER_COLORS,
    BGP_PAL_UNKNOWN4_COLOR_VAL,
    BGP_TILE_DIM,
    BGP_TILEMAP_ENTRY_BYTELEN,
    Bgp,
)


class BgpWriter:
    def __init__(self, model: Bgp):
        self.model = model
        self.data: bytearray = None  # type: ignore
        self.bytes_written = 0

    def write(self) -> bytes:
        bytelen_single_tile = int(BGP_TILE_DIM * BGP_TILE_DIM / 2)

        palette_length = u32_checked(
            len(self.model.palettes) * BGP_PAL_NUMBER_COLORS * BGP_PAL_ENTRY_LEN
        )
        tiles_length = u32_checked(len(self.model.tiles) * bytelen_single_tile)
        tilemapping_length = u32_checked(
            len(self.model.tilemap) * BGP_TILEMAP_ENTRY_BYTELEN
        )
        palette_begin = BGP_HEADER_LENGTH
        tilemapping_begin = u32_checked(palette_begin + palette_length)
        tiles_begin = u32_checked(tilemapping_begin + tilemapping_length)
        # 32 byte header + palette, tiles and tilemapping data
        self.data = bytearray(
            BGP_HEADER_LENGTH + palette_length + tiles_length + tilemapping_length
        )

        # Header
        write_u32(self.data, u32(palette_begin), 0)
        write_u32(self.data, palette_length, 4)
        write_u32(self.data, tiles_begin, 8)
        write_u32(self.data, tiles_length, 12)
        write_u32(self.data, tilemapping_begin, 16)
        write_u32(self.data, tilemapping_length, 20)
        write_u32(self.data, self.model.header.unknown3, 24)
        write_u32(self.data, self.model.header.unknown4, 28)
        self.bytes_written = BGP_HEADER_LENGTH

        assert self.bytes_written == palette_begin
        # Palettes
        for palette in self.model.palettes:
            for i, color in enumerate(palette):
                self._write_byte(u8(color))
                if i % 3 == 2:
                    # Insert the fourth color
                    self._write_byte(u8(BGP_PAL_UNKNOWN4_COLOR_VAL))

        assert self.bytes_written == tilemapping_begin
        # Tile Mappings
        for entry in self.model.tilemap:
            write_u16(self.data, entry.to_int(), self.bytes_written)
            self.bytes_written += BGP_TILEMAP_ENTRY_BYTELEN

        assert self.bytes_written == tiles_begin
        # Tiles
        for tile in self.model.tiles:
            self.data[
                self.bytes_written : self.bytes_written + bytelen_single_tile
            ] = tile
            self.bytes_written += bytelen_single_tile

        return self.data

    def _write_byte(self, val: u8):
        write_u8(self.data, val, self.bytes_written)
        self.bytes_written += 1
