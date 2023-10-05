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

from range_typed_integers import u8_checked, u32_checked, u32
from collections.abc import Sequence

from range_typed_integers import u8_checked, u32_checked, u8

from skytemple_files.common.i18n_util import _
from skytemple_files.graphics.dpla import DPLA_COLORS_PER_PALETTE
from skytemple_files.graphics.dpla.protocol import DplaProtocol, chunk

from skytemple_files.common.i18n_util import _
from skytemple_files.common.util import (
    write_u32,
    read_u16,
    iter_bytes,
    read_u32,
    write_u8,
)

# XXX: Removing this re-export his is a breaking change in skytemple-dtef due to a typo.
# noinspection PyUnresolvedReferences
from skytemple_files.common.util import chunks  # nopycln: import


class Dpla(DplaProtocol):
    """
    This palette file contains sets of 16 colors and "frames" of animations for them. Each Sir0 poiinter
    points to one color entry and each of these color entries has 0-X frames of animation.
    """

    def __init__(self, data: bytes, pointer_to_pointers: int):
        toc_pointers = []
        for i in range(pointer_to_pointers, len(data), 4):
            toc_pointers.append(read_u32(data, i))

        # A list of colors stored in this file. The colors are lists of RGB values: [R, G, B, R, G, B...]
        self.colors: list[list[int]] = []
        self.durations_per_frame_for_colors: list[int] = []
        for pnt in toc_pointers:
            # 0x0         2           uint16      (NbColors) The amount of colors in this entry.
            number_colors = read_u16(data, pnt)
            # 0x2         2           uint16      unknown
            self.durations_per_frame_for_colors.append(read_u16(data, pnt + 2))
            # 0x4         (NbColors * 4)          A list of colors. Always at least 4 bytes even when empty! Is completely 0 if nb of color == 0 !
            # [
            #     0x0     4           RGBX32      A color.
            #     ...
            # ]
            frame_colors = []
            for r, g, b, x in iter_bytes(
                data, 4, pnt + 4, pnt + 4 + (number_colors * 4)
            ):
                frame_colors.append(r)
                frame_colors.append(g)
                frame_colors.append(b)
                assert (
                    x == 128
                )  # just in case it isn't... then we'd have a real alpha channel
            self.colors.append(frame_colors)

    def get_palette_for_frame(self, pal_idx: int, frame_id: int) -> list[int]:
        """
        Returns the color palette at the given frame id. Returned is a stream of RGB colors: [R, G, B, R, G, B...].
        Returned are always 16 colors. If the palette file has more than 16 colors, the pal_idx specifies what set
        of 16 colors to return.
        """
        colors = self.colors[pal_idx * 16 : (pal_idx + 1) * 16]
        frame_pal = []
        for color in colors:
            color_len = int(len(color) / 3)
            if len(color) < 1:
                color = [0, 0, 0]
            frame_pal += color[
                (frame_id % color_len) * 3 : ((frame_id % color_len) * 3) + 3
            ]

        return frame_pal

    def has_for_palette(self, palette_idx: int) -> bool:
        if len(self.colors) <= palette_idx * DPLA_COLORS_PER_PALETTE:
            return False
        return len(self.colors[palette_idx * DPLA_COLORS_PER_PALETTE]) > 0

    def get_frame_count_for_palette(self, palette_idx: int) -> int:
        if not self.has_for_palette(palette_idx):
            raise ValueError(_("This palette has no animation."))
        return int(len(self.colors[palette_idx * DPLA_COLORS_PER_PALETTE]) / 3)

    def enable_for_palette(self, palid: int):
        if not self.has_for_palette(palid):
            # Add one entry, this enables it.
            self.colors[
                palid * DPLA_COLORS_PER_PALETTE : (palid + 1) * DPLA_COLORS_PER_PALETTE
            ] = [[0, 0, 0] for _ in range(0, 16)]

    def disable_for_palette(self, palid: int):
        if self.has_for_palette(palid):
            # Remove all entries, this disables ist.
            self.colors[
                palid * DPLA_COLORS_PER_PALETTE : (palid + 1) * DPLA_COLORS_PER_PALETTE
            ] = [[] for _ in range(0, 16)]

    def get_duration_for_palette(self, palette_idx: int) -> int:
        """
        Warning: Colors in-game are animated separately. There is no speed for an entire palette.
        We are asuming there's one speed for the entire palette.
        This could be inaccurate.
        """
        return self.durations_per_frame_for_colors[
            palette_idx * DPLA_COLORS_PER_PALETTE
        ]

    def set_duration_for_palette(self, palid: int, duration: int) -> None:
        """
        Warning: Colors in-game are animated separately. There is no speed for an entire palette.
        We are asuming there's one speed for the entire palette.
        This could be inaccurate.
        """
        self.durations_per_frame_for_colors[
            palid * DPLA_COLORS_PER_PALETTE : (palid + 1) * DPLA_COLORS_PER_PALETTE
        ] = [duration] * 16

    def apply_palette_animations(
        self, palettes: Sequence[Sequence[int]], frame_idx: int
    ) -> list[list[int]]:
        """
        Returns a modified copy of `palettes`.

        This copy is modified to have colors swapped out for the current frame of palette animation.
        > The first 16 colors of the DPLA model are placed in the palette 11 (if color 0 has at least one frame).
        > The second 16 colors of the DPLA model are placed in the palette 12 (if color 16 has at least one frame).
        > If the model has more colors, they are ignored.

        Warning: Colors in-game are animated separately. There is no speed for an entire palette.
        We are asuming there's one speed for the entire palette.
        This could be inaccurate.
        """
        new_pal = [[y for y in x] for x in palettes]
        if self.has_for_palette(0):
            new_pal[10] = self.get_palette_for_frame(0, frame_idx)
        if self.has_for_palette(1):
            new_pal[11] = self.get_palette_for_frame(1, frame_idx)

        return new_pal

    def sir0_serialize_parts(self) -> tuple[bytes, list[u32], u32 | None]:
        data = bytearray()
        pointers = []
        pointer_offsets = []
        for i, color_frames in enumerate(self.colors):
            pointers.append(u32_checked(len(data)))
            number_colors = len(color_frames) // 3
            buffer_entry = bytearray((number_colors + 1) * 4)
            # Number colors
            write_u8(buffer_entry, u8_checked(number_colors), 0)
            # Unk
            write_u8(
                buffer_entry, u8_checked(self.durations_per_frame_for_colors[i]), 2
            )
            # Always one null color
            null_color = False
            if len(color_frames) == 0:
                null_color = True
                color_frames = [0, 0, 0]
            cursor = 4
            for j, (r, g, b) in enumerate(chunk(color_frames, 3)):
                write_u8(buffer_entry, r, cursor)
                write_u8(buffer_entry, g, cursor + 1)
                write_u8(buffer_entry, b, cursor + 2)
                write_u8(buffer_entry, u8(128 if not null_color else 0), cursor + 3)
                cursor += 4

            data += buffer_entry
        data_offset = cursor = len(data)
        data += bytes(4 * len(pointers))
        for pnt in pointers:
            write_u32(data, pnt, cursor)
            pointer_offsets.append(u32(cursor))
            cursor += 4

        return data, pointer_offsets, u32(data_offset)

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int, config=None) -> Dpla:
        return cls(content_data, data_pointer)
