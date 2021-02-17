"""Converts WazaP models back into the binary format used by the game"""
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
from typing import Optional, Dict

from skytemple_files.common.util import *
from skytemple_files.data.waza_cd.model import WazaCD


class WazaCDWriter:
    def __init__(self, model: WazaCD):
        self.model = model

    def write(self) -> bytes:
        nb_moves = len(self.model.moves_effects)
        
        header = bytearray(4+2*nb_moves+len(self.model.effects_code)*8)
        write_uintle(header, 4+2*nb_moves, 0, 4)
        code_data = bytearray(0)
        current_ptr = len(header)
        for i, c in enumerate(self.model.effects_code):
            write_uintle(header, current_ptr, 4+2*nb_moves+i*8, 4)
            write_uintle(header, len(c), 4+2*nb_moves+i*8+4, 4)
            code_data += bytearray(c)
            current_ptr += len(c)
        
        for i, x in enumerate(self.model.moves_effects):
            write_uintle(header, x, 4+2*i, 2)
        file_data = header + code_data
        return bytes(file_data)
