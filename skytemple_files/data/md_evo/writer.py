"""Converts MdEvo models back into the binary format used by the game"""
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

from range_typed_integers import u32_checked

from skytemple_files.common.util import write_u32
from skytemple_files.data.md_evo import MEVO_ENTRY_LENGTH
from skytemple_files.data.md_evo.model import MdEvo


class MdEvoWriter:
    def __init__(self, model: MdEvo):
        self.model = model

    def write(self) -> bytes:
        file_data = bytearray(4)
        write_u32(
            file_data,
            u32_checked(len(self.model.evo_entries) * MEVO_ENTRY_LENGTH + 4),
            0,
        )

        for x in self.model.evo_entries:
            file_data += x.to_bytes()
        for y in self.model.evo_stats:
            file_data += y.to_bytes()
        return bytes(file_data)
