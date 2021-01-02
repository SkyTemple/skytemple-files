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

from skytemple_files.compression.generic_nrl.compressor import GenericNrlCompressor

DEBUG = False


# noinspection PyAttributeOutsideInit
class BpcTilemapCompressor(GenericNrlCompressor):
    """
    The compression ist just simple NRL in two runs, first
    skipping all low bytes and then all high bytes.
    """

    def compress(self) -> bytes:
        self.reset()
        if DEBUG:
            print("BPC Tilemap NRL compressor start...")

        # First we process all the high bytes (LE)
        self.cursor = 1
        while self.cursor < self.length_input:
            self._process(2)

        if DEBUG:
            print(f"End Phase 1. Begin Phase 2.")
            print(f"Cursor begin phase 2: {self.bytes_written}")

        # And then all the low bytes (LE)
        self.cursor = 0
        while self.cursor < self.length_input:
            self._process(2)

        return self.compressed_data[:self.bytes_written]
