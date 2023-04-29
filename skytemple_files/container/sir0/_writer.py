"""Converts Sir0 models back into the binary format used by the game"""
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

from typing import Sequence

from range_typed_integers import u32_checked, u32

from skytemple_files.common.util import (
    write_u32,
    read_u32,
)
from skytemple_files.container.sir0 import HEADER_LEN
from skytemple_files.container.sir0._model import Sir0
from skytemple_files.container.sir0.sir0_util import encode_sir0_pointer_offsets


class Sir0Writer:
    def __init__(self):
        self.data: bytearray = None  # type: ignore
        self.bytes_written = 0

    def write(self, model: Sir0) -> bytes:
        model = Sir0(
            bytearray(model.content),
            list(model.content_pointer_offsets),
            model.data_pointer,
        )
        # Correct all pointers in content by HEADER_LEN
        if not isinstance(model.content, bytearray):
            model.content = bytearray(model.content)
        for i, pnt_off in enumerate(model.content_pointer_offsets):
            model.content_pointer_offsets[i] = u32_checked(pnt_off + HEADER_LEN)
            write_u32(
                model.content,
                u32(read_u32(model.content, pnt_off) + HEADER_LEN),
                pnt_off,
            )

        # Also add the two header pointers
        pointer_offsets = [u32(4), u32(8)] + model.content_pointer_offsets

        # Pointer offsets list
        pol = bytearray(4 * len(pointer_offsets))
        pol_cursor = self._encode_pointer_offsets(pol, pointer_offsets)
        pol = pol[:pol_cursor]

        len_content_padding = self._len_pad(len(model.content))
        len_eof_padding = self._len_pad(len(pol))

        pointer_pol = HEADER_LEN + len(model.content) + len_content_padding
        self.bytes_written = 0
        self.data = bytearray(pointer_pol + len(pol) + len_eof_padding)

        # Header
        self._append(b"SIR0")
        self._write_u32(u32_checked(model.data_pointer + HEADER_LEN))
        self._write_u32(u32_checked(pointer_pol))
        self._write_u32(u32(0))

        assert self.bytes_written == HEADER_LEN
        self._append(model.content)
        self._pad(len_content_padding)

        assert self.bytes_written == pointer_pol
        self._append(pol)
        self._pad(len_eof_padding)

        assert self.bytes_written == len(self.data)
        return self.data

    def _append(self, data: bytes):
        self.data[self.bytes_written : self.bytes_written + len(data)] = data  # type: ignore
        self.bytes_written += len(data)

    def _pad(self, padding_length):
        self._append(bytes(0xAA for _ in range(0, padding_length)))

    def _len_pad(self, cur_len):
        if cur_len % 16 == 0:
            return 0
        return 16 - (cur_len % 16)

    def _write_u32(self, val: u32):
        write_u32(self.data, val, self.bytes_written)
        self.bytes_written += 4

    # Based on C++ algorithm by psy_commando from
    # https://projectpokemon.org/docs/mystery-dungeon-nds/sir0siro-format-r46/
    def _encode_pointer_offsets(
        self, buffer: bytearray, pointer_offsets: Sequence[int]
    ) -> u32:
        return encode_sir0_pointer_offsets(buffer, pointer_offsets)
