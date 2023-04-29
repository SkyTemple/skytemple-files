"""Converts Bpl models back into the binary format used by the game"""
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

from range_typed_integers import u16, u8

from skytemple_files.common.util import write_u16, write_u8
from skytemple_files.graphics.bpl import (
    BPL_COL_INDEX_ENTRY_LEN,
    BPL_FOURTH_COLOR,
    BPL_PAL_ENTRY_LEN,
    BPL_PAL_SIZE,
)
from skytemple_files.graphics.bpl._model import Bpl


class BplWriter:
    def __init__(self) -> None:
        self.bytes_written = 0

    def write(self, model: Bpl) -> bytes:
        # Calculate the size of the palette animation bit
        animation_size = 0
        if model.has_palette_animation:
            animation_palette_size = len(model.animation_palette) * BPL_PAL_ENTRY_LEN
            animation_size = (
                model.number_palettes * BPL_COL_INDEX_ENTRY_LEN + animation_palette_size
            )

        # 4 byte header + palettes + animation
        data = bytearray(4 + (model.number_palettes * BPL_PAL_SIZE) + animation_size)

        # Header
        self._write_16uintle(data, model.number_palettes)
        self._write_16uintle(data, u16(int(model.has_palette_animation)))

        for palette in model.get_real_palettes():
            # Palettes [Starts with transparent color! This is removed!]
            for i, color in enumerate(palette[3:]):
                self._write_byte(data, u8(color))
                if i % 3 == 2:
                    # Insert the fourth color
                    self._write_byte(data, u8(BPL_FOURTH_COLOR))

        if model.has_palette_animation:
            # Palette Animation Spec
            for spec in model.animation_specs:
                self._write_16uintle(data, spec.duration_per_frame)
                self._write_16uintle(data, spec.number_of_frames)

            # Palette Animation Palette
            for frame in model.animation_palette:
                for i, color in enumerate(frame):
                    self._write_byte(data, u8(color))
                    if i % 3 == 2:
                        # Insert the fourth color
                        self._write_byte(data, u8(BPL_FOURTH_COLOR))

        return data

    def _write_16uintle(self, data: bytearray, val: u16) -> None:
        write_u16(data, val, self.bytes_written)
        self.bytes_written += 2

    def _write_byte(self, data: bytearray, val: u8) -> None:
        write_u8(data, val, self.bytes_written)
        self.bytes_written += 1
