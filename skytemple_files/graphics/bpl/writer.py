"""Converts Bpl models back into the binary format used by the game"""
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
from skytemple_files.graphics.bpl.model import Bpl, BPL_PAL_ENTRY_LEN, BPL_COL_INDEX_ENTRY_LEN, BPL_FOURTH_COLOR
from skytemple_files.graphics.bpl.model import BPL_PAL_SIZE


class BplWriter:
    def __init__(self, model: Bpl):
        self.model = model
        self.data = None
        self.bytes_written = 0

    def write(self) -> bytes:

        # Calculate the size of the palette animation bit
        animation_size = 0
        if self.model.has_palette_animation:
            animation_palette_size = len(self.model.animation_palette) * BPL_PAL_ENTRY_LEN
            animation_size = self.model.number_palettes * BPL_COL_INDEX_ENTRY_LEN + animation_palette_size

        # 4 byte header + palettes + animation
        self.data = bytearray(
            4 + (self.model.number_palettes * BPL_PAL_SIZE) + animation_size
        )

        # Header
        self._write_16uintle(self.model.number_palettes)
        self._write_16uintle(self.model.has_palette_animation)

        for palette in self.model.get_real_palettes():
            # Palettes [Starts with transparent color! This is removed!]
            for i, color in enumerate(palette[3:]):
                self._write_byte(color)
                if i % 3 == 2:
                    # Insert the fourth color
                    self._write_byte(BPL_FOURTH_COLOR)

        if self.model.has_palette_animation:
            # Palette Animation Spec
            for spec in self.model.animation_specs:
                self._write_16uintle(spec.duration_per_frame)
                self._write_16uintle(spec.number_of_frames)

            # Palette Animation Palette
            for frame in self.model.animation_palette:
                for i, color in enumerate(frame):
                    self._write_byte(color)
                    if i % 3 == 2:
                        # Insert the fourth color
                        self._write_byte(BPL_FOURTH_COLOR)

        return self.data

    def _write_16uintle(self, val):
        write_uintle(self.data, val, self.bytes_written, 2)
        self.bytes_written += 2

    def _write_byte(self, val):
        write_uintle(self.data, val, self.bytes_written)
        self.bytes_written += 1
