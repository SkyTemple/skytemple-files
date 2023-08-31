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
from range_typed_integers import u32_checked, u32, u8

from skytemple_files.common.types.hybrid_data_handler import WriterProtocol
from skytemple_files.common.util import write_u32, write_u8, write_u16
from skytemple_files.graphics.bgp._model import Bgp
from skytemple_files.graphics.bgp import (
    BGP_HEADER_LENGTH,
    BGP_PAL_ENTRY_LEN,
    BGP_PAL_UNKNOWN4_COLOR_VAL,
    BGP_PAL_NUMBER_COLORS,
    BGP_TILEMAP_ENTRY_BYTELEN,
    BGP_TILE_DIM,
)


class BgpWriter(WriterProtocol[Bgp]):
    def write(self, model: Bgp) -> bytes:
        bytelen_single_tile = int(BGP_TILE_DIM * BGP_TILE_DIM / 2)

        palette_length = len(model.palettes) * BGP_PAL_NUMBER_COLORS * BGP_PAL_ENTRY_LEN
        tiles_length = len(model.tiles) * bytelen_single_tile
        tilemapping_length = len(model.tilemap) * BGP_TILEMAP_ENTRY_BYTELEN
        palette_begin = BGP_HEADER_LENGTH
        tilemapping_begin = palette_begin + palette_length
        tiles_begin = tilemapping_begin + tilemapping_length
        # 32 byte header + palette, tiles and tilemapping data
        data = bytearray(
            BGP_HEADER_LENGTH + palette_length + tiles_length + tilemapping_length
        )

        # Header
        write_u32(data, u32(palette_begin), 0)
        write_u32(data, u32_checked(palette_length), 4)
        write_u32(data, u32_checked(tiles_begin), 8)
        write_u32(data, u32_checked(tiles_length), 12)
        write_u32(data, u32_checked(tilemapping_begin), 16)
        write_u32(data, u32_checked(tilemapping_length), 20)
        write_u32(data, model.header.unknown3, 24)
        write_u32(data, model.header.unknown4, 28)
        bytes_written = BGP_HEADER_LENGTH

        assert bytes_written == palette_begin
        # Palettes
        for palette in model.palettes:
            for i, color in enumerate(palette):
                write_u8(data, u8(color), bytes_written)
                bytes_written += 1
                if i % 3 == 2:
                    # Insert the fourth color
                    write_u8(data, BGP_PAL_UNKNOWN4_COLOR_VAL, bytes_written)
                    bytes_written += 1

        assert bytes_written == tilemapping_begin
        # Tile Mappings
        for entry in model.tilemap:
            write_u16(data, entry.to_int(), bytes_written)
            bytes_written += BGP_TILEMAP_ENTRY_BYTELEN

        assert bytes_written == tiles_begin
        # Tiles
        for tile in model.tiles:
            data[bytes_written : bytes_written + bytelen_single_tile] = tile
            bytes_written += bytelen_single_tile

        return data
