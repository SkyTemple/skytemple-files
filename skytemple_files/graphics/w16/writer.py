"""Converts W16 models back into the binary format used by the game"""
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

from skytemple_files.common.util import *
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
            write_uintle(toc_buffer, len(toc_buffer) + len(image_buffer), toc_cursor, 4)
            # entry data
            write_uintle(toc_buffer, w16.entry_data.width, toc_cursor + 4, 1)
            write_uintle(toc_buffer, w16.entry_data.height, toc_cursor + 5, 1)
            write_uintle(toc_buffer, w16.entry_data.index, toc_cursor + 6, 1)
            write_uintle(toc_buffer, w16.entry_data.null, toc_cursor + 7, 1)
            toc_cursor += 8
            # Palettes
            pal = bytes(w16.pal)
            assert len(pal) == 3 * 16
            image_buffer += pal
            # Data
            image_buffer += w16.compressed_img_data

        # Null toc entry
        write_uintle(toc_buffer, len(toc_buffer) + len(image_buffer), toc_cursor, 4)

        return toc_buffer + image_buffer
