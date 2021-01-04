"""Converts GraphicFont models back into the binary format used by the game"""
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
from skytemple_files.graphics.chr import *
from skytemple_files.graphics.chr.model import Chr


class ChrWriter:
    def __init__(self, model: Chr):
        self.model = model

    def write(self) -> bytes:
        buffer = bytearray((CHR_TILE_WIDTH**2) * len(self.model.tiles))

        for i, t in enumerate(self.model.tiles):
            buffer[(CHR_TILE_WIDTH**2)*i:(CHR_TILE_WIDTH**2)*(i+1)] = t.tobytes()
        return buffer
