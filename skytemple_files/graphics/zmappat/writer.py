"""Converts Wte models back into the binary format used by the game"""
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
from typing import Optional

from skytemple_files.common.util import *
from skytemple_files.graphics.zmappat import *
from skytemple_files.graphics.zmappat.model import ZMappaT

class ZMappaTWriter:
    def __init__(self, model: ZMappaT):
        self.model = model

    def write(self) -> Tuple[bytes, List[int], Optional[int]]:
        pointer_offsets = []
        buffer = bytearray()

        # Insert the tiles with their masks
        tile_table = []
        for i in range(len(self.model.tiles)):
            tile_table.append(len(buffer))
            current_mask = self.model.masks[i]
            current_tile = self.model.tiles[i]
            for x in range(ZMAPPAT_TILE_SIZE//8):
                buffer += current_mask[x*4:x*4+4]+current_tile[x*4:x*4+4]
                

        # Insert the tile pointers table
        table = bytearray(len(tile_table)*4)
        table_pointer = len(buffer)
        for i, x in enumerate(tile_table):
            pointer_offsets.append(len(buffer)+i*4)
            write_uintle(table, x, i*4, 4)
        buffer += table

        # The palette
        palette_pointer = len(buffer)
        palette_buffer = bytearray(len(self.model.palette) * 4 // 3)
        j = 0
        for i, p in enumerate(self.model.palette):
            write_uintle(palette_buffer, p, j)
            j += 1
            if i % 3 == 2:
                # Insert the fourth color
                write_uintle(palette_buffer, 0, j)
                j += 1
        assert j == len(palette_buffer)
        buffer += palette_buffer

        # The header
        header_pointer = len(buffer)
        header = bytearray(0x8)
        pointer_offsets.append(len(buffer))
        pointer_offsets.append(len(buffer)+4)
        write_uintle(header, table_pointer, 0, 4)
        write_uintle(header, palette_pointer, 4, 4)
        
        buffer += header
        return buffer, pointer_offsets, header_pointer
