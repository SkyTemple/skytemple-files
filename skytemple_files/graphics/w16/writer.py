"""Converts W16 models back into the binary format used by the game"""
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

from range_typed_integers import u32_checked

from skytemple_files.common.util import write_u8, write_u32
from skytemple_files.graphics.w16.model import W16


class W16Writer:
    def __init__(self, model: W16):
        self.model = model

    def write(self) -> bytes:
        toc_buffer = bytearray(8 * (len(self.model) + 1))
        toc_cursor = 0
        image_buffer = bytearray()
        # File list
        for w16 in self.model:
            # TOC entry
            # Pointer
            write_u32(
                toc_buffer, u32_checked(len(toc_buffer) + len(image_buffer)), toc_cursor
            )
            # entry data
            write_u8(toc_buffer, w16.entry_data.width, toc_cursor + 4)
            write_u8(toc_buffer, w16.entry_data.height, toc_cursor + 5)
            write_u8(toc_buffer, w16.entry_data.index, toc_cursor + 6)
            write_u8(toc_buffer, w16.entry_data.null, toc_cursor + 7)
            toc_cursor += 8
            # Palettes
            pal = bytes(w16.pal)
            assert len(pal) == 3 * 16
            image_buffer += pal
            # Data
            image_buffer += w16.compressed_img_data

        # Null toc entry
        write_u32(
            toc_buffer, u32_checked(len(toc_buffer) + len(image_buffer)), toc_cursor
        )

        return toc_buffer + image_buffer
