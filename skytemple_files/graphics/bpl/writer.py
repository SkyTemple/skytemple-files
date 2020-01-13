"""Converts Bpl models back into the binary format used by the game"""
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

        for palette in self.model.palettes:
            # Palettes [Starts with transparent color! This is removed!]
            for i, color in enumerate(palette[3:]):
                self._write_byte(color)
                if i % 3 == 2:
                    # Insert the fourth color
                    self._write_byte(BPL_FOURTH_COLOR)

        if self.model.has_palette_animation:
            # Palette Animation Spec
            for spec in self.model.animation_specs:
                self._write_16uintle(spec.unk3)
                self._write_16uintle(spec.unk4)

            # Palette Animation Palette
            for color_list in self.model.animation_palette:
                for color in color_list:
                    self._write_byte(color)
                # Insert the fourth color
                self._write_byte(BPL_FOURTH_COLOR)

        return self.data

    def _write_16uintle(self, val):
        write_uintle(self.data, val, self.bytes_written, 2)
        self.bytes_written += 2

    def _write_byte(self, val):
        write_uintle(self.data, val, self.bytes_written)
        self.bytes_written += 1
