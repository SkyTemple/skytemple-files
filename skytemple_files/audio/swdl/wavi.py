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
from typing import Union, Optional

from skytemple_files.common.util import *


class SampleFormatConsts:
    PCM_8BIT = 0x0000
    PCM_16BIT = 0x0100
    ADPCM_4BIT = 0x0200
    PSG = 0x0300  # possibly


LEN_SAMPLE_INFO_ENTRY = 0x40


class SwdlSampleInfoTblEntry(AutoString):
    def __init__(self, data: Union[bytes, memoryview], _assertId: int):
        assert data[0x00:0x04] != bytes([0x01, 0xAA]), "Data is not valid WDL WAVI Sample Info"
        self.id = read_uintle(data, 0x02, 2)
        assert self.id == _assertId, "Data is not valid WDL WAVI Sample Info"
        self.ftune = read_sintle(data, 0x04)
        self.ctune = read_sintle(data, 0x05)
        self.rootkey = read_sintle(data, 0x06)  # seems unused by game!
        self.ktps = read_sintle(data, 0x07)
        self.volume = read_sintle(data, 0x08)  # (0-127)
        self.pan = read_sintle(data, 0x09)  # (0-64-127)
        self.unk5 = read_uintle(data, 0x0A)  # probably key_group, always 0
        self.unk58 = read_uintle(data, 0x0B)
        assert data[0x0C:0x0E] == bytes(2), "Data is not valid WDL WAVI Sample Info"
        assert data[0x0E:0x10] == bytes([0xAA, 0xAA]), "Data is not valid WDL WAVI Sample Info"
        assert data[0x10:0x12] == bytes([0x15, 0x04]), "Data is not valid WDL WAVI Sample Info"
        self.sample_format = read_uintle(data, 0x12, 2)  # compare against SampleFormatConsts
        self.unk9 = read_uintle(data, 0x14)
        self.loop = bool(read_uintle(data, 0x15))
        self.unk10 = read_uintle(data, 0x16, 2)
        self.unk11 = read_uintle(data, 0x18, 2)
        self.unk12 = read_uintle(data, 0x1A, 2)
        self.unk13 = read_uintle(data, 0x1C, 4)
        self.sample_rate = read_uintle(data, 0x20, 4)
        # Read sample data later into this model
        self.sample: Optional[bytes] = None
        self._sample_pos = read_uintle(data, 0x24, 4)
        self.loop_begin_pos = read_uintle(data, 0x28, 4)  # (For ADPCM samples, the 4 bytes preamble is counted in the loopbeg!)
        self.loop_length = read_uintle(data, 0x2C, 4)

        self.envelope = read_uintle(data, 0x30)
        self.envelope_multiplier = read_uintle(data, 0x31)
        self.unk19 = read_uintle(data, 0x32)
        self.unk20 = read_uintle(data, 0x33)
        self.unk21 = read_uintle(data, 0x34, 2)
        self.unk22 = read_uintle(data, 0x36, 2)
        self.attack_volume = read_sintle(data, 0x38)
        self.attack = read_sintle(data, 0x39)
        self.decay = read_sintle(data, 0x3A)
        self.sustain = read_sintle(data, 0x3B)
        self.hold = read_sintle(data, 0x3C)
        self.decay2 = read_sintle(data, 0x3D)
        self.release = read_sintle(data, 0x3E)
        self.unk57 = read_sintle(data, 0x3F)

    @property
    def sample_length(self):
        return self.loop_begin_pos + self.loop_length

    def get_initial_sample_pos(self):
        return self._sample_pos


class SwdlWavi:
    def __init__(self, data: Union[bytes, memoryview], number_slots: int):
        assert data[0x00:0x04] == b'wavi', "Data is not valid SWDL WAVI"
        assert data[0x04:0x06] == bytes(2), "Data is not valid SWDL WAVI"
        assert data[0x06:0x08] == bytes([0x15, 0x04]), "Data is not valid SWDL WAVI"
        assert data[0x08:0x0C] == bytes([0x10, 0x00, 0x00, 0x00]), "Data is not valid SWDL WAVI"
        len_chunk_data = read_uintle(data, 0x0C, 4)
        self.sample_info_table: List[Optional[SwdlSampleInfoTblEntry]] = []

        self._length = 0x10 + len_chunk_data

        for idx, seek in enumerate(range(0, number_slots * 2, 2)):
            pnt = read_uintle(data, 0x10 + seek, 2)
            assert pnt < len_chunk_data, "Data is not valid SWDL WAVI"
            if pnt == 0:
                self.sample_info_table.append(None)
            else:
                self.sample_info_table.append(SwdlSampleInfoTblEntry(data[0x10 + pnt:], _assertId=idx))

    def get_initial_length(self):
        return self._length

    def __str__(self):
        chunks = ""
        for sample_info in self.sample_info_table:
            chunks += f">> {sample_info}\n"
        return """WAVI
""" + chunks