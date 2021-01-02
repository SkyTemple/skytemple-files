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
from typing import Optional

from skytemple_files.common.util import *
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.container.sir0.sir0_util import decode_sir0_pointer_offsets

# TODO: Consider actually reading until the header later, in case modded games
#       have added move moves.
MOVE_COUNT = 559
MOVE_ENTRY_BYTELEN = 26


class LevelUpMove(AutoString):
    def __init__(self, move_id: int, level_id: int):
        self.move_id = move_id
        self.level_id = level_id

    def __eq__(self, other):
        if not isinstance(other, LevelUpMove):
            return False
        return self.move_id == other.move_id and self.level_id == other.level_id


class MoveLearnset(AutoString):
    def __init__(self, level_up_moves: List[LevelUpMove], tm_hm_moves: List[int], egg_moves: List[int]):
        self.level_up_moves = level_up_moves
        self.tm_hm_moves = tm_hm_moves
        self.egg_moves = egg_moves

    def __eq__(self, other):
        if not isinstance(other, MoveLearnset):
            return False
        return self.level_up_moves == other.level_up_moves \
               and self.tm_hm_moves == other.tm_hm_moves \
               and self.egg_moves == other.egg_moves


class WazaP(Sir0Serializable, AutoString):
    def __init__(self, data: bytes, waza_content_pointer: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        move_data_pointer = read_uintle(data, waza_content_pointer, 4)
        move_learnset_pointer = read_uintle(data, waza_content_pointer + 4, 4)

        # TODO: Implement model for actual move data
        self.move_data = data[move_data_pointer:move_data_pointer+(MOVE_COUNT*MOVE_ENTRY_BYTELEN)]

        self.learnsets: List[MoveLearnset] = []
        i = 0
        while True:
            if move_learnset_pointer+(i*12) >= waza_content_pointer:
                break
            list_pointers = data[move_learnset_pointer+(i*12):move_learnset_pointer+((i+1)*12)]
            level_up = []
            tm_hm = []
            egg = []

            pointer_level_up = read_uintle(list_pointers, 0, 4)
            pointer_tm_hm = read_uintle(list_pointers, 4, 4)
            pointer_egg = read_uintle(list_pointers, 8, 4)
            if pointer_level_up == 0xAAAAAAAA or pointer_tm_hm == 0xAAAAAAAA or pointer_egg == 0xAAAAAAAA:
                break

            # Read Level Up Data
            if pointer_level_up != 0:
                level_up_raw = self._decode_ints(data, pointer_level_up)
                for move_id, level_id in chunks(level_up_raw, 2):
                    level_up.append(LevelUpMove(move_id, level_id))

            # TM/HM Move data
            if pointer_tm_hm:
                tm_hm = self._decode_ints(data, pointer_tm_hm)

            # TM/HM Move data
            if pointer_egg:
                egg = self._decode_ints(data, pointer_egg)

            self.learnsets.append(MoveLearnset(
                level_up, tm_hm, egg
            ))
            i += 1

    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int,
                    static_data: Optional[Pmd2Data] = None) -> 'Sir0Serializable':
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.data.waza_p.writer import WazaPWriter
        return WazaPWriter(self).write()

    def __eq__(self, other):
        if not isinstance(other, WazaP):
            return False
        return self.learnsets == other.learnsets and self.move_data == other.move_data

    @staticmethod
    def _decode_ints(data: bytes, pnt_start: int) -> List[int]:
        return decode_sir0_pointer_offsets(data, pnt_start, False)
