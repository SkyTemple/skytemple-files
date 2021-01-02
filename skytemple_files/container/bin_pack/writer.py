"""Converts BinPack models back into the binary format used by the game"""
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
from skytemple_files.container.bin_pack.model import BinPack


class BinPackWriter:
    def __init__(self, model: BinPack, fixed_header_len=0):
        self.model = model
        self.fixed_header_len = fixed_header_len

    def write(self) -> bytes:
        files = self.model.get_files_bytes()
        len_header = (len(self.model.get_files_bytes()) + 1) * 8 + 16  # 16 is a row of padding
        if len_header % 16 != 0:
            len_header += 16 - (len_header % 16)
        out_buffer = bytearray(
            b'\xff' * (
                # Header len:
                max(self.fixed_header_len, len_header) +
                # File data:
                self._get_file_sizes(files)
            )
        )

        write_uintle(out_buffer, 0, 0x00, 4)
        write_uintle(out_buffer, len(files), 0x04, 4)

        data_cursor = len_header
        toc_curosr = 8
        for file in files:
            # toc pointer
            write_uintle(out_buffer, data_cursor, toc_curosr, 4)
            # toc length
            write_uintle(out_buffer, len(file), toc_curosr + 0x04, 4)
            # file
            out_buffer[data_cursor:data_cursor+len(file)] = file

            data_cursor += len(file)
            # If the cursor is not aligned with 16 bytes, we pad.
            if data_cursor % 16 != 0:
                data_cursor += 16 - (data_cursor % 16)

            toc_curosr += 8

        # If the toc cursor is not aligned with 16 bytes, we will with zeros
        if toc_curosr % 16 != 0:
            pad = 16 - (toc_curosr % 16)
            out_buffer[toc_curosr:toc_curosr+pad] = b'\x00' * pad

        return out_buffer

    def _get_file_sizes(self, files):
        size = 0
        for file in files:
            size += len(file)
            # Padding to 16 bytes after file end:
            if len(file) % 16 != 0:
                size += 16 - (len(file) % 16)

        return size
