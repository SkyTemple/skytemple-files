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
from typing import Union, Optional, List

from skytemple_files.audio.common import HasId
from skytemple_files.audio.swdl._model_pcmd import SwdlPcmd
from skytemple_files.audio.swdl.protocol import SwdlSampleInfoTblEntryProtocol, SwdlPcmdReferenceProtocol, \
    SwdlWaviProtocol
from skytemple_files.common.util import *


class SwdlPcmdReference(SwdlPcmdReferenceProtocol[SwdlPcmd]):
    def __init__(self, pcmd: Optional[SwdlPcmd], offset: int, length: int):
        self.pcmd = pcmd
        self.offset = offset
        self.length = length

    def to_bytes_for_pcmd(self, pcmd: SwdlPcmd):
        return bytes(pcmd.chunk_data[self.offset:self.offset + self.length])

    def __bytes__(self):
        if self.pcmd:
            return self.to_bytes_for_pcmd(self.pcmd)
        raise ValueError("No pcmd defined. Use to_bytes_for_pcmd instead.")


LEN_SAMPLE_INFO_ENTRY = 0x40


class SwdlSampleInfoTblEntry(SwdlSampleInfoTblEntryProtocol[SwdlPcmdReference], AutoString, HasId):
    def __init__(self, data: Optional[Union[bytes, memoryview]], _assertId: Optional[int]):
        if data is None:
            return
        assert data[0x00:0x04] != bytes([0x01, 0xAA]), "Data is not valid WDL WAVI Sample Info"
        self.id = read_uintle(data, 0x02, 2)
        HasId.__init__(self, self.id)
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
        self.loops = bool(read_uintle(data, 0x15))
        self.unk10 = read_uintle(data, 0x16, 2)
        self.unk11 = read_uintle(data, 0x18, 2)
        self.unk12 = read_uintle(data, 0x1A, 2)
        self.unk13 = read_uintle(data, 0x1C, 4)
        self.sample_rate = read_uintle(data, 0x20, 4)
        # Read sample data later into this model
        self.sample: Optional[SwdlPcmdReference] = None
        self._sample_pos = read_uintle(data, 0x24, 4)
        self.loop_begin_pos = read_uintle(data, 0x28,
                                              4)  # (For ADPCM samples, the 4 bytes preamble is counted in the loopbeg!)
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
        return (self.loop_begin_pos + self.loop_length) * 4

    def get_initial_sample_pos(self):
        return self._sample_pos

    def force_set_sample_pos(self, sample_start):
        self._sample_pos = sample_start
        self.sample = None

    def copy(self, new_start=None) -> 'SwdlSampleInfoTblEntry':
        n = SwdlSampleInfoTblEntry(None, None)
        if new_start is None:
            new_start = self._sample_pos
        vars(n).update(vars(self))
        vars(n).update({'_sample_pos': new_start})
        return n

    def to_bytes(self):
        data = bytearray(64)
        data[0x00:0x04] = bytes([0x01, 0xAA])
        write_uintle(data, self.id, 0x02, 2)
        write_sintle(data, self.ftune, 0x04, 1)
        write_sintle(data, self.ctune, 0x05, 1)
        write_sintle(data, self.rootkey, 0x06, 1)
        write_sintle(data, self.ktps, 0x07, 1)
        write_sintle(data, self.volume, 0x08, 1)
        write_sintle(data, self.pan, 0x09, 1)
        write_uintle(data, self.unk5, 0x0A, 1)
        write_uintle(data, self.unk58, 0x0B, 1)
        data[0x0E:0x10] = bytes([0xAA, 0xAA])
        data[0x10:0x12] = bytes([0x15, 0x04])
        write_uintle(data, self.sample_format, 0x12, 2)
        write_uintle(data, self.unk9, 0x14, 1)
        write_uintle(data, self.loops, 0x15, 1)
        write_uintle(data, self.unk10, 0x16, 2)
        write_uintle(data, self.unk11, 0x18, 2)
        write_uintle(data, self.unk12, 0x1A, 2)
        write_uintle(data, self.unk13, 0x1C, 4)
        write_uintle(data, self.sample_rate, 0x20, 4)
        write_uintle(data, self._sample_pos, 0x24, 4)
        write_uintle(data, self.loop_begin_pos, 0x28, 4)
        write_uintle(data, self.loop_length, 0x2C, 4)
        write_uintle(data, self.envelope, 0x30, 1)
        write_uintle(data, self.envelope_multiplier, 0x31, 1)
        write_uintle(data, self.unk19, 0x32, 1)
        write_uintle(data, self.unk20, 0x33, 1)
        write_uintle(data, self.unk21, 0x34, 2)
        write_uintle(data, self.unk22, 0x36, 2)
        write_sintle(data, self.attack_volume, 0x38, 1)
        write_sintle(data, self.attack, 0x39, 1)
        write_sintle(data, self.decay, 0x3A, 1)
        write_sintle(data, self.sustain, 0x3B, 1)
        write_sintle(data, self.hold, 0x3C, 1)
        write_sintle(data, self.decay2, 0x3D, 1)
        write_sintle(data, self.release, 0x3E, 1)
        write_sintle(data, self.unk57, 0x3F, 1)
        return data

    def equals_without_id(self, other):
        if not isinstance(other, SwdlSampleInfoTblEntry):
            return False
        return self.ftune == other.ftune and \
               self.ctune == other.ctune and \
               self.rootkey == other.rootkey and \
               self.ktps == other.ktps and \
               self.volume == other.volume and \
               self.pan == other.pan and \
               self.unk5 == other.unk5 and \
               self.unk58 == other.unk58 and \
               self.sample_format == other.sample_format and \
               self.unk9 == other.unk9 and \
               self.loops == other.loop and \
               self.unk10 == other.unk10 and \
               self.unk11 == other.unk11 and \
               self.unk12 == other.unk12 and \
               self.unk13 == other.unk13 and \
               self.sample_rate == other.sample_rate and \
               self._sample_pos == other._sample_pos and \
               self.loop_begin_pos == other.loop_begin_pos and \
               self.loop_length == other.loop_length and \
               self.envelope == other.envelope and \
               self.envelope_multiplier == other.envelope_multiplier and \
               self.unk19 == other.unk19 and \
               self.unk20 == other.unk20 and \
               self.unk21 == other.unk21 and \
               self.unk22 == other.unk22 and \
               self.attack_volume == other.attack_volume and \
               self.attack == other.attack and \
               self.decay == other.decay and \
               self.sustain == other.sustain and \
               self.hold == other.hold and \
               self.decay2 == other.decay2 and \
               self.release == other.release and \
               self.unk57 == other.unk57


class SwdlWavi(SwdlWaviProtocol[SwdlSampleInfoTblEntry]):
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

    def to_bytes(self) -> bytes:
        chunk = bytearray(len(self.sample_info_table) * 2)
        # Padding after TOC
        if len(chunk) % 16 != 0:
            chunk += bytes([0xAA] * (16 - (len(chunk) % 16)))
        for i, wav in enumerate(self.sample_info_table):
            if wav is not None:
                assert wav.id == i
                write_uintle(chunk, len(chunk), i * 2, 2)
                chunk += wav.to_bytes()
            else:
                write_uintle(chunk, 0, i * 2, 2)

        buffer = bytearray(b'wavi\0\0\x15\x04\x10\0\0\0\0\0\0\0')
        write_uintle(buffer, len(chunk), 0x0C, 4)
        return buffer + chunk

    def __str__(self):
        chunks = ""
        for sample_info in self.sample_info_table:
            chunks += f">> {sample_info}\n"
        return """WAVI
""" + chunks

    def __eq__(self, other):
        if not isinstance(other, SwdlWavi):
            return False
        return self.sample_info_table == other.sample_info_table
