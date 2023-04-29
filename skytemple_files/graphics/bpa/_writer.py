"""Converts Bpa models back into the binary format used by the game"""
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

from range_typed_integers import u16

from skytemple_files.common.util import write_u16
from skytemple_files.graphics.bpa import BPA_TILE_DIM
from skytemple_files.graphics.bpa._model import Bpa


class BpaWriter:
    def __init__(self) -> None:
        self.bytes_written = 0

    def write(self, model: Bpa) -> bytes:
        # 4 byte header + animation info for each + images
        data = bytearray(
            4
            + (model.number_of_frames * 4)
            + int(model.number_of_tiles * model.number_of_frames / 2)
        )

        self._write_16uintle(data, model.number_of_tiles)
        self._write_16uintle(data, model.number_of_frames)

        assert model.number_of_frames == len(model.frame_info)
        for finfo in model.frame_info:
            self._write_16uintle(data, finfo.duration_per_frame)
            self._write_16uintle(data, finfo.unk2)

        # Tiles
        bytelen_single_tile = int(BPA_TILE_DIM * BPA_TILE_DIM / 2)
        for tile in model.tiles:
            data[self.bytes_written : self.bytes_written + bytelen_single_tile] = tile
            self.bytes_written += bytelen_single_tile

        return data

    def _write_16uintle(self, data: bytearray, val: u16) -> None:
        write_u16(data, val, self.bytes_written)
        self.bytes_written += 2
