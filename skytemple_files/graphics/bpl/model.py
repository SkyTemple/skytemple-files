from typing import List

from skytemple_files.common.util import *

# Length of a palette in colors. Color 0 is auto-generated (transparent)
BPL_PAL_LEN = 15
# Actual colors in an image, (including the color 0)
BPL_IMG_PAL_LEN = BPL_PAL_LEN + 1
# Maximum number of palettes
BPL_MAX_PAL = 16
# Number of color bytes per palette entry. Fourth is always 0x00.
BPL_PAL_ENTRY_LEN = 4
# Size of a single palette in bytes
BPL_PAL_SIZE = BPL_PAL_LEN * BPL_PAL_ENTRY_LEN
BPL_COL_INDEX_ENTRY_LEN = 4
# The value of the fourth color
BPL_FOURTH_COLOR = 0x00


class BplAnimationSpec:

    def __init__(self, unk3, unk4):
        # TODO: My palette animation assumption doesn't work with these values.
        #       Value 1 goes from 0-16 and 2 from 0 to at least 63.
        #       ...there are only 16 colors in the palettes. However maybe the first value
        #       is actually the color index and 16 is a special value (cycle entire palette?)?
        self.unk3 = unk3
        self.unk4 = unk4

    def __repr__(self):
        return f"<{self.unk3},{self.unk4}>"


class Bpl:
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        self.number_palettes = read_uintle(data, 0, 2)

        # The second 2 byte value should just be a boolean
        #assert 0 <= read_bytes(data, 2, 2).uintle <= 1
        self.has_palette_animation = read_uintle(data, 2, 2)

        # Read palettes:
        pal_end = 4 + (self.number_palettes * BPL_PAL_SIZE)
        # Format: [ [r,g,b,r,g,b,r,g,b,r,g,b...], ...]
        self.palettes = []
        self.current_palette = [0, 0, 0]  # Transparent first color - to be removed during serialization!
        colors_read_for_current_palette = 0
        for pal_entry in iter_bytes(data, BPL_PAL_ENTRY_LEN, 4, pal_end):
            r, g, b, unk = pal_entry
            self.current_palette.append(r)
            self.current_palette.append(g)
            self.current_palette.append(b)
            assert unk == BPL_FOURTH_COLOR
            colors_read_for_current_palette += 1
            if colors_read_for_current_palette >= 15:
                self.palettes.append(self.current_palette)
                self.current_palette = [0, 0, 0]  # Transparent first color - see above!
                colors_read_for_current_palette = 0

        # If the second flag is set (has_second_color_table) then there should be
        # more data. Otherwise not!
        #assert len(data) - pal_end == 0 if not self.has_second_color_table else len(data) - pal_end > 0

        # Mapped 1:1 with self.palettes, if exists:
        self.animation_specs: List[BplAnimationSpec] = []

        # Extra colors
        # Format: [ [r,g,b], ...]
        self.animation_palette = []
        if self.has_palette_animation:
            # My current guess is that these extra colors are part of a palette animation process!!
            # unk3 might be the delay between color changes! Color index is then actually the index
            # of the color in the PALETTE to change NOT from the extra color table!
            # I named the variables with this assumption in mind for now

            # Read color index table
            cit_end = pal_end + self.number_palettes * BPL_COL_INDEX_ENTRY_LEN
            for entry in iter_bytes(data, BPL_COL_INDEX_ENTRY_LEN, pal_end, cit_end):
                self.animation_specs.append(BplAnimationSpec(
                    unk3=read_uintle(entry, 0, 2),
                    unk4=read_uintle(entry, 2, 4)
                ))

            # Read color table 2
            # We don't know the length, so read until EOF
            for col in iter_bytes(data, BPL_PAL_ENTRY_LEN, cit_end):
                r, g, b, unk = col
                self.animation_palette.append([r, g, b])
                assert unk == BPL_FOURTH_COLOR

    def import_palettes(self, palettes: List[List[int]]):
        """
        Replace all palettes with the ones passed in
        Animated palette is not changed, but the number of spec entries is adjusted.
        """
        assert len(palettes) <= BPL_MAX_PAL
        nb_pal_old = self.number_palettes
        self.number_palettes = len(palettes)
        self.palettes = palettes
        if self.has_palette_animation:
            if self.number_palettes < nb_pal_old:
                # Remove the extra spec entries
                self.animation_specs = self.animation_specs[:self.number_palettes]
            elif self.number_palettes > nb_pal_old:
                # Add missing spec entries
                for _ in range(nb_pal_old, self.number_palettes):
                    self.animation_specs.append(BplAnimationSpec(
                        unk3=0, unk4=0
                    ))
