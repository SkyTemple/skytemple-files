"""Converts Bpa models back into the binary format used by the game"""
from skytemple_files.common.util import *
from skytemple_files.graphics.bpa.model import Bpa, BPA_TILE_DIM


class BpaWriter:
    def __init__(self, model: Bpa):
        self.model = model
        self.data = None
        self.bytes_written = 0

    def write(self) -> bytes:
        # 4 byte header + animation info for each + images
        self.data = bytearray(
            4 + (self.model.number_of_frames * 4) + int(self.model.number_of_tiles * self.model.number_of_frames / 2)
        )

        self._write_16uintle(self.model.number_of_tiles)
        self._write_16uintle(self.model.number_of_frames)

        assert self.model.number_of_frames == len(self.model.frame_info)
        for finfo in self.model.frame_info:
            self._write_16uintle(finfo.duration_per_frame)
            self._write_16uintle(finfo.unk2)

        # Tiles
        bytelen_single_tile = int(BPA_TILE_DIM * BPA_TILE_DIM / 2)
        for tile in self.model.tiles:
            self.data[self.bytes_written:self.bytes_written+bytelen_single_tile] = tile
            self.bytes_written += bytelen_single_tile

        return self.data

    def _write_16uintle(self, val):
        write_uintle(self.data, val, self.bytes_written, 2)
        self.bytes_written += 2
