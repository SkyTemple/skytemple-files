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
from skytemple_files.container.sir0.sir0_util import encode_sir0_pointer_offsets
from skytemple_files.data.waza_p.model import WazaP


class WazaPWriter:
    def __init__(self, model: WazaP):
        self.model = model

    def write(self) -> Tuple[bytes, List[int], Optional[int]]:
        pointer_offsets: List[int] = []
        data = bytearray(3)
        # Learnset
        learnset_pointers: List[Tuple[int, int, int]] = []
        for learnset in self.model.learnsets:
            # Level Up
            pnt_lvlup = len(data)
            buff = bytearray(8 * (len(learnset.level_up_moves) + 1))
            lvl_up_move_list = []
            for lvl_up_move in learnset.level_up_moves:
                lvl_up_move_list.append(lvl_up_move.move_id)
                lvl_up_move_list.append(lvl_up_move.level_id)
            c = encode_sir0_pointer_offsets(buff, lvl_up_move_list, False)
            data += buff[:c]
            # TM/HM
            pnt_tm_hm = len(data)
            buff = bytearray(4 * (len(learnset.tm_hm_moves) + 1))
            c = encode_sir0_pointer_offsets(buff, learnset.tm_hm_moves, False)
            data += buff[:c]
            # Egg
            pnt_egg = len(data)
            buff = bytearray(4 * (len(learnset.egg_moves) + 1))
            c = encode_sir0_pointer_offsets(buff, learnset.egg_moves, False)
            data += buff[:c]

            learnset_pointers.append((pnt_lvlup, pnt_tm_hm, pnt_egg))
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        # Move data
        move_pointer = len(data)
        for move in self.model.moves:
            data += move.to_bytes()
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        # Learnset pointer table
        learnset_pointer_table_pnt = len(data)
        learnset_pointer_table = bytearray(len(learnset_pointers) * 12)
        for i, (lvlup, tm_hm, egg) in enumerate(learnset_pointers):
            pointer_offsets.append(len(data) + i * 12)
            pointer_offsets.append(len(data) + i * 12 + 4)
            pointer_offsets.append(len(data) + i * 12 + 8)
            write_uintle(learnset_pointer_table, lvlup, i * 12, 4)
            write_uintle(learnset_pointer_table, tm_hm, i * 12 + 4, 4)
            write_uintle(learnset_pointer_table, egg, i * 12 + 8, 4)
        data += learnset_pointer_table
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        # Waza Header (<- content pointer)
        header = bytearray(8)
        waza_header_start = len(data)
        pointer_offsets.append(waza_header_start)
        write_uintle(header, move_pointer, 0, 4)
        pointer_offsets.append(waza_header_start + 4)
        write_uintle(header, learnset_pointer_table_pnt, 4, 4)
        data += header
        # Padding
        if len(data) % 16 != 0:
            data += bytes(0xAA for _ in range(0, 16 - (len(data) % 16)))
        return data, pointer_offsets, waza_header_start
