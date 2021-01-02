"""Converts Bma models back into the binary format used by the game"""
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
from skytemple_files.graphics.bma.model import Bma


class BmaWriter:
    def __init__(self, model: Bma):
        self.model = model
        self.data = None
        self.bytes_written = 0

    def write(self) -> bytes:
        # First collect the layers, collision layers and unknown data layer,
        # so we know the sizes
        layers = []
        collisions = []
        unknown_data = None
        size = 0xC  # Header
        for i in range(0, self.model.number_of_layers):
            layer = self._convert_layer(i)
            size += len(layer)
            layers.append(layer)
        for i in range(0, self.model.number_of_collision_layers):
            col = self._convert_collision(i)
            size += len(col)
            collisions.append(col)
        if self.model.unk6:
            unknown_data = self._convert_unknown_data_layer()
            size += len(unknown_data)

        self.data = bytearray(size)

        self._write_byte(self.model.map_width_camera)
        self._write_byte(self.model.map_height_camera)
        self._write_byte(self.model.tiling_width)
        self._write_byte(self.model.tiling_height)
        self._write_byte(self.model.map_width_chunks)
        self._write_byte(self.model.map_height_chunks)
        assert self.model.number_of_layers < 3
        self._write_16uintle(self.model.number_of_layers)
        assert self.model.unk6 < 2
        self._write_16uintle(self.model.unk6)
        assert self.model.number_of_collision_layers < 3
        self._write_16uintle(self.model.number_of_collision_layers)

        self.bytes_written = 0xC

        for layer in layers:
            lenlayer = len(layer)
            self.data[self.bytes_written:self.bytes_written+lenlayer] = layer
            #print(f"w> layer 0x{self.bytes_written:02x}")
            self.bytes_written += lenlayer

        if unknown_data:
            lendata = len(unknown_data)
            self.data[self.bytes_written:self.bytes_written+lendata] = unknown_data
            #print(f"w> unk   0x{self.bytes_written:02x}")
            self.bytes_written += lendata

        for col in collisions:
            lencol = len(col)
            self.data[self.bytes_written:self.bytes_written+lencol] = col
            #print(f"w> col   0x{self.bytes_written:02x}")
            self.bytes_written += lencol

        return self.data

    def _convert_layer(self, layeri) -> bytes:
        """
        Converts chunk mappings for a layer back into bytes.
        If map size is odd, adds one extra tiles per row.
        Every row is NRL encoded separately, because the game decodes the rows separately!
        """
        from skytemple_files.common.types.file_types import FileType

        layer = self.model.layer0 if layeri == 0 else self.model.layer1

        # The actual values are "encoded" using XOR.
        previous_row_values = [0 for _ in range(0, self.model.map_width_chunks)]
        size = self.model.map_width_chunks * self.model.map_height_chunks * 2
        assert size == len(layer) * 2
        if self.model.map_width_chunks % 2 != 0:
            # Keep in mind there's an extra null tile to be added per row
            size += self.model.map_height_chunks * 2

        layer_bytes = bytearray(size)
        layer_bytes_cursor = 0

        # Each tile is separately encoded, so we also build them separately
        for row in range(0, self.model.map_height_chunks):
            row_bytes = bytearray(int(size / self.model.map_height_chunks))
            for col in range(0, self.model.map_width_chunks):
                i = row * self.model.map_width_chunks + col
                actual_value = layer[i] ^ previous_row_values[col]
                write_uintle(row_bytes, actual_value, col*2, 2)
                previous_row_values[col] = layer[i]
            assert len(row_bytes) == int(size / self.model.map_height_chunks)
            # Extra null tile is already there because of the bytearray size!
            comp_row_bytes = FileType.BMA_LAYER_NRL.compress(row_bytes)
            len_comp_row_bytes = len(comp_row_bytes)
            layer_bytes[layer_bytes_cursor:layer_bytes_cursor+len_comp_row_bytes] = comp_row_bytes
            layer_bytes_cursor += len_comp_row_bytes

        return layer_bytes[:layer_bytes_cursor]

    def _convert_collision(self, layeri):
        """
        Converts collision mappings back into bytes.
        If map size is odd, adds one extra tiles per row
        Every row is NRL encoded separately, because the game decodes the rows separately!
        """
        from skytemple_files.common.types.file_types import FileType

        collision_layer = self.model.collision if layeri == 0 else self.model.collision2

        # The actual values are "encoded" using XOR.
        previous_row_values = [0 for _ in range(0, self.model.map_width_camera)]
        size = self.model.map_width_camera * self.model.map_height_camera
        assert size == len(collision_layer)

        layer_bytes = bytearray(size)
        layer_bytes_cursor = 0

        # Each tile is separately encoded, so we also build them separately
        for row in range(0, self.model.map_height_camera):
            row_bytes = bytearray(int(size / self.model.map_height_camera))
            for col in range(0, self.model.map_width_camera):
                i = row * self.model.map_width_camera + col
                actual_value = collision_layer[i] ^ previous_row_values[col]
                write_uintle(row_bytes, actual_value, col)
                previous_row_values[col] = collision_layer[i]
            assert len(row_bytes) == int(size / self.model.map_height_camera)
            comp_row_bytes = FileType.BMA_COLLISION_RLE.compress(row_bytes)
            len_comp_row_bytes = len(comp_row_bytes)
            layer_bytes[layer_bytes_cursor:layer_bytes_cursor+len_comp_row_bytes] = comp_row_bytes
            layer_bytes_cursor += len_comp_row_bytes

        return layer_bytes[:layer_bytes_cursor]

    def _convert_unknown_data_layer(self) -> bytes:
        """
        Converts the unknown data layer back into bytes
        Every row is NRL encoded separately, because the game decodes the rows separately!
        """
        from skytemple_files.common.types.file_types import FileType

        size = self.model.map_width_camera * self.model.map_height_camera
        assert size == len(self.model.unknown_data_block)

        layer_bytes = bytearray(size)
        layer_bytes_cursor = 0
        # Each tile is separately encoded, so we also build them separately
        for row in range(0, self.model.map_height_camera):
            row_bytes = bytearray(int(size / self.model.map_height_camera))
            for col in range(0, self.model.map_width_camera):
                i = row * self.model.map_width_camera + col
                actual_value = self.model.unknown_data_block[i]
                write_uintle(row_bytes, actual_value, col)
            assert len(row_bytes) == int(size / self.model.map_height_camera)
            comp_row_bytes = FileType.GENERIC_NRL.compress(row_bytes)
            len_comp_row_bytes = len(comp_row_bytes)
            layer_bytes[layer_bytes_cursor:layer_bytes_cursor+len_comp_row_bytes] = comp_row_bytes
            layer_bytes_cursor += len_comp_row_bytes

        return layer_bytes[:layer_bytes_cursor]

    def _write_16uintle(self, val):
        assert val <= 0xffff
        write_uintle(self.data, val, self.bytes_written, 2)
        self.bytes_written += 2

    def _write_byte(self, val):
        assert val <= 0xff
        write_uintle(self.data, val, self.bytes_written)
        self.bytes_written += 1
