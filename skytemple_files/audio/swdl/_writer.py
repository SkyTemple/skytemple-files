"""Converts Swdl models back into the binary format used by the game"""
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
from skytemple_files.audio.swdl._model import Swdl, SwdlPcmdLen


class SwdlWriter:
    def write(self, model: Swdl) -> bytes:
        wavi = model.wavi.to_bytes() if model.wavi is not None else bytes()
        prgi = model.prgi.to_bytes() if model.prgi is not None else bytes()
        kgrp = model.kgrp.to_bytes() if model.kgrp is not None else bytes()
        pcmd = model.pcmd.to_bytes() if model.pcmd is not None else bytes()
        if len(pcmd) > 0:
            pcmdlen = SwdlPcmdLen(len(pcmd), False)
        else:
            pcmdlen = SwdlPcmdLen(model.header.pcmdlen.ref, True)

        # The file might have PRGI slots set, even if none are defined
        prgi_slots = model.header.get_initial_number_prgi_slots()
        if model.prgi is not None:
            prgi_slots = len(model.prgi.program_table)

        data = bytes(wavi)
        assert len(data) % 16 == 0
        data += prgi
        assert len(data) % 16 == 0
        data += kgrp
        assert len(data) % 16 == 0
        data += pcmd
        assert len(data) % 16 == 0
        data += bytearray(b'eod \x00\x00\x15\x04\x10\x00\x00\x00\x00\x00\x00\x00')
        assert len(data) % 16 == 0
        header = model.header.to_bytes(
            80 + len(data), pcmdlen, len(model.wavi.sample_info_table) if model.wavi else 0,
            prgi_slots, len(wavi) - 0x10
        )

        return header + data
