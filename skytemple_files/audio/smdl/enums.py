#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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
from enum import Enum
from typing import Optional


class SmdlNote(Enum):
    C = 0x0
    CS = 0x1
    D = 0x2
    DS = 0x3
    E = 0x4
    F = 0x5
    FS = 0x6
    G = 0x7
    GS = 0x8
    A = 0x9
    AS = 0xA
    B = 0xB
    INVALID_C = 0xC
    INVALID_D = 0xD
    INVALID_E = 0xE
    UNK = 0xF


class SmdlPause(Enum):
    HALF_NOTE = 0x80, 96
    DOTTED_QUARTER_NOTE = 0x81, 72
    X2_3_OF_HALF_NOTE = 0x82, 64
    QUARTER_NOTE = 0x83, 48
    DOTTED_EIGHT_NOTE = 0x84, 36
    X2_3_OF_QUARTER_NOTE = 0x85, 32
    EIGTH_NOTE = 0x86, 24
    DOTTED_SIXTEENTH_NOTE = 0x87, 18
    X2_3_OF_EIGTH_NOTE = 0x88, 16
    SIXTEENTH_NOTE = 0x89, 12
    DOTTED_THRITYSECOND_NOTE = 0x8A, 9
    X2_3_OF_SIXTEENTH_NOTE = 0x8B, 8
    THRITYSECOND_NOTE = 0x8C, 6
    DOTTED_SIXTYFORTH_NOTE = 0x8D, 4
    X2_3_OF_THRITYSECOND_NOTE = 0x8E, 3
    SIXTYFORTH_NOTE = 0x8F, 2

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: str, length: Optional[int] = None
    ):
        # in ticks
        self.length = length


class SmdlSpecialOpCode(Enum):
    WAIT_AGAIN = 0x90, 0
    WAIT_ADD = 0x91, 1
    WAIT_1BYTE = 0x92, 1
    WAIT_2BYTE = 0x93, 2  # LE
    WAIT_3BYTE = 0x94, 2  # LE
    TRACK_END = 0x98, 0
    LOOP_POINT = 0x99, 0
    SET_OCTAVE = 0xA0, 1
    SET_TEMPO = 0xA4, 1
    SET_HEADER1 = 0xA9, 1
    SET_HEADER2 = 0xAA, 1
    SET_SAMPLE = 0xAC, 1
    SET_MODU = 0xBE, 1
    SET_BEND = 0xD7, 2
    SET_VOLUME = 0xE0, 1
    SET_XPRESS = 0xE3, 1
    SET_PAN = 0xE8, 1
    NA_NOTE = 0x00, -1
    NA_DELTATIME = 0x80, 1
    UNK_9C = 0x9C, 1
    UNK_9D = 0x9D, 0
    UNK_A8 = 0xA8, 2
    UNK_B2 = 0xB2, 1
    UNK_B4 = 0xB4, 2
    UNK_B5 = 0xB5, 1
    UNK_BF = 0xBF, 1
    UNK_C0 = 0xC0, 0
    UNK_D0 = 0xD0, 1
    UNK_D1 = 0xD1, 1
    UNK_D2 = 0xD2, 1
    UNK_D4 = 0xD4, 3
    UNK_D6 = 0xD6, 2
    UNK_DB = 0xDB, 1
    UNK_DC = 0xDC, 5
    UNK_E2 = 0xE2, 3
    UNK_EA = 0xEA, 3
    UNK_F6 = 0xF6, 1

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: str, parameters: Optional[int] = None
    ):
        # Number of parameters
        self.parameters = parameters
