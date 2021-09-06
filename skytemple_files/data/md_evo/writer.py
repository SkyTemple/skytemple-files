"""Converts MdEvo models back into the binary format used by the game"""
#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
from typing import Optional, Dict

from skytemple_files.common.util import *
from skytemple_files.data.md_evo import *
from skytemple_files.data.md_evo.model import MdEvo


class MdEvoWriter:
    def __init__(self, model: MdEvo):
        self.model = model

    def write(self) -> bytes:
        file_data = bytearray(4)
        write_uintle(file_data, len(self.model.evo_entries)*MEVO_ENTRY_LENGTH+4, 0, 4)
        
        for x in self.model.evo_entries:
            file_data += x.to_bytes()
        for x in self.model.evo_stats:
            file_data += x.to_bytes()
        return bytes(file_data)
