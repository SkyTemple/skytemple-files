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

from typing import List

from skytemple_files.common.util import *

# Length of a palette in colors. Color 0 is auto-generated (transparent)
BPL_PAL_LEN = 15
# Actual colors in an image, (including the color 0)
BPL_IMG_PAL_LEN = BPL_PAL_LEN + 1
# Maximum number of palettes
BPL_MAX_PAL = 16
# Maximum number of normal palettes
BPL_NORMAL_MAX_PAL = 14

# Number of color bytes per palette entry. Fourth is always 0x00.
BPL_PAL_ENTRY_LEN = 4
# Size of a single palette in bytes
BPL_PAL_SIZE = BPL_PAL_LEN * BPL_PAL_ENTRY_LEN
BPL_COL_INDEX_ENTRY_LEN = 4
# The value of the fourth color
BPL_FOURTH_COLOR = 0x00


class BplAnimationSpec:

    def __init__(self, duration_per_frame, number_of_frames):
        self.duration_per_frame = duration_per_frame
        self.number_of_frames = number_of_frames

    def __repr__(self):
        return f"<{self.duration_per_frame},{self.number_of_frames}>"


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
        self.set_palettes(self.palettes)
        # If the second flag is set (has_second_color_table) then there should be
        # more data. Otherwise not!
        #assert len(data) - pal_end == 0 if not self.has_second_color_table else len(data) - pal_end > 0

        # Mapped 1:1 with self.palettes, if exists:
        self.animation_specs: List[BplAnimationSpec] = []

        # Extra colors - Palette animation
        # Format: [ [r,g,b,r,g,b,r,g,b,r,g,b...], ...]
        # Only 15 colors per frame!
        self.animation_palette = []
        if self.has_palette_animation:
            # Read color index table
            cit_end = pal_end + self.number_palettes * BPL_COL_INDEX_ENTRY_LEN
            for entry in iter_bytes(data, BPL_COL_INDEX_ENTRY_LEN, pal_end, cit_end):
                self.animation_specs.append(BplAnimationSpec(
                    duration_per_frame=read_uintle(entry, 0, 2),
                    number_of_frames=read_uintle(entry, 2, 2)
                ))

            # Read color table 2
            # We don't know the length, so read until EOF
            current_ani_pal = []
            for i, col in enumerate(iter_bytes(data, BPL_PAL_ENTRY_LEN, cit_end)):
                r, g, b, unk = col
                current_ani_pal += [r, g, b]
                assert unk == BPL_FOURTH_COLOR
                if (i + 1) % BPL_PAL_LEN == 0:
                    self.animation_palette.append(current_ani_pal)
                    current_ani_pal = []

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
                        duration_per_frame=0, number_of_frames=0
                    ))

    def apply_palette_animations(self, frame: int) -> List[List[int]]:
        """
        Returns a modified copy of self.palettes.

        This copy is modified to have colors swapped out for the current frame of palette animation.
        The information for this is stored in self.animation_specs and the animation palette in
        self.animation_palette.

        Only available if self.has_palette_animation.

        The maximum number of frames is the length of self.animation_palette
        """
        # TODO: First frame is missing: No change!
        f_palettes = []
        for i, spec in enumerate(self.animation_specs):
            if spec.number_of_frames > 0:
                actual_frame_for_pal = frame % spec.number_of_frames
                pal_for_frame = self.animation_palette[actual_frame_for_pal]
                f_palettes.append([0, 0, 0] + pal_for_frame)
            else:
                f_palettes.append(self.palettes[i])
        return f_palettes

    def is_palette_affected_by_animation(self, pal_idx):
        """Returns whether or not the palette with that index is affected by animation. """
        if not self.has_palette_animation:
            return False
        spec = self.animation_specs[pal_idx]
        return spec.number_of_frames > 0

    def get_real_palettes(self):
        """Gets the actual palettes defined (without dummy grayscale entries). """
        return self.palettes[:self.number_palettes]
        
    def set_palettes(self, palettes):
        """Sets the palette properly, adding dummy grayscale entries if needed. """
        self.palettes = palettes
        self.number_palettes = len(palettes)
        while len(self.palettes)<BPL_MAX_PAL:
            self.palettes.append([(i//3)*BPL_MAX_PAL for i in range(BPL_MAX_PAL*3)])
